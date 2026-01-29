# Cercalia SDK for Python

The official, type-safe Python SDK for [Cercalia](https://www.cercalia.com/) web services. Built by [Nexus Geographics](https://www.nexusgeographics.com/), this SDK empowers you to build robust location-based applications with features like geocoding, routing, and POI search using modern Python practices.

[![Cercalia](https://img.shields.io/badge/Powered%20by-Cercalia-blue)](https://www.cercalia.com)
[![Nexus Geographics](https://img.shields.io/badge/Product%20of-Nexus%20Geographics-green)](https://www.nexusgeographics.com)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PyPI version](https://img.shields.io/pypi/v/cercalia-sdk.svg)](https://pypi.org/project/cercalia-sdk/)

## 🌟 About Cercalia

[**Cercalia**](https://www.cercalia.com/) is a comprehensive SaaS geospatial platform developed by [**Nexus Geographics**](https://www.nexusgeographics.com/), a leading company in geospatial technology and innovation. Cercalia provides enterprise-grade mapping, geocoding, routing, and location intelligence services, with exceptional coverage of European markets and advanced spatial analysis capabilities.

Trusted by leading enterprises across logistics, emergency services, fleet management, and smart city solutions, Cercalia delivers the precision and reliability that mission-critical applications demand.

### Why Choose Cercalia?

- **Global Coverage**: Based on TomTom content, enriched with OpenStreetMap data
- **European Leadership**: Unmatched data quality and coverage across all of Europe, with particular strength in Western, Central, and Southern regions—ideal for pan-European applications and businesses seeking reliable, up-to-date geospatial information
- **Live & Historical Traffic Data**: Global coverage of road incidents, congestion, closures, traffic-based ETAs, and routing with live or expected traffic
- **Enterprise-Ready**: Built for scale with high availability, performance SLAs, and dedicated support
- **Comprehensive Platform**: 12+ geospatial services accessible through modern, type-safe SDKs
- **Innovation Leader**: Powered by Nexus Geographics' 25+ years of GIS expertise

**Learn More:**
- 🌐 Official Website: [www.cercalia.com](https://www.cercalia.com)
- 📝 Sign Up: [clients.cercalia.com/register](https://clients.cercalia.com/register)
- 🏢 Nexus Geographics: [www.nexusgeographics.com](https://www.nexusgeographics.com)
- 🐦 Twitter: [@nexusgeographics](https://x.com/nexusgeographic)
- 💼 LinkedIn: [Nexus Geographics](https://www.linkedin.com/company/nexus-geographics/)

## ✨ Features

- **🎯 Type-Safe**: Fully typed with Pydantic models for excellent IDE support and data validation
- **🐍 Pythonic**: Clean, idiomatic API following PEP 8 conventions
- **📦 Modern Architecture**: Modular design with clear separation of concerns
- **🔄 Comprehensive Services**: Access 12+ geospatial services
- **🛡️ Resilient**: Built-in retry logic and robust error handling
- **🧪 Well-Tested**: Full test coverage with pytest (172 tests)

## 🚀 Installation

```bash
pip install cercalia-sdk
```

### From Source (Local Development)

If you want to contribute or run the examples locally, follow these steps to set up your environment:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/cercalia/cercalia-sdk-python.git
   cd cercalia-sdk-python
   ```

2. **Set up a virtual environment**:
   ```bash
   # Create the virtual environment
   python3 -m venv venv

   # Activate it (Linux/macOS)
   source venv/bin/activate

   # Activate it (Windows)
   # venv\Scripts\activate
   ```

3. **Install dependencies**:
   Using the provided `Makefile`:
   ```bash
   make install
   ```

## 🔑 Getting Started

### 1. Get Your API Key

Register for a free Cercalia account and obtain your API key:

👉 **[Register here](https://clients.cercalia.com/register)**

### 2. Quick Example

```python
from cercalia import GeocodingService, RoutingService, CercaliaConfig, Coordinate

# Configure the SDK
config = CercaliaConfig(api_key="YOUR_API_KEY_HERE")

# Geocode an address
geocoding = GeocodingService(config)
results = geocoding.geocode(
    street="Paseo de la Castellana, 1",
    locality="Madrid",
    country_code="ESP"
)

print(f"Found: {results[0].name}")
print(f"Coordinates: {results[0].coord.lat}, {results[0].coord.lng}")

# Calculate a route
routing = RoutingService(config)
route = routing.calculate_route(
    origin=results[0].coord,
    destination=Coordinate(lat=41.387015, lng=2.170047)  # Barcelona
)

print(f"Distance: {route.distance / 1000:.2f} km")
print(f"Duration: {route.duration // 60} minutes")
```

## 🛠️ Available Services

| Service | Description | Class |
|---------|-------------|-------|
| **Geocoding** | Convert addresses to geographic coordinates | `GeocodingService` |
| **Reverse Geocoding** | Get addresses from coordinates | `ReverseGeocodingService` |
| **Routing** | Calculate optimal routes with turn-by-turn directions | `RoutingService` |
| **Suggest** | Autocomplete and place search suggestions | `SuggestService` |
| **POI Search** | Find Points of Interest near locations | `PoiService` |
| **Isochrones** | Calculate reachability areas (drive time/distance) | `IsochroneService` |
| **Proximity** | Distance calculations and nearest neighbor search | `ProximityService` |
| **Geofencing** | Point-in-polygon and spatial boundary operations | `GeofencingService` |
| **Static Maps** | Generate static map images | `StaticMapsService` |
| **Snap to Road** | Match GPS traces to road network | `SnapToRoadService` |
| **Geoment** | Geographic element queries and geometries | `GeomentService` |

## 📚 Documentation

- **📖 SDK API Reference**: [docs.cercalia.com/sdk/docs/python/](https://docs.cercalia.com/sdk/docs/python/)
- **📘 Official Cercalia API Docs**: [docs.cercalia.com/docs/](https://docs.cercalia.com/docs/)
- **💡 Examples**: Browse the [`examples/`](./examples) directory for runnable code samples

## 🧪 Development

The project includes a `Makefile` for common development tasks:

```bash
# Install development dependencies
make install

# Run tests with coverage
make test

# Run linting (ruff and mypy)
make lint

# Format code
make format

# Build package distribution
make build

# Clean build artifacts
make clean
```

## 🤝 Support & Community

Need help or have questions?

- **Documentation**: [docs.cercalia.com](https://docs.cercalia.com)
- **Support Portal**: Available through your Cercalia dashboard
- **Issues**: [GitHub Issues](https://github.com/cercalia/cercalia-sdk-python/issues)

## 📄 License

This SDK is provided for use with Cercalia web services. Please refer to your Cercalia service agreement for terms of use.

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://www.nexusgeographics.com">Nexus Geographics</a></strong><br>
  <a href="https://www.cercalia.com">www.cercalia.com</a> • 
  <a href="https://x.com/nexusgeographic">Twitter</a> • 
  <a href="https://www.linkedin.com/company/nexus-geographics/">LinkedIn</a>
</p>
