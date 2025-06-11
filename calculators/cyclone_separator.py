import math
import plotly.graph_objects as go
from models.requests import CycloneSeparatorRequest
from models.responses import CycloneSeparatorResult

class CycloneSeparatorCalculator:
    def calculate(self, request: CycloneSeparatorRequest) -> CycloneSeparatorResult:
        """Calculate cyclone separator parameters"""
        inlet_velocity = request.inlet_velocity
        cyclone_diameter = request.cyclone_diameter
        particle_density = request.particle_density
        gas_density = request.gas_density
        gas_viscosity = request.gas_viscosity
        cut_size = request.cut_size / 1000000  # Convert microns to meters

        # Calculate d50 cut size using Barth equation
        # d50 = sqrt(18 * μ * Q / (2π * N * Vt * (ρp - ρg) * Dc))
        
        # Calculate volumetric flow rate
        inlet_area = cyclone_diameter * 0.2 * 0.5  # Typical inlet dimensions
        volumetric_flow_rate = inlet_velocity * inlet_area

        # Number of effective turns (typical range 1.5-5)
        effective_turns = 1.5 + (cyclone_diameter - 0.5) * 2  # Increases with diameter

        # Calculate tangential velocity at radius
        tangential_velocity = inlet_velocity * 0.8  # Reduce due to friction

        # Calculate d50 cut size
        numerator = 18 * gas_viscosity * volumetric_flow_rate
        denominator = 2 * math.pi * effective_turns * tangential_velocity * (particle_density * 1000 - gas_density) * cyclone_diameter
        d50_calculated = math.sqrt(numerator / denominator) * 1000000  # Convert to microns

        # Calculate collection efficiency using Lapple equation
        # η = 1 / (1 + (d50/dp)²)
        if cut_size * 1000000 > 0:
            efficiency_factor = (d50_calculated / (cut_size * 1000000))**2
            collection_efficiency = efficiency_factor / (1 + efficiency_factor)
        else:
            collection_efficiency = 0.5

        # Calculate pressure drop using Shepherd and Lapple correlation
        # ΔP = K * ρg * V²/2, where K is loss coefficient (4-8 for cyclones)
        loss_coefficient = 6  # Typical value
        pressure_drop = loss_coefficient * gas_density * (inlet_velocity**2) / 2

        # Calculate throughput based on inlet conditions
        throughput = volumetric_flow_rate * gas_density * 3600  # kg/hr

        return CycloneSeparatorResult(
            cut_size_d50=d50_calculated,
            pressure_drop=pressure_drop,
            collection_efficiency=collection_efficiency,
            throughput=throughput
        )

    def create_performance_chart(self, request: CycloneSeparatorRequest, result: CycloneSeparatorResult):
        """Create performance chart showing efficiency vs particle size"""
        particle_sizes = [i for i in range(1, 101, 5)]  # 1 to 100 microns
        efficiencies = []

        for size in particle_sizes:
            # Calculate efficiency for each particle size
            d50 = result.cut_size_d50
            if d50 > 0:
                efficiency_factor = (d50 / size)**2
                efficiency = efficiency_factor / (1 + efficiency_factor)
            else:
                efficiency = 0.5
            efficiencies.append(efficiency * 100)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=particle_sizes,
            y=efficiencies,
            mode='lines+markers',
            name='Collection Efficiency',
            line=dict(color='#1f77b4', width=2)
        ))

        # Highlight cut size
        fig.add_trace(go.Scatter(
            x=[request.cut_size],
            y=[50],  # 50% efficiency at cut size
            mode='markers',
            name='Cut Size (50% efficiency)',
            marker=dict(color='red', size=12)
        ))

        fig.update_layout(
            title='Cyclone Collection Efficiency vs Particle Size',
            xaxis_title='Particle Size (microns)',
            yaxis_title='Collection Efficiency (%)',
            showlegend=True,
            height=400
        )

        return fig

    def get_recommendations(self, request: CycloneSeparatorRequest, result: CycloneSeparatorResult) -> list:
        """Generate recommendations"""
        recommendations = []
        
        # Cut size recommendations
        if result.cut_size_d50 > 20:
            recommendations.append("Large cut size. Consider smaller diameter cyclone for finer separation.")
        elif result.cut_size_d50 < 2:
            recommendations.append("Very fine cut size achieved. Verify this meets separation requirements.")
        
        # Pressure drop considerations
        if result.pressure_drop > 2500:  # Pa
            recommendations.append("High pressure drop increases fan power requirements.")
        elif result.pressure_drop < 500:
            recommendations.append("Low pressure drop may indicate poor separation performance.")
        
        # Inlet velocity optimization
        if request.inlet_velocity < 10:
            recommendations.append("Low inlet velocity reduces separation efficiency.")
        elif request.inlet_velocity > 30:
            recommendations.append("High inlet velocity increases pressure drop and erosion.")
        
        # Cyclone diameter effects
        if request.cyclone_diameter < 0.3:
            recommendations.append("Small cyclone diameter provides fine separation but low capacity.")
        elif request.cyclone_diameter > 3:
            recommendations.append("Large cyclone diameter increases cut size but handles high flow rates.")
        
        # Collection efficiency
        if result.collection_efficiency < 0.7:
            recommendations.append("Low collection efficiency. Consider multiple cyclones in series or parallel.")
        
        # Particle density considerations
        if request.particle_density < 2:
            recommendations.append("Low particle density makes separation more difficult.")
        
        return recommendations
