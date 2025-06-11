import math
import plotly.graph_objects as go
from models.requests import ScrewConveyorRequest
from models.responses import ScrewConveyorResult

class ScrewConveyorCalculator:
    def calculate(self, request: ScrewConveyorRequest) -> ScrewConveyorResult:
        """Calculate screw conveyor capacity, torque, and power requirements"""
        diameter = request.diameter
        pitch = request.pitch
        rpm = request.rpm
        length = request.length
        bulk_density = request.bulk_density
        material_factor = request.material_factor
        incline_angle = request.incline_angle

        # Calculate capacity in ft³/hr
        capacity_ft3_hr = (math.pi * (diameter/12)**2 / 4) * (pitch/12) * rpm * 60 * material_factor

        # Apply incline factor
        incline_factor = 1 - (incline_angle / 45) * 0.3  # Reduce capacity by up to 30% at 45°
        capacity_ft3_hr *= incline_factor

        # Convert to tons/hr
        capacity_tons_hr = (capacity_ft3_hr * bulk_density) / 2000

        # Calculate torque (simplified formula)
        # Torque = (Material load + Friction) × Radius
        material_load = capacity_ft3_hr * bulk_density * length / 3600  # lb-ft
        friction_factor = 0.02 + (incline_angle / 90) * 0.03  # Increases with incline
        torque_in_lbs = (material_load * friction_factor * (diameter/2)) * 12  # Convert to in-lbs

        # Calculate horsepower
        horsepower = (torque_in_lbs * rpm) / 63000

        # Calculate efficiency
        efficiency = 0.85 - (incline_angle / 90) * 0.15  # Decreases with incline

        return ScrewConveyorResult(
            capacity_ft3_hr=capacity_ft3_hr,
            capacity_tons_hr=capacity_tons_hr,
            torque_in_lbs=torque_in_lbs,
            horsepower=horsepower,
            efficiency=efficiency
        )

    def create_performance_chart(self, request: ScrewConveyorRequest):
        """Create a performance chart showing capacity vs RPM"""
        rpm_range = list(range(10, 201, 10))
        capacities = []

        for rpm in rpm_range:
            temp_request = ScrewConveyorRequest(
                diameter=request.diameter,
                pitch=request.pitch,
                rpm=rpm,
                length=request.length,
                bulk_density=request.bulk_density,
                material_factor=request.material_factor,
                incline_angle=request.incline_angle
            )
            result = self.calculate(temp_request)
            capacities.append(result.capacity_tons_hr)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=rpm_range,
            y=capacities,
            mode='lines+markers',
            name='Capacity',
            line=dict(color='#1f77b4', width=2),
            marker=dict(size=6)
        ))

        # Highlight selected RPM
        selected_result = self.calculate(request)
        fig.add_trace(go.Scatter(
            x=[request.rpm],
            y=[selected_result.capacity_tons_hr],
            mode='markers',
            name='Selected',
            marker=dict(color='red', size=12)
        ))

        fig.update_layout(
            title='Screw Conveyor Capacity vs RPM',
            xaxis_title='RPM',
            yaxis_title='Capacity (tons/hr)',
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return fig

    def get_recommendations(self, request: ScrewConveyorRequest, result: ScrewConveyorResult) -> list:
        """Generate recommendations based on calculation results"""
        recommendations = []
        
        # RPM recommendations
        if request.rpm < 30:
            recommendations.append("Low RPM may cause material bridging in certain applications.")
        elif request.rpm > 150:
            recommendations.append("High RPM increases wear and power consumption.")
        
        # Power requirements
        if result.horsepower > 20:
            recommendations.append("High power requirement. Consider multiple smaller units or larger diameter.")
        
        # Efficiency considerations
        if result.efficiency < 0.7:
            recommendations.append("Low efficiency due to incline. Consider belt conveyor for steep angles.")
        
        # Capacity utilization
        if result.capacity_tons_hr < 1:
            recommendations.append("Low capacity. Consider smaller diameter for better material movement.")
        elif result.capacity_tons_hr > 100:
            recommendations.append("High capacity system. Verify structural and drive requirements.")
        
        return recommendations
