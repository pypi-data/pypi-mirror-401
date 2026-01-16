import numpy

from .extension import TimeStepper, register_time_stepper_class
from .typing import TimeDelay


class _ArrayDelayBuffer:
    """Array-based delay buffer for high-performance array time stepping."""

    def __init__(self, keys, delays, default_delay, time_step):
        self.keys = keys
        self.num_keys = len(keys)
        self.default_delay_steps = int(default_delay / time_step)

        # compute delay in time steps for each port
        self.delay_steps = numpy.array(
            [int(delays.get(name, default_delay) / time_step) for name in keys],
            dtype=numpy.intp,
        )

        # create buffer array: shape (num_keys, max_delay + 1)
        max_delay = max(self.delay_steps) if self.num_keys > 0 else self.default_delay_steps
        self.buffer_size = max_delay + 1
        self.buffers = numpy.zeros((self.num_keys, self.buffer_size), dtype=complex)
        self.initialized = False

    def reset(self):
        self.buffers.fill(0)
        # lazy initialization: get() returns fallback values until first put()
        self.initialized = False

    def put(self, buffer_index, values):
        """Store values at the current buffer index."""
        for i in range(self.num_keys):
            idx = buffer_index % (self.delay_steps[i] + 1)
            self.buffers[i, idx] = values[i]
        self.initialized = True

    def get(self, buffer_index, fallback, out):
        """Get delayed values from the buffer into pre-allocated output array.

        Args:
            buffer_index: Current buffer position.
            fallback: Array of fallback values for uninitialized or zero-delay ports.
            out: Pre-allocated output array to write results into.

        Returns:
            The same ``out`` array, now containing delayed values.
        """
        if not self.initialized:
            numpy.copyto(out, fallback)
            return out
        for i in range(self.num_keys):
            delay = self.delay_steps[i]
            if delay == 0:
                out[i] = fallback[i]
            else:
                idx = (buffer_index + 1) % (delay + 1)
                out[i] = self.buffers[i, idx]
        return out


class DelayedTimeStepper(TimeStepper):
    """Time stepper that adds time delays to other time steppers.

    Args:
        time_stepper: The time stepper to wrap with delays.
        input_delay: Default delay applied to the inputs.
        output_delay: Default delay applied to the outputs.
    """

    def __init__(
        self,
        time_stepper: TimeStepper,
        input_delay: TimeDelay = 0,
        output_delay: TimeDelay = 0,
    ):
        super().__init__(
            time_stepper=time_stepper, input_delay=input_delay, output_delay=output_delay
        )

    def setup_state(
        self,
        *,
        time_step: float,
        input_delays: dict[str, TimeDelay] = {},
        output_delays: dict[str, TimeDelay] = {},
        **kwargs,
    ):
        """Initialize internal buffers and set port-specific delays.

        Args:
            time_step: The interval between time steps (in seconds).
            input_delays: Mapping of port names to delays to override the
              default input delay.
            output_delays: Mapping of port names to delays to override the
              default output delay.
            kwargs: Unused.
        """
        self.buffer_index = 0
        self.time_stepper = self.parametric_kwargs["time_stepper"]
        self._time_step = time_step
        self._input_delays = input_delays
        self._output_delays = output_delays
        self._buffers_initialized = False

        # Simply return whatever the inner stepper returns
        return self.time_stepper.setup_state(time_step=time_step, **kwargs)

    def _initialize_buffers(self):
        """Initialize delay buffers once the wrapped stepper is ready."""
        if self._buffers_initialized:
            return

        keys = list(self.time_stepper.keys)
        num_keys = len(keys)
        self._input_buffer_array = _ArrayDelayBuffer(
            keys,
            self._input_delays,
            self.parametric_kwargs["input_delay"],
            self._time_step,
        )
        self._output_buffer_array = _ArrayDelayBuffer(
            keys,
            self._output_delays,
            self.parametric_kwargs["output_delay"],
            self._time_step,
        )

        # pre-allocate temporary buffers for step_single (avoids allocation in hot loop)
        self._temp_input_buffer = numpy.zeros(num_keys, dtype=complex)
        self._temp_output_buffer = numpy.zeros(num_keys, dtype=complex)
        self._buffers_initialized = True

    def reset(self):
        self.buffer_index = 0
        if self._buffers_initialized:
            self._input_buffer_array.reset()
            self._output_buffer_array.reset()
        self.time_stepper.reset()

    @property
    def keys(self) -> tuple[str, ...]:
        """Tuple of input/output keys."""
        return tuple(self.time_stepper.keys)

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
              function for the original :class:`TimeSeries`.
        """
        if not self._buffers_initialized:
            self._initialize_buffers()

        buffer_index = self.buffer_index
        if update_state:
            self.buffer_index += 1
            self._input_buffer_array.put(buffer_index, inputs)

        # use pre-allocated buffer for delayed inputs
        self._input_buffer_array.get(buffer_index, inputs, self._temp_input_buffer)

        # step the wrapped time stepper
        self.time_stepper.step_single(
            self._temp_input_buffer, outputs, time_index, update_state, shutdown
        )

        if update_state:
            self._output_buffer_array.put(buffer_index, outputs)

        # get delayed outputs directly into the outputs array
        self._output_buffer_array.get(buffer_index, outputs, self._temp_output_buffer)
        numpy.copyto(outputs, self._temp_output_buffer)

    def _step_single_unchecked(
        self,
        inputs: numpy.ndarray,
        outputs: numpy.ndarray,
        time_index: int,
        update_state: bool,
        shutdown: bool,
    ) -> None:
        """Fast-path step for internal use by CircuitTimeStepper.

        Skips argument validation but still ensures buffers are initialized.
        """
        if not self._buffers_initialized:
            self._initialize_buffers()

        buffer_index = self.buffer_index
        if update_state:
            self.buffer_index += 1
            self._input_buffer_array.put(buffer_index, inputs)

        # use pre-allocated buffer for delayed inputs
        self._input_buffer_array.get(buffer_index, inputs, self._temp_input_buffer)

        # step the wrapped time stepper using fast path if available
        unchecked = getattr(
            self.time_stepper, "_step_single_unchecked", self.time_stepper.step_single
        )
        unchecked(self._temp_input_buffer, outputs, time_index, update_state, shutdown)

        if update_state:
            self._output_buffer_array.put(buffer_index, outputs)

        # get delayed outputs directly into the outputs array
        self._output_buffer_array.get(buffer_index, outputs, self._temp_output_buffer)
        numpy.copyto(outputs, self._temp_output_buffer)


register_time_stepper_class(DelayedTimeStepper)
