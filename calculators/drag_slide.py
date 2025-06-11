import math
from models.requests import DragSlideRequest
from models.responses import DragSlideResult

class DragSlideCalculator:
    def calculate(self, request: DragSlideRequest) -> DragSlideResult:
        """Calculate drag slide dimensions with and without magnet"""
        x_val = request.x_value
        y_val = request.y_value

        # With magnet calculations
        A_with = 82.0
        B_with = math.sqrt(x_val**2 + y_val**2) + 28.0
        OAL_with = math.sqrt(x_val**2 + y_val**2) + 101.44

        # Without magnet calculations
        A_without = 82.0
        B_without = math.sqrt(x_val**2 + y_val**2) + 13.0
        OAL_without = math.sqrt(x_val**2 + y_val**2) + 80.34

        return DragSlideResult(
            with_magnet={
                "A": A_with,
                "B": B_with,
                "OAL": OAL_with
            },
            without_magnet={
                "A": A_without,
                "B": B_without,
                "OAL": OAL_without
            }
        )

    def get_recommendations(self, request: DragSlideRequest, result: DragSlideResult) -> list:
        """Generate recommendations based on calculation results"""
        recommendations = []
        
        # Size considerations
        diagonal = math.sqrt(request.x_value**2 + request.y_value**2)
        
        if diagonal < 50:
            recommendations.append("Compact design suitable for tight spaces.")
        elif diagonal > 200:
            recommendations.append("Large dimensions. Consider structural support requirements.")
        
        # Magnet vs non-magnet comparison
        oal_difference = result.with_magnet["OAL"] - result.without_magnet["OAL"]
        recommendations.append(f"Magnet configuration adds {oal_difference:.1f} units to overall length.")
        
        # Material handling considerations
        if request.x_value > request.y_value * 2:
            recommendations.append("High aspect ratio. Consider material flow characteristics.")
        
        return recommendations
