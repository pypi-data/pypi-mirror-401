import re
import warnings
from collections.abc import Sequence
from typing import Any, Literal

import numpy
import tidy3d

from .analytic_models import WaveguideModel
from .cache import cache_s_matrix
from .eme_model import EMEModel
from .extension import (
    Z_INF,
    Component,
    ExtrusionSpec,
    GaussianPort,
    MaskSpec,
    Model,
    Port,
    Rectangle,
    Reference,
    SMatrix,
    _content_repr,
    frequency_classification,
    snap_to_grid,
)
from .tidy3d_model import _ModeSolverRunner
from .utils import C_0


def _gather_status(*runners: Any) -> dict[str, Any]:
    """Create an overall status based on a collection of runners."""
    num_tasks = 0
    progress = 0
    message = "success"
    tasks = {}
    for task in runners:
        task_status = (
            {"progress": 100, "message": "success"} if isinstance(task, SMatrix) else task.status
        )
        inner_tasks = task_status.get("tasks", {})
        tasks.update(inner_tasks)
        task_weight = max(1, len(inner_tasks))
        num_tasks += task_weight
        if message != "error":
            if task_status["message"] == "error":
                message = "error"
            elif task_status["message"] == "running":
                message = "running"
                progress += task_weight * task_status["progress"]
            elif task_status["message"] == "success":
                progress += task_weight * 100
    if message == "running":
        progress /= num_tasks
    else:
        progress = 100
    return {"progress": progress, "message": message, "tasks": tasks}


def _reference_ports(component, level, cache):
    if cache is not None and len(cache) > level:
        return cache[level]
    result = []
    index = 0
    if level == 0:
        for reference in component.references:
            for instance in reference.get_repetition():
                result.extend((index, k, v[0]) for k, v in instance.get_ports().items())
                index += 1
    else:
        for reference in component.references:
            ports = _reference_ports(reference.component, level - 1, None)
            for instance in reference.get_repetition():
                for *x, name, port in ports:
                    instance.component = Component(name="", technology=component.technology)
                    instance.component.add_port(port, name)
                    result.append((index, *x, name, instance[name]))
                index += 1
    if cache is not None:
        cache.append(result)
    return result


def _get_port_by_instance(component, port, cache):
    level = 0
    level_ports = _reference_ports(component, level, cache)
    while len(level_ports) > 0:
        for x in level_ports:
            if x[-1] == port:
                return x
        level += 1
        level_ports = _reference_ports(component, level, cache)
    return None


def _validate_query(
    key: tuple[str | re.Pattern | int | None],
) -> tuple[tuple[re.Pattern, int] | None]:
    if len(key) == 0:
        raise KeyError("Empty key is not allowed as query parameter.")
    valid_key = []
    expect_int = False
    for i, k in enumerate(key):
        if k is None:
            if len(valid_key) == 0 or valid_key[-1] is not None:
                valid_key.append(None)
            expect_int = False
        elif isinstance(k, str):
            valid_key.append((re.compile(k), -1))
            expect_int = True
        elif isinstance(k, re.Pattern):
            valid_key.append((re.compile(k), -1))
            expect_int = True
        elif isinstance(k, int) and expect_int:
            valid_key[-1] = (valid_key[-1][0], k)
            expect_int = False
        elif (
            isinstance(k, tuple)
            and len(k) == 2
            and isinstance(k[0], re.Pattern)
            and isinstance(k[1], int)
        ):
            valid_key.append(k)
        else:
            raise RuntimeError(
                f"Invalid value in position {i} in key {tuple(key)}: {k}. Expected a "
                "string, a compiled regular expression pattern, "
                + ("an integer, " if expect_int else "")
                + "or 'None'."
            )
    return tuple(valid_key)


def _compare_angles(a: float, b: float) -> bool:
    r = (a - b) % 360
    return r <= 1e-12 or 360 - r <= 1e-12


# Return a flattening key (for caching) if flattening is required, and
# a bool indicating whether phase correction is required
def _analyze_transform(
    reference: Reference,
    classification: Literal["optical", "electrical"],
    frequencies: Sequence[float],
) -> tuple[tuple[tuple[float, float] | None, float, bool] | None, bool]:
    technology = reference.component.technology

    background_medium = technology.get_background_medium(classification)
    extrusion_media = [e.get_medium(classification) for e in technology.extrusion_specs]

    uniform = background_medium.is_spatially_uniform and all(
        medium.is_spatially_uniform for medium in extrusion_media
    )

    translated = not numpy.allclose(reference.origin, (0, 0), atol=1e-12)
    rotated = not _compare_angles(reference.rotation, 0)

    if not uniform and (translated or rotated):
        return (tuple(reference.origin.tolist()), reference.rotation, reference.x_reflection), None

    if reference.x_reflection:
        return (None, reference.rotation, reference.x_reflection), None

    # _align_and_overlap only works for rotations that are a multiple of 90°
    rotation_fraction = reference.rotation % 90
    is_multiple_of_90 = rotation_fraction < 1e-12 or (90 - rotation_fraction < 1e-12)
    if not is_multiple_of_90:
        return (None, reference.rotation, reference.x_reflection), None

    # _align_and_overlap does not support angled ports either
    ports = reference.component.select_ports(classification)
    for port in ports.values():
        if isinstance(port, GaussianPort):
            _, _, _, theta, _ = port._axis_aligned_properties(frequencies)
        else:
            _, _, _, theta, _ = port._axis_aligned_properties()
        if theta != 0.0:
            return (None, reference.rotation, reference.x_reflection), None

    translated_mask = any(e.mask_spec.uses_translation() for e in technology.extrusion_specs)
    if translated_mask and rotated:
        return (None, reference.rotation, reference.x_reflection), None

    fully_anisotropic = background_medium.is_fully_anisotropic or any(
        medium.is_fully_anisotropic for medium in extrusion_media
    )
    in_plane_isotropic = (
        not fully_anisotropic
        and (
            not isinstance(background_medium, tidy3d.AnisotropicMedium)
            or background_medium.xx == background_medium.yy
        )
        and all(
            (not isinstance(medium, tidy3d.AnisotropicMedium) or medium.xx == medium.yy)
            for medium in extrusion_media
        )
    )

    if (fully_anisotropic and rotated) or (
        not in_plane_isotropic and rotated and not _compare_angles(reference.rotation, 180)
    ):
        return (None, reference.rotation, reference.x_reflection), None

    return None, rotated


def _de_embedding_straight(name, port, length, technology, mesh_refinement, verbose):
    component = Component(name, technology)
    port_spec = port.spec

    a = port.input_direction / 180 * numpy.pi
    end_point = snap_to_grid(port.center + length * numpy.array([numpy.cos(a), numpy.sin(a)]))
    for layer, path in port_spec.get_paths(port.center):
        component.add(layer, path.segment(end_point))

    component.add_port(port, "B0")
    component.add_port(Port(end_point, 180 + port.input_direction, port_spec, inverted=True), "B1")
    component.add_model(
        WaveguideModel(length=-length, mesh_refinement=mesh_refinement, verbose=verbose)
    )

    return component


class _ImpedanceMismatchRunner:
    def __init__(self, frequencies, ports, technologies, mesh_refinement, verbose, cost_estimation):
        self.frequencies = frequencies
        self.ports = ports
        self.runners = {}
        for (name, port), technology in zip(ports.items(), technologies, strict=True):
            # No mode solver runs for 1D ports: fallback to 50Ω
            if port.spec.impedance is None and not port.spec._is_1D():
                if port.spec.polarization != "":
                    raise RuntimeError(
                        "Butt-coupling is not supported on ports with polarization filtering."
                    )
                self.runners[name] = _ModeSolverRunner(
                    port,
                    frequencies,
                    mesh_refinement,
                    technology,
                    center_in_origin=True,
                    cost_estimation=cost_estimation,
                    verbose=verbose,
                )

    @property
    def status(self):
        all_stat = [runner.status for runner in self.runners.values()]
        tasks = {}
        for s in all_stat:
            tasks.update(s.get("tasks", {}))

        if all(s["message"] == "success" for s in all_stat):
            message = "success"
            progress = 100
        elif any(s["message"] == "error" for s in all_stat):
            message = "error"
            progress = 100
        else:
            message = "running"
            progress = sum(
                100 if s["message"] == "success" else s["progress"] for s in all_stat
            ) / len(all_stat)
        return {"progress": progress, "message": message, "tasks": tasks}

    @property
    def s_matrix(self):
        num_modes = min(p.num_modes for p in self.ports.values())
        names = sorted(self.ports)
        z = [None, None]
        for index, name in enumerate(names):
            port = self.ports[name]
            if port.spec.impedance is not None:
                z[index] = port.spec.impedance(self.frequencies)[:num_modes]
            elif name in self.runners:
                ic = port.to_tidy3d_impedance_calculator()
                impedance = ic.compute_impedance(self.runners[name].data)
                # Only valid for polarization == ""
                z[index] = impedance.transpose("mode_index", "f").values[:num_modes]
            else:
                z[index] = numpy.full((num_modes, len(self.frequencies)), 50.0 + 0j)

        y = 1 / (z[0] + z[1])
        r = y * (z[1] - z[0])
        t = 2 * y * numpy.sqrt(z[0] * z[1])
        s = (
            (r, t),
            (t, -r),
        )
        elements = {
            (f"{port_in}@{mode}", f"{port_out}@{mode}"): s[j][i][mode]
            for i, port_in in enumerate(names)
            for j, port_out in enumerate(names)
            for mode in range(num_modes)
        }
        return SMatrix(self.frequencies, elements, ports=self.ports)


class _ImpedanceMismatchModel(Model):
    def __init__(self, port0, port1, technology0, technology1, mesh_refinement, verbose):
        super().__init__(
            port0=port0,
            port1=port1,
            technology0=technology0,
            technology1=technology1,
            mesh_refinement=mesh_refinement,
            verbose=verbose,
        )

    @cache_s_matrix
    def start(
        self,
        component: Component,
        frequencies: Sequence[float],
        *,
        verbose: bool | None = None,
        cost_estimation: bool = False,
        **kwargs: Any,
    ):
        p = self.parametric_kwargs
        if verbose is None:
            verbose = p["verbose"]

        return _ImpedanceMismatchRunner(
            frequencies,
            {"B0": p["port0"], "B1": p["port1"]},
            (p["technology0"], p["technology1"]),
            p["mesh_refinement"],
            verbose,
            cost_estimation,
        )

    def black_box_component(self):
        p = self.parametric_kwargs
        port0 = p["port0"].copy()
        port1 = p["port1"].copy()
        port0.input_direction = 0
        port1.input_direction = 180
        w = max(port0.spec.width, port1.spec.width)
        component = Component("Butt-Coupler", p["technology0"])
        component.add(Rectangle(center=(0, 0), size=(2 * w, w)))
        component.add_port(port0, "B0")
        component.add_port(port1, "B1")
        component.add_model(self)
        return component


_warn_butt_coupling = True


def _process_butt_coupling(netlist, wavelength, mesh_refinement, verbose):
    global _warn_butt_coupling
    if _warn_butt_coupling:
        _warn_butt_coupling = False
        warnings.warn(
            "Automatic butt-coupling handling is an experimental feature. Manual modeling of the "
            "connection (using e.g. 'pf.parametric.transition') may give more accurate results. ",
            stacklevel=5,
        )

    instances = netlist["instances"]
    virtual_connections = netlist["virtual connections"]
    for (index0, name0, num_modes0), (index1, name1, num_modes1) in netlist["butt couplings"]:
        technology0 = instances[index0].component.technology
        technology1 = instances[index1].component.technology
        port0 = instances[index0][name0]
        port1 = instances[index1][name1]
        fraction = port0.input_direction % 90

        if not isinstance(port0, Port) or not isinstance(port1, Port):
            if num_modes0 != num_modes1:
                raise RuntimeError(
                    f"Butt-coupling is only supported for Port instances. Connection between ports "
                    f"{name0} in '{instances[index0].component_name}' and {name1} in "
                    f"'{instances[index1].component_name}' with different numbers of modes is not "
                    f"supported."
                )
            warnings.warn(
                f"Butt-coupling is only supported for Port instances. Connection between ports "
                f"{name0} in '{instances[index0].component_name}' and {name1} in "
                f"'{instances[index1].component_name}' will be ideal.",
                stacklevel=3,
            )
            virtual_connections.append(((index0, name0, num_modes0), (index1, name1, num_modes1)))

        elif (
            port0.spec._is_1D()
            or port1.spec._is_1D()
            or port0.spec.impedance is not None
            or port1.spec.impedance is not None
        ):
            model = _ImpedanceMismatchModel(
                port0, port1, technology0, technology1, mesh_refinement, verbose
            )
            coupler = model.black_box_component()
            ref = Reference(coupler)
            index = len(instances)
            instances.append(ref)
            virtual_connections.extend(
                [
                    ((index0, name0, num_modes0), (index, "B0", num_modes0)),
                    ((index1, name1, num_modes1), (index, "B1", num_modes1)),
                ]
            )

        elif fraction > 1e-12 and 90 - fraction > 1e-12:
            if num_modes0 != num_modes1:
                raise RuntimeError(
                    f"Butt-coupling is only supported for axis-aligned ports. Connection between "
                    f"ports {name0} in '{instances[index0].component_name}' and {name1} in "
                    f"'{instances[index1].component_name}' with different numbers of modes is not "
                    f"supported."
                )
            warnings.warn(
                f"Butt-coupling is only supported for axis-aligned ports. Connection between ports "
                f"{name0} in '{instances[index0].component_name}' and {name1} in "
                f"'{instances[index1].component_name}' will be ideal.",
                stacklevel=3,
            )
            virtual_connections.append(((index0, name0, num_modes0), (index1, name1, num_modes1)))

        else:
            if technology0 != technology1:
                raise RuntimeError(
                    "Butt-coupling is not supported across ports from different technologies."
                )

            # Add PECMedium around the ports to make sure the modes found in EME match the
            # ones found during mode-solving. We add a PEC extrusion rule to technology.
            technology = technology0.copy(True)
            layers = [x.layer for x in technology.layers.values()]
            layer = (100000, 100000)
            while layer in layers:
                layer = (layer[0] + 1, layer[1] + 1)
            technology.insert_extrusion_spec(
                -1, ExtrusionSpec(MaskSpec(layer), tidy3d.PECMedium(), (-Z_INF, Z_INF))
            )

            spec0 = port0.spec
            spec1 = port1.spec
            width = max(spec0.width, spec1.width)
            gap = abs(spec0.width - spec1.width)

            if gap > 0:
                port0 = port0.copy(True)
                spec0 = port0.spec
                offset = 0.5 * spec0.width + 0.5 * gap
                spec0.path_profiles = [
                    (gap, offset, layer),
                    (gap, -offset, layer),
                    *spec0.path_profiles_list(),
                ]
                port1 = port1.copy(True)
                spec1 = port1.spec
                offset = 0.5 * spec1.width + 0.5 * gap
                spec1.path_profiles = [
                    (gap, offset, layer),
                    (gap, -offset, layer),
                    *spec1.path_profiles_list(),
                ]

            length = min(2 * width, 0.5 * wavelength)
            straight0 = _de_embedding_straight(
                f"Butt-Coupler_{index0}_{name0}",
                port0,
                length,
                technology,
                mesh_refinement,
                verbose,
            )
            straight1 = _de_embedding_straight(
                f"Butt-Coupler_{index1}_{name1}",
                port1,
                length,
                technology,
                mesh_refinement,
                verbose,
            )

            coupler = Component(f"Butt-Coupler_{index0}_{name0}_{index1}_{name1}", technology)
            r0 = coupler.add_reference(straight0)
            r1 = coupler.add_reference(straight1)

            coupler.add_port(r0["B1"], "B0")
            coupler.add_port(r1["B1"], "B1")

            direction = round(port0.input_direction % 360) // 90
            propagation_axis = direction % 2
            transversal_axis = 1 - propagation_axis

            bounds = ([None, None, None], [None, None, None])
            bounds[0][transversal_axis] = -0.5 * width
            bounds[1][transversal_axis] = 0.5 * width

            eme_num_modes0 = spec0.num_modes + spec0.added_solver_modes
            eme_num_modes1 = spec1.num_modes + spec1.added_solver_modes
            mode_spec0 = tidy3d.EMEModeSpec(num_modes=eme_num_modes0, target_neff=spec0.target_neff)
            mode_spec1 = tidy3d.EMEModeSpec(num_modes=eme_num_modes1, target_neff=spec1.target_neff)
            mode_specs = [mode_spec0, mode_spec1] if direction > 1 else [mode_spec1, mode_spec0]

            center = port0.center[propagation_axis]

            coupler.add_model(
                EMEModel(
                    eme_grid_spec=tidy3d.EMEExplicitGrid(
                        boundaries=[center], mode_specs=mode_specs
                    ),
                    bounds=bounds,
                    grid_spec=mesh_refinement,
                    verbose=verbose,
                )
            )

            r2 = Reference(coupler)
            i0 = len(instances)
            i1 = i0 + 1
            i2 = i1 + 1
            instances.extend([r0, r1, r2])
            virtual_connections.extend(
                [
                    ((index0, name0, num_modes0), (i0, "B1", num_modes0)),
                    ((index1, name1, num_modes1), (i1, "B1", num_modes1)),
                    ((i0, "B0", num_modes0), (i2, "B0", num_modes0)),
                    ((i1, "B0", num_modes1), (i2, "B1", num_modes1)),
                ]
            )


def _process_component_netlist(
    component,
    frequencies,
    mesh_refinement,
    monitors,
    updates,
    chain_technology_updates,
    verbose,
    cost_estimation,
    kwargs,
    s_matrix_kwargs,
    time_stepper_kwargs,
):
    classification = frequency_classification(frequencies)
    netlist = component.get_netlist()
    if len(netlist["butt couplings"]) > 0:
        _process_butt_coupling(netlist, C_0 / numpy.min(frequencies), mesh_refinement, verbose)

    # 'inputs' is not supported in CircuitModel
    kwargs = dict(kwargs)
    if "inputs" in kwargs:
        del kwargs["inputs"]

    reference_index = {}

    valid_updates = [(_validate_query(k), v) for k, v in updates.items()]

    if isinstance(monitors, dict):
        valid_monitors = []
        cache = []
        for monitor_name, port in monitors.items():
            match = _get_port_by_instance(component, port, cache)
            if match is None:
                warnings.warn(
                    f"{port} does not match any circuit ports and will be ignored.", stacklevel=2
                )
            else:
                *indices, port_name, port = match
                valid_monitors.append((indices, port_name, port.num_modes, monitor_name))
    else:
        valid_monitors = monitors

    # Store copies of instance ports and their reference for phase correction
    instance_port_data = [(None, None)] * len(netlist["instances"])

    runners = {}
    time_steppers = {}
    flattened_component_cache = {}
    active_monitors = []

    for index, reference in enumerate(netlist["instances"]):
        ref_component = reference.component
        current_reference_index = reference_index.get(ref_component.name, -1) + 1
        reference_index[ref_component.name] = current_reference_index

        if ref_component.select_active_model(classification) is None:
            # Check if the model is really needed
            if any(
                index0 == index or index1 == index
                for (index0, _, _), (index1, _, _) in netlist["connections"]
                + netlist["butt couplings"]
                + netlist["virtual connections"]
            ) or any(i == index for i, _, _ in netlist["ports"]):
                raise RuntimeError(f"Component '{ref_component.name}' has no active model.")
            continue

        ports = ref_component.select_ports(classification)
        instance_port_data[index] = (
            tuple((port_name, port.copy(True)) for port_name, port in ports.items()),
            None,
        )

        # Match updates with current reference
        reference_updates = {}
        technology_updates = {}
        component_updates = {}
        model_updates = {}
        for key, value in valid_updates:
            if key[0] is None:
                reference_updates[key] = value
                key = key[1:]
            if len(key) == 0:
                technology_updates.update(value.get("technology_updates", {}))
                component_updates.update(value.get("component_updates", {}))
                model_updates.update(value.get("model_updates", {}))
            elif key[0][0].match(ref_component.name):
                if key[0][1] < 0 or key[0][1] == current_reference_index:
                    if len(key) == 1:
                        technology_updates.update(value.get("technology_updates", {}))
                        component_updates.update(value.get("component_updates", {}))
                        model_updates.update(value.get("model_updates", {}))
                    else:
                        reference_updates[key[1:]] = value

        # Match monitors
        monitors = []
        for indices, port_name, num_modes, monitor_name in valid_monitors:
            if indices[0] == index:
                if len(indices) == 1:
                    active_monitors.append((index, port_name, num_modes, monitor_name))
                else:
                    active_monitors.append((index, monitor_name, num_modes, monitor_name))
                    monitors.append((indices[1:], port_name, num_modes, monitor_name))

        # Apply required updates
        reset_list = reference.update(
            technology_updates=technology_updates,
            component_updates=component_updates,
            model_updates=model_updates,
            chain_technology_updates=chain_technology_updates,
            classification=classification,
        )

        # Account for reference transformations
        inner_component = ref_component
        flattening_key, requires_phase_correction = _analyze_transform(
            reference, classification, frequencies
        )
        if flattening_key is not None:
            flattening_key = _content_repr(ref_component, *flattening_key, include_config=False)
            inner_component = flattened_component_cache.get(flattening_key)
            if inner_component is None:
                inner_component = reference.transformed_component(ref_component.name + "-flattened")
                flattened_component_cache[flattening_key] = inner_component
        elif requires_phase_correction:
            # S matrix correction factor depends on the mode solver for transformed ports
            port_keys = {}
            for port_name, port in ports.items():
                # TODO: Phase correction for fiber and Gaussian ports
                # No mode solver runs for 1D ports
                if isinstance(port, Port) and not port.spec._is_1D():
                    runners[(index, port_name, 0)] = _ModeSolverRunner(
                        port,
                        frequencies[:1],
                        mesh_refinement,
                        ref_component.technology,
                        cost_estimation=cost_estimation,
                        verbose=verbose,
                    )
                    runners[(index, port_name, 1)] = _ModeSolverRunner(
                        reference[port_name],
                        frequencies[:1],
                        mesh_refinement,
                        ref_component.technology,
                        cost_estimation=cost_estimation,
                        verbose=verbose,
                    )
                    port_keys[port_name] = _content_repr(
                        ref_component.technology,
                        port.spec,
                        port.input_direction % 360,
                        port.inverted,
                        reference.rotation % 360,
                        include_config=False,
                    )

            instance_port_data[index] = (instance_port_data[index][0], port_keys)

        if time_stepper_kwargs is not None:
            instance_kwargs = dict(time_stepper_kwargs)
            instance_kwargs["updates"] = {}
            instance_kwargs["chain_technology_updates"] = chain_technology_updates
            instance_kwargs.update(kwargs)
            instance_kwargs.update(reference_updates.pop("time_stepper_kwargs", {}))
            # TODO: Reference.time_stepper_kwargs
            # if reference.time_stepper_kwargs is not None:
            #     instance_kwargs.update(reference.time_stepper_kwargs)
            instance_kwargs["updates"].update(reference_updates)
            instance_kwargs["monitors"] = monitors
            instance_kwargs["component"] = inner_component
            instance_kwargs["show_progress"] = False

            time_stepper = ref_component.select_active_model(classification).time_stepper.__copy__()
            time_steppers[index] = time_stepper

            if getattr(time_stepper, "_requires_connection_info", False):
                instance_connections = {}
                # NOTE: Butt couplings must be checked first, otherwise any impedance mismatch
                # will be masked by the added instances/connections from butt-coupling processing
                for connection_type in ("butt couplings", "connections", "virtual connections"):
                    for (index0, name0, _), (index1, name1, _) in netlist[connection_type]:
                        if index0 == index and name0 not in instance_connections:
                            other_ref = netlist["instances"][index1]
                            instance_connections[name0] = (
                                other_ref[name1],
                                other_ref.component.technology,
                            )
                        if index1 == index and name1 not in instance_connections:
                            other_ref = netlist["instances"][index0]
                            instance_connections[name1] = (
                                other_ref[name0],
                                other_ref.component.technology,
                            )
                instance_kwargs["connections"] = instance_connections

            runners[index] = time_stepper.setup_state(**instance_kwargs)

        elif s_matrix_kwargs is not None:
            instance_kwargs = dict(s_matrix_kwargs)
            instance_kwargs["updates"] = {}
            instance_kwargs["chain_technology_updates"] = chain_technology_updates
            instance_kwargs.update(kwargs)
            instance_kwargs.update(reference_updates.pop("s_matrix_kwargs", {}))
            if reference.s_matrix_kwargs is not None:
                instance_kwargs.update(reference.s_matrix_kwargs)
            instance_kwargs["updates"].update(reference_updates)

            runners[index] = ref_component.select_active_model(classification).start(
                inner_component, frequencies, **instance_kwargs
            )

        # Reset all updates
        for item, kwds in reset_list:
            item.parametric_kwargs = kwds
            item.update()

    if len(runners) == 0:
        warnings.warn(
            f"No subcomponents found in the circuit model for component '{component.name}'.",
            stacklevel=2,
        )

    component_ports = {
        name: port.copy(True) for name, port in component.select_ports(classification).items()
    }
    port_connections = netlist["ports"]
    # In the circuit model, virtual connections behave like real connections
    connections = netlist["connections"] + netlist["virtual connections"]

    return (
        runners,
        time_steppers,
        component_ports,
        port_connections,
        connections,
        instance_port_data,
        active_monitors,
    )
