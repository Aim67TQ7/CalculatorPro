from models.requests import BeltHorsepowerRequest
from models.responses import BeltHorsepowerResult

class BeltHorsepowerCalculator:
    def __init__(self):
        # Coefficient lookup table
        self.cv_table = {
            90: 0.75,
            75: 0.6,
            60: 0.45,
            45: 0.3,
            30: 0.2
        }

    def calculate(self, request: BeltHorsepowerRequest) -> BeltHorsepowerResult:
        """Calculate belt horsepower based on input parameters"""
        belt_speed = request.belt_speed
        part_feed_rate = request.part_feed_rate
        belt_width = request.belt_width
        incline_angle = request.incline_angle

        # Get closest angle coefficient
        closest_angle = min(self.cv_table.keys(), key=lambda x: abs(x - incline_angle))
        cvf = self.cv_table.get(closest_angle, 0.45)

        # Distance, Parts/ft, and Force Calculation (from original code)
        sections_data = {
            "Type": ["Incline", "Curve", "Horiz"],
            "Distance": [7.82, 1.5, 7.8],
            "# Parts/ft": [1, 1, 14],
            "# per part": [20, 20, 20]
        }

        # Calculate forces
        total_force = sum(p * n for p, n in zip(sections_data["# Parts/ft"], sections_data["# per part"]))
        calculated_force = total_force * cvf

        # Tension calculations
        T_E = calculated_force  # Effective tension
        T_2 = T_E * 0.45        # Slack side tension
        T_1 = T_E + T_2         # Tight side tension

        # Horsepower calculation
        horsepower = (T_E * belt_speed) / 28000

        return BeltHorsepowerResult(
            total_force=total_force,
            calculated_force=calculated_force,
            effective_tension=T_E,
            slack_tension=T_2,
            tight_tension=T_1,
            horsepower=horsepower
        )

    def get_recommendations(self, request: BeltHorsepowerRequest, result: BeltHorsepowerResult) -> list:
        """Generate recommendations based on calculation results"""
        recommendations = []
        
        # Horsepower recommendations
        if result.horsepower < 1:
            recommendations.append("Low power requirement. Standard motor should be sufficient.")
        elif result.horsepower > 10:
            recommendations.append("High power requirement. Consider energy efficiency measures.")
        
        # Belt speed considerations
        if request.belt_speed < 50:
            recommendations.append("Low belt speed may cause material spillage or poor conveying.")
        elif request.belt_speed > 800:
            recommendations.append("High belt speed. Check for excessive wear and material degradation.")
        
        # Incline angle recommendations
        if request.incline_angle > 20:
            recommendations.append("Steep incline. Consider cleats or textured belt for better grip.")
        
        # Tension considerations
        if result.tight_tension > 1000:
            recommendations.append("High belt tension. Verify belt and pulley specifications.")
        
        return recommendations
