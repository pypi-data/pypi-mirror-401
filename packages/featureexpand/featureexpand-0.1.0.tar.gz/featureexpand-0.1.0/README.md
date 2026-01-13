# FeatureExpand

[![PyPI version](https://badge.fury.io/py/featureexpand.svg)](https://badge.fury.io/py/featureexpand)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Documentation Status](https://readthedocs.org/projects/featureexpand/badge/?version=latest)](https://featureexpand.readthedocs.io/en/latest/?badge=latest)

**FeatureExpand** is a powerful Python library designed to enhance your datasets through automatic feature engineering using logical formula simplification. Whether you're working on machine learning, data analysis, or any data-driven application, FeatureExpand helps you extract maximum value from your data by generating optimized boolean and continuous features.

## ✨ Features

- **Automatic Feature Engineering**: Generates new features using logical formulas optimized by the Exactor API
- **Scikit-learn Compatible**: Fully compatible with scikit-learn pipelines and transformers
- **Boolean & Continuous Features**: Supports both boolean logic features and continuous relaxations
- **Model Booster**: `LinearModelBooster` automatically selects the best model among linear, polynomial, and logic-guided regression
- **Smart Caching**: Cached API calls for improved performance
- **Flexible Configuration**: Customizable precision, depth, and feature generation strategies

## 🚀 Quick Start

### Installation

```bash
pip install featureexpand
```

### Basic Usage

```python
import numpy as np
import pandas as pd
from featureexpand import FeatureExpander, LinearModelBooster
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

# Create sample data
X = pd.DataFrame({
    'feature1': np.random.rand(100),
    'feature2': np.random.rand(100),
})
y = (X['feature1'] > 0.5) & (X['feature2'] < 0.5)  # Boolean logic target

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Use FeatureExpander
expander = FeatureExpander(
    token="your_exactor_api_token",  # Get from https://www.booloptimizer.com
    deep=2,  # Bits per feature
    environment="PROD"
)

# Fit and transform
X_train_expanded = expander.fit_transform(X_train, y_train)
X_test_expanded = expander.transform(X_test)

print(f"Original features: {X_train.shape[1]}")
print(f"Expanded features: {X_train_expanded.shape[1]}")
print(f"Generated formula: {expander.formula_string_}")
```

### Using LinearModelBooster

```python
from featureexpand import LinearModelBooster

# Automatically selects best model (Linear, Polynomial, or Logic-Guided)
booster = LinearModelBooster(
    token="your_exactor_api_token",
    poly_degrees=[2, 3],
    logic_depths=[1, 2],
    cv=5,
    scoring='r2'
)

# Fit and predict
booster.fit(X_train, y_train)
y_pred = booster.predict(X_test)

# View results
booster.summary()
print(f"Best model: {booster.best_model_name_}")
print(f"Best score: {booster.best_score_:.4f}")
```

## 📚 Documentation

For comprehensive documentation, including tutorials, API reference, and examples, visit:
- **Documentation**: [https://featureexpand.readthedocs.io](https://featureexpand.readthedocs.io)
- **Examples**: See the `examples/` directory in the repository

## 🔑 API Token

FeatureExpand uses the Exactor API for boolean formula optimization. You can:

1. Get a free token at [https://www.booloptimizer.com](https://www.booloptimizer.com)
2. Set it as an environment variable: `export EXACTOR_API_TOKEN=your_token`
3. Pass it directly: `FeatureExpander(token="your_token")`

## 💡 Use Cases

- **Machine Learning**: Enhance model performance with engineered features
- **Binary Classification**: Extract logical patterns from data
- **Feature Discovery**: Automatically discover feature interactions
- **Model Interpretation**: Understand data relationships through boolean formulas
- **Trading Signals**: Generate forex/stock trading signals (see `examples/forex/`)

## 🛠️ Requirements

- Python >= 3.8
- NumPy >= 1.19.0
- Pandas >= 1.1.0
- Scikit-learn >= 0.24.0
- Requests >= 2.25.0

## 📦 What's Included

- **`FeatureExpander`**: Core transformer for automatic feature generation
- **`LinearModelBooster`**: Automatic model selection with feature expansion
- **Neural utilities**: Neural network guidance for feature engineering
- **Utility functions**: Encoding, formula conversion, and migration tools

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Powered by the [Exactor API](https://www.booloptimizer.com) for boolean formula optimization
- Built with [Scikit-learn](https://scikit-learn.org/)
- Inspired by research in boolean function minimization and automatic feature engineering

## 📞 Contact

- **Author**: Juan Carlos Lopez Gonzalez
- **Email**: jlopez1967@gmail.com
- **GitHub**: [https://github.com/jlopezCell/featureexpand](https://github.com/jlopezCell/featureexpand)
- **Issues**: [https://github.com/jlopezCell/featureexpand/issues](https://github.com/jlopezCell/featureexpand/issues)

---

**Made with ❤️ for the ML community**
