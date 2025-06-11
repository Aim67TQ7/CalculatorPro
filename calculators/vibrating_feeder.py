import math
import plotly.graph_objects as go
from models.requests import VibratingFeederRequest
from models.responses import VibratingFeederResult

class VibratingFeederCalculator:
    def calculate(self, request: VibratingFeederRequest) -> VibratingFeederResult:
        """Calculate vibrating feeder parameters"""
        deck_width = request.deck_width
        deck_length = request.deck_length
        amplitude = request.amplitude
        frequency = request.frequency
        bulk_density = request.bulk_density
        stroke_angle = request.stroke_angle

        # Calculate stroke length
        stroke_length = 2 * amplitude

        # Calculate conveying velocity (simplified formula)
        # Velocity is function of amplitude, frequency, and stroke angle
        conveying_velocity = (amplitude * frequency * 2 * math.pi * 
                            math.cos(math.radians(stroke_angle))) * 60  # ft/min

        # Calculate bed depth (assumed based on deck dimensions)
        bed_depth = min(deck_width * 0.1, 6)  # Max 6 inches

        # Calculate flow rate
        # Cross-sectional area × velocity × bulk density
        cross_section_area = (deck_width * bed_depth) / 144  # Convert to sq ft
        flow_rate_ft3_hr = cross_section_area * conveying_velocity * 60
        flow_rate_tons_hr = (flow_rate_ft3_hr * bulk_density) / 2000

        # Calculate power required (simplified)
        # Power is function of mass, acceleration, and efficiency
        acceleration = (2 * math.pi * frequency)**2 * amplitude / 12  # ft/s²
        material_mass = flow_rate_ft3_hr * bulk_density / 3600  # lb/s
        power_required = (material_mass * acceleration * conveying_velocity / 60) / 550  # HP

        return VibratingFeederResult(
            flow_rate_tons_hr=flow_rate_tons_hr,
            stroke_length=stroke_length,
            conveying_velocity=conveying_velocity,
            power_required=power_required
        )

    def create_performance_chart(self, request: VibratingFeederRequest, result: VibratingFeederResult):
        """Create performance chart showing flow rate vs frequency"""
        freq_range = list(range(10, 61, 5))
        flow_rates = []

        for freq in freq_range:
            temp_request = VibratingFeederRequest(
                deck_width=request.deck_width,
                deck_length=request.deck_length,
                amplitude=request.amplitude,
                frequency=freq,
                bulk_density=request.bulk_density,
                stroke_angle=request.stroke_angle
            )
            temp_result = self.calculate(temp_request)
            flow_rates.append(temp_result.flow_rate_tons_hr)

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=freq_range,
            y=flow_rates,
            mode='lines+markers',
            name='Flow Rate',
            line=dict(color='#1f77b4', width=2)
        ))

        # Highlight selected frequency
        fig.add_trace(go.Scatter(
            x=[request.frequency],
            y=[result.flow_rate_tons_hr],
            mode='markers',
            name='Selected',
            marker=dict(color='red', size=12)
        ))

        fig.update_layout(
            title='Vibrating Feeder Flow Rate vs Frequency',
            xaxis_title='Frequency (Hz)',
            yaxis_title='Flow Rate (tons/hr)',
            showlegend=True,
            height=400
        )

        return fig

    def get_recommendations(self, request: VibratingFeederRequest, result: VibratingFeederResult) -> list:
        """Generate recommendations based on calculation results"""
        recommendations = []
        
        # Frequency recommendations
        if request.frequency < 15:
            recommendations.append("Low frequency may cause uneven material flow.")
        elif request.frequency > 50:
            recommendations.append("High frequency increases wear and maintenance requirements.")
        
        # Amplitude considerations
        if request.amplitude < 0.05:
            recommendations.append("Low amplitude may not provide sufficient material movement.")
        elif request.amplitude > 0.3:
            recommendations.append("High amplitude may cause material spillage.")
        
        # Power requirements
        if result.power_required > 5:
            recommendations.append("High power requirement. Consider optimizing frequency and amplitude.")
        
        # Stroke angle optimization
        if request.stroke_angle < 20:
            recommendations.append("Low stroke angle reduces conveying efficiency.")
        elif request.stroke_angle > 50:
            recommendations.append("High stroke angle may cause material bounce.")
        
        return recommendations
