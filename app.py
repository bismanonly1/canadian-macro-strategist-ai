import streamlit as st
import pandas as pd

from src.boc_client import fetch_canadian_yields
from src.market_client import fetch_etf_prices, calculate_returns
from src.regime_engine import detect_canadian_regime
from src.allocation_engine import recommend_allocation
from src.explanation_engine import generate_explanation
from src.backtest_engine import (
    run_static_backtest,
    run_dynamic_regime_backtest,
    calculate_performance_metrics
)


st.set_page_config(
    page_title="Canadian Macro Strategist AI",
    layout="wide"
)

st.title("Canadian Macro Strategist AI Agent")
st.caption("A Canadian macro regime detection and portfolio allocation system.")

st.markdown("""
This app looks at Canadian bond-yield signals, detects the current macro environment,
recommends a portfolio allocation, and tests the strategy against a Canadian equity benchmark.
""")

backtest_type = st.selectbox(
    "Choose backtest type",
    ["Dynamic Regime Switching", "Static Current Allocation"]
)

start_date = st.date_input(
    "Select start date",
    value=pd.to_datetime("2020-01-01")
)

run_button = st.button("Run Macro Strategy Analysis")

if run_button:
    with st.spinner("Fetching Canadian macro data..."):
        yield_df = fetch_canadian_yields(start_date=str(start_date))

    with st.spinner("Detecting macro regime..."):
        regime_result = detect_canadian_regime(yield_df)
        allocation = recommend_allocation(regime_result["regime"])
        explanation = generate_explanation(regime_result, allocation)

    with st.spinner("Fetching Canadian ETF market data..."):
        price_df = fetch_etf_prices(start_date=str(start_date))
        returns_df = calculate_returns(price_df)

    with st.spinner("Running backtest..."):
        if backtest_type == "Dynamic Regime Switching":
            backtest_df = run_dynamic_regime_backtest(
                returns_df,
                yield_df
            )
        else:
            backtest_df = run_static_backtest(
                returns_df,
                allocation
            )

        metrics = calculate_performance_metrics(backtest_df)

    st.success("Analysis complete.")

    st.header("1. Current Canadian Macro Regime")

    st.subheader(regime_result["regime"])

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "2-Year Yield",
        f"{regime_result['latest_two_year_yield']:.2f}%"
    )

    col2.metric(
        "10-Year Yield",
        f"{regime_result['latest_ten_year_yield']:.2f}%"
    )

    col3.metric(
        "Yield Curve Inverted",
        str(regime_result["yield_curve_inverted"])
    )

    st.header("2. Recommended Portfolio Allocation")

    allocation_df = pd.DataFrame(
        allocation.items(),
        columns=["Asset Class", "Weight (%)"]
    )

    st.dataframe(allocation_df, use_container_width=True)

    st.bar_chart(
        allocation_df.set_index("Asset Class")
    )

    st.header("3. Backtest Performance")

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    metric_col1.metric(
        "Strategy Return",
        f"{metrics['strategy_total_return']:.2%}"
    )

    metric_col2.metric(
        "Benchmark Return",
        f"{metrics['benchmark_total_return']:.2%}"
    )

    metric_col3.metric(
        "Strategy Sharpe",
        f"{metrics['strategy_sharpe']:.2f}"
    )

    metric_col4.metric(
        "Strategy Max Drawdown",
        f"{metrics['strategy_max_drawdown']:.2%}"
    )

    st.subheader("Strategy vs Benchmark Growth")

    chart_df = backtest_df[
        ["strategy_equity_curve", "benchmark_equity_curve"]
    ].rename(
        columns={
            "strategy_equity_curve": "Macro Strategy",
            "benchmark_equity_curve": "Canadian Equity Benchmark"
        }
    )

    st.line_chart(chart_df)

    st.header("4. Simple Explanation")

    if metrics["strategy_total_return"] < metrics["benchmark_total_return"]:
        st.info(
            "The benchmark made more money, but the macro strategy may still be useful "
            "because it tries to reduce risk and protect capital."
        )

    if metrics["strategy_sharpe"] > metrics["benchmark_sharpe"]:
        st.success(
            "The macro strategy produced better risk-adjusted performance than the benchmark."
        )

    if metrics["strategy_max_drawdown"] > metrics["benchmark_max_drawdown"]:
        st.success(
            "The strategy had a smaller worst loss than the benchmark, meaning it protected downside better."
        )

    with st.expander("Full Macro Explanation"):
        st.text(explanation)

    if backtest_type == "Dynamic Regime Switching":
        st.header("5. Regime History")

        regime_counts = backtest_df["regime"].value_counts()

        st.dataframe(
            regime_counts.rename("Days").reset_index().rename(
                columns={"index": "Regime"}
            ),
            use_container_width=True
        )

        st.bar_chart(regime_counts)