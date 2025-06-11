from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class BaseCalculatorResponse(BaseModel):
    success: bool
    errors: List[str] = []
    warnings: List[str] = []

class GravityFlowResult(BaseModel):
    flow_rate_volume: float
    flow_rate_mass: float
    volume_unit: str
    mass_unit: str

class GravityFlowResponse(BaseCalculatorResponse):
    result: Optional[GravityFlowResult] = None
    chart_data: Optional[str] = None  # Base64 encoded chart
    recommendations: List[str] = []

class ColumnVelocityResult(BaseModel):
    flow_rate_lb_hr: float
    flow_rate_ft3_hr: float
    flow_rate_in3_sec: float
    material_velocity: float

class ColumnVelocityResponse(BaseCalculatorResponse):
    result: Optional[ColumnVelocityResult] = None
    recommendations: List[str] = []

class SpoutResult(BaseModel):
    diameter: Optional[float] = None
    size: Optional[str] = None
    area: float
    max_cfh: float

class SpoutRequirementsResult(BaseModel):
    required_cfh: float
    round_spout: Optional[SpoutResult] = None
    square_spout: Optional[SpoutResult] = None

class SpoutRequirementsResponse(BaseCalculatorResponse):
    result: Optional[SpoutRequirementsResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class BeltHorsepowerResult(BaseModel):
    total_force: float
    calculated_force: float
    effective_tension: float
    slack_tension: float
    tight_tension: float
    horsepower: float

class BeltHorsepowerResponse(BaseCalculatorResponse):
    result: Optional[BeltHorsepowerResult] = None
    recommendations: List[str] = []

class DragSlideResult(BaseModel):
    with_magnet: Dict[str, float]
    without_magnet: Dict[str, float]

class DragSlideResponse(BaseCalculatorResponse):
    result: Optional[DragSlideResult] = None
    recommendations: List[str] = []

class ScrewConveyorResult(BaseModel):
    capacity_ft3_hr: float
    capacity_tons_hr: float
    torque_in_lbs: float
    horsepower: float
    efficiency: float

class ScrewConveyorResponse(BaseCalculatorResponse):
    result: Optional[ScrewConveyorResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class VibratingFeederResult(BaseModel):
    flow_rate_tons_hr: float
    stroke_length: float
    conveying_velocity: float
    power_required: float

class VibratingFeederResponse(BaseCalculatorResponse):
    result: Optional[VibratingFeederResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class MagneticSeparatorResult(BaseModel):
    separation_efficiency: float
    magnetic_force: float
    throughput_capacity: float
    recovery_rate: float

class MagneticSeparatorResponse(BaseCalculatorResponse):
    result: Optional[MagneticSeparatorResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class AirClassifierResult(BaseModel):
    terminal_velocity: float
    classification_efficiency: float
    air_requirement: float
    pressure_drop: float

class AirClassifierResponse(BaseCalculatorResponse):
    result: Optional[AirClassifierResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class PneumaticConveyingResult(BaseModel):
    air_velocity: float
    pressure_drop: float
    power_required: float
    conveying_velocity: float
    air_flow_rate: float

class PneumaticConveyingResponse(BaseCalculatorResponse):
    result: Optional[PneumaticConveyingResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class MaterialHandlingResult(BaseModel):
    residence_time: float
    bed_depth: float
    mass_flow_rate: float
    volumetric_efficiency: float

class MaterialHandlingResponse(BaseCalculatorResponse):
    result: Optional[MaterialHandlingResult] = None
    recommendations: List[str] = []

class ScreenSizingResult(BaseModel):
    screen_area: float
    capacity: float
    efficiency: float
    underflow_rate: float
    overflow_rate: float

class ScreenSizingResponse(BaseCalculatorResponse):
    result: Optional[ScreenSizingResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class CycloneSeparatorResult(BaseModel):
    cut_size_d50: float
    pressure_drop: float
    collection_efficiency: float
    throughput: float

class CycloneSeparatorResponse(BaseCalculatorResponse):
    result: Optional[CycloneSeparatorResult] = None
    chart_data: Optional[str] = None
    recommendations: List[str] = []

class Calculator(BaseModel):
    id: str
    name: str
    description: str
    category: str

class CalculatorListResponse(BaseModel):
    calculators: List[Calculator]

class Material(BaseModel):
    name: str
    bulk_density_metric: float  # kg/m³
    bulk_density_imperial: float  # lb/ft³
    angle_of_repose: float  # degrees
    particle_size: float  # mm
    abrasiveness: str  # Low, Medium, High
    flowability: str  # Poor, Fair, Good, Excellent

class MaterialListResponse(BaseModel):
    materials: List[Material]
