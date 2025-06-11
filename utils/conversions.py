"""Unit conversion utilities for engineering calculations"""

def convert_bulk_density_to_metric(value):
    """Convert bulk density from lb/ft³ to kg/m³."""
    return value * 16.0185  # 1 lb/ft³ = 16.0185 kg/m³

def convert_bulk_density_to_imperial(value):
    """Convert bulk density from kg/m³ to lb/ft³."""
    return value / 16.0185  # 1 kg/m³ = 0.062428 lb/ft³

def convert_flow_rate_volume_to_metric(value):
    """Convert volume flow rate from ft³/hr to m³/hr."""
    return value * 0.0283168  # 1 ft³/hr = 0.0283168 m³/hr

def convert_flow_rate_volume_to_imperial(value):
    """Convert volume flow rate from m³/hr to ft³/hr."""
    return value / 0.0283168

def convert_flow_rate_mass_to_metric(value):
    """Convert mass flow rate from lb/hr to kg/hr."""
    return value * 0.453592  # 1 lb/hr = 0.453592 kg/hr

def convert_flow_rate_mass_to_imperial(value):
    """Convert mass flow rate from kg/hr to lb/hr."""
    return value / 0.453592

def convert_pressure_to_metric(value):
    """Convert pressure from psi to Pa."""
    return value * 6894.76  # 1 psi = 6894.76 Pa

def convert_pressure_to_imperial(value):
    """Convert pressure from Pa to psi."""
    return value / 6894.76

def convert_power_to_metric(value):
    """Convert power from HP to kW."""
    return value * 0.746  # 1 HP = 0.746 kW

def convert_power_to_imperial(value):
    """Convert power from kW to HP."""
    return value / 0.746

def convert_temperature_to_celsius(fahrenheit):
    """Convert temperature from Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5/9

def convert_temperature_to_fahrenheit(celsius):
    """Convert temperature from Celsius to Fahrenheit."""
    return celsius * 9/5 + 32

def convert_length_to_metric(value):
    """Convert length from feet to meters."""
    return value * 0.3048  # 1 ft = 0.3048 m

def convert_length_to_imperial(value):
    """Convert length from meters to feet."""
    return value / 0.3048

def convert_area_to_metric(value):
    """Convert area from sq ft to sq m."""
    return value * 0.092903  # 1 sq ft = 0.092903 sq m

def convert_area_to_imperial(value):
    """Convert area from sq m to sq ft."""
    return value / 0.092903
