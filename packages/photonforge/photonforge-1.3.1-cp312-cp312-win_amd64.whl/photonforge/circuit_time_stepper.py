import threading
import time
import warnings
from collections.abc import Sequence
from typing import Any

import numpy

from . import typing as pft
from .cache import _mode_overlap_cache
from .circuit_base import _gather_status, _process_component_netlist
from .extension import (
    Component,
    FiberPort,
    GaussianPort,
    Port,
    TimeStepper,
    config,
    register_time_stepper_class,
)
from .tidy3d_model import _align_and_overlap


def _stepper(work_queue, *steppers):
    while True:
        work_item = work_queue.get()
        if work_item is None:
            return
        for i, fn in enumerate(steppers):
            work_item[i] = fn(*work_item[i])
        work_queue.task_done()


class CircuitTimeStepper(TimeStepper):
    """Circuit-level time stepper.

    Constructs time steppers for individual circuit elements and handles
    connections between them. Each time stepper initialization is preceded
    by an update to the componoent's technology, the component itself, and
    its active model by calling :attr:`Reference.update`. They are reset to
    their original state afterwards.

    More information on the handling of references and connections can be
    found :class:`CircuitModel`.

    Args:
        mesh_refinement: Minimum number of mesh elements per wavelength used
          for mode solving.
        max_iterations: Maximum number of iterations for self-consistent
          signal propagation through the circuit. A larger value may be
          needed for larger circuits or high-Q feedback loops.
        abs_tolerance: The absolute tolerance for the convergence check.
        rel_tolerance: The relative tolerance for the convergence check.
        max_threads: Maximum number of threads used for stepping individual
          subcomponents.
        verbose: Flag setting the verbosity of mode solver runs.
    """

    def __init__(
        self,
        mesh_refinement: pft.PositiveFloat | None = None,
        max_iterations: pft.PositiveInt = 100,
        abs_tolerance: pft.PositiveFloat = 1e-8,
        rel_tolerance: pft.PositiveFloat = 1e-5,
        max_threads: pft.PositiveInt = 8,
        verbose: bool = True,
    ):
        super().__init__(
            mesh_refinement=mesh_refinement,
            max_iterations=max_iterations,
            abs_tolerance=abs_tolerance,
            rel_tolerance=rel_tolerance,
            max_threads=max_threads,
            verbose=verbose,
        )
        self._status = None

    def setup_state(
        self,
        *,
        component: Component,
        time_step: float,
        carrier_frequency: float,
        monitors: dict[str, Port | FiberPort | GaussianPort] = {},
        updates: dict[Sequence[str | int | None], dict[str, dict[str, Any]]] = {},
        chain_technology_updates: bool = True,
        verbose: bool | None = None,
        **kwargs,
    ):
        """Initialize internal circuit variables.

        Args:
            component: Component for the time stepper.
            time_step: The interval between time steps (in seconds).
            carrier_frequency: The carrier frequency used to construct the time
              stepper. The carrier should be omitted from the input signals, as
              it is handled automatically by the time stepper.
            monitors: Additional ports to include in the outputs as a dictionary
              with monitor names as keys. Subcomponent ports can be obtained
              with :func:`Reference.get_ports` for the 1st level of references
              or with :func:`Component.query` for more deeply-nested ports.
            updates: Dictionary of parameter updates to be applied to
              components, technologies, and models for references within the
              main component. See :func:`CircuitModel.start` for examples.
            chain_technology_updates: if set, a technology update will trigger
              an update for all components using that technology.
            verbose: If set, overrides the model's ``verbose`` attribute and
              is passed to reference models.
            kwargs: Keyword arguments passed to reference models.

        Returns:
            Object with a status dictionary.
        """
        time_stepper_kwargs = {
            "time_step": time_step,
            "carrier_frequency": carrier_frequency,
        }
        if verbose is None:
            verbose = self.parametric_kwargs["verbose"]
        else:
            time_stepper_kwargs["verbose"] = verbose

        frequencies = [carrier_frequency if carrier_frequency > 0 else (1 / time_step)]
        (
            runners,
            self.time_steppers,
            _,
            port_connections,
            self.connections,
            instance_port_data,
            self.monitors,
        ) = _process_component_netlist(
            component,
            frequencies,
            self.parametric_kwargs["mesh_refinement"],
            monitors,
            updates,
            chain_technology_updates,
            verbose,
            False,
            kwargs,
            None,
            time_stepper_kwargs,
        )

        # Build external port names list
        port_conn_list = [
            (index, f"{ref_port_name}@{n}", f"{port_name}@{n}")
            for (index, ref_port_name, num_modes), port_name in port_connections.items()
            for n in range(num_modes)
        ]
        external_port_names = sorted({pc[2] for pc in port_conn_list})
        for _index, _port_name, num_modes, monitor_name in self.monitors:
            for mode in range(num_modes):
                external_port_names.append(f"{monitor_name}@{mode}-")
                external_port_names.append(f"{monitor_name}@{mode}+")
        self._external_port_names = tuple(external_port_names)

        # Store data needed by background thread
        self._setup_data = (
            runners,
            instance_port_data,
            self.connections,
            self.monitors,
            port_conn_list,
            {name: i for i, name in enumerate(external_port_names)},
        )

        self._component_name = component.name
        self._lock = threading.Lock()
        self._status = {"message": "running", "progress": 0}
        self._setup_thread = threading.Thread(daemon=True, target=self._setup_and_monitor)
        self._setup_thread.start()
        return self

    def _setup_and_monitor(self):
        (
            runners,
            instance_port_data,
            self.connections,
            self.monitors,
            port_conn_list,
            ext_port_to_idx,
        ) = self._setup_data
        del self._setup_data

        runners = {k: v for k, v in runners.items() if v is not None}
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

        # Compute mode factors for rotated ports
        mode_factors = [{} for _ in range(len(instance_port_data))]
        for index, (instance_ports, instance_keys) in enumerate(instance_port_data):
            if instance_ports is None or instance_keys is None:
                continue
            for port_name, port in instance_ports:
                key = instance_keys.get(port_name)
                if key is None:
                    continue
                overlap = _mode_overlap_cache[key]
                if overlap is None:
                    overlap = _align_and_overlap(
                        runners[(index, port_name, 0)].data, runners[(index, port_name, 1)].data
                    )[0]
                    _mode_overlap_cache[key] = overlap
                mode_factors[index].update(
                    {f"{port_name}@{mode}": overlap[mode] for mode in range(port.num_modes)}
                )
            with self._lock:
                self._status["progress"] = 95 + 5 * (index + 1) / len(instance_port_data)

        self._build_fast_lookup_tables(
            mode_factors, port_conn_list, ext_port_to_idx, len(instance_port_data)
        )

        self._emitted_convergence_warning = False

        with self._lock:
            self._status["progress"] = 100
            self._status["message"] = "success"

    def _build_fast_lookup_tables(
        self, mode_factors, port_conn_list, ext_port_to_idx, num_instances
    ):
        """Build pre-computed index mappings for fast array-based stepping.

        This method constructs all the lookup tables needed to avoid string-based
        dictionary lookups during the hot stepping loop. All mappings use integer
        indices into numpy arrays.

        The time_steppers dict may have sparse keys (when some netlist instances
        are skipped due to having no active model). We re-index to dense arrays
        for fast iteration in the stepping loop.

        Args:
            mode_factors: List of dicts mapping port names to phase correction factors.
            port_conn_list: List of (instance_idx, ref_port_name, external_port_name) tuples.
            ext_port_to_idx: Dict mapping external port names to array indices.
            num_instances: Total number of netlist instances (including skipped ones).

        Sets:
            _time_steppers_list: Dense list of time steppers for fast iteration.
            _port_state_arrays: Per-instance signal state arrays.
            _mode_factor_data: Per-instance phase correction (indices, values) tuples.
            _connection_index_map: Per-instance connection routing tables.
            _external_port_mappings: External-to-internal port index mappings.
            _monitor_mappings: Monitor port index mappings.
            _child_output_buffers: Pre-allocated output buffers for child steppers.
        """
        # Re-index time_steppers from sparse dict to dense list.
        # The dict keys are original netlist indices which may have gaps when
        # some instances are skipped (no active model and not used in connections).
        sparse_to_dense = {}
        time_steppers_list = []
        for dense_idx, (sparse_idx, ts) in enumerate(self.time_steppers.items()):
            sparse_to_dense[sparse_idx] = dense_idx
            time_steppers_list.append(ts)
        self._time_steppers_list = time_steppers_list

        # Build port name to index mappings for each instance (dense indexing)
        # port_name_to_index[dense_idx]: dict mapping port name -> array index
        port_name_to_index = [
            {name: i for i, name in enumerate(ts.keys)} for ts in time_steppers_list
        ]

        # Initialize array-based port state
        # _port_state_arrays[i]: numpy array of complex values for instance i
        self._port_state_arrays = [
            numpy.zeros(len(pmap), dtype=complex) for pmap in port_name_to_index
        ]

        # Pre-compute mode factor arrays for phase correction at rotated ports
        # _mode_factor_data[dense_idx]: None or (indices_array, values_array) tuple
        # mode_factors uses sparse (original netlist) indices
        self._mode_factor_data = []
        for sparse_idx in self.time_steppers.keys():
            dense_idx = sparse_to_dense[sparse_idx]
            mf = mode_factors[sparse_idx]
            if mf:
                indices = []
                values = []
                for pname, mfval in mf.items():
                    pidx = port_name_to_index[dense_idx].get(pname)
                    if pidx is not None:
                        indices.append(pidx)
                        values.append(mfval)
                if indices:
                    self._mode_factor_data.append(
                        (numpy.array(indices, dtype=numpy.intp), numpy.array(values, dtype=complex))
                    )
                else:
                    self._mode_factor_data.append(None)
            else:
                self._mode_factor_data.append(None)

        # Pre-compute connection index mappings
        # _connection_index_map[dense_idx]: list of (src_port_idx, dst_dense_idx, dst_port_idx)
        # self.connections uses sparse (original netlist) indices
        num_dense = len(time_steppers_list)
        self._connection_index_map = [[] for _ in range(num_dense)]
        connections_map = [{} for _ in range(num_dense)]
        for (idx1, port_name1, num_modes), (idx2, port_name2, _) in self.connections:
            dense1 = sparse_to_dense.get(idx1)
            dense2 = sparse_to_dense.get(idx2)
            if dense1 is None or dense2 is None:
                continue  # Skip connections to instances that were not processed
            for mode in range(num_modes):
                key1 = f"{port_name1}@{mode}"
                key2 = f"{port_name2}@{mode}"
                connections_map[dense1][key1] = (dense2, key2)
                connections_map[dense2][key2] = (dense1, key1)

        for dense_idx in range(num_dense):
            conn_list = []
            for pname, pidx in port_name_to_index[dense_idx].items():
                if pname in connections_map[dense_idx]:
                    dense2, key2 = connections_map[dense_idx][pname]
                    pidx2 = port_name_to_index[dense2].get(key2)
                    if pidx2 is not None:
                        conn_list.append((pidx, dense2, pidx2))
            self._connection_index_map[dense_idx] = conn_list

        # Pre-compute external port mappings
        # _external_port_mappings: list of (external_idx, dense_idx, internal_idx) tuples
        # port_conn_list uses sparse (original netlist) indices
        self._external_port_mappings = []
        for sparse_idx, ref_name, port_name in port_conn_list:
            dense_idx = sparse_to_dense.get(sparse_idx)
            if dense_idx is None:
                continue  # Skip ports for instances that were not processed
            ext_idx = ext_port_to_idx[port_name]
            internal_idx = port_name_to_index[dense_idx].get(ref_name)
            self._external_port_mappings.append((ext_idx, dense_idx, internal_idx))

        # Pre-compute monitor mappings
        # _monitor_mappings: list of (ext_minus_idx, ext_plus_idx, dense_idx, internal_idx)
        # self.monitors uses sparse (original netlist) indices
        self._monitor_mappings = []
        for sparse_idx, port_name, num_modes, monitor_name in self.monitors:
            dense_idx = sparse_to_dense.get(sparse_idx)
            if dense_idx is None:
                continue  # Skip monitors for instances that were not processed
            for mode in range(num_modes):
                internal_idx = port_name_to_index[dense_idx].get(f"{port_name}@{mode}")
                if internal_idx is not None:
                    self._monitor_mappings.append(
                        (
                            ext_port_to_idx[f"{monitor_name}@{mode}-"],
                            ext_port_to_idx[f"{monitor_name}@{mode}+"],
                            dense_idx,
                            internal_idx,
                        )
                    )

        # Pre-allocate output buffers for child steppers
        self._child_output_buffers = [
            numpy.zeros(len(pmap), dtype=complex) for pmap in port_name_to_index
        ]

    def reset(self):
        """Reset the state of the circuit variables."""
        for arr in self._port_state_arrays:
            arr.fill(0)
        self._emitted_convergence_warning = False
        for ts in self.time_steppers.values():
            ts.reset()

    @property
    def status(self):
        if not self._setup_thread.is_alive() and self._status["message"] == "running":
            self._status["message"] = "error"
        with self._lock:
            return self._status

    @property
    def keys(self) -> tuple[str, ...]:
        """Tuple of input/output keys."""
        return self._external_port_names

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
        # Prepare input state (copy if not updating state)
        port_state = self._port_state_arrays
        if update_state:
            input_arrays = list(port_state)
        else:
            input_arrays = [arr.copy() for arr in port_state]

        # Apply external inputs
        for ext_idx, inst_idx, int_idx in self._external_port_mappings:
            if int_idx is not None:
                input_arrays[inst_idx][int_idx] = inputs[ext_idx]

        # Gauss-Seidel iteration
        abs_tol = self.parametric_kwargs["abs_tolerance"]
        rel_tol = self.parametric_kwargs["rel_tolerance"]
        max_iter = max(self.parametric_kwargs["max_iterations"], 1)
        num_instances = len(port_state)
        output_arrays = [None] * num_instances
        time_steppers = self._time_steppers_list
        mode_factor_data = self._mode_factor_data
        connection_map = self._connection_index_map
        child_buffers = self._child_output_buffers

        converged = True
        is_last = False
        for iteration in range(1, max_iter + 1):
            if iteration == max_iter:
                is_last = True

            do_update = update_state and is_last
            do_shutdown = shutdown and is_last

            if not is_last:
                converged = True
            check_conv = not is_last and converged

            for idx in range(num_instances):
                inp = input_arrays[idx]
                mf = mode_factor_data[idx]

                # Apply mode factors
                if mf is not None:
                    inp[mf[0]] *= mf[1]

                # Step (step_single modifies out_buf in-place)
                out_buf = child_buffers[idx]
                out_buf.fill(0)
                # Use fast path if available, otherwise fall back to step_single
                unchecked = getattr(
                    time_steppers[idx], "_step_single_unchecked", time_steppers[idx].step_single
                )
                unchecked(inp, out_buf, time_index, do_update, do_shutdown)

                # Unapply mode factors
                if mf is not None:
                    inp[mf[0]] /= mf[1]
                    out_buf[mf[0]] /= mf[1]

                output_arrays[idx] = out_buf

                # Propagate connections
                for src_idx, dst_inst, dst_idx in connection_map[idx]:
                    val = out_buf[src_idx]
                    dst_arr = input_arrays[dst_inst]
                    if check_conv:
                        v2 = dst_arr[dst_idx]
                        diff = abs(val - v2)
                        if diff > abs_tol and diff > rel_tol * max(abs(val), abs(v2)):
                            converged = False
                            check_conv = False
                    dst_arr[dst_idx] = val

            if is_last:
                break
            if converged:
                is_last = True

        # Commit state if needed
        if update_state:
            for idx in range(num_instances):
                if input_arrays[idx] is not port_state[idx]:
                    numpy.copyto(port_state[idx], input_arrays[idx])

        if max_iter > 1 and not self._emitted_convergence_warning and not converged:
            warnings.warn(
                f"Time stepper for component '{self._component_name}' failed to converge. "
                f"Consider increasing 'max_iterations'.",
                stacklevel=3,
            )
            self._emitted_convergence_warning = True

        # Build output
        outputs.fill(0)
        for ext_idx, inst_idx, int_idx in self._external_port_mappings:
            if int_idx is not None:
                outputs[ext_idx] = output_arrays[inst_idx][int_idx]

        for ext_minus, ext_plus, inst_idx, int_idx in self._monitor_mappings:
            outputs[ext_minus] = input_arrays[inst_idx][int_idx]
            outputs[ext_plus] = output_arrays[inst_idx][int_idx]


register_time_stepper_class(CircuitTimeStepper)
config.default_time_steppers["CircuitModel"] = CircuitTimeStepper()
