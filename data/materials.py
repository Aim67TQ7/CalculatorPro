"""Material properties database for engineering calculations"""

MATERIAL_DATABASE = [
    {
        "name": "Wheat",
        "bulk_density_metric": 770.0,  # kg/m³
        "bulk_density_imperial": 48.1,  # lb/ft³
        "angle_of_repose": 25.0,  # degrees
        "particle_size": 5.0,  # mm
        "abrasiveness": "Low",
        "flowability": "Good",
        "category": "Agricultural"
    },
    {
        "name": "Corn (Whole Kernel)",
        "bulk_density_metric": 720.0,
        "bulk_density_imperial": 45.0,
        "angle_of_repose": 27.0,
        "particle_size": 8.0,
        "abrasiveness": "Low",
        "flowability": "Good",
        "category": "Agricultural"
    },
    {
        "name": "Soybeans",
        "bulk_density_metric": 750.0,
        "bulk_density_imperial": 47.0,
        "angle_of_repose": 26.0,
        "particle_size": 6.0,
        "abrasiveness": "Low",
        "flowability": "Good",
        "category": "Agricultural"
    },
    {
        "name": "Rice",
        "bulk_density_metric": 1540.0,
        "bulk_density_imperial": 96.0,
        "angle_of_repose": 33.0,
        "particle_size": 4.0,
        "abrasiveness": "Low",
        "flowability": "Fair",
        "category": "Agricultural"
    },
    {
        "name": "Sand (Dry)",
        "bulk_density_metric": 1600.0,
        "bulk_density_imperial": 100.0,
        "angle_of_repose": 35.0,
        "particle_size": 0.5,
        "abrasiveness": "High",
        "flowability": "Excellent",
        "category": "Minerals"
    },
    {
        "name": "Limestone (Crushed)",
        "bulk_density_metric": 1550.0,
        "bulk_density_imperial": 97.0,
        "angle_of_repose": 37.0,
        "particle_size": 12.0,
        "abrasiveness": "High",
        "flowability": "Good",
        "category": "Minerals"
    },
    {
        "name": "Coal (Bituminous)",
        "bulk_density_metric": 830.0,
        "bulk_density_imperial": 52.0,
        "angle_of_repose": 35.0,
        "particle_size": 25.0,
        "abrasiveness": "Medium",
        "flowability": "Fair",
        "category": "Minerals"
    },
    {
        "name": "Salt (Granular)",
        "bulk_density_metric": 1200.0,
        "bulk_density_imperial": 75.0,
        "angle_of_repose": 32.0,
        "particle_size": 2.0,
        "abrasiveness": "Medium",
        "flowability": "Good",
        "category": "Chemical"
    },
    {
        "name": "Sugar (Granulated)",
        "bulk_density_metric": 800.0,
        "bulk_density_imperial": 50.0,
        "angle_of_repose": 30.0,
        "particle_size": 0.8,
        "abrasiveness": "Low",
        "flowability": "Good",
        "category": "Food"
    },
    {
        "name": "Flour (Wheat)",
        "bulk_density_metric": 590.0,
        "bulk_density_imperial": 37.0,
        "angle_of_repose": 45.0,
        "particle_size": 0.05,
        "abrasiveness": "Low",
        "flowability": "Poor",
        "category": "Food"
    },
    {
        "name": "Cement (Portland)",
        "bulk_density_metric": 1500.0,
        "bulk_density_imperial": 94.0,
        "angle_of_repose": 40.0,
        "particle_size": 0.02,
        "abrasiveness": "High",
        "flowability": "Poor",
        "category": "Construction"
    },
    {
        "name": "Sawdust (Dry)",
        "bulk_density_metric": 210.0,
        "bulk_density_imperial": 13.0,
        "angle_of_repose": 45.0,
        "particle_size": 2.0,
        "abrasiveness": "Low",
        "flowability": "Fair",
        "category": "Biomass"
    },
    {
        "name": "Wood Pellets",
        "bulk_density_metric": 650.0,
        "bulk_density_imperial": 40.6,
        "angle_of_repose": 28.0,
        "particle_size": 6.0,
        "abrasiveness": "Low",
        "flowability": "Excellent",
        "category": "Biomass"
    },
    {
        "name": "Plastic Pellets (PE)",
        "bulk_density_metric": 560.0,
        "bulk_density_imperial": 35.0,
        "angle_of_repose": 25.0,
        "particle_size": 3.0,
        "abrasiveness": "Low",
        "flowability": "Excellent",
        "category": "Plastics"
    },
    {
        "name": "Iron Ore (Pellets)",
        "bulk_density_metric": 2000.0,
        "bulk_density_imperial": 125.0,
        "angle_of_repose": 30.0,
        "particle_size": 12.0,
        "abrasiveness": "High",
        "flowability": "Good",
        "category": "Metals"
    },
    {
        "name": "Aluminum Oxide",
        "bulk_density_metric": 1520.0,
        "bulk_density_imperial": 95.0,
        "angle_of_repose": 38.0,
        "particle_size": 0.1,
        "abrasiveness": "High",
        "flowability": "Fair",
        "category": "Chemical"
    },
    {
        "name": "Fertilizer (Granular)",
        "bulk_density_metric": 1100.0,
        "bulk_density_imperial": 69.0,
        "angle_of_repose": 30.0,
        "particle_size": 3.0,
        "abrasiveness": "Medium",
        "flowability": "Good",
        "category": "Agricultural"
    },
    {
        "name": "Coffee Beans",
        "bulk_density_metric": 430.0,
        "bulk_density_imperial": 27.0,
        "angle_of_repose": 28.0,
        "particle_size": 8.0,
        "abrasiveness": "Low",
        "flowability": "Good",
        "category": "Food"
    },
    {
        "name": "Cocoa Beans",
        "bulk_density_metric": 590.0,
        "bulk_density_imperial": 37.0,
        "angle_of_repose": 32.0,
        "particle_size": 12.0,
        "abrasiveness": "Low",
        "flowability": "Good",
        "category": "Food"
    },
    {
        "name": "Activated Carbon",
        "bulk_density_metric": 480.0,
        "bulk_density_imperial": 30.0,
        "angle_of_repose": 40.0,
        "particle_size": 1.0,
        "abrasiveness": "Medium",
        "flowability": "Fair",
        "category": "Chemical"
    }
]
