import plotly.graph_objects as go
from models.requests import SpoutRequirementsRequest
from models.responses import SpoutRequirementsResult, SpoutResult

class SpoutRequirementsCalculator:
    def __init__(self):
        self.round_spout_data = {
            "Diameter (in)": [4, 5, 6, 8, 10, 12, 14, 16, 18, 20],
            "Area (sq. in.)": [12.6, 19.6, 28.3, 50.3, 78.5, 113.0, 153.9, 201.0, 254.5, 314.2],
            "Capacity at 50 PCF (CFH)": [504, 784, 1132, 2012, 3140, 4520, 6156, 8040, 10180, 12568],
            "Capacity at 35 PCF (CFH)": [360, 561, 809, 1439, 2245, 3232, 4402, 5749, 7279, 8986],
        }

        self.square_spout_data = {
            "Size (in)": ["4x4", "5x5", "6x6", "8x8", "10x10", "12x12", "14x14", "16x16", "18x18", "20x20"],
            "Area (sq. in.)": [16.0, 25.0, 36.0, 64.0, 100.0, 144.0, 196.0, 256.0, 324.0, 400.0],
            "Capacity at 50 PCF (CFH)": [640, 1000, 1440, 2560, 4000, 5760, 7840, 10240, 12960, 16000],
            "Capacity at 35 PCF (CFH)": [458, 715, 1030, 1830, 2860, 4118, 5606, 7322, 9266, 11440],
        }

    def convert_capacity_to_cfh(self, capacity_value, unit, bulk_density):
        """Convert capacity from tons/hr or lbs/hr to cubic feet per hour"""
        if unit == "tons/hr":
            lbs_per_hour = capacity_value * 2000
        else:  # lbs/hr
            lbs_per_hour = capacity_value

        return lbs_per_hour / bulk_density

    def calculate(self, request: SpoutRequirementsRequest) -> SpoutRequirementsResult:
        """Calculate spout requirements based on inputs"""
        bulk_density = request.bulk_density
        capacity_value = request.capacity_value
        capacity_unit = request.capacity_unit

        # Convert to cubic feet per hour
        cfh = self.convert_capacity_to_cfh(capacity_value, capacity_unit, bulk_density)

        # Calculate density factor
        density_factor = bulk_density / 50

        # Find suitable spouts
        round_spout = None
        square_spout = None

        # Check round spouts
        for i, capacity in enumerate(self.round_spout_data["Capacity at 50 PCF (CFH)"]):
            if capacity * density_factor >= cfh:
                round_spout = SpoutResult(
                    diameter=self.round_spout_data["Diameter (in)"][i],
                    area=self.round_spout_data["Area (sq. in.)"][i],
                    max_cfh=capacity * density_factor
                )
                break

        # Check square spouts
        for i, capacity in enumerate(self.square_spout_data["Capacity at 50 PCF (CFH)"]):
            if capacity * density_factor >= cfh:
                square_spout = SpoutResult(
                    size=self.square_spout_data["Size (in)"][i],
                    area=self.square_spout_data["Area (sq. in.)"][i],
                    max_cfh=capacity * density_factor
                )
                break

        return SpoutRequirementsResult(
            required_cfh=cfh,
            round_spout=round_spout,
            square_spout=square_spout
        )

    def create_comparison_chart(self, bulk_density, capacity_cfh):
        """Create a bar chart comparing both round and square spout capacities"""
        density_factor = bulk_density / 50

        # Calculate capacities for both types
        round_capacities = [cap * density_factor for cap in self.round_spout_data["Capacity at 50 PCF (CFH)"]]
        square_capacities = [cap * density_factor for cap in self.square_spout_data["Capacity at 50 PCF (CFH)"]]

        # Create figure
        fig = go.Figure()

        # Add round spout bars
        fig.add_trace(go.Bar(
            name='Round Spout',
            x=[f"{d}\" Dia" for d in self.round_spout_data["Diameter (in)"]],
            y=round_capacities,
            marker_color='#1f77b4'
        ))

        # Add square spout bars
        fig.add_trace(go.Bar(
            name='Square Spout',
            x=[size for size in self.square_spout_data["Size (in)"]],
            y=square_capacities,
            marker_color='#ff7f0e'
        ))

        # Add target capacity line
        all_x_values = ([f"{d}\" Dia" for d in self.round_spout_data["Diameter (in)"]] + 
                       [size for size in self.square_spout_data["Size (in)"]])
        
        fig.add_trace(go.Scatter(
            name='Required Capacity',
            x=all_x_values,
            y=[capacity_cfh] * len(all_x_values),
            line=dict(color='red', dash='dash')
        ))

        fig.update_layout(
            title='Spout Capacity Comparison',
            xaxis_title='Spout Size',
            yaxis_title='Capacity (CFH)',
            barmode='group',
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=50, b=50)
        )

        return fig

    def get_recommendations(self, request: SpoutRequirementsRequest, result: SpoutRequirementsResult) -> list:
        """Generate recommendations based on calculation results"""
        recommendations = []
        
        if not result.round_spout and not result.square_spout:
            recommendations.append("No suitable spout found. Consider reducing flow rate or using custom sizing.")
        
        if result.round_spout and result.square_spout:
            if result.round_spout.area < result.square_spout.area:
                recommendations.append("Round spout provides more compact solution.")
            else:
                recommendations.append("Square spout may provide better flow characteristics.")
        
        # Capacity utilization
        if result.round_spout:
            utilization = (result.required_cfh / result.round_spout.max_cfh) * 100
            if utilization > 80:
                recommendations.append("High capacity utilization. Consider next size up for safety margin.")
        
        # Material handling considerations
        if request.bulk_density > 75:
            recommendations.append("High density material. Consider reinforced spout construction.")
        
        return recommendations
