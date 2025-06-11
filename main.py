from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any
import uvicorn

from models.requests import (
    GravityFlowRequest, ColumnVelocityRequest, SpoutRequirementsRequest,
    BeltHorsepowerRequest, DragSlideRequest, ScrewConveyorRequest,
    VibratingFeederRequest, MagneticSeparatorRequest, AirClassifierRequest,
    PneumaticConveyingRequest, MaterialHandlingRequest, ScreenSizingRequest,
    CycloneSeparatorRequest
)
from models.responses import (
    GravityFlowResponse, ColumnVelocityResponse, SpoutRequirementsResponse,
    BeltHorsepowerResponse, DragSlideResponse, ScrewConveyorResponse,
    VibratingFeederResponse, MagneticSeparatorResponse, AirClassifierResponse,
    PneumaticConveyingResponse, MaterialHandlingResponse, ScreenSizingResponse,
    CycloneSeparatorResponse, CalculatorListResponse, MaterialListResponse
)
from services.calculator_service import CalculatorService
from services.material_service import MaterialService

app = FastAPI(
    title="Engineering Calculators API",
    description="Comprehensive FastAPI backend for specialized engineering calculators for conveyor and separation equipment design",
    version="1.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

calculator_service = CalculatorService()
material_service = MaterialService()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Engineering Calculators API",
        "version": "1.0.0",
        "documentation": "/docs"
    }

@app.get("/calculators")
async def get_calculators():
    """Get list of available calculators with their descriptions"""
    calculators = [
        {
            "id": "gravity_flow",
            "name": "Gravity MD Flow Rate Calculator",
            "description": "Calculate gravity flow rates based on aperture size and bulk density with metric/imperial conversion",
            "category": "Flow Control"
        },
        {
            "id": "column_velocity",
            "name": "Column Velocity Calculator",
            "description": "Calculate material velocity and flow rates in vertical columns",
            "category": "Flow Control"
        },
        {
            "id": "spout_requirements",
            "name": "Spout Requirements Calculator",
            "description": "Determine optimal spout sizing for material discharge applications",
            "category": "Material Handling"
        },
        {
            "id": "belt_horsepower",
            "name": "Belt Horsepower Calculator",
            "description": "Calculate power requirements for belt conveyor systems",
            "category": "Conveyor Systems"
        },
        {
            "id": "drag_slide",
            "name": "Drag Slide Calculator",
            "description": "Calculate drag slide dimensions with and without magnetic components",
            "category": "Magnetic Systems"
        },
        {
            "id": "screw_conveyor",
            "name": "Screw Conveyor Calculator",
            "description": "Calculate capacity, torque, and power requirements for screw conveyors",
            "category": "Conveyor Systems"
        },
        {
            "id": "vibrating_feeder",
            "name": "Vibrating Feeder Calculator",
            "description": "Calculate amplitude, frequency, and flow rate for vibrating feeders",
            "category": "Feeding Systems"
        },
        {
            "id": "magnetic_separator",
            "name": "Magnetic Separator Calculator",
            "description": "Calculate magnetic field strength and separation efficiency",
            "category": "Separation Systems"
        },
        {
            "id": "air_classifier",
            "name": "Air Classifier Calculator",
            "description": "Calculate air velocity and particle separation parameters",
            "category": "Separation Systems"
        },
        {
            "id": "pneumatic_conveying",
            "name": "Pneumatic Conveying Calculator",
            "description": "Calculate air requirements and pressure drop for pneumatic systems",
            "category": "Conveyor Systems"
        },
        {
            "id": "material_handling",
            "name": "Material Handling Calculator",
            "description": "Calculate throughput and residence time for material handling systems",
            "category": "Material Handling"
        },
        {
            "id": "screen_sizing",
            "name": "Screen Sizing Calculator",
            "description": "Calculate mesh size, capacity, and efficiency for screening applications",
            "category": "Separation Systems"
        },
        {
            "id": "cyclone_separator",
            "name": "Cyclone Separator Calculator",
            "description": "Calculate cut size, pressure drop, and efficiency for cyclone separators",
            "category": "Separation Systems"
        }
    ]
    return {"calculators": calculators}

@app.get("/materials")
async def get_materials():
    """Get list of available materials with their properties"""
    materials = material_service.get_all_materials()
    return {"materials": materials}

# Gravity Flow Calculator Endpoints
@app.post("/calculators/gravity-flow", response_model=GravityFlowResponse)
async def calculate_gravity_flow(request: GravityFlowRequest):
    """Calculate gravity MD flow rate based on aperture size and bulk density"""
    try:
        return calculator_service.calculate_gravity_flow(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Column Velocity Calculator Endpoints
@app.post("/calculators/column-velocity", response_model=ColumnVelocityResponse)
async def calculate_column_velocity(request: ColumnVelocityRequest):
    """Calculate column velocity and related flow rates"""
    try:
        return calculator_service.calculate_column_velocity(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Spout Requirements Calculator Endpoints
@app.post("/calculators/spout-requirements", response_model=SpoutRequirementsResponse)
async def calculate_spout_requirements(request: SpoutRequirementsRequest):
    """Calculate spout requirements based on material properties and capacity"""
    try:
        return calculator_service.calculate_spout_requirements(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Belt Horsepower Calculator Endpoints
@app.post("/calculators/belt-horsepower", response_model=BeltHorsepowerResponse)
async def calculate_belt_horsepower(request: BeltHorsepowerRequest):
    """Calculate belt horsepower requirements"""
    try:
        return calculator_service.calculate_belt_horsepower(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Drag Slide Calculator Endpoints
@app.post("/calculators/drag-slide", response_model=DragSlideResponse)
async def calculate_drag_slide(request: DragSlideRequest):
    """Calculate drag slide dimensions"""
    try:
        return calculator_service.calculate_drag_slide(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Screw Conveyor Calculator Endpoints
@app.post("/calculators/screw-conveyor", response_model=ScrewConveyorResponse)
async def calculate_screw_conveyor(request: ScrewConveyorRequest):
    """Calculate screw conveyor capacity, torque, and power requirements"""
    try:
        return calculator_service.calculate_screw_conveyor(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Vibrating Feeder Calculator Endpoints
@app.post("/calculators/vibrating-feeder", response_model=VibratingFeederResponse)
async def calculate_vibrating_feeder(request: VibratingFeederRequest):
    """Calculate vibrating feeder parameters"""
    try:
        return calculator_service.calculate_vibrating_feeder(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Magnetic Separator Calculator Endpoints
@app.post("/calculators/magnetic-separator", response_model=MagneticSeparatorResponse)
async def calculate_magnetic_separator(request: MagneticSeparatorRequest):
    """Calculate magnetic separator parameters"""
    try:
        return calculator_service.calculate_magnetic_separator(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Air Classifier Calculator Endpoints
@app.post("/calculators/air-classifier", response_model=AirClassifierResponse)
async def calculate_air_classifier(request: AirClassifierRequest):
    """Calculate air classifier parameters"""
    try:
        return calculator_service.calculate_air_classifier(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Pneumatic Conveying Calculator Endpoints
@app.post("/calculators/pneumatic-conveying", response_model=PneumaticConveyingResponse)
async def calculate_pneumatic_conveying(request: PneumaticConveyingRequest):
    """Calculate pneumatic conveying parameters"""
    try:
        return calculator_service.calculate_pneumatic_conveying(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Material Handling Calculator Endpoints
@app.post("/calculators/material-handling", response_model=MaterialHandlingResponse)
async def calculate_material_handling(request: MaterialHandlingRequest):
    """Calculate material handling parameters"""
    try:
        return calculator_service.calculate_material_handling(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Screen Sizing Calculator Endpoints
@app.post("/calculators/screen-sizing", response_model=ScreenSizingResponse)
async def calculate_screen_sizing(request: ScreenSizingRequest):
    """Calculate screen sizing parameters"""
    try:
        return calculator_service.calculate_screen_sizing(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Cyclone Separator Calculator Endpoints
@app.post("/calculators/cyclone-separator", response_model=CycloneSeparatorResponse)
async def calculate_cyclone_separator(request: CycloneSeparatorRequest):
    """Calculate cyclone separator parameters"""
    try:
        return calculator_service.calculate_cyclone_separator(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
