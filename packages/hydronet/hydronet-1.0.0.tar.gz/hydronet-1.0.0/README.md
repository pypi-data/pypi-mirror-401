# HydroNet: Network-Based Early Warning System for Hydrological Collapse

## 📋 Overview
HydroNet is an early warning system for hydrological collapse based on multi-domain network analysis using 12 key indicators across climatic, hydrological, infrastructural, and socioeconomic domains. The system provides early warnings with a median lead time of 8.4 months before conventional indicators signal emergency.

## 🚀 Quick Start

### 1. Installation
```bash
# Clone the repository
git clone https://github.com/emerladcompass/HydroNet.git
cd HydroNet

# Install dependencies
pip install -r requirements-test.txt
```

2. Run Tests

```bash
# Test core functionality
python -m pytest tests/test_hydronet.py -v

# Or run all tests
make test-all
```

3. View Research Paper

```bash
# Open in browser (HTML version - recommended)
open hydronet.html

# Or view Markdown version
open hydronet.md
```

📊 Core Package Usage

A. Basic Prediction Example

```python
import numpy as np
from Core_Package.hydronet.extended.predictor import HydroPredictor

# Create sample data
data = {
    "precipitation": np.random.normal(0, 1, 100),
    "streamflow": np.random.normal(0, 1, 100),
    "groundwater_levels": np.random.normal(0, 1, 100),
    # ... add all 12 indicators
}

# Predict collapse risk
predictor = HydroPredictor(threshold=0.6)
result = predictor.predict_collapse_risk(data)

print(f"System Vulnerability Index: {result['svi']:.3f}")
print(f"Risk Level: {result['risk_level']}")
print(f"Warning: {result['warning']}")
```

B. Real-Time Monitoring

```python
from Core_Package.hydronet.extended.monitor import HydroMonitor

# Start monitoring a basin
monitor = HydroMonitor(
    basin_name="Colorado River Basin",
    update_interval=3600  # seconds
)

# Run monitoring for 24 hours
monitor.run_monitoring(hours=24)

# Generate report
report = monitor.generate_report()
print(report)
```

🖥️ Command Line Tools

Using Interactive CLI

```bash
cd CLI_Tools
python interactive_cli_extended.py
```

Basic CLI Commands

```bash
# Analyze data
python CLI_Tools/interactive_cli.py --analyze --data your_data.csv

# Generate report
python CLI_Tools/interactive_cli.py --report --format html

# Monitor basin
python CLI_Tools/interactive_cli.py --monitor --basin "Nile Basin"
```

🌐 Web Interface

Run Local Server

```bash
cd Web_Interfaces
python web_app.py

# Open browser at: http://localhost:5000
```

Web Interface Features:

· Interactive dashboard
· Network visualization
· Real-time updates
· Downloadable reports

🔧 Project Structure

```
HydroNet/
├── hydronet.md              # Complete research paper
├── hydronet.html           # HTML version
├── Core_Package/           # Core implementation
│   └── hydronet/
│       ├── __init__.py     # 12-parameter definitions
│       └── extended/       # Extended implementation
│           ├── hydro_metrics.py    # Network metrics
│           ├── predictor.py        # Collapse prediction
│           └── monitor.py          # Real-time monitoring
├── tests/                  # Test suite
│   └── test_hydronet.py   # Main tests
├── CLI_Tools/             # Command-line tools
├── Web_Interfaces/        # Web applications
├── Documentation/         # API documentation
└── manuscript/            # Organized manuscript
```

📈 The 12 Network Indicators

1. Climatic Domain:
   · Precipitation
   · Evapotranspiration
   · Atmospheric Pressure
2. Surface Water Domain:
   · Streamflow
   · Lake Levels
   · Reservoir Storage
3. Groundwater Domain:
   · Groundwater Levels
   · Groundwater Quality
4. Soil & Land Domain:
   · Soil Moisture
   · Land Subsidence
5. Human Impact Domain:
   · Water Extraction
   · Land Use Change

🔍 Interpreting Results

System Vulnerability Index (SVI)

· 0.0 - 0.4: Low risk
· 0.4 - 0.6: Medium risk
· 0.6 - 0.8: High risk
· 0.8 - 1.0: Critical (requires immediate intervention)

Alert Levels

· LOW: System stable
· HIGH: Increased monitoring needed
· CRITICAL: Immediate intervention required

🎯 Use Cases

1. For Researchers

```python
# Analyze historical data
from Core_Package.hydronet.extended.hydro_metrics import HydroMetrics

metrics = HydroMetrics()
network_density = metrics.network_density(adjacency_matrix)
transfer_entropy = metrics.transfer_entropy(source_data, target_data)
```

2. For Water Managers

```bash
# Monitor multiple basins
python CLI_Tools/basin_monitor.py --basins "Nile,Colorado,Indus"
```

3. For Developers

```bash
# Develop new features
git checkout -b feature/new-algorithm
# After development
make test-all  # Ensure all tests pass
```

📞 Support & Troubleshooting

Common Issues

```bash
# Issue: Circular import
# Solution: Reinstall requirements and run make clean

# Issue: Insufficient data
# Solution: Each indicator needs at least 30 data points
```

Getting Help

1. Open an Issue on GitHub
2. Check documentation in Documentation/
3. Review test files in tests/ for examples

📚 Additional Resources

Research Paper

· Complete: hydronet.md (13,700 words)
· Abstract: manuscript/sections/00_abstract.md
· Organized: manuscript/versions/concise_manuscript.md

Detailed Documentation

· Documentation/api_reference.md - API reference
· Documentation/extended_parameters.md - Extended parameters

Website

```
https://emerladcompass.github.io/HydroNet/
```

✅ Next Steps

1. Customize settings in _config.yml
2. Add your real data to the project
3. Adjust alert thresholds for your needs
4. Integrate with external data sources

📊 Performance Metrics

· Prediction Lead Time: 8.4 months (median)
· AUC Score: 0.876
· Sensitivity: 82.1%
· Specificity: 79.6%
· Parameters: 12 network indicators
· Paper Length: 13,700 words

🔗 Links

· GitHub Repository: https://github.com/emerladcompass/HydroNet
· Live Demo: https://emerladcompass.github.io/HydroNet/
· Research Paper: https://emerladcompass.github.io/HydroNet/hydronet.html

👤 Author

Samir Baladi
Emerald Compass Research
emerladcompass@gmail.com

📄 License

MIT License - See LICENSE file for details.

---

HydroNet is ready to use! 🚀

Start with python -m pytest tests/test_hydronet.py to verify everything works, then use the package to analyze your hydrological data.
