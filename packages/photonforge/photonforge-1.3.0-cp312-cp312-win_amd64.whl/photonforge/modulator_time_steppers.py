import copy as libcopy
import threading
import time
from typing import Literal

import numpy

from .analytic_models import _port_with_x_section
from .circuit_base import _gather_status
from .extension import (
    Component,
    Interpolator,
    Port,
    PortSpec,
    Technology,
    TimeStepper,
    register_time_stepper_class,
)
from .tidy3d_model import _isotropic_uniform, _ModeSolverRunner
from .typing import (
    Coordinate,
    Frequency,
    Impedance,
    PositiveFloat,
    PositiveInt,
    PropagationLoss,
    TimeDelay,
    annotate,
)
from .utils import C_0, route_length


def _impedance_monitor(time_stepper, runner):
    status = runner.status
    with time_stepper._lock:
        time_stepper._status = dict(status)
        time_stepper._status["progress"] *= 0.99

    while status["message"] == "running":
        time.sleep(0.3)
        status = runner.status
        with time_stepper._lock:
            time_stepper._status = dict(status)
            time_stepper._status["progress"] *= 0.99

    if status["message"] == "error":
        with time_stepper._lock:
            time_stepper._status = status
        return

    with time_stepper._lock:
        time_stepper._status = status
        time_stepper._status["message"] = "running"
        time_stepper._status["progress"] *= 0.99

    time_stepper._z0 = time_stepper._ic.compute_impedance(runner.data).values[0, 0].item()

    time_stepper.reset()

    with time_stepper._lock:
        time_stepper._status = status
        time_stepper._status["message"] = "success"
        time_stepper._status["progress"] = 100


def _get_impedance_runner(time_stepper, component, port_name, time_step, verbose):
    p = time_stepper.parametric_kwargs
    mesh_refinement = p["mesh_refinement"]
    if verbose is None:
        verbose = p["verbose"]

    runner = None
    frequency = 0.25 / time_step  # Half Nyquist frequency
    time_stepper._z0 = p["z0"]
    if time_stepper._z0 is None:
        ms_port = component.ports[port_name].copy(True)
        impedance = ms_port.spec.impedance
        if impedance is not None:
            time_stepper._z0 = impedance(frequency)[0]
        elif not ms_port.spec._is_1D():
            tech = component.technology
            ms_port.center = (0, 0)
            mode_solver = ms_port.to_tidy3d_mode_solver(
                [frequency],
                mesh_refinement,
                technology=tech,
                use_angle_rotation=_isotropic_uniform(tech, "electrical"),
            )
            runner = _ModeSolverRunner(
                mode_solver, [frequency], mesh_refinement, tech, verbose=verbose
            )
            time_stepper._ic = ms_port.to_tidy3d_impedance_calculator()
            time_stepper._lock = threading.Lock()
            time_stepper._status = {"message": "running", "progress": 0}
            time_stepper._setup_thread = threading.Thread(
                daemon=True, target=_impedance_monitor, args=(time_stepper, runner)
            )
            time_stepper._setup_thread.start()
        else:
            time_stepper._z0 = 50.0
    elif isinstance(time_stepper._z0, Interpolator):
        time_stepper._z0 = time_stepper._z0(frequency)

    return runner


class PhaseModTimeStepper(TimeStepper):
    r"""Time-stepper for a uniform electro-optic phase modulator.

    This model implements a two-port optical phase modulator with a single
    electrical drive. It features a length-aware phase modulation law with
    optional nonlinear terms, a voltage-dependent loss model, and an
    optional first-order low-pass filter on the electrical input to model
    finite bandwidth. The optical path includes group delay based on a
    constant group index.

    The induced phase shift and optical loss are given by:

    .. math::

       \Delta\phi &= \frac{\pi V \ell}{V_{\pi L}}
         + k_2 V^2 \ell + k_3 V^3 \ell

       L &= \left(L_p + \frac{{\rm d}L_p}{{\rm d}V} V
         + \frac{{\rm d}^2 L_p}{{\rm d}V^2} V^2 \right) \ell

    Args:
        length: Physical length of the modulator.
        n_eff: Effective index of the optical mode at the carrier frequency.
        n_group: Group index of the optical mode, used to calculate delay.
        v_piL: Electro-optic phase coefficient :math:`V_{\pi L}`.
        z0: Characteristic impedance of the electrical port used to convert
          the input field amplitude to voltage. If ``None``, derived from
          port impedance, calculated by mode-solving, or set to 50 Ω.
        propagation_loss: Optical propagation loss.
        k2: Quadratic nonlinear phase coefficient.
        k3: Cubic nonlinear phase coefficient.
        dloss_dv: Linear voltage-dependent optical loss coefficient.
        dloss_dv2: Quadratic voltage-dependent optical loss coefficient.
        tau_rc: Time constant of the optional first-order low-pass filter
          for the electrical input. Only active for positive values.
        mesh_refinement: Minimal number of mesh elements per wavelength used
          for mode solving.
        verbose: Flag setting the verbosity of mode solver runs.

    Important:
        The electrical input :math:`A` is converted to a voltage signal
        through the port impedance:

        .. math:: V = \Re\{A\} \sqrt{\Re\{Z_0\}}

    Notes:
        The total loss is clamped are 0 dB to avoid gain.

        The group delay :math:`n_g \ell / c_0` is implemented as a fixed
        multiple of the time step.

    See also:
        :class:`TerminatedModTimeStepper`: terminated travelling-wave phase
        modulator.
    """

    def __init__(
        self,
        *,
        length: Coordinate | None = None,
        n_eff: float,
        n_group: float = 0,
        v_piL: annotate(float, label="VπL", units="V·μm") = 0,
        z0: Impedance | Interpolator | None = None,
        propagation_loss: PropagationLoss = 0,
        k2: annotate(float, label="k₂", units="rad/μm/V²") = 0,
        k3: annotate(float, label="k₃", units="rad/μm/V³") = 0,
        dloss_dv: annotate(float, label="dL/dV", units="dB/μm/V") = 0,
        dloss_dv2: annotate(float, label="d²L/dV²", units="dB/μm/V²") = 0,
        tau_rc: TimeDelay = 0,
        mesh_refinement: PositiveFloat | None = None,
        verbose: bool = True,
    ):
        super().__init__(
            length=length,
            n_eff=n_eff,
            n_group=n_group,
            v_piL=v_piL,
            z0=z0,
            propagation_loss=propagation_loss,
            k2=k2,
            k3=k3,
            dloss_dv=dloss_dv,
            dloss_dv2=dloss_dv2,
            tau_rc=tau_rc,
            mesh_refinement=mesh_refinement,
            verbose=verbose,
        )

    def setup_state(
        self,
        *,
        component: Component,
        time_step: TimeDelay,
        carrier_frequency: Frequency,
        verbose: bool | None = None,
        **kwargs,
    ):
        """Initialize internal state.

        Args:
            component: Component representing the laser source.
            time_step: The interval between time steps (in seconds).
            carrier_frequency: The carrier frequency used to construct the time
              stepper. The carrier should be omitted from the input signals, as
              it is handled automatically by the time stepper.
            verbose: If set, overrides the time stepper's `verbose` attribute.
            kwargs: Unused.
        """
        ports = sorted(component.select_ports("optical"))
        e_ports = tuple(component.select_ports("electrical"))
        if len(ports) != 2 or len(e_ports) != 1:
            raise RuntimeError(
                "PhaseModTimeStepper can only be used in components with 2 optical and 1 "
                "electrical ports."
            )
        self._e = e_ports[0] + "@0"
        self._opt0 = ports[0] + "@0"
        self._opt1 = ports[1] + "@0"
        self.keys = (self._opt0, self._opt1, self._e)

        p = self.parametric_kwargs

        length = p["length"]
        if length is None:
            length = 0
            port0 = component.ports[ports[0]]
            port1 = component.ports[ports[1]]
            for _, _, layer in port0.spec.path_profiles_list():
                length = max(length, route_length(component, layer))
            if length <= 0:
                length = numpy.sqrt(numpy.sum((port0.center - port1.center) ** 2))

        self._phi0 = 2.0 * numpy.pi * carrier_frequency * p["n_eff"] * length / C_0
        self._phi1 = (numpy.pi * length / p["v_piL"]) if p["v_piL"] != 0 else 0
        self._phi2 = p["k2"] * length
        self._phi3 = p["k3"] * length

        self._g0 = p["propagation_loss"] * length / -20.0
        self._g1 = p["dloss_dv"] * length / -20.0
        self._g2 = p["dloss_dv2"] * length / -20.0

        self._filter = 0.0 if p["tau_rc"] <= 0 else numpy.exp(-time_step / p["tau_rc"])
        self._delay = max(0, int(numpy.round(p["n_group"] * length / C_0 / time_step)))
        self._buffer = numpy.empty((self._delay, 2), dtype=complex)

        if _get_impedance_runner(self, component, e_ports[0], time_step, verbose) is not None:
            return self

        self.reset()

    @property
    def status(self):
        if not self._setup_thread.is_alive() and self._status["message"] == "running":
            self._status["message"] = "error"
        with self._lock:
            return self._status

    def reset(self):
        """Reset internal state."""
        self._sqrt_r_in = numpy.real(self._z0) ** 0.5
        self._v = 0
        self._index = 0
        self._buffer[:, :] = 1e-30

    def step_single(
        self,
        inputs: numpy.ndarray,
        outputs: numpy.ndarray,
        time_index: int,
        update_state: bool,
        shutdown: bool,
    ) -> None:
        """Take a single time step on the given inputs.

        Args:
            inputs: Input values at the current time step. Must be a 1D array of
              complex values ordered according to :attr:`keys`.
            outputs: Pre-allocated output array where results will be stored.
              Same size and type as ``inputs``.
            time_index: Time series index for the current input.
            update_state: Whether to update the internal stepper state.
            shutdown: Whether this is the last call to the single stepping
              function for the provided :class:`TimeSeries`.
        """
        v_in = self._sqrt_r_in * inputs[2].real
        v = v_in * (1.0 - self._filter) + self._v * self._filter
        phi = self._phi0 + v * (self._phi1 + v * (self._phi2 + v * self._phi3))
        attenuation = 10.0 ** (self._g0 + v * (self._g1 + v * self._g2))
        factor = attenuation * numpy.exp(1j * phi)

        if self._delay > 0:
            a0, a1 = self._buffer[self._index]
        else:
            a0 = inputs[0]
            a1 = inputs[1]

        outputs[0] = factor * a1
        outputs[1] = factor * a0
        outputs[2] = 0  # Electrical port has no output

        if update_state:
            self._v = v
            if self._delay > 0:
                a0 = inputs[0]
                a1 = inputs[1]
                self._buffer[self._index] = (a0, a1)
                self._index = (self._index + 1) % self._delay


def _eo_s21(frequencies, length, n_group, n_rf, propagation_loss, z0, zl, zs):
    """
    Electro-optic transfer function for a traveling-wave modulator.

    Returns
    -------
    eo_s21 : complex array
        EO S21 (normalized to DC value).
    """
    omega = 2 * numpy.pi * frequencies
    alpha = abs(propagation_loss) / (20 * numpy.log10(numpy.e)) + 1e-15
    gl = (alpha + 1j * (omega / C_0) * n_rf) * length

    tgl = numpy.tanh(gl)
    z_in = z0 * (zl + z0 * tgl) / (z0 + zl * tgl)

    jf = 1j * (omega / C_0) * n_group * length
    f_p = (1 - numpy.exp(gl - jf)) / (gl - jf)
    f_m = (1 - numpy.exp(-gl - jf)) / (-gl - jf)

    return (-2 * z_in / (z_in + zs) * ((zl + z0) * f_p + (zl - z0) * f_m)) / (
        (zl + z0) * numpy.exp(gl) + (zl - z0) * numpy.exp(-gl)
    )


class TerminatedModTimeStepper(TimeStepper):
    r"""Time-stepper for a travelling-wave electro-optic phase modulator.

    This model implements a two-port optical phase modulator with a single
    electrical drive. The forward optical path is phase-modulated, and the
    reverse path propagates passively (attenuation only). The model assumes
    that the transmission line is terminated, so a single electrical port
    is used.

    Args:
        v_piL: Electro-optic phase coefficient :math:`V_{\pi L}`.
        length: Physical length of the modulator. If not provided, the
          length is measured by :func:`route_length` or ports distance.
        n_eff: Effective index of the optical mode at the carrier frequency.
          If ``None``, automatic computation is performed by mode-solving
          the first optical port of the component. If desired, the port
          specification can be overridden by setting ``n_eff`` to
          ``"cross-section"`` (uses :func:`Component.slice_profile`) or to
          a :class:`PortSpec` object.
        n_group: Group index of the optical mode. If ``None``, calculated
          together with ``n_eff`` by mode-solving or set to the value of
          ``n_rf`` (perfect phase-matching).
        n_rf: Effective index of the electrical (RF/microwave) mode.
          If ``None``, automatic computation is performed by mode-solving
          the electrical port of the component. If desired, the port
          specification can be overridden by setting ``n_rf`` to
          ``"cross-section"`` (uses :func:`Component.slice_profile`) or to
          a :class:`PortSpec` object.
        z0: Characteristic impedance of the transmission line. If ``None``,
          derived from port impedance, calculated by mode-solving, or set to
          50 Ω.
        z_load: Load impedance. Use ``"z0"`` to match ``z0``.
        z_source: Source impedance. If ``None``, derived from the connected
          port. Use ``"z0"`` to match ``z0``.
        propagation_loss: Optical propagation loss.
        rf_propagation_loss: Electrical propagation loss.
        k2: Quadratic nonlinear phase coefficient.
        k3: Cubic nonlinear phase coefficient.
        optical_input: Name of the optical port used as input. If ``None``,
          the first one is used (sorted alphabetically).
        mesh_refinement: Minimal number of mesh elements per wavelength used
          for mode solving.
        verbose: Flag setting the verbosity of mode solver runs.

    Important:
        The electrical input :math:`A` is converted to a voltage signal
        through the port impedance:

        .. math:: V = \Re\{A\} \sqrt{\Re\{Z_0\}}

    Notes:
        Phase non-linearities are applied before the RF dynamics
        (Hammerstein form).

        The group delay :math:`n_g \ell / c_0` is implemented as a fixed
        multiple of the time step.

    See also:
        :class:`PhaseModTimeStepper`: lumped phase modulator.
    """

    # Flag used within circuits to indicate that this time stepper requires
    # connection information for source impedance calculation.
    _requires_connection_info = True

    def __init__(
        self,
        *,
        v_piL: annotate(PositiveFloat, label="VπL", units="V·μm"),
        length: Coordinate | None = None,
        n_eff: complex | PortSpec | Literal["cross-section"] | None = None,
        n_group: float | None = None,
        n_rf: complex | Interpolator | PortSpec | Literal["cross-section"] | None = None,
        z0: Impedance | Interpolator | None = None,
        z_load: Impedance | Interpolator | Literal["z0"] = "z0",
        z_source: Impedance | Interpolator | Literal["z0"] | None = None,
        propagation_loss: PropagationLoss = 0,
        rf_propagation_loss: PropagationLoss | Interpolator = 0,
        k2: annotate(float, label="k₂", units="rad/μm/V²") = 0,
        k3: annotate(float, label="k₃", units="rad/μm/V³") = 0,
        fir_taps: annotate(PositiveInt, label="FIR Taps") = 4096,
        optical_input: str | None = None,
        mesh_refinement: PositiveFloat | None = None,
        verbose: bool = True,
    ):
        super().__init__(
            v_piL=v_piL,
            length=length,
            n_eff=n_eff,
            n_group=n_group,
            n_rf=n_rf,
            z0=z0,
            z_load=z_load,
            z_source=z_source,
            propagation_loss=propagation_loss,
            rf_propagation_loss=rf_propagation_loss,
            k2=k2,
            k3=k3,
            fir_taps=fir_taps,
            optical_input=optical_input,
            mesh_refinement=mesh_refinement,
            verbose=verbose,
        )

    def setup_state(
        self,
        *,
        component: Component,
        time_step: TimeDelay,
        carrier_frequency: Frequency,
        connections: dict[str, tuple[Port, Technology]] = {},
        verbose: bool | None = None,
        **kwargs,
    ):
        """Initialize internal state.

        Args:
            component: Component representing the laser source.
            time_step: The interval between time steps (in seconds).
            carrier_frequency: The carrier frequency used to construct the time
              stepper. The carrier should be omitted from the input signals, as
              it is handled automatically by the time stepper.
            connections: Mapping of the ports (and respective technologies)
              connected to each of ports in ``component``.
            verbose: If set, overrides the time stepper's `verbose` attribute.
            kwargs: Unused.
        """
        ports = sorted(component.select_ports("optical"))
        e_ports = tuple(component.select_ports("electrical"))
        if len(ports) != 2 or len(e_ports) != 1:
            raise RuntimeError(
                "TerminatedModTimeStepper can only be used in components with 2 optical and 1 "
                "electrical ports."
            )

        p = self.parametric_kwargs

        port_name = p["optical_input"]
        if port_name is not None:
            if port_name == ports[1]:
                ports = ports[::-1]
            elif port_name != ports[0]:
                raise RuntimeError(
                    f"Optical input port {port_name!r} not found in component {component.name!r}."
                )
        e_port = e_ports[0]
        self._e = e_port + "@0"
        self._opt0 = ports[0] + "@0"
        self._opt1 = ports[1] + "@0"
        self.keys = (self._opt0, self._opt1, self._e)

        f_nyquist = 0.5 / time_step
        self._freqs = numpy.linspace(0, f_nyquist, p["fir_taps"])

        n = min(100, p["fir_taps"])
        ms_freqs = numpy.linspace(max(f_nyquist / n, 1e5), f_nyquist, n)

        runners = {}
        tech = component.technology
        mesh_refinement = p["mesh_refinement"]

        if verbose is None:
            verbose = p["verbose"]

        self._n_eff = p["n_eff"]
        self._n_group = p["n_group"]

        if self._n_eff is None or isinstance(self._n_eff, (PortSpec, str)):
            if isinstance(self._n_eff, str):
                if self._n_eff != "cross-section":
                    raise ValueError(
                        f"'n_eff' must be a scalar, PortSpec object, or the string "
                        f"'cross-section'. {self._n_eff!r} is not a valid value."
                    )
                ms_port = _port_with_x_section(ports[0], component)
            else:
                ms_port = component.ports[ports[0]].copy(True)
                if isinstance(self._n_eff, PortSpec):
                    if self._n_eff.classification != "optical":
                        raise ValueError("Port spec used in 'n_eff' is not optical.")
                    ms_port.spec = libcopy.deepcopy(self._n_eff)
            ms_port.center = (0, 0)
            mode_solver = ms_port.to_tidy3d_mode_solver(
                [carrier_frequency],
                mesh_refinement,
                group_index=self._n_group is None,
                technology=tech,
                use_angle_rotation=_isotropic_uniform(tech, "optical"),
            )
            runners["n_eff"] = _ModeSolverRunner(
                mode_solver, [carrier_frequency], mesh_refinement, tech, verbose=verbose
            )

        if self._n_group is None and "n_eff" not in runners:
            # No mode-solver run: fallback to n_eff
            self._n_group = self._n_eff

        self._n_rf = p["n_rf"]
        if self._n_rf is None or isinstance(self._n_rf, (PortSpec, str)):
            if isinstance(self._n_rf, str):
                if self._n_rf != "cross-section":
                    raise ValueError(
                        f"'n_rf' must be a scalar, PortSpec object, or the string "
                        f"'cross-section'. {self._n_rf!r} is not a valid value."
                    )
                ms_port = _port_with_x_section(e_port, component)
            else:
                ms_port = component.ports[e_port].copy(True)
                if isinstance(self._n_rf, PortSpec):
                    if self._n_rf.classification != "electrical":
                        raise ValueError("Port spec used in 'n_rf' is not electrical.")
                    ms_port.spec = libcopy.deepcopy(self._n_rf)
            ms_port.center = (0, 0)
            mode_solver = ms_port.to_tidy3d_mode_solver(
                ms_freqs,
                mesh_refinement,
                technology=tech,
                use_angle_rotation=_isotropic_uniform(tech, "electrical"),
            )
            runners["n_rf"] = _ModeSolverRunner(
                mode_solver, ms_freqs, mesh_refinement, tech, verbose=verbose
            )
            self._ic0 = ms_port.to_tidy3d_impedance_calculator()
        elif isinstance(self._n_rf, Interpolator):
            self._n_rf = self._n_rf(self._freqs)

        self._z0 = p["z0"]
        if self._z0 is None:
            impedance = component.ports[e_port].spec.impedance
            if impedance is not None:
                self._z0 = impedance(self._freqs)[0]
            elif "n_rf" not in runners:
                # No mode-solver run: fallback to 50Ω
                self._z0 = 50.0
        elif isinstance(self._z0, Interpolator):
            self._z0 = self._z0(self._freqs)

        self._z_load = p["z_load"]
        if isinstance(self._z_load, Interpolator):
            self._z_load = self._z_load(self._freqs)

        self._z_source = p["z_source"]
        if self._z_source is None:
            src_port, src_tech = connections.get(e_port, (None, None))
            if not isinstance(src_port, Port):
                self._z_source = 50.0
            elif src_port.spec.impedance is not None:
                self._z_source = src_port.spec.impedance(self._freqs)[0]
            elif src_port.spec._is_1D():
                self._z_source = 50.0
            else:
                ms_port = src_port.copy(True)
                ms_port.center = (0, 0)
                mode_solver = ms_port.to_tidy3d_mode_solver(
                    ms_freqs,
                    mesh_refinement,
                    technology=src_tech,
                    use_angle_rotation=_isotropic_uniform(src_tech, "electrical"),
                )
                runners["z_source"] = _ModeSolverRunner(
                    mode_solver, ms_freqs, mesh_refinement, src_tech, verbose=verbose
                )
                self._ic_source = ms_port.to_tidy3d_impedance_calculator()
        elif isinstance(self._z_source, Interpolator):
            self._z_source = self._z_source(self._freqs)

        self._rf_loss = p["rf_propagation_loss"]
        if isinstance(self._rf_loss, Interpolator):
            self._rf_loss = self._rf_loss(self._freqs)

        self._length = p["length"]
        if self._length is None:
            self._length = 0
            port0 = component.ports[ports[0]]
            port1 = component.ports[ports[1]]
            for _, _, layer in port0.spec.path_profiles_list():
                self._length = max(self._length, route_length(component, layer))
            if self._length <= 0:
                self._length = numpy.sqrt(numpy.sum((port0.center - port1.center) ** 2))

        self._loss = 10 ** (p["propagation_loss"] * self._length / -20.0)

        vL = p["v_piL"] / numpy.pi
        self._v2 = p["k2"] * vL
        self._v3 = p["k3"] * vL
        self._phi1 = (self._length / vL) if vL != 0 else 0

        # updated with n_eff and n_group after runners
        self._phi0 = 2.0 * numpy.pi * carrier_frequency * self._length / C_0
        self._delay = self._length / C_0 / time_step

        self._lock = threading.Lock()
        self._status = {"message": "running", "progress": 0}
        self._setup_thread = threading.Thread(
            daemon=True, target=self._setup_and_monitor, args=(runners,)
        )
        self._setup_thread.start()
        return self

    def _setup_and_monitor(self, runners):
        joint_status = _gather_status(*runners.values())

        with self._lock:
            self._status = dict(joint_status)
            self._status["progress"] *= 0.95

        while joint_status["message"] == "running":
            time.sleep(0.3)
            joint_status = _gather_status(*runners.values())
            with self._lock:
                self._status = dict(joint_status)
                self._status["progress"] *= 0.95

        if joint_status["message"] == "error":
            with self._lock:
                self._status = joint_status
            return

        with self._lock:
            self._status = joint_status
            self._status["message"] = "running"
            self._status["progress"] *= 0.95

        runner = runners.get("n_eff")
        if runner is not None:
            self._n_eff = runner.data.n_complex.values[0, 0].item()
            if self._n_group is None:
                self._n_group = runner.data.n_group.values[0, 0].item()

        runner = runners.get("n_rf")
        if runner is not None:
            n_complex = runner.data.n_complex.isel(mode_index=0)
            self._n_rf = numpy.interp(self._freqs, n_complex.coords["f"].values, n_complex.values)
            if self._z0 is None:
                z = self._ic0.compute_impedance(runner.data).isel(mode_index=0)
                self._z0 = numpy.interp(self._freqs, z.coords["f"].values, z.values)

        self._sqrt_r_in = numpy.mean(numpy.real(self._z0)) ** 0.5

        if isinstance(self._z_load, str) and self._z_load == "z0":
            self._z_load = self._z0

        runner = runners.get("z_source")
        if runner is not None:
            z = self._ic_source.compute_impedance(runner.data).isel(mode_index=0)
            self._z_source = numpy.interp(self._freqs, z.coords["f"].values, z.values)
        elif isinstance(self._z_source, str) and self._z_source == "z0":
            self._z_source = self._z0

        self._phi0 *= self._n_eff
        self._delay = max(0, int(numpy.round(self._n_group * self._delay)))

        s21 = _eo_s21(
            self._freqs,
            self._length,
            self._n_group,
            self._n_rf,
            self._rf_loss,
            self._z0,
            self._z_load,
            self._z_source,
        )

        # Build causal FIR kernel from one-sided EO S21 on the correct FFT grid
        fir_taps = self.parametric_kwargs["fir_taps"]
        n_fft = 1 << int(numpy.ceil(numpy.log2(fir_taps)))
        n_half = n_fft // 2 + 1
        df = 2 * self._freqs[-1] / n_fft
        f = numpy.arange(0, n_half) * df
        s = numpy.interp(f, self._freqs, s21)
        # s = numpy.interp(f, self._freqs, s21.real) + 1j * numpy.interp(f, self._freqs, s21.imag)

        # Two-sided Hermitian spectrum
        h = numpy.empty(n_fft, dtype=complex)
        h[:n_half] = s
        if n_half > 2:
            h[n_half:] = numpy.conj(s[-2:0:-1])

        # IFFT → real impulse
        self._h_fir = numpy.fft.ifft(h).real
        self._v = numpy.empty(fir_taps - 1, dtype=numpy.float64)
        self._buffer = numpy.empty((self._delay, 2), dtype=complex)

        self.reset()

        with self._lock:
            self._status = joint_status
            self._status["message"] = "success"
            self._status["progress"] = 100

    def reset(self):
        """Reset internal state."""
        self._index = 0
        self._buffer[:, :] = 1e-30
        self._v[:] = 0

    @property
    def status(self):
        if not self._setup_thread.is_alive() and self._status["message"] == "running":
            self._status["message"] = "error"
        with self._lock:
            return self._status

    def step_single(
        self,
        inputs: numpy.ndarray,
        outputs: numpy.ndarray,
        time_index: int,
        update_state: bool,
        shutdown: bool,
    ) -> None:
        """Take a single time step on the given inputs.

        Args:
            inputs: Input values at the current time step. Must be a 1D array of
              complex values ordered according to :attr:`keys`.
            outputs: Pre-allocated output array where results will be stored.
              Same size and type as ``inputs``.
            time_index: Time series index for the current input.
            update_state: Whether to update the internal stepper state.
            shutdown: Whether this is the last call to the single stepping
              function for the provided :class:`TimeSeries`.
        """
        v_in = self._sqrt_r_in * inputs[2].real
        # Nonlinear preprocessing
        v_in = v_in * (1 + v_in * (self._v2 + v_in * self._v3))

        # FIR dynamic response
        phi = self._phi0 + self._phi1 * (
            self._h_fir[0] * v_in + numpy.dot(self._h_fir[1:], self._v)
        )

        if self._delay > 0:
            a0, a1 = self._buffer[self._index]
        else:
            a0 = inputs[0]
            a1 = inputs[1]

        outputs[0] = numpy.exp(1j * self._phi0) * self._loss * a1
        outputs[1] = numpy.exp(1j * phi) * self._loss * a0

        if update_state:
            self._v[1:] = self._v[:-1]
            self._v[0] = v_in
            if self._delay > 0:
                a0 = inputs[0]
                a1 = inputs[1]
                self._buffer[self._index] = (a0, a1)
                self._index = (self._index + 1) % self._delay


register_time_stepper_class(PhaseModTimeStepper)
register_time_stepper_class(TerminatedModTimeStepper)
