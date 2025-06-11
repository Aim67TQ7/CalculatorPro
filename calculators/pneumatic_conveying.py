import math
import plotly.graph_objects as go
from models.requests import PneumaticConveyingRequest
from models.responses import PneumaticConveyingResult

class PneumaticConveyingCalculator:
    def calculate(self, request: PneumaticConveyingRequest) -> PneumaticConveyingResult:
        """Calculate pneumatic conveying parameters"""
        material_flow_rate = request.material_flow_rate
        conveying_distance = request.conveying_distance
        vertical_lift = request.vertical_lift
        pipe_diameter = request.pipe_diameter
        bulk_density = request.bulk_density
        particle_size = request.particle_size

        # Convert units
        material_flow_rate_kg_s = material_flow_rate * 1000 / 3600  # tons/hr to kg/s
        pipe_diameter_m = pipe_diameter * 0.0254  # inches to meters
        pipe_area = math.pi * (pipe_diameter_m / 2)**2

        # Calculate minimum conveying velocity
        # Based on Rizk's correlation for minimum conveying velocity
        particle_terminal_velocity = 0.05 * math.sqrt(particle_size)  # Simplified
        min_velocity = 12 + 2.5 * particle_terminal_velocity

        # Calculate actual air velocity (typically 1.5-2x minimum)
        air_velocity = min_velocity * 1.8

        # Calculate air flow rate
        air_flow_rate = air_velocity * pipe_area  # m³/s

        # Calculate conveying velocity (material velocity in pipe)
        # Typically 70-90% of air velocity
        conveying_velocity = air_velocity * 0.8

        # Calculate pressure drop
        # Total pressure drop = acceleration + friction + gravity
        
        # Acceleration pressure drop
        dp_acceleration = (material_flow_rate_kg_s * air_velocity) / pipe_area
        
        # Friction pressure drop (Darcy-Weisbach equation)
        friction_factor = 0.02  # Typical for pneumatic conveying
        air_density = 1.2  # kg/m³ at standard conditions
        dp_friction = friction_factor * (conveying_distance / pipe_diameter_m) * (air_density * air_velocity**2) / 2
        
        # Gravity pressure drop
        dp_gravity = air_density * 9.81 * vertical_lift
        
        # Total pressure drop
        pressure_drop = dp_acceleration + dp_friction + dp_gravity

        # Calculate power required
        # Power = air flow rate × pressure drop / efficiency
        fan_efficiency = 0.75
        power_required = (air_flow_rate * pressure_drop) / (fan_efficiency * 1000)  # kW

        return PneumaticConveyingResult(
            air_velocity=air_velocity,
            pressure_drop=pressure_drop,
            power_required=power_required,
            conveying_velocity=conveying_velocity,
            air_flow_rate=air_flow_rate
        )

    def create_pressure_chart(self, request: PneumaticConveyingRequest, result: PneumaticConveyingResult):
        """Create pressure drop chart vs distance"""
        distance_range = list(range(50, 1001, 50))
        pressure_drops = []

        for distance in distance_range:
            temp_request = PneumaticConveyingRequest(
                material_flow_rate=request.material_flow_rate,
                conveying_distance=distance,
                vertical_lift=request.vertical_lift,
                pipe_diameter=request.pipe_diameter,
                bulk_density=request.bulk_density,
                particle_size=request.particle_size
            )
            temp_result = self.calculate(temp_request)
            pressure_drops.append(temp_result.pressure_drop / 1000)  # Convert to kPa

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=distance_range,
            y=pressure_drops,
            mode='lines+markers',
            name='Pressure Drop',
            line=dict(color='#1f77b4', width=2)
        ))

        # Highlight selected distance
        fig.add_trace(go.Scatter(
            x=[request.conveying_distance],
            y=[result.pressure_drop / 1000],
            mode='markers',
            name='Selected',
            marker=dict(color='red', size=12)
        ))

        fig.update_layout(
            title='Pneumatic Conveying Pressure Drop vs Distance',
            xaxis_title='Conveying Distance (ft)',
            yaxis_title='Pressure Drop (kPa)',
            showlegend=True,
            height=400
        )

        return fig

    def get_recommendations(self, request: PneumaticConveyingRequest, result: PneumaticConveyingResult) -> list:
        """Generate recommendations"""
        recommendations = []
        
        # Air velocity recommendations
        if result.air_velocity < 15:
            recommendations.append("Low air velocity may cause material settling in the pipeline.")
        elif result.air_velocity > 40:
            recommendations.append("High air velocity increases power consumption and product degradation.")
        
        # Pressure drop considerations
        if result.pressure_drop > 50000:  # Pa
            recommendations.append("High pressure drop. Consider larger pipe diameter or shorter distance.")
        
        # Power requirements
        if result.power_required > 50:
            recommendations.append("High power requirement. Consider system optimization or staged conveying.")
        
        # Pipe diameter recommendations
        if request.pipe_diameter < 3:
            recommendations.append("Small pipe diameter increases pressure drop and blockage risk.")
        elif request.pipe_diameter > 8:
            recommendations.append("Large pipe diameter may reduce conveying efficiency for low flow rates.")
        
        # Material considerations
        if request.bulk_density > 100:
            recommendations.append("High bulk density material requires higher air velocities.")
        
        if request.particle_size > 20:
            recommendations.append("Large particles may require dense phase conveying system.")
        
        return recommendations
