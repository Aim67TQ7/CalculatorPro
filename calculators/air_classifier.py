import math
import plotly.graph_objects as go
from models.requests import AirClassifierRequest
from models.responses import AirClassifierResult

class AirClassifierCalculator:
    def calculate(self, request: AirClassifierRequest) -> AirClassifierResult:
        """Calculate air classifier parameters"""
        air_velocity = request.air_velocity
        particle_density = request.particle_density
        particle_diameter = request.particle_diameter / 1000000  # Convert microns to meters
        air_temperature = request.air_temperature
        air_pressure = request.air_pressure

        # Calculate air properties at given conditions
        air_density = (air_pressure * 1000) / (287 * (air_temperature + 273.15))  # kg/m³
        air_viscosity = 1.8e-5 * ((273.15 + air_temperature) / 273.15)**0.7  # Pa·s

        # Calculate terminal velocity using Stokes' law (for small particles)
        gravity = 9.81
        if particle_diameter < 0.0001:  # For particles < 100 microns
            terminal_velocity = ((particle_density * 1000 - air_density) * gravity * particle_diameter**2) / (18 * air_viscosity)
        else:  # For larger particles, use drag equation
            cd = 0.44  # Drag coefficient for spheres
            terminal_velocity = math.sqrt((4 * gravity * particle_diameter * (particle_density * 1000 - air_density)) / (3 * cd * air_density))

        # Calculate classification efficiency
        # Efficiency depends on ratio of air velocity to terminal velocity
        velocity_ratio = air_velocity / terminal_velocity
        if velocity_ratio > 1.5:
            classification_efficiency = 0.95
        elif velocity_ratio > 0.8:
            classification_efficiency = 0.7 + (velocity_ratio - 0.8) * 0.36
        else:
            classification_efficiency = 0.4 + velocity_ratio * 0.375

        # Calculate air requirement (m³/s per kg/s of material)
        # Simplified: based on minimum fluidization velocity
        air_requirement = air_velocity * 2  # m³/s per m² of classifier area

        # Calculate pressure drop (simplified)
        # ΔP = f × (L/D) × (ρV²/2) where f is friction factor
        friction_factor = 0.02
        length_diameter_ratio = 4  # Typical for classifiers
        pressure_drop = friction_factor * length_diameter_ratio * (air_density * air_velocity**2) / 2

        return AirClassifierResult(
            terminal_velocity=terminal_velocity,
            classification_efficiency=classification_efficiency,
            air_requirement=air_requirement,
            pressure_drop=pressure_drop
        )

    def create_classification_chart(self, request: AirClassifierRequest, result: AirClassifierResult):
        """Create classification efficiency chart vs air velocity"""
        velocity_range = [v/10 for v in range(50, 501, 25)]  # 0.5 to 50 m/s
        efficiencies = []

        for velocity in velocity_range:
            temp_request = AirClassifierRequest(
                air_velocity=velocity,
                particle_density=request.particle_density,
                particle_diameter=request.particle_diameter,
                air_temperature=request.air_temperature,
                air_pressure=request.air_pressure
            )
            temp_result = self.calculate(temp_request)
            efficiencies.append(temp_result.classification_efficiency * 100)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=velocity_range,
            y=efficiencies,
            mode='lines+markers',
            name='Classification Efficiency',
            line=dict(color='#1f77b4', width=2)
        ))

        # Highlight selected velocity
        fig.add_trace(go.Scatter(
            x=[request.air_velocity],
            y=[result.classification_efficiency * 100],
            mode='markers',
            name='Selected',
            marker=dict(color='red', size=12)
        ))

        fig.update_layout(
            title='Air Classification Efficiency vs Air Velocity',
            xaxis_title='Air Velocity (m/s)',
            yaxis_title='Classification Efficiency (%)',
            showlegend=True,
            height=400
        )

        return fig

    def get_recommendations(self, request: AirClassifierRequest, result: AirClassifierResult) -> list:
        """Generate recommendations"""
        recommendations = []
        
        # Air velocity recommendations
        if request.air_velocity < 2:
            recommendations.append("Low air velocity may not provide adequate particle separation.")
        elif request.air_velocity > 30:
            recommendations.append("Very high air velocity increases power consumption and wear.")
        
        # Particle size considerations
        if request.particle_diameter < 10:
            recommendations.append("Very fine particles require careful control of air velocity.")
        elif request.particle_diameter > 500:
            recommendations.append("Coarse particles may require screening instead of air classification.")
        
        # Efficiency optimization
        if result.classification_efficiency < 0.7:
            recommendations.append("Low efficiency. Consider adjusting air velocity or using multi-stage classification.")
        
        # Pressure drop concerns
        if result.pressure_drop > 5000:  # Pa
            recommendations.append("High pressure drop increases fan power requirements.")
        
        # Operating conditions
        if request.air_temperature > 80:
            recommendations.append("High temperature affects air density and classification performance.")
        
        return recommendations
