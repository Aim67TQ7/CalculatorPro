from models.requests import MaterialHandlingRequest
from models.responses import MaterialHandlingResult

class MaterialHandlingCalculator:
    def calculate(self, request: MaterialHandlingRequest) -> MaterialHandlingResult:
        """Calculate material handling parameters"""
        throughput = request.throughput
        equipment_length = request.equipment_length
        equipment_width = request.equipment_width
        material_velocity = request.material_velocity
        bulk_density = request.bulk_density

        # Calculate residence time
        # Residence time = Equipment Volume / Volumetric Flow Rate
        equipment_volume = equipment_length * equipment_width * 2  # Assume 2 ft depth
        volumetric_flow_rate = (throughput * 2000) / bulk_density / 3600  # ft³/s
        residence_time = equipment_volume / volumetric_flow_rate  # seconds

        # Calculate bed depth
        # Based on cross-sectional area and flow rate
        cross_sectional_area = equipment_width * 2  # ft²
        bed_depth = volumetric_flow_rate / (equipment_width * material_velocity)

        # Calculate mass flow rate
        mass_flow_rate = throughput * 2000  # lb/hr

        # Calculate volumetric efficiency
        # Ratio of actual to theoretical capacity
        theoretical_capacity = equipment_length * equipment_width * 2 * material_velocity * bulk_density * 3600 / 2000
        volumetric_efficiency = min(throughput / theoretical_capacity, 1.0) if theoretical_capacity > 0 else 0

        return MaterialHandlingResult(
            residence_time=residence_time,
            bed_depth=bed_depth,
            mass_flow_rate=mass_flow_rate,
            volumetric_efficiency=volumetric_efficiency
        )

    def get_recommendations(self, request: MaterialHandlingRequest, result: MaterialHandlingResult) -> list:
        """Generate recommendations"""
        recommendations = []
        
        # Residence time recommendations
        if result.residence_time < 30:
            recommendations.append("Short residence time may not allow proper material processing.")
        elif result.residence_time > 300:
            recommendations.append("Long residence time may cause material degradation or contamination.")
        
        # Bed depth considerations
        if result.bed_depth < 1:
            recommendations.append("Shallow bed depth may cause uneven flow distribution.")
        elif result.bed_depth > 6:
            recommendations.append("Deep bed depth may cause compaction and flow problems.")
        
        # Velocity recommendations
        if request.material_velocity < 0.5:
            recommendations.append("Low material velocity may cause bridging or stagnation.")
        elif request.material_velocity > 5:
            recommendations.append("High material velocity may cause excessive wear and product degradation.")
        
        # Efficiency considerations
        if result.volumetric_efficiency < 0.6:
            recommendations.append("Low volumetric efficiency. Consider optimizing equipment dimensions or operating conditions.")
        
        # Equipment sizing
        aspect_ratio = request.equipment_length / request.equipment_width
        if aspect_ratio < 2:
            recommendations.append("Short equipment may not provide adequate processing time.")
        elif aspect_ratio > 10:
            recommendations.append("Long equipment may cause uneven residence time distribution.")
        
        return recommendations
