from models.requests import ColumnVelocityRequest
from models.responses import ColumnVelocityResult

class ColumnVelocityCalculator:
    def calculate(self, request: ColumnVelocityRequest) -> ColumnVelocityResult:
        """Calculate column velocity and related flow rates"""
        molder_shot_size = request.molder_shot_size
        molder_cycle_time = request.molder_cycle_time
        material_density = request.material_density
        area_inside_tube = request.area_inside_tube

        # Calculate Flow Rate (Lbs/Hour)
        flow_rate_lb_hr = (molder_shot_size / molder_cycle_time) * 3600

        # Calculate Flow Rate (Cu. Ft./Hour)
        flow_rate_ft3_hr = flow_rate_lb_hr / material_density

        # Calculate Flow Rate (Cu. In./Sec.)
        flow_rate_in3_sec = flow_rate_ft3_hr * 1728 / 3600

        # Calculate Material Velocity in Column (In./Sec.)
        material_velocity = flow_rate_in3_sec / area_inside_tube

        return ColumnVelocityResult(
            flow_rate_lb_hr=flow_rate_lb_hr,
            flow_rate_ft3_hr=flow_rate_ft3_hr,
            flow_rate_in3_sec=flow_rate_in3_sec,
            material_velocity=material_velocity
        )

    def get_recommendations(self, request: ColumnVelocityRequest, result: ColumnVelocityResult) -> list:
        """Generate recommendations based on calculation results"""
        recommendations = []
        
        # Velocity recommendations
        if result.material_velocity < 0.1:
            recommendations.append("Very low material velocity. Check for potential bridging or flow issues.")
        elif result.material_velocity > 10:
            recommendations.append("High material velocity. Consider larger tube diameter to reduce velocity.")
        
        # Flow rate considerations
        if result.flow_rate_lb_hr < 10:
            recommendations.append("Low throughput rate. Verify this meets production requirements.")
        elif result.flow_rate_lb_hr > 1000:
            recommendations.append("High throughput rate. Ensure equipment can handle this capacity.")
        
        # Cycle time recommendations
        if request.molder_cycle_time < 10:
            recommendations.append("Very short cycle time. Verify material can flow adequately at this rate.")
        elif request.molder_cycle_time > 300:
            recommendations.append("Long cycle time. Consider process optimization for better efficiency.")
        
        return recommendations
