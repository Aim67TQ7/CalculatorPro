import math
import plotly.graph_objects as go
from models.requests import ScreenSizingRequest
from models.responses import ScreenSizingResult

class ScreenSizingCalculator:
    def calculate(self, request: ScreenSizingRequest) -> ScreenSizingResult:
        """Calculate screen sizing parameters"""
        feed_rate = request.feed_rate
        oversize_percentage = request.oversize_percentage
        undersize_percentage = request.undersize_percentage
        mesh_size = request.mesh_size
        bulk_density = request.bulk_density
        moisture_content = request.moisture_content

        # Calculate basic capacity using Tyler standard
        # Base capacity for 1 sq ft of screen area (tons/hr/sq ft)
        base_capacity = 0.5  # Base capacity for dry material

        # Apply corrections for moisture content
        moisture_factor = 1 - (moisture_content / 100) * 0.3  # Reduce capacity by 30% at 10% moisture

        # Apply mesh size factor
        # Smaller mesh sizes have lower capacity
        mesh_factor = max(0.3, mesh_size / 50)  # Normalized to 50mm

        # Calculate actual capacity per sq ft
        capacity_per_sqft = base_capacity * moisture_factor * mesh_factor

        # Calculate required screen area
        screen_area = feed_rate / capacity_per_sqft

        # Calculate efficiency based on oversize/undersize split
        # Efficiency is affected by near-size particles
        near_size_factor = 1 - abs(oversize_percentage - undersize_percentage) / 200
        efficiency = 0.85 + near_size_factor * 0.10  # 85-95% efficiency range

        # Calculate actual flow rates
        underflow_rate = feed_rate * (undersize_percentage / 100)
        overflow_rate = feed_rate * (oversize_percentage / 100)

        return ScreenSizingResult(
            screen_area=screen_area,
            capacity=capacity_per_sqft,
            efficiency=efficiency,
            underflow_rate=underflow_rate,
            overflow_rate=overflow_rate
        )

    def create_efficiency_chart(self, request: ScreenSizingRequest, result: ScreenSizingResult):
        """Create efficiency chart vs mesh size"""
        mesh_range = list(range(5, 101, 5))
        efficiencies = []

        for mesh in mesh_range:
            temp_request = ScreenSizingRequest(
                feed_rate=request.feed_rate,
                oversize_percentage=request.oversize_percentage,
                undersize_percentage=request.undersize_percentage,
                mesh_size=mesh,
                bulk_density=request.bulk_density,
                moisture_content=request.moisture_content
            )
            temp_result = self.calculate(temp_request)
            efficiencies.append(temp_result.efficiency * 100)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=mesh_range,
            y=efficiencies,
            mode='lines+markers',
            name='Screening Efficiency',
            line=dict(color='#1f77b4', width=2)
        ))

        # Highlight selected mesh size
        fig.add_trace(go.Scatter(
            x=[request.mesh_size],
            y=[result.efficiency * 100],
            mode='markers',
            name='Selected',
            marker=dict(color='red', size=12)
        ))

        fig.update_layout(
            title='Screening Efficiency vs Mesh Size',
            xaxis_title='Mesh Size (mm)',
            yaxis_title='Screening Efficiency (%)',
            showlegend=True,
            height=400
        )

        return fig

    def get_recommendations(self, request: ScreenSizingRequest, result: ScreenSizingResult) -> list:
        """Generate recommendations"""
        recommendations = []
        
        # Screen area recommendations
        if result.screen_area < 10:
            recommendations.append("Small screen area. Consider multiple decks for higher capacity.")
        elif result.screen_area > 100:
            recommendations.append("Large screen area required. Consider multiple screens in parallel.")
        
        # Mesh size considerations
        if request.mesh_size < 2:
            recommendations.append("Very fine mesh may cause blinding. Consider scalping and pre-screening.")
        elif request.mesh_size > 50:
            recommendations.append("Coarse mesh screening. Verify material size distribution.")
        
        # Moisture effects
        if request.moisture_content > 5:
            recommendations.append("High moisture content reduces screening efficiency. Consider drying.")
        
        # Efficiency optimization
        if result.efficiency < 0.8:
            recommendations.append("Low screening efficiency. Consider larger screen area or multiple decks.")
        
        # Feed rate considerations
        split_ratio = request.oversize_percentage / request.undersize_percentage if request.undersize_percentage > 0 else float('inf')
        if split_ratio > 4 or split_ratio < 0.25:
            recommendations.append("Uneven size distribution may require staged screening.")
        
        return recommendations
