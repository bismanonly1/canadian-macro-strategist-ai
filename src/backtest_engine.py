import pandas as pd
import numpy as np


def run_static_backtest(returns_df: pd.DataFrame, allocation: dict) -> pd.DataFrame:
    weights = {
        "equities": allocation["Canadian Equities"] / 100,
        "short_bonds": allocation["Short-Term Canadian Bonds"] / 100,
        "gold": allocation["Gold"] / 100,
        "cash": allocation["Cash"] / 100
    }

    strategy_returns = (
        returns_df["equities"] * weights["equities"]
        + returns_df["short_bonds"] * weights["short_bonds"]
        + returns_df["gold"] * weights["gold"]
        + returns_df["cash"] * weights["cash"]
    )

    benchmark_returns = returns_df["equities"]

    result = pd.DataFrame({
        "strategy_returns": strategy_returns,
        "benchmark_returns": benchmark_returns
    })

    result["strategy_equity_curve"] = (1 + result["strategy_returns"]).cumprod()
    result["benchmark_equity_curve"] = (1 + result["benchmark_returns"]).cumprod()

    return result


def calculate_performance_metrics(backtest_df: pd.DataFrame) -> dict:
    strategy_total_return = backtest_df["strategy_equity_curve"].iloc[-1] - 1
    benchmark_total_return = backtest_df["benchmark_equity_curve"].iloc[-1] - 1

    strategy_volatility = backtest_df["strategy_returns"].std() * np.sqrt(252)
    benchmark_volatility = backtest_df["benchmark_returns"].std() * np.sqrt(252)

    strategy_sharpe = (
        backtest_df["strategy_returns"].mean() / backtest_df["strategy_returns"].std()
    ) * np.sqrt(252)

    benchmark_sharpe = (
        backtest_df["benchmark_returns"].mean() / backtest_df["benchmark_returns"].std()
    ) * np.sqrt(252)

    strategy_drawdown = (
        backtest_df["strategy_equity_curve"]
        / backtest_df["strategy_equity_curve"].cummax()
        - 1
    ).min()

    benchmark_drawdown = (
        backtest_df["benchmark_equity_curve"]
        / backtest_df["benchmark_equity_curve"].cummax()
        - 1
    ).min()

    return {
        "strategy_total_return": strategy_total_return,
        "benchmark_total_return": benchmark_total_return,
        "strategy_volatility": strategy_volatility,
        "benchmark_volatility": benchmark_volatility,
        "strategy_sharpe": strategy_sharpe,
        "benchmark_sharpe": benchmark_sharpe,
        "strategy_max_drawdown": strategy_drawdown,
        "benchmark_max_drawdown": benchmark_drawdown
    }


def print_performance_report(metrics: dict) -> None:
    print("\nBacktest Performance Report")
    print("-" * 40)

    print(f"Strategy Total Return: {metrics['strategy_total_return']:.2%}")
    print(f"Benchmark Total Return: {metrics['benchmark_total_return']:.2%}")

    print(f"Strategy Volatility: {metrics['strategy_volatility']:.2%}")
    print(f"Benchmark Volatility: {metrics['benchmark_volatility']:.2%}")

    print(f"Strategy Sharpe Ratio: {metrics['strategy_sharpe']:.2f}")
    print(f"Benchmark Sharpe Ratio: {metrics['benchmark_sharpe']:.2f}")

    print(f"Strategy Max Drawdown: {metrics['strategy_max_drawdown']:.2%}")
    print(f"Benchmark Max Drawdown: {metrics['benchmark_max_drawdown']:.2%}")