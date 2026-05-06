from src.boc_client import fetch_canadian_yields
from src.market_client import fetch_etf_prices, calculate_returns
from src.regime_engine import detect_canadian_regime
from src.allocation_engine import recommend_allocation
from src.explanation_engine import generate_explanation
from src.backtest_engine import (
    run_static_backtest,
    calculate_performance_metrics
)


def print_macro_strategy_report(
    explanation: str,
    metrics: dict
) -> None:

    print("\n" + "=" * 70)
    print("CANADIAN MACRO STRATEGIST AI REPORT")
    print("=" * 70)

    print("\nMACRO REGIME ANALYSIS")
    print("-" * 70)

    print(explanation)

    print("\nBACKTEST PERFORMANCE ANALYSIS")
    print("-" * 70)

    print(f"Strategy Total Return: {metrics['strategy_total_return']:.2%}")
    print(f"Benchmark Total Return: {metrics['benchmark_total_return']:.2%}")

    print()

    print(f"Strategy Volatility: {metrics['strategy_volatility']:.2%}")
    print(f"Benchmark Volatility: {metrics['benchmark_volatility']:.2%}")

    print()

    print(f"Strategy Sharpe Ratio: {metrics['strategy_sharpe']:.2f}")
    print(f"Benchmark Sharpe Ratio: {metrics['benchmark_sharpe']:.2f}")

    print()

    print(f"Strategy Max Drawdown: {metrics['strategy_max_drawdown']:.2%}")
    print(f"Benchmark Max Drawdown: {metrics['benchmark_max_drawdown']:.2%}")

    print("\nSTRATEGY INTERPRETATION")
    print("-" * 70)

    if metrics["strategy_sharpe"] > metrics["benchmark_sharpe"]:
        print(
            "The macro strategy generated superior risk-adjusted returns "
            "compared to the benchmark."
        )
    else:
        print(
            "The benchmark generated superior risk-adjusted returns "
            "compared to the macro strategy."
        )

    if metrics["strategy_max_drawdown"] > metrics["benchmark_max_drawdown"]:
        print(
            "The strategy experienced smaller downside losses during stress periods."
        )

    print(
        "\nThe current system prioritizes capital preservation and "
        "risk-adjusted allocation rather than maximizing upside during bull markets."
    )

    print("\n" + "=" * 70)


def main():
    print("Fetching Canadian macro data...")

    yield_df = fetch_canadian_yields(start_date="2020-01-01")
    yield_df.to_csv("data/canadian_yields.csv")

    regime_result = detect_canadian_regime(yield_df)

    allocation = recommend_allocation(regime_result["regime"])

    explanation = generate_explanation(
        regime_result,
        allocation
    )

    print("\nFetching Canadian ETF market data...")

    price_df = fetch_etf_prices(start_date="2020-01-01")
    price_df.to_csv("data/canadian_etf_prices.csv")

    returns_df = calculate_returns(price_df)
    returns_df.to_csv("data/canadian_etf_returns.csv")

    backtest_df = run_static_backtest(
        returns_df,
        allocation
    )

    backtest_df.to_csv("data/backtest_results.csv")

    metrics = calculate_performance_metrics(backtest_df)

    print_macro_strategy_report(
        explanation,
        metrics
    )


if __name__ == "__main__":
    main()