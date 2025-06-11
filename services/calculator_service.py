import base64
from io import BytesIO
from typing import Dict, Any

from models.requests import *
from models.responses import *
from calculators.gravity_flow import GravityFlowCalculator
from calculators.column_velocity import ColumnVelocityCalculator
from calculators.spout_requirements import SpoutRequirementsCalculator
from calculators.belt_horsepower import BeltHorsepowerCalculator
from calculators.drag_slide import DragSlideCalculator
from calculators.screw_conveyor import ScrewConveyorCalculator
from calculators.vibrating_feeder import VibratingFeederCalculator
from calculators.magnetic_separator import MagneticSeparatorCalculator
from calculators.air_classifier import AirClassifierCalculator
from calculators.pneumatic_conveying import PneumaticConveyingCalculator
from calculators.material_handling import MaterialHandlingCalculator
from calculators.screen_sizing import ScreenSizingCalculator
from calculators.cyclone_separator import CycloneSeparatorCalculator
from services.chart_service import ChartService

class CalculatorService:
    def __init__(self):
        self.gravity_flow_calc = GravityFlowCalculator()
        self.column_velocity_calc = ColumnVelocityCalculator()
        self.spout_calc = SpoutRequirementsCalculator()
        self.belt_calc = BeltHorsepowerCalculator()
        self.drag_slide_calc = DragSlideCalculator()
        self.screw_calc = ScrewConveyorCalculator()
        self.vibrating_calc = VibratingFeederCalculator()
        self.magnetic_calc = MagneticSeparatorCalculator()
        self.air_calc = AirClassifierCalculator()
        self.pneumatic_calc = PneumaticConveyingCalculator()
        self.material_calc = MaterialHandlingCalculator()
        self.screen_calc = ScreenSizingCalculator()
        self.cyclone_calc = CycloneSeparatorCalculator()
        self.chart_service = ChartService()

    def calculate_gravity_flow(self, request: GravityFlowRequest) -> GravityFlowResponse:
        """Calculate gravity flow with chart visualization"""
        try:
            result = self.gravity_flow_calc.calculate(request)
            
            # Generate comparison chart
            chart_fig = self.gravity_flow_calc.create_comparison_chart(
                request.aperture_size_mm, 
                request.bulk_density,
                request.use_imperial
            )
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            # Generate recommendations
            recommendations = self.gravity_flow_calc.get_recommendations(request, result)
            
            return GravityFlowResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return GravityFlowResponse(success=False, errors=[str(e)])

    def calculate_column_velocity(self, request: ColumnVelocityRequest) -> ColumnVelocityResponse:
        """Calculate column velocity parameters"""
        try:
            result = self.column_velocity_calc.calculate(request)
            recommendations = self.column_velocity_calc.get_recommendations(request, result)
            
            return ColumnVelocityResponse(
                success=True,
                result=result,
                recommendations=recommendations
            )
        except Exception as e:
            return ColumnVelocityResponse(success=False, errors=[str(e)])

    def calculate_spout_requirements(self, request: SpoutRequirementsRequest) -> SpoutRequirementsResponse:
        """Calculate spout requirements with comparison chart"""
        try:
            result = self.spout_calc.calculate(request)
            
            # Generate comparison chart
            chart_fig = self.spout_calc.create_comparison_chart(request.bulk_density, result.required_cfh)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.spout_calc.get_recommendations(request, result)
            
            return SpoutRequirementsResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return SpoutRequirementsResponse(success=False, errors=[str(e)])

    def calculate_belt_horsepower(self, request: BeltHorsepowerRequest) -> BeltHorsepowerResponse:
        """Calculate belt horsepower requirements"""
        try:
            result = self.belt_calc.calculate(request)
            recommendations = self.belt_calc.get_recommendations(request, result)
            
            return BeltHorsepowerResponse(
                success=True,
                result=result,
                recommendations=recommendations
            )
        except Exception as e:
            return BeltHorsepowerResponse(success=False, errors=[str(e)])

    def calculate_drag_slide(self, request: DragSlideRequest) -> DragSlideResponse:
        """Calculate drag slide dimensions"""
        try:
            result = self.drag_slide_calc.calculate(request)
            recommendations = self.drag_slide_calc.get_recommendations(request, result)
            
            return DragSlideResponse(
                success=True,
                result=result,
                recommendations=recommendations
            )
        except Exception as e:
            return DragSlideResponse(success=False, errors=[str(e)])

    def calculate_screw_conveyor(self, request: ScrewConveyorRequest) -> ScrewConveyorResponse:
        """Calculate screw conveyor parameters"""
        try:
            result = self.screw_calc.calculate(request)
            
            # Generate performance chart
            chart_fig = self.screw_calc.create_performance_chart(request)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.screw_calc.get_recommendations(request, result)
            
            return ScrewConveyorResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return ScrewConveyorResponse(success=False, errors=[str(e)])

    def calculate_vibrating_feeder(self, request: VibratingFeederRequest) -> VibratingFeederResponse:
        """Calculate vibrating feeder parameters"""
        try:
            result = self.vibrating_calc.calculate(request)
            
            chart_fig = self.vibrating_calc.create_performance_chart(request, result)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.vibrating_calc.get_recommendations(request, result)
            
            return VibratingFeederResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return VibratingFeederResponse(success=False, errors=[str(e)])

    def calculate_magnetic_separator(self, request: MagneticSeparatorRequest) -> MagneticSeparatorResponse:
        """Calculate magnetic separator parameters"""
        try:
            result = self.magnetic_calc.calculate(request)
            
            chart_fig = self.magnetic_calc.create_efficiency_chart(request, result)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.magnetic_calc.get_recommendations(request, result)
            
            return MagneticSeparatorResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return MagneticSeparatorResponse(success=False, errors=[str(e)])

    def calculate_air_classifier(self, request: AirClassifierRequest) -> AirClassifierResponse:
        """Calculate air classifier parameters"""
        try:
            result = self.air_calc.calculate(request)
            
            chart_fig = self.air_calc.create_classification_chart(request, result)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.air_calc.get_recommendations(request, result)
            
            return AirClassifierResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return AirClassifierResponse(success=False, errors=[str(e)])

    def calculate_pneumatic_conveying(self, request: PneumaticConveyingRequest) -> PneumaticConveyingResponse:
        """Calculate pneumatic conveying parameters"""
        try:
            result = self.pneumatic_calc.calculate(request)
            
            chart_fig = self.pneumatic_calc.create_pressure_chart(request, result)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.pneumatic_calc.get_recommendations(request, result)
            
            return PneumaticConveyingResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return PneumaticConveyingResponse(success=False, errors=[str(e)])

    def calculate_material_handling(self, request: MaterialHandlingRequest) -> MaterialHandlingResponse:
        """Calculate material handling parameters"""
        try:
            result = self.material_calc.calculate(request)
            recommendations = self.material_calc.get_recommendations(request, result)
            
            return MaterialHandlingResponse(
                success=True,
                result=result,
                recommendations=recommendations
            )
        except Exception as e:
            return MaterialHandlingResponse(success=False, errors=[str(e)])

    def calculate_screen_sizing(self, request: ScreenSizingRequest) -> ScreenSizingResponse:
        """Calculate screen sizing parameters"""
        try:
            result = self.screen_calc.calculate(request)
            
            chart_fig = self.screen_calc.create_efficiency_chart(request, result)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.screen_calc.get_recommendations(request, result)
            
            return ScreenSizingResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return ScreenSizingResponse(success=False, errors=[str(e)])

    def calculate_cyclone_separator(self, request: CycloneSeparatorRequest) -> CycloneSeparatorResponse:
        """Calculate cyclone separator parameters"""
        try:
            result = self.cyclone_calc.calculate(request)
            
            chart_fig = self.cyclone_calc.create_performance_chart(request, result)
            chart_data = self.chart_service.fig_to_base64(chart_fig)
            
            recommendations = self.cyclone_calc.get_recommendations(request, result)
            
            return CycloneSeparatorResponse(
                success=True,
                result=result,
                chart_data=chart_data,
                recommendations=recommendations
            )
        except Exception as e:
            return CycloneSeparatorResponse(success=False, errors=[str(e)])
