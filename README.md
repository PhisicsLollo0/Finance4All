# Finance4All
> **⚠️ Disclaimer: This project is under active development and is not ready for production use. Features, APIs, and results may change without notice. Use at your own risk.**

Finance4All is a Python-based toolkit for analyzing, backtesting, and visualizing financial portfolios. It provides tools for scraping historical price data, computing portfolio returns, evaluating risk metrics, and generating insightful plots.

## Features

- **Data Scraping:** Download and update historical price data for various assets.
- **Portfolio Analysis:** Load, prune, and analyze custom portfolios.
- **Return Computation:** Calculate annualized and rolling returns for different time windows.
- **Risk Metrics:** Compute geometric means, quantiles, and maximum drawdown.
- **Visualization:** Plot returns distributions, rolling returns, and drawdown charts.

## Project Structure

```
.
├── data/                # Raw and processed data files
├── notebooks/           # Jupyter notebooks for exploration and analysis
├── src/                 # Source code modules
│   ├── computations/    # Return and risk computations
│   ├── plots/           # Plotting utilities
│   ├── portfolio/       # Portfolio management and manipulation
│   ├── scraping/        # Data scraping utilities
│   └── utils/           # Utility functions
├── prices_scraping.ipynb# Main notebook for data scraping and analysis
├── README.md            # Project documentation
└── .env                 # Environment variables (not tracked)
```

## Getting Started

1. **Clone the repository:**
   ```sh
   git clone <repo-url>
   cd Finance4All
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the main notebook:**
   Open `prices_scraping.ipynb` in Jupyter or VS Code and execute the cells to scrape data, compute returns, and generate plots.

## Example Usage

```python
from src.scraping.get_data import *
from src.portfolio.data_manipulation import *
from src.computations.compute_returns import *

# Download and load data
get_data_info()
data = get_data_updated_2025()

# Analyze portfolios
portfolios = ['100_2factors', '80_20_2factors', ...]
for portfolio_name in portfolios:
    portfolio = load_portfolio(portfolio_name)
    data, weights = prune_data_portfolio(portfolio)
    results = compute_portfolio_returns_combined(data, weights, years=10)
```

## Notebooks

- **prices_scraping.ipynb:** Main workflow for scraping, analysis, and plotting.
- Additional notebooks in `notebooks/` for in-depth exploration.

## License

MIT License

---

For more details, see the code in [src/](src/) and the main workflow in [prices_scraping.ipynb](prices_scraping.ipynb).
```
