"""Validation utilities for engineering calculations"""

def validate_positive_number(value, field_name):
    """Validate that a value is a positive number"""
    if value <= 0:
        raise ValueError(f"{field_name} must be greater than 0")
    return True

def validate_range(value, min_val, max_val, field_name):
    """Validate that a value is within a specified range"""
    if value < min_val or value > max_val:
        raise ValueError(f"{field_name} must be between {min_val} and {max_val}")
    return True

def validate_bulk_density(value, use_imperial=False):
    """Validate bulk density based on unit system"""
    validate_positive_number(value, "Bulk density")
    
    if use_imperial:
        if value > 200:
            raise ValueError("Bulk density seems too high (>200 lb/ft³)")
    else:
        if value > 3203.7:  # 200 lb/ft³ converted to kg/m³
            raise ValueError("Bulk density seems too high (>3203.7 kg/m³)")
    
    return True

def validate_aperture_size(value):
    """Validate aperture size against standard sizes"""
    valid_sizes = [30, 50, 70, 90, 120, 150, 200, 250, 300, 350, 400]
    if value not in valid_sizes:
        raise ValueError(f"Aperture size must be one of: {', '.join(map(str, valid_sizes))}")
    return True

def validate_percentages_sum(percentage1, percentage2, field1_name, field2_name):
    """Validate that two percentages don't exceed 100%"""
    if percentage1 + percentage2 > 100:
        raise ValueError(f"{field1_name} and {field2_name} cannot exceed 100% combined")
    return True

def validate_material_properties(bulk_density, particle_size, angle_of_repose=None):
    """Validate material properties for consistency"""
    validate_positive_number(bulk_density, "Bulk density")
    validate_positive_number(particle_size, "Particle size")
    
    if angle_of_repose is not None:
        validate_range(angle_of_repose, 0, 90, "Angle of repose")
    
    # Check for realistic combinations
    if bulk_density > 150 and particle_size < 0.1:  # lb/ft³ and mm
        raise ValueError("High bulk density with very fine particles may cause flow issues")
    
    return True

def validate_flow_parameters(velocity, flow_rate, area=None):
    """Validate flow parameters for consistency"""
    validate_positive_number(velocity, "Velocity")
    validate_positive_number(flow_rate, "Flow rate")
    
    if area is not None:
        validate_positive_number(area, "Area")
        # Check if velocity and flow rate are consistent with area
        calculated_velocity = flow_rate / area
        if abs(calculated_velocity - velocity) > velocity * 0.1:  # 10% tolerance
            raise ValueError("Velocity and flow rate are not consistent with the given area")
    
    return True

def validate_power_calculation(power, efficiency=None):
    """Validate power calculation results"""
    validate_positive_number(power, "Power")
    
    if efficiency is not None:
        validate_range(efficiency, 0, 1, "Efficiency")
    
    # Check for unrealistic power values
    if power > 1000:  # HP or kW
        raise ValueError("Calculated power seems unrealistically high")
    
    return True

def validate_temperature_pressure(temperature, pressure):
    """Validate temperature and pressure combinations"""
    # Temperature in Celsius, pressure in kPa
    if temperature < -50 or temperature > 200:
        raise ValueError("Temperature outside reasonable operating range (-50 to 200°C)")
    
    if pressure < 50 or pressure > 1000:
        raise ValueError("Pressure outside reasonable operating range (50 to 1000 kPa)")
    
    return True
