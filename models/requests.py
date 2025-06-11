from pydantic import BaseModel, Field, validator
from typing import Optional, Literal
from enum import Enum

class UnitSystem(str, Enum):
    METRIC = "metric"
    IMPERIAL = "imperial"

class CapacityUnit(str, Enum):
    TONS_HR = "tons/hr"
    LBS_HR = "lbs/hr"

class GravityFlowRequest(BaseModel):
    aperture_size_mm: int = Field(..., description="Aperture size in millimeters")
    bulk_density: float = Field(..., gt=0, description="Bulk density")
    use_imperial: bool = Field(default=False, description="Use imperial units")
    
    @validator('aperture_size_mm')
    def validate_aperture_size(cls, v):
        valid_sizes = [30, 50, 70, 90, 120, 150, 200, 250, 300, 350, 400]
        if v not in valid_sizes:
            raise ValueError(f"Aperture size must be one of: {', '.join(map(str, valid_sizes))}")
        return v
    
    @validator('bulk_density')
    def validate_bulk_density(cls, v, values):
        use_imperial = values.get('use_imperial', False)
        if use_imperial and v > 200:
            raise ValueError("Bulk density seems too high (>200 lb/ft³)")
        elif not use_imperial and v > 3203.7:
            raise ValueError("Bulk density seems too high (>3203.7 kg/m³)")
        return v

class ColumnVelocityRequest(BaseModel):
    molder_shot_size: float = Field(..., gt=0, description="Molder shot size in lbs")
    molder_cycle_time: float = Field(..., gt=0, description="Molder cycle time in seconds")
    material_density: float = Field(..., gt=0, description="Material density in lb/ft³")
    area_inside_tube: float = Field(..., gt=0, description="Area inside tube in sq. in.")

class SpoutRequirementsRequest(BaseModel):
    bulk_density: float = Field(..., gt=0, le=200, description="Bulk density in PCF")
    capacity_value: float = Field(..., gt=0, description="Capacity value")
    capacity_unit: CapacityUnit = Field(..., description="Capacity unit")

class BeltHorsepowerRequest(BaseModel):
    belt_speed: float = Field(..., gt=0, le=1000, description="Belt speed in FPM")
    part_feed_rate: float = Field(..., gt=0, description="Part feed rate")
    belt_width: float = Field(..., gt=0, le=100, description="Belt width in inches")
    incline_angle: float = Field(..., ge=0, le=90, description="Incline angle in degrees")

class DragSlideRequest(BaseModel):
    x_value: float = Field(..., gt=0, le=1000, description="X dimension value")
    y_value: float = Field(..., gt=0, le=1000, description="Y dimension value")

class ScrewConveyorRequest(BaseModel):
    diameter: float = Field(..., gt=0, le=24, description="Screw diameter in inches")
    pitch: float = Field(..., gt=0, description="Screw pitch in inches")
    rpm: float = Field(..., gt=0, le=200, description="Rotational speed in RPM")
    length: float = Field(..., gt=0, le=100, description="Conveyor length in feet")
    bulk_density: float = Field(..., gt=0, le=200, description="Material bulk density in lb/ft³")
    material_factor: float = Field(default=0.45, ge=0.1, le=1.0, description="Material loading factor")
    incline_angle: float = Field(default=0, ge=0, le=45, description="Incline angle in degrees")

class VibratingFeederRequest(BaseModel):
    deck_width: float = Field(..., gt=0, le=120, description="Deck width in inches")
    deck_length: float = Field(..., gt=0, le=240, description="Deck length in inches")
    amplitude: float = Field(..., gt=0, le=0.5, description="Amplitude in inches")
    frequency: float = Field(..., gt=0, le=60, description="Frequency in Hz")
    bulk_density: float = Field(..., gt=0, le=200, description="Material bulk density in lb/ft³")
    stroke_angle: float = Field(default=45, ge=15, le=60, description="Stroke angle in degrees")

class MagneticSeparatorRequest(BaseModel):
    belt_width: float = Field(..., gt=0, le=120, description="Belt width in inches")
    belt_speed: float = Field(..., gt=0, le=500, description="Belt speed in FPM")
    material_depth: float = Field(..., gt=0, le=6, description="Material depth in inches")
    magnetic_intensity: float = Field(..., gt=0, le=3000, description="Magnetic intensity in Gauss")
    particle_size: float = Field(..., gt=0, le=50, description="Average particle size in mm")

class AirClassifierRequest(BaseModel):
    air_velocity: float = Field(..., gt=0, le=50, description="Air velocity in m/s")
    particle_density: float = Field(..., gt=0, le=10, description="Particle density in g/cm³")
    particle_diameter: float = Field(..., gt=0, le=1000, description="Particle diameter in microns")
    air_temperature: float = Field(default=20, ge=-20, le=100, description="Air temperature in °C")
    air_pressure: float = Field(default=101.325, gt=0, description="Air pressure in kPa")

class PneumaticConveyingRequest(BaseModel):
    material_flow_rate: float = Field(..., gt=0, description="Material flow rate in tons/hr")
    conveying_distance: float = Field(..., gt=0, le=1000, description="Conveying distance in feet")
    vertical_lift: float = Field(default=0, ge=0, le=200, description="Vertical lift in feet")
    pipe_diameter: float = Field(..., gt=0, le=12, description="Pipe diameter in inches")
    bulk_density: float = Field(..., gt=0, le=200, description="Material bulk density in lb/ft³")
    particle_size: float = Field(..., gt=0, le=50, description="Average particle size in mm")

class MaterialHandlingRequest(BaseModel):
    throughput: float = Field(..., gt=0, description="Throughput in tons/hr")
    equipment_length: float = Field(..., gt=0, le=100, description="Equipment length in feet")
    equipment_width: float = Field(..., gt=0, le=20, description="Equipment width in feet")
    material_velocity: float = Field(..., gt=0, le=10, description="Material velocity in ft/s")
    bulk_density: float = Field(..., gt=0, le=200, description="Material bulk density in lb/ft³")

class ScreenSizingRequest(BaseModel):
    feed_rate: float = Field(..., gt=0, description="Feed rate in tons/hr")
    oversize_percentage: float = Field(..., ge=0, le=100, description="Oversize percentage")
    undersize_percentage: float = Field(..., ge=0, le=100, description="Undersize percentage")
    mesh_size: float = Field(..., gt=0, le=100, description="Mesh opening in mm")
    bulk_density: float = Field(..., gt=0, le=200, description="Material bulk density in lb/ft³")
    moisture_content: float = Field(default=0, ge=0, le=50, description="Moisture content in %")
    
    @validator('undersize_percentage')
    def validate_percentages(cls, v, values):
        oversize = values.get('oversize_percentage', 0)
        if oversize + v > 100:
            raise ValueError("Oversize and undersize percentages cannot exceed 100%")
        return v

class CycloneSeparatorRequest(BaseModel):
    inlet_velocity: float = Field(..., gt=0, le=50, description="Inlet velocity in m/s")
    cyclone_diameter: float = Field(..., gt=0, le=5, description="Cyclone diameter in meters")
    particle_density: float = Field(..., gt=0, le=10, description="Particle density in g/cm³")
    gas_density: float = Field(default=1.2, gt=0, le=10, description="Gas density in kg/m³")
    gas_viscosity: float = Field(default=1.8e-5, gt=0, description="Gas viscosity in Pa·s")
    cut_size: float = Field(..., gt=0, le=100, description="Target cut size in microns")
