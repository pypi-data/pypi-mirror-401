from typing import Annotated, Any, Literal, NewType

from pydantic import BaseModel, Discriminator, Field, Tag

type UInt8 = Annotated[int, Field(ge=0, le=2**8 - 1)]
type UInt32 = Annotated[int, Field(ge=0, le=2**32 - 1)]
type UInt64 = Annotated[int, Field(ge=0, le=2**64 - 1)]
type Int64 = Annotated[int, Field(ge=-(2**63), le=2**63 - 1)]

type Coordinate = Annotated[Int64, Field(json_schema_extra={"scale": 1e-5, "unit": "μm"})]
type Coordinate2D = tuple[Coordinate, Coordinate]
type Coordinate3D = tuple[Coordinate, Coordinate, Coordinate]
type Coordinate2DVector = list[Coordinate2D]

type PositiveCoordinate = Annotated[Coordinate, Field(gt=0)]
type NonNegativeCoordinate = Annotated[Coordinate, Field(ge=0)]

type Float2D = tuple[float, float]
type Float3D = tuple[float, float, float]

type Radius = Annotated[float, Field(gt=0, json_schema_extra={"scale": 1e-5, "unit": "μm"})]

type Fraction = Annotated[float, Field(ge=0, le=1)]
type Angle = Annotated[float, Field(json_schema_extra={"unit": "°"})]

type Complex = tuple[float, float]

type Layer = tuple[UInt32, UInt32]

type Color = tuple[UInt8, UInt8, UInt8, UInt8]  # RGBA

# Union, intersection, difference, symmetric difference
type Operation = Literal["+", "*", "-", "^"]

type Polarization = Literal["", "TE", "TM"]

StoreType = 1
PropertiesType = 2
RandomVariableType = 3
ExpressionType = 4
NativeType = 5  # Used for native python objects
MediumType = 6  # Used for any Tidy3D base models
LayerSpecType = 7
MaskSpecType = 8
ExtrusionSpecType = 9
PortSpecType = 10
TechnologyType = 11
RectangleType = 12
CircleType = 13
PolygonType = 14
PathType = 15
PolyhedronType = 16
ExtrudedType = 17
ConstructiveSolidType = 18
LabelType = 19
PortType = 20
FiberPortType = 21
GaussianPortType = 22
TerminalType = 23
ModelType = 24
ReferenceType = 25
ComponentType = 26
SMatrixType = 27
PoleResidueMatrixType = 28
TimeDomainModelType = 29
TimeSeriesType = 30
TimeStepperType = 31
InterpolatorType = 32

PhotonForgeType = Literal[
    StoreType,
    PropertiesType,
    RandomVariableType,
    ExpressionType,
    NativeType,
    MediumType,
    LayerSpecType,
    MaskSpecType,
    ExtrusionSpecType,
    PortSpecType,
    TechnologyType,
    RectangleType,
    CircleType,
    PolygonType,
    PathType,
    PolyhedronType,
    ExtrudedType,
    ConstructiveSolidType,
    LabelType,
    PortType,
    FiberPortType,
    GaussianPortType,
    TerminalType,
    ModelType,
    ReferenceType,
    ComponentType,
    SMatrixType,
    PoleResidueMatrixType,
    TimeDomainModelType,
    TimeSeriesType,
    TimeStepperType,
    InterpolatorType,
]


NoID = Literal[""]

PropertiesID = NewType("PropertiesID", str)
RandomVariableID = NewType("RandomVariableID", str)
ExpressionID = NewType("ExpressionID", str)
NativeID = NewType("NativeID", str)
MediumID = NewType("MediumID", str)
LayerSpecID = NewType("LayerSpecID", str)
MaskSpecID = NewType("MaskSpecID", str)
ExtrusionSpecID = NewType("ExtrusionSpecID", str)
PortSpecID = NewType("PortSpecID", str)
TechnologyID = NewType("TechnologyID", str)
RectangleID = NewType("RectangleID", str)
CircleID = NewType("CircleID", str)
PolygonID = NewType("PolygonID", str)
PathID = NewType("PathID", str)
PolyhedronID = NewType("PolyhedronID", str)
ExtrudedID = NewType("ExtrudedID", str)
ConstructiveSolidID = NewType("ConstructiveSolidID", str)
LabelID = NewType("LabelID", str)
PortID = NewType("PortID", str)
FiberPortID = NewType("FiberPortID", str)
GaussianPortID = NewType("GaussianPortID", str)
TerminalID = NewType("TerminalID", str)
ModelID = NewType("ModelID", str)
ReferenceID = NewType("ReferenceID", str)
ComponentID = NewType("ComponentID", str)
SMatrixID = NewType("SMatrixID", str)
PoleResidueMatrixID = NewType("PoleResidueMatrixID", str)
TimeDomainModelID = NewType("TimeDomainModelID", str)
TimeSeriesID = NewType("TimeSeriesID", str)
TimeStepperID = NewType("TimeStepperID", str)
InterpolatorID = NewType("InterpolatorID", str)

type ID = (
    PropertiesID
    | RandomVariableID
    | ExpressionID
    | NativeID
    | MediumID
    | LayerSpecID
    | MaskSpecID
    | ExtrusionSpecID
    | PortSpecID
    | TechnologyID
    | RectangleID
    | CircleID
    | PolygonID
    | PathID
    | PolyhedronID
    | ExtrudedID
    | ConstructiveSolidID
    | LabelID
    | PortID
    | FiberPortID
    | GaussianPortID
    | TerminalID
    | ModelID
    | ReferenceID
    | ComponentID
    | SMatrixID
    | PoleResidueMatrixID
    | TimeDomainModelID
    | TimeSeriesID
    | TimeStepperID
    | InterpolatorID
)

type StructureID = RectangleID | CircleID | PolygonID | PathID

type Structure3DID = PolyhedronID | ExtrudedID | ConstructiveSolidID

type AnyPortID = PortID | FiberPortID | GaussianPortID

type NativeData = (
    None
    | bool
    | float
    | str
    | list[NativeData]  # python sequences, except tuple
    | NativeInteger
    | NativeComplex
    | NativeBytes
    | NativeDict
    | NativeTuple
    | NativeRegex
    | NativeTidy3D
    | NativePhotonForge
)


class NativeInteger(BaseModel):
    type: Literal["integer"]
    value: Int64


class NativeComplex(BaseModel):
    type: Literal["complex"]
    real: float
    imag: float


class NativeBytes(BaseModel):
    type: Literal["b64encoded"]
    value: str  # Base64-encoded byte string


class NativeDict(BaseModel):
    type: Literal["dict"]
    values: list[tuple[NativeData, NativeData]]  # (key, value) array


class NativeTuple(BaseModel):
    type: Literal["tuple"]
    values: list[NativeData]


class NativeRegex(BaseModel):
    type: Literal["regex"]
    pattern: str
    flags: int  # flags used in the python re module


class NativeTidy3D(BaseModel):
    type: Literal["tidy3d"]
    # Not all tidy3d models can be serialized as json. In those cases we use a
    # Base64-encoded byte string with the hdf5 representation of the model.
    # Using Any to avoid Pydantic v1/v2 incompatibility with Tidy3dBaseModel.
    value: Any | str


class NativePhotonForge(BaseModel):
    type: Literal["photonforge"]
    id: ID


class BaseType(BaseModel):
    type: PhotonForgeType
    type_version: str  # major.minor
    id: ID
    properties: PropertiesID | NoID


class Native(BaseType):
    type: Literal[NativeType]
    type_version: str
    id: NativeID
    data: NativeData


class ScalarProperty(BaseModel):
    variant: Literal["int64", "double", "string"]
    value: Int64 | float | str


class Property(BaseModel):
    variant: Literal["int64", "double", "string", "array"]
    value: Int64 | float | str | list[ScalarProperty]


class NamedProperties(BaseModel):
    name: str
    values: list[Property]


class Properties(BaseModel):
    type: Literal[PropertiesType]
    type_version: str
    id: PropertiesID
    data: list[NamedProperties]
    metadata: NativeData


class RandomVariable(BaseType):
    variant: Literal["Fixed", "Normal", "Uniform", "Discrete"]
    name: str
    value_spec: NativeData


class SingleExpression(BaseModel):
    name: str
    variant: Literal["float64", "str"]
    value: float | str


# Used in-place, not as a separate object
class DirectExpression(BaseModel):
    parameters: list[str]
    expressions: list[SingleExpression]


# Full object that can be pointed to
class Expression(BaseType):
    parameters: list[str]
    expressions: list[SingleExpression]


class Interpolator(BaseType):
    scalar_value: bool
    method: Literal["linear", "barycentric", "cubicspline", "pchip", "akima", "makima"]
    coords: Literal["real_imag", "mag_phase"]
    x: list[float]
    y: list[list[float] | list[Complex]]


class LayerSpec(BaseType):
    layer: Layer
    description: str
    color: Color
    pattern: Literal[  # hatching patterns
        "solid",  # solid fill
        "hollow",  # no-fill, only outlines
        "\\",  # left 45° lines
        "\\\\",  # dense left 45° lines
        "/",  # right 45° lines
        "//",  # dense right 45° lines
        "|",  # vertical lines
        "||",  # dense vertical lines
        "-",  # horizontal lines
        "=",  # dense horizontal lines
        "x",  # left and right 45° lines
        "xx",  # dense left and right 45° lines
        "+",  # horizontal and vertical lines
        "++",  # dense horizontal and vertical lines
        ".",  # polka-dot pattern
        ":",  # dense polka-dot pattern
    ]


type MaskOperand = list[InnerMaskSpec]


class InnerMaskSpec(BaseModel):
    mask_type: Literal["boolean", "layer"]
    layer: Layer
    operation: Operation
    operands0: MaskOperand
    operands1: MaskOperand
    dilation: Coordinate
    translation: Coordinate2D


class MaskSpec(BaseType):
    mask_type: Literal["boolean", "layer"]
    layer: Layer
    operation: Operation
    operands0: MaskOperand
    operands1: MaskOperand
    dilation: Coordinate
    translation: Coordinate2D


class Medium(BaseType):
    # TODO: Using Any to avoid Pydantic v1/v2 incompatibility with Tidy3dBaseModel.
    medium: Any


class Media(BaseModel):
    optical: MediumID
    electrical: MediumID


class ExtrusionSpec(BaseType):
    media: Media
    limits: Coordinate2D
    sidewall_angle: Angle
    reference: Coordinate
    mask_spec: MaskSpecID


class PathProfile(BaseModel):
    width: PositiveCoordinate
    offset: Coordinate
    layer: Layer


class NamedPathProfile(BaseModel):
    name: str
    width: PositiveCoordinate
    offset: Coordinate
    layer: Layer


class ElectricalSpec(BaseModel):
    voltage_path: Coordinate2DVector
    current_path: Coordinate2DVector
    impedance: InterpolatorID | NoID


# Ports can be of 2 types: electrical or optical, indicated by the value
# of the "electrical_spec" property.
class PortSpec(BaseType):
    description: str
    width: PositiveCoordinate
    limits: Coordinate2D
    default_radius: Coordinate
    num_modes: UInt32
    added_solver_modes: UInt32
    polarization: Polarization
    target_neff: float
    path_profiles: list[PathProfile] | list[NamedPathProfile]
    electrical_spec: ElectricalSpec | None


class ParametricData(BaseModel):
    function: str | None
    kwargs: list[tuple[str, NativeData]]
    random_variables: list[RandomVariableID]


class Technology(BaseType):
    name: str
    version: str
    layers: list[tuple[str, LayerSpecID]]  # str is unique
    extrusion_specs: list[ExtrusionSpecID]
    ports: list[tuple[str, PortSpecID]]  # str is unique
    connections: list[tuple[Layer, Layer]]
    background_media: Media
    parametric_data: ParametricData | None


class Rectangle(BaseType):
    center: Coordinate2D
    size: tuple[NonNegativeCoordinate, NonNegativeCoordinate]
    rotation: Angle


class Circle(BaseType):
    radius: tuple[PositiveCoordinate, PositiveCoordinate]
    inner_radius: tuple[NonNegativeCoordinate, NonNegativeCoordinate]
    center: Coordinate2D
    sector: tuple[Angle, Angle]
    rotation: Angle
    min_evals: UInt32


class Polygon(BaseType):
    vertices: Coordinate2DVector
    holes: list[Coordinate2DVector]


type PathInterpolator = (
    ConstantInterpolator
    | LinearInterpolator
    | SmoothInterpolator
    | ParametricInterpolator
    | SliceInterpolator
)


class ConstantInterpolator(BaseModel):
    variant: Literal["constant"]
    value: float


class LinearInterpolator(BaseModel):
    variant: Literal["linear"]
    values: tuple[float, float]


class SmoothInterpolator(BaseModel):
    variant: Literal["smooth"]
    values: tuple[float, float]


class ParametricInterpolator(BaseModel):
    variant: Literal["parametric"]
    expression: DirectExpression
    scaling: float
    offset: float


class SliceInterpolator(BaseModel):
    variant: Literal["slice"]
    base: PathInterpolator
    limits: tuple[Fraction, Fraction]


type PathSection = (
    SegmentPathSection
    | ArcPathSection
    | EulerPathSection
    | BezierPathSection
    | ParametricPathSection
)


class BasePathSection(BaseModel):
    variant: Literal["segment", "arc", "euler", "bezier", "parametric"]
    width: PathInterpolator
    offset: PathInterpolator
    min_evals: UInt32
    max_evals: UInt32


class SegmentPathSection(BasePathSection):
    vertices: Coordinate2DVector
    bevel_join_limit: float
    round_joins: bool


class ArcPathSection(BasePathSection):
    radius: tuple[Radius, Radius]
    center: Float2D
    endpoint_delta: Float2D
    initial_angle: Angle
    final_angle: Angle
    rotation: Angle


class EulerPathSection(BasePathSection):
    radius_eff: Radius
    origin: Float2D
    endpoint_delta: Float2D
    initial_angle: Angle
    final_angle: Angle
    euler_fraction: Fraction


class BezierPathSection(BasePathSection):
    controls: Coordinate2DVector


class ParametricPathSection(BasePathSection):
    expression: DirectExpression
    origin: Float2D
    rotation: Angle
    scaling: float
    x_reflection: bool


class Path(BaseType):
    scale_profile: bool  # whether the width and offset are scaled when the path is scaled
    round_caps: tuple[bool, bool]  # begin and end caps should be round (if true, not extended)
    cap_extensions: tuple[float, float]  # begin and end extensions, if not round.
    end_position: Coordinate2D
    end_width: NonNegativeCoordinate
    end_offset: Coordinate
    path_sections: list[PathSection]


class Polyhedron(BaseType):
    vertices: list[Coordinate3D]
    triangles: list[tuple[UInt64, UInt64, UInt64]]
    medium: MediumID


class Extruded(BaseType):
    face: StructureID
    limits: Coordinate2D
    dilations: Coordinate2D
    axis: Literal["x", "y", "z"]
    medium: MediumID


class ConstructiveSolid(BaseType):
    operands: tuple[list[Structure3DID], list[Structure3DID]]
    operation: Operation
    medium: MediumID


class Label(BaseType):
    text: str
    origin: Coordinate2D
    rotation: Angle
    scaling: float
    anchor: Literal["NW", "N", "NE", "W", "O", "E", "SW", "S", "SE"]
    x_reflection: bool


class Port(BaseType):
    center: Coordinate2D
    input_direction: float
    bend_radius: Coordinate
    spec: PortSpecID
    extended: bool
    inverted: bool


class GaussianPort(BaseType):
    center: Coordinate3D
    input_vector: Float3D
    waist_radius: float
    waist_position: float
    polarization_angle: float
    field_tolerance: float


class FiberPort(BaseType):
    center: Coordinate3D
    input_vector: Float3D
    size: Coordinate2D
    extrusion_limits: Coordinate2D
    cross_section: list[tuple[StructureID, MediumID]]
    target_neff: float
    num_modes: UInt32
    added_solver_modes: UInt32
    polarization: Polarization


class Terminal(BaseType):
    routing_layer: Layer
    structure: StructureID


class TimeStepper(BaseType):
    name: str
    parametric_data: ParametricData | None


class Model(BaseType):
    name: str
    time_stepper: TimeStepperID
    parametric_data: ParametricData | None


class ReferencePort(BaseModel):
    reference: ReferenceID
    port_name: str
    repetition_index: UInt64


type VirtualConnection = tuple[ReferencePort, ReferencePort]


class UpdateKwargs(BaseModel):
    technology: NativeDict | None
    component: NativeDict | None
    model: NativeDict | None
    s_matrix: NativeDict | None


class Reference(BaseType):
    component: ComponentID
    origin: Coordinate2D
    rotation: Angle
    scaling: float
    x_reflection: bool
    columns: UInt32
    rows: UInt32
    spacing: Coordinate2D
    update_kwargs: UpdateKwargs | None


class Component(BaseType):
    name: str
    references: list[ReferenceID]
    structures: list[tuple[Layer, list[StructureID]]]  # Layer is unique
    labels: list[tuple[Layer, list[LabelID]]]  # Layer is unique
    ports: list[tuple[str, AnyPortID]]  # str is unique
    terminals: list[tuple[str, TerminalID]]  # str is unique
    virtual_connections: list[VirtualConnection]
    models: list[tuple[str, ModelID]]  # str is unique
    active_optical_model_name: str
    active_electrical_model_name: str
    technology: TechnologyID
    parametric_data: ParametricData | None


type SMatrixKey = tuple[str, str]


class SMatrix(BaseType):
    frequencies: list[float]
    elements: list[tuple[SMatrixKey, list[Complex]]]
    ports: list[tuple[str, AnyPortID | NoID]]


class PoleResidueMatrix(BaseType):
    residues: list[tuple[SMatrixKey, list[Complex]]]
    poles: list[Complex]
    delays: list[tuple[SMatrixKey, float]]
    ports: list[tuple[str, AnyPortID | NoID]]
    frequency_scaling: float


class TimeDomainModel(BaseType):
    pole_residue_matrix: PoleResidueMatrixID
    state: list[tuple[str, list[Complex]]]
    output: list[tuple[SMatrixKey, list[Complex]]]
    time_step: float


class TimeSeries(BaseType):
    shape: tuple[UInt64, UInt64, Literal[2]]
    values: list[float]  # stored in column-major order in the first 2 indices
    keys: list[str]
    time_step: float
    time_index: Int64


class ConfigData(BaseModel):
    grid: Coordinate
    tolerance: Coordinate
    mesh_refinement: float
    default_technology: TechnologyID | NoID
    default_time_steppers: NativeDict
    default_kwargs: NativeDict


def _get_object_discriminator(obj: Any) -> int:
    if isinstance(obj, dict):
        return obj.get("type", 0)
    return getattr(obj, "type", 0)


type AnyObject = Annotated[
    Annotated[Properties, Tag(PropertiesType)]
    | Annotated[RandomVariable, Tag(RandomVariableType)]
    | Annotated[Expression, Tag(ExpressionType)]
    | Annotated[Native, Tag(NativeType)]
    | Annotated[Medium, Tag(MediumType)]
    | Annotated[LayerSpec, Tag(LayerSpecType)]
    | Annotated[MaskSpec, Tag(MaskSpecType)]
    | Annotated[ExtrusionSpec, Tag(ExtrusionSpecType)]
    | Annotated[PortSpec, Tag(PortSpecType)]
    | Annotated[Technology, Tag(TechnologyType)]
    | Annotated[Rectangle, Tag(RectangleType)]
    | Annotated[Circle, Tag(CircleType)]
    | Annotated[Polygon, Tag(PolygonType)]
    | Annotated[Path, Tag(PathType)]
    | Annotated[Polyhedron, Tag(PolyhedronType)]
    | Annotated[Extruded, Tag(ExtrudedType)]
    | Annotated[ConstructiveSolid, Tag(ConstructiveSolidType)]
    | Annotated[Label, Tag(LabelType)]
    | Annotated[Port, Tag(PortType)]
    | Annotated[FiberPort, Tag(FiberPortType)]
    | Annotated[GaussianPort, Tag(GaussianPortType)]
    | Annotated[Terminal, Tag(TerminalType)]
    | Annotated[Model, Tag(ModelType)]
    | Annotated[Reference, Tag(ReferenceType)]
    | Annotated[Component, Tag(ComponentType)]
    | Annotated[SMatrix, Tag(SMatrixType)]
    | Annotated[PoleResidueMatrix, Tag(PoleResidueMatrixType)]
    | Annotated[TimeDomainModel, Tag(TimeDomainModelType)]
    | Annotated[TimeSeries, Tag(TimeSeriesType)]
    | Annotated[TimeStepper, Tag(TimeStepperType)]
    | Annotated[Interpolator, Tag(InterpolatorType)],
    Discriminator(_get_object_discriminator),
]


class Store(BaseType):
    config: ConfigData
    top_content: list[tuple[ID, PhotonForgeType]]  # IDs and types of explicitly-exported objects
    data: list[tuple[ID, AnyObject]]  # All object data


# Netlist

# Specifies a refrence port by index in the instance list, port name, and number of supported modes
type InstancePort = tuple[UInt64, str, int]

# Indicates that a specific reference port is used as an IO port for this circuit with a given name
type ExternalPort = tuple[InstancePort, str]


if __name__ == "__main__":
    import json

    schema = Store.model_json_schema()
    print(json.dumps(schema, indent=2))
