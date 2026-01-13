# Research Trends Scopus

[![PyPI version](https://badge.fury.io/py/research-trends-scopus.svg)](https://badge.fury.io/py/research-trends-scopus)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation Status](https://readthedocs.org/projects/research-trends-scopus/badge/?version=latest)](https://research-trends-scopus.readthedocs.io/en/latest/?badge=latest)

A comprehensive Python package to retrieve research data from the Scopus API, analyze publication trends, and generate interactive dashboards with actionable recommendations for research exploration.

## 🚀 Features

- **Data Retrieval**: Fetch research publications from Scopus API with advanced query support
- **Trend Analysis**: Analyze publication trends over time, by author, institution, and topic
- **Network Analysis**: Visualize collaboration networks and citation patterns
- **Topic Modeling**: Discover emerging research themes using NLP techniques
- **Interactive Dashboard**: Generate beautiful dashboards using Plotly and Dash
- **Smart Recommendations**: Get AI-powered suggestions for research areas to explore
- **Caching**: Built-in caching to minimize API calls and improve performance
- **Export**: Export data and visualizations in multiple formats

## 📦 Installation

### From PyPI

```bash
pip install research-trends-scopus
```

### With optional dependencies

```bash
# For development
pip install research-trends-scopus[dev]

# For documentation
pip install research-trends-scopus[docs]

# For Jupyter notebook support
pip install research-trends-scopus[notebook]

# Install all optional dependencies
pip install research-trends-scopus[all]
```

### From source

```bash
git clone https://github.com/research-trends/research-trends-scopus.git
cd research-trends-scopus
pip install -e ".[all]"
```

## ⚙️ Configuration

### Setting up Scopus API Key

1. Register for a Scopus API key at [Elsevier Developer Portal](https://dev.elsevier.com/)

2. Set your API key using one of these methods:

**Environment Variable:**
```bash
export SCOPUS_API_KEY="your-api-key-here"
```

**`.env` file:**
```
SCOPUS_API_KEY=your-api-key-here
```

**Configuration file (`~/.research_trends/config.yaml`):**
```yaml
scopus:
  api_key: your-api-key-here
  institution_token: optional-inst-token
```

## 🎯 Quick Start

### Python API

```python
from research_trends import ScopusClient, TrendAnalyzer, Dashboard

# Initialize the client
client = ScopusClient()

# Search for publications
publications = client.search(
    query="machine learning healthcare",
    start_year=2020,
    end_year=2025,
    max_results=1000
)

# Analyze trends
analyzer = TrendAnalyzer(publications)
trends = analyzer.analyze()

# Get recommendations
recommendations = analyzer.get_recommendations()

# Launch interactive dashboard
dashboard = Dashboard(analyzer)
dashboard.run(port=8050)
```

### Command Line Interface

```bash
# Search and analyze
research-trends search "artificial intelligence" --years 2020-2025 --output results.json

# Generate dashboard
research-trends dashboard results.json --port 8050

# Get recommendations
research-trends recommend results.json --top 10
```

## 📊 Dashboard Features

The interactive dashboard includes:

- **Publication Timeline**: Track publication volume over time
- **Author Analysis**: Identify top authors and their productivity
- **Institution Rankings**: Compare research output by institution
- **Geographic Distribution**: World map of research activity
- **Keyword Trends**: Track emerging keywords and topics
- **Citation Analysis**: Analyze citation patterns and impact
- **Collaboration Network**: Interactive network visualization
- **Topic Clusters**: Discover research themes and clusters

## 📈 Analysis Capabilities

### Trend Analysis
- Publication count trends
- Citation trends
- Author productivity trends
- Keyword emergence patterns

### Network Analysis
- Co-authorship networks
- Citation networks
- Institutional collaboration networks

### Topic Modeling
- Keyword extraction
- Topic clustering
- Emerging topic detection

### Recommendations
- Underexplored research areas
- Potential collaboration opportunities
- High-impact journals for publication
- Trending research directions

## 📚 Documentation

Full documentation is available at [https://research-trends-scopus.readthedocs.io](https://research-trends-scopus.readthedocs.io)

## 🧪 Examples

Check out the [examples](./examples) directory for:

- Jupyter notebooks with step-by-step tutorials
- Sample analyses for different research domains
- Dashboard customization examples

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on:

- Code of conduct
- Development setup
- Submitting pull requests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Elsevier](https://www.elsevier.com/) for the Scopus API
- The open-source Python community

## 📬 Contact

- Issues: [GitHub Issues](https://github.com/research-trends/research-trends-scopus/issues)
- Email: research-trends@example.com
