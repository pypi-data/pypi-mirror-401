# custom-pyod

High-performance outlier detection algorithms using Polars.

## Features

- **COPOD**: Copula-Based Outlier Detection
- **ECOD**: Empirical Cumulative Distribution Based Outlier Detection
- Built on Polars for high performance
- Compatible with scikit-learn API

## Installation

```bash
pip install custom-pyod
```

## Quick Start

```python
from custom_pyod.models import COPOD, ECOD
import polars as pl

# Load your data as a Polars DataFrame
df = pl.DataFrame({
    'feature1': [1, 2, 3, 100],
    'feature2': [1, 1, 1, 50]
})

# COPOD
copod = COPOD()
outlier_scores = copod.fit_predict(df)

# ECOD
ecod = ECOD()
outlier_scores = ecod.fit_predict(df)
```

## License

MIT License
