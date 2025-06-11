import math
import plotly.graph_objects as go
from models.requests import GravityFlowRequest
from models.responses import GravityFlowResult
from utils.conversions import convert_bulk_density_to_imperial, convert_bulk_density_to_metric

class GravityFlowCalculator:
    def __init__(self):
        # Aperture flow map from original code
        self.aperture_flow_map = {
            30: 35.32,
            50: 98.88,
            70: 194.23,
            90: 254.27,
            120: 395.53,
            150: 568.57,
            200: 889.94,
            250: 1528.11,
            300: 2468.52,
            350: 3556.22,
            400: 6921.74
        }

    def calculate(self, request: GravityFlowRequest) -> GravityFlowResult:
        """Calculate gravity MD flow rate based on aperture size and bulk density"""
        aperture_size_mm = request.aperture_size_mm
        bulk_density = request.bulk_density
        use_imperial = request.use_imperial

        # Convert bulk density to lb/ft³ if it's in kg/m³
        if not use_imperial:
            bulk_density_imperial = convert_bulk_density_to_imperial(bulk_density)
        else:
            bulk_density_imperial = bulk_density

        if aperture_size_mm in self.aperture_flow_map:
            ft3_hr = self.aperture_flow_map[aperture_size_mm]
            lb_hr = ft3_hr * bulk_density_imperial

            if not use_imperial:
                # Convert results to metric (m³/hr and kg/hr)
                volume_flow = ft3_hr * 0.0283168  # Convert ft³/hr to m³/hr
                mass_flow = lb_hr * 0.453592      # Convert lb/hr to kg/hr
                volume_unit = "m³/hr"
                mass_unit = "kg/hr"
            else:
                volume_flow = ft3_hr
                mass_flow = lb_hr
                volume_unit = "ft³/hr"
                mass_unit = "lb/hr"

            return GravityFlowResult(
                flow_rate_volume=volume_flow,
                flow_rate_mass=mass_flow,
                volume_unit=volume_unit,
                mass_unit=mass_unit
            )
        else:
            raise ValueError(f"Invalid aperture size: {aperture_size_mm}")

    def create_comparison_chart(self, aperture_size, bulk_density, use_imperial=False):
        """Create a bar chart comparing flow rates for different aperture sizes"""
        aperture_sizes = list(self.aperture_flow_map.keys())
        flow_rates = []

        # Convert bulk_density for calculations
        if not use_imperial:
            bulk_density_calc = convert_bulk_density_to_imperial(bulk_density)
        else:
            bulk_density_calc = bulk_density

        for size in aperture_sizes:
            ft3_hr = self.aperture_flow_map[size]
            if not use_imperial:
                ft3_hr = ft3_hr * 0.0283168  # Convert to m³/hr
            flow_rates.append(ft3_hr)

        fig = go.Figure()

        # Add bar chart
        fig.add_trace(go.Bar(
            x=aperture_sizes,
            y=flow_rates,
            name='Flow Rate',
            marker_color='#1f77b4'
        ))

        # Highlight selected aperture size
        if aperture_size in aperture_sizes:
            selected_flow = flow_rates[aperture_sizes.index(aperture_size)]
            fig.add_trace(go.Scatter(
                x=[aperture_size],
                y=[selected_flow],
                mode='markers',
                name='Selected',
                marker=dict(color='red', size=12)
            ))

        volume_unit = "m³/hr" if not use_imperial else "ft³/hr"
        
        fig.update_layout(
            title='Flow Rate Comparison by Aperture Size',
            xaxis_title='Aperture Size (mm)',
            yaxis_title=f'Flow Rate ({volume_unit})',
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return fig

    def get_recommendations(self, request: GravityFlowRequest, result: GravityFlowResult) -> list:
        """Generate recommendations based on calculation results"""
        recommendations = []
        
        # Flow rate recommendations
        if result.flow_rate_volume < 50:
            recommendations.append("Low flow rate detected. Consider larger aperture size for higher throughput.")
        elif result.flow_rate_volume > 5000:
            recommendations.append("High flow rate. Ensure downstream equipment can handle this capacity.")
        
        # Aperture size recommendations
        if request.aperture_size_mm < 100:
            recommendations.append("Small aperture size may be prone to bridging with cohesive materials.")
        
        # Bulk density considerations
        density_threshold = 100 if request.use_imperial else 1600  # lb/ft³ or kg/m³
        if request.bulk_density > density_threshold:
            recommendations.append("High bulk density material. Consider structural reinforcement for equipment.")
        
        return recommendations
