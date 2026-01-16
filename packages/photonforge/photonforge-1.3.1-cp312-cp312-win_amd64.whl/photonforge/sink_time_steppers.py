import numpy
from numpy.random import SeedSequence, default_rng
from scipy.signal import firwin2

from .extension import Component, Interpolator, TimeStepper, register_time_stepper_class
from .modulator_time_steppers import _get_impedance_runner
from .typing import (
    Frequency,
    Impedance,
    NonNegativeFloat,
    NonNegativeInt,
    PositiveFloat,
    TimeDelay,
    annotate,
)
from .utils import Q as _Q

_PINK_TAPS = 2048
_PINK_SAMPLES = 100


class _LPFilter:
    def __init__(self, f_3dB, time_step):
        self.alpha = numpy.exp(-2.0 * numpy.pi * f_3dB * time_step)
        self.reset()

    def reset(self):
        self.y = 0

    def __call__(self, x, update_state):
        y = self.alpha * self.y + (1.0 - self.alpha) * x
        if update_state:
            self.y = y
        return y


# Direct-Form II Transposed biquad filter
class _BiquadDF2T:
    def __init__(self, frequency, quality, gain, time_step):
        # Design a 2nd-order lowpass via bilinear transform with prewarping.
        k = 2 / time_step
        w0p = k * numpy.tan(numpy.pi * frequency * time_step)
        a = k**2
        b = (w0p / quality) * k
        c = w0p**2
        den = a + b + c
        self.b0 = (gain * c) / den
        self.b1 = (2 * gain * c) / den
        self.b2 = self.b0
        self.a1 = (2 * (c - a)) / den
        self.a2 = (a - b + c) / den
        self.reset()

    def reset(self):
        self.state = (0, 0)

    def __call__(self, x, update_state):
        y = self.b0 * x + self.state[0]
        if update_state:
            self.state = (self.b1 * x - self.a1 * y + self.state[1], self.b2 * x - self.a2 * y)
        return y


class _PinkNoiseApproximator:
    def __init__(self, scale):
        self.scale = scale
        self.b = (0.049922035, -0.095993537, 0.050612699, -0.004408786)
        self.a = (-2.494956002, 2.017265875, -0.522189400)

    def reset(self, rng):
        self.state = [0, 0, 0]
        self.rng = rng
        self.norm = 1.0
        samples = 5000
        rms = (sum(self.sample() ** 2 for _ in range(samples)) / samples) ** 0.5
        self.norm = self.scale / max(1e-12, rms)

    def sample(self):
        w = self.rng.normal(0.0, 1.0)
        y = self.state[0] + self.b[0] * w
        self.state = (
            self.state[1] + self.b[1] * w - self.a[0] * y,
            self.state[2] + self.b[2] * w - self.a[1] * y,
            self.b[3] * w - self.a[2] * y,
        )
        return self.norm * y


class PhotodiodeTimeStepper(TimeStepper):
    r"""Time-stepper for a photodiode and a transimpedance amplifier (TIA).

    This model simulates a photodetector front-end, converting an incident
    optical field into an electrical output. The model accounts for
    space-charge saturation in the photodiode, output saturation in the TIA,
    and response bandwidth limit via a low-pass filter. It also includes
    shot, thermal, and pink noise simulation.


    Args:
        responsivity: Optical power to current conversion factor.
        gain: TIA gain.
        saturation_voltage: If non-zero, output saturation voltage of the
          TIA.
        saturation_current: If non-zero, photocurrent of the space-charge
          saturation model.
        roll_off: Roll-off factor for the space-charge saturation model.
        dark_current: Photodiode's dark current.
        thermal_noise: One-sided power spectral density (PSD) of the TIA's
          input-referred thermal noise current.
        pink_noise_frequency: Pink (1/f) noise corner frequency. If set to
          0, pink noise is disabled.
        current_time_constant: Time constant for the running photocurrent
          average. A value of zero sets a default of 100 time steps.
        filter_frequency: If positive, sets the -3 dB frequency bandwidth
          for the first-order low-pass TIA filter. If a second-order filter
          is used (``filter_quality > 0``), this is its natural frequency.
        filter_quality: If positive, enables a second-order filter for the
          TIA with this quality factor. Only when ``filter_frequency > 0``.
        filter_gain: Gain of the second-order TIA filter. Only used when
          ``filter_frequency > 0`` and ``filter_quality > 0``.
        reflection: Reflection coefficient for incident fields.
        z0: Characteristic impedance of the electrical port used to convert
          the output voltage to field amplitude. If ``None``, derived from
          port impedance, calculated by mode-solving, or set to 50 Ω.
        mesh_refinement: Minimal number of mesh elements per wavelength used
          for mode solving.
        verbose: Flag setting the verbosity of mode solver runs.
        seed: Random number generator seed to ensure reproducibility.

    Important:
        The electrical output field amplitude :math:`A` is converted from
        the photodiode voltage through the port impedance:

        .. math:: A = \frac{V}{\sqrt{\Re\{Z_0\}}}
    """

    def __init__(
        self,
        *,
        responsivity: annotate(NonNegativeFloat, units="A/W"),
        gain: annotate(float, units="V/A"),
        saturation_voltage: annotate(NonNegativeFloat, units="V") = 0,
        saturation_current: NonNegativeFloat = 0,
        roll_off: NonNegativeFloat = 2,
        dark_current: annotate(float, units="A") = 0,
        thermal_noise: annotate(NonNegativeFloat, units="A²/Hz") = 0,
        pink_noise_frequency: Frequency = 0,
        current_time_constant: TimeDelay = 0,
        filter_frequency: Frequency = 0,
        filter_quality: NonNegativeFloat = 0,
        filter_gain: PositiveFloat = 1,
        reflection: complex = 0,
        z0: Impedance | Interpolator | None = None,
        mesh_refinement: PositiveFloat | None = None,
        verbose: bool = True,
        seed: NonNegativeInt | None = None,
    ):
        super().__init__(
            responsivity=responsivity,
            gain=gain,
            saturation_voltage=saturation_voltage,
            saturation_current=saturation_current,
            roll_off=roll_off,
            dark_current=dark_current,
            thermal_noise=thermal_noise,
            pink_noise_frequency=pink_noise_frequency,
            current_time_constant=current_time_constant,
            filter_frequency=filter_frequency,
            filter_quality=filter_quality,
            filter_gain=filter_gain,
            reflection=reflection,
            z0=z0,
            mesh_refinement=mesh_refinement,
            verbose=verbose,
            seed=seed,
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
        ports = tuple(component.select_ports("optical"))
        e_ports = tuple(component.select_ports("electrical"))
        if len(ports) != 1 or len(e_ports) != 1:
            raise RuntimeError(
                "PhotodiodeTimeStepper can only be used in components with 1 optical port and 1 "
                "electrical port."
            )
        self._port = ports[0] + "@0"
        self._e_port = e_ports[0] + "@0"
        self.keys = (self._port, self._e_port)

        self._time_step = time_step

        p = self.parametric_kwargs

        self._responsivity = abs(p["responsivity"])
        self._gain = abs(p["gain"])
        self._saturation_voltage = abs(p["saturation_voltage"])
        self._saturation_current = p["saturation_current"]
        self._roll_off = p["roll_off"]
        self._dark_current = abs(p["dark_current"])
        self._thermal_noise = abs(p["thermal_noise"])
        self._r = complex(p["reflection"])

        tau = p["current_time_constant"]
        if tau <= 0:
            tau = 100 * time_step
        self._current_factor = 1 - numpy.exp(-time_step / tau)

        self._filter = None
        if p["filter_frequency"] > 0:
            self._filter = (
                _BiquadDF2T(
                    p["filter_frequency"], p["filter_quality"], abs(p["filter_gain"]), time_step
                )
                if p["filter_quality"] > 0
                else _LPFilter(p["filter_frequency"], time_step)
            )

        nyquist = 0.5 / time_step
        fp = abs(p["pink_noise_frequency"])
        self._pink_noise = None
        if 0 < fp < nyquist:
            f_min = 1e-3 * fp
            f_max = min(1e3 * fp, 0.99 * nyquist)
            freqs = numpy.logspace(numpy.log10(f_min), numpy.log10(f_max), _PINK_SAMPLES)
            gains = numpy.sqrt(fp / freqs)
            freqs = numpy.concatenate(([0.0], freqs, [nyquist]))
            gains = numpy.concatenate((gains[:1], gains, [0.0]))
            self._pink_noise = firwin2(_PINK_TAPS, freqs, gains, fs=1 / time_step)

        self._seed = SeedSequence() if p["seed"] is None else p["seed"]

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
        self._current = 0.0
        if self._filter is not None:
            self._filter.reset()
        if self._pink_noise is not None:
            self._pink_noise_state = numpy.zeros(self._pink_noise.size - 1)
        self._rng = default_rng(self._seed)
        self._sample_noise()

    def _sample_noise(self):
        noise = 2 * _Q * (self._current + self._dark_current) + self._thermal_noise
        stdev = (0.5 * noise / self._time_step) ** 0.5
        self._current_noise = self._rng.normal(0, stdev)
        if self._pink_noise is not None:
            x = self._rng.normal(0, 1)
            self._current_noise += stdev * (
                self._pink_noise[0] * x + numpy.dot(self._pink_noise[1:], self._pink_noise_state)
            )
            self._pink_noise_state[1:] = self._pink_noise_state[:-1]
            self._pink_noise_state[0] = x

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
        a_in = inputs[0]
        current_in = self._responsivity * abs(a_in) ** 2

        # space-charge saturation
        current_eff = current_in
        if self._saturation_current > 0:
            x = abs(current_in) / self._saturation_current
            current_eff /= (1 + x**self._roll_off) ** (1 / self._roll_off)

        current_eff += self._current_noise

        if self._filter is not None:
            current_eff = self._filter(current_eff, update_state)

        v_out = self._gain * current_eff
        if self._saturation_voltage > 0:
            v_out = self._saturation_voltage * numpy.tanh(v_out / self._saturation_voltage)

        outputs[0] = self._r * a_in
        outputs[1] = v_out / self._sqrt_r_in

        if update_state:
            self._current += self._current_factor * (current_in - self._current)
            self._sample_noise()


register_time_stepper_class(PhotodiodeTimeStepper)
