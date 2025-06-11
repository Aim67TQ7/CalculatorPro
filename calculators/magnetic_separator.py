import math
import plotly.graph_objects as go
from models.requests import MagneticSeparatorRequest
from models.responses import MagneticSeparatorResult

class MagneticSeparatorCalculator:
    def calculate(self, request: MagneticSeparatorRequest) -> MagneticSeparatorResult:
        """Calculate magnetic separator parameters"""
        belt_width = request.belt_width
        belt_speed = request.belt_speed
        material_depth = request.material_depth
        magnetic_intensity = request.magnetic_intensity
        particle_size = request.particle_size

        # Calculate magnetic force (simplified model)
        # Force is proportional to magnetic intensity and inversely to distance squared
        effective_distance = material_depth + 2  # Add air gap
        magnetic_force = (magnetic_intensity**2) / (effective_distance**2) * 0.001

        # Calculate separation efficiency based on particle size and magnetic intensity
        # Smaller particles are harder to separate
        size_factor = min(particle_size / 10, 1.0)  # Normalize to 10mm
        intensity_factor = min(magnetic_intensity / 1000, 1.0)  # Normalize to 1000 Gauss
        separation_efficiency = size_factor * intensity_factor * 0.95  # Max 95%

        # Calculate throughput capacity
        belt_area = belt_width * 12  # Assume 1 ft belt length per calculation
        throughput_capacity = (belt_area * material_depth * belt_speed * 60) / 1728  # ft³/hr

        # Calculate recovery rate (percentage of magnetic material recovered)
        # Higher speed reduces recovery
        speed_factor = max(0.5, 1 - (belt_speed - 100) / 1000)
        recovery_rate = separation_efficiency * speed_factor

        return MagneticSeparatorResult(
            separation_efficiency=separation_efficiency,
            magnetic_force=magnetic_force,
            throughput_capacity=throughput_capacity,
            recovery_rate=recovery_rate
        )

    def create_efficiency_chart(self, request: MagneticSeparatorRequest, result: MagneticSeparatorResult):
        """Create efficiency chart vs magnetic intensity"""
        intensity_range = list(range(500, 3001, 250))
        efficiencies = []

        for intensity in intensity_range:
            temp_request = MagneticSeparatorRequest(
                belt_width=request.belt_width,
                belt_speed=request.belt_speed,
                material_depth=request.material_depth,
                magnetic_intensity=intensity,
                particle_size=request.particle_size
            )
            temp_result = self.calculate(temp_request)
            efficiencies.append(temp_result.separation_efficiency * 100)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=intensity_range,
            y=efficiencies,
            mode='lines+markers',
            name='Separation Efficiency',
            line=dict(color='#1f77b4', width=2)
        ))

        # Highlight selected intensity
        fig.add_trace(go.Scatter(
            x=[request.magnetic_intensity],
            y=[result.separation_efficiency * 100],
            mode='markers',
            name='Selected',
            marker=dict(color='red', size=12)
        ))

        fig.update_layout(
            title='Magnetic Separation Efficiency vs Magnetic Intensity',
            xaxis_title='Magnetic Intensity (Gauss)',
            yaxis_title='Separation Efficiency (%)',
            showlegend=True,
            height=400
        )

        return fig

    def get_recommendations(self, request: MagneticSeparatorRequest, result: MagneticSeparatorResult) -> list:
        """Generate recommendations"""
        recommendations = []
        
        # Magnetic intensity recommendations
        if request.magnetic_intensity < 1000:
            recommendations.append("Low magnetic intensity may result in poor separation of weakly magnetic materials.")
        elif request.magnetic_intensity > 2500:
            recommendations.append("Very high magnetic intensity increases power consumption.")
        
        # Belt speed considerations
        if request.belt_speed > 300:
            recommendations.append("High belt speed reduces contact time and separation efficiency.")
        elif request.belt_speed < 50:
            recommendations.append("Low belt speed may cause material buildup.")
        
        # Material depth effects
        if request.material_depth > 4:
            recommendations.append("Deep material bed reduces magnetic field penetration.")
        
        # Particle size considerations
        if request.particle_size < 1:
            recommendations.append("Fine particles require higher magnetic intensity for effective separation.")
        
        # Efficiency warnings
        if result.separation_efficiency < 0.6:
            recommendations.append("Low separation efficiency. Consider adjusting parameters or multiple passes.")
        
        return recommendations
