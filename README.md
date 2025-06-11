# Engineering Calculators API

A comprehensive FastAPI backend providing specialized engineering calculators for conveyor and separation equipment design with validation, visual outputs, and equipment recommendations.

## Features

- **13 Specialized Calculators** covering all major equipment types
- **Request/Response Validation** using Pydantic models
- **Visual Chart Generation** using Plotly for performance analysis
- **Material Properties Database** with 20+ common materials
- **Unit Conversion Utilities** supporting metric and imperial units
- **Equipment Recommendations** based on calculation results
- **Interactive API Documentation** available at `/docs`

## Available Calculators

### Flow Control
- **Gravity Flow Calculator**: Calculate gravity flow rates based on aperture size and bulk density
- **Column Velocity Calculator**: Calculate material velocity and flow rates in vertical columns

### Conveyor Systems
- **Belt Horsepower Calculator**: Calculate power requirements for belt conveyor systems
- **Screw Conveyor Calculator**: Calculate capacity, torque, and power requirements
- **Pneumatic Conveying Calculator**: Calculate air requirements and pressure drop

### Separation Systems
- **Magnetic Separator Calculator**: Calculate magnetic field strength and separation efficiency
- **Air Classifier Calculator**: Calculate air velocity and particle separation parameters
- **Screen Sizing Calculator**: Calculate mesh size, capacity, and efficiency
- **Cyclone Separator Calculator**: Calculate cut size, pressure drop, and efficiency

### Material Handling
- **Spout Requirements Calculator**: Determine optimal spout sizing for material discharge
- **Drag Slide Calculator**: Calculate drag slide dimensions with/without magnetic components
- **Vibrating Feeder Calculator**: Calculate amplitude, frequency, and flow rate
- **Material Handling Calculator**: Calculate throughput and residence time

## API Endpoints

- `GET /` - API information
- `GET /calculators` - List all available calculators
- `GET /materials` - List material properties database
- `POST /calculators/{calculator-name}` - Individual calculator endpoints
- `GET /docs` - Interactive API documentation

## Deployment

### Railway Deployment

1. Connect your repository to Railway
2. The application will automatically deploy using the included configuration files
3. Environment variables are automatically handled
4. Access your deployed API at the provided Railway URL

### Local Development

```bash
python main.py
```

The server will start on `http://localhost:5000`

## Usage Example

```python
import requests

# Get list of calculators
response = requests.get("https://your-app.railway.app/calculators")
calculators = response.json()

# Calculate gravity flow
data = {
    "aperture_size_mm": 150,
    "bulk_density": 50.0,
    "use_imperial": True
}
response = requests.post("https://your-app.railway.app/calculators/gravity-flow", json=data)
result = response.json()
```

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Plotly**: Interactive charts and visualizations
- **Pandas/NumPy**: Data manipulation and numerical calculations
- **Uvicorn**: ASGI server for production deployment