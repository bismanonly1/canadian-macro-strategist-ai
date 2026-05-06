from src.boc_client import fetch_canadian_yields
from src.market_client import fetch_etf_prices, calculate_returns
from src.regime_engine import detect_canadian_regime
from src.allocation_engine import recommend_allocation
from src.explanation_engine import generate_explanation
from src.backtest_engine import (
    run_static_backtest,
    calculate_performance_metrics,
    print_performance_report
)


def main():
    print("Fetching Canadian macro data...")

    yield_df = fetch_canadian_yields(start_date="2020-01-01")
    yield_df.to_csv("data/canadian_yields.csv")

    regime_result = detect_canadian_regime(yield_df)
    allocation = recommend_allocation(regime_result["regime"])
    explanation = generate_explanation(regime_result, allocation)

    print(explanation)

    print("\nFetching Canadian ETF market data...")

    price_df = fetch_etf_prices(start_date="2020-01-01")
    price_df.to_csv("data/canadian_etf_prices.csv")

    returns_df = calculate_returns(price_df)
    returns_df.to_csv("data/canadian_etf_returns.csv")

    backtest_df = run_static_backtest(returns_df, allocation)
    backtest_df.to_csv("data/backtest_results.csv")

    metrics = calculate_performance_metrics(backtest_df)
    print_performance_report(metrics)


if __name__ == "__main__":
    main()