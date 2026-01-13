# Network Data Usage Monitor (IDU)

[![PyPI version](https://badge.fury.io/py/idu-network-monitor.svg)](https://badge.fury.io/py/idu-network-monitor)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A cross-platform Python tool to monitor and analyze internet data usage. Generates beautiful HTML reports with interactive charts showing network usage statistics over the last 60 days. Works on Windows, macOS, and Linux.

## Features

- 📊 **Real-time Network Statistics** - View current session download/upload data
- 📈 **60-Day Usage Analysis** - Estimated daily breakdown based on usage patterns
- 📉 **Interactive Charts** - Line charts and bar charts using Chart.js
- 📋 **Detailed Reports** - Daily breakdown with visual usage bars
- 🎨 **Beautiful HTML Reports** - Dark theme with modern UI design
- 📓 **Jupyter Notebook Support** - Interactive analysis with Plotly visualizations

## Installation

### From PyPI

```bash
pip install idu-network-monitor
```

### From Source

```bash
git clone https://github.com/yourusername/idu.git
cd idu
pip install -e .
```

## Quick Start

### Command Line

```bash
# Generate HTML report
idu-report

# Or run directly
python -m idu.report
```

### Python API

```python
from idu import generate_report

# Generate and open the HTML report
report_path = generate_report()
print(f"Report saved to: {report_path}")
```

### Jupyter Notebook

Open `examples/network_usage_analysis.ipynb` for an interactive analysis experience with:
- Per-interface statistics
- Interactive Plotly charts
- Weekly and day-of-week analysis

## Usage

### Generate Report

```bash
idu-report
```

This will:
1. Collect current network statistics using `psutil`
2. Generate estimated daily usage for the past 60 days
3. Create an HTML report with interactive charts
4. Open the report in your default browser

### Output

The tool generates:
- `network_usage_report.html` - Interactive HTML report

## Report Contents

### Current Session Statistics
- Downloaded data since last boot
- Uploaded data since last boot
- Session duration
- Total data transferred

### 60-Day Analysis
- Estimated total data usage
- Daily average usage
- Peak usage day
- Download vs Upload breakdown

### Visualizations
- **Line Chart**: Daily usage trend
- **Stacked Bar Chart**: Upload vs Download comparison
- **Usage Bars**: Visual comparison in the daily table

## Requirements

- Python 3.8+
- psutil >= 5.9.0

### Supported Platforms
- ✅ Windows
- ✅ macOS  
- ✅ Linux

## Dependencies

```
psutil>=5.9.0
```

For Jupyter Notebook analysis:
```
pandas>=1.3.0
plotly>=5.0.0
```

## How It Works

1. **Data Collection**: Uses `psutil` to get network I/O counters since system boot
2. **Estimation**: Calculates average daily usage from current session
3. **Variation**: Applies realistic daily/weekly variations to estimates
4. **Visualization**: Generates HTML with Chart.js for interactive charts

> **Note**: Most operating systems don't provide historical per-day network data. The daily breakdown is estimated based on current session usage patterns with realistic variations (weekends typically show higher usage).

## Project Structure

```
idu/
├── src/                           # Source code (package)
│   └── idu/
│       ├── __init__.py            # Package exports
│       ├── __main__.py            # CLI entry point
│       ├── report.py              # Main report generator
│       └── utils.py               # Utility functions
├── examples/                      # Usage examples
│   ├── standalone_report.py       # Standalone script example
│   └── network_usage_analysis.ipynb  # Jupyter notebook
├── docs/                          # Documentation
│   ├── architecture.tex           # Software architecture (LaTeX)
│   └── architecture.pdf           # Compiled documentation
├── tests/                         # Unit tests
│   └── test_report.py
├── dist/                          # Built packages
├── README.md
├── LICENSE
├── pyproject.toml
└── .gitignore
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Created with ❤️ for network usage monitoring

## Changelog

### v0.1.0 (2026-01-10)
- Initial release
- HTML report generation
- 60-day usage estimation
- Interactive charts with Chart.js
- Jupyter notebook for analysis
