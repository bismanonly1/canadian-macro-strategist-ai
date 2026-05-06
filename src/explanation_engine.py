def generate_explanation(regime_result: dict, allocation: dict) -> str:
    regime = regime_result["regime"]

    explanation = f"""
Canadian Macro Regime Detected: {regime}

Signal Interpretation:
- 2-year yield rising: {regime_result["two_year_rising"]}
- 10-year yield rising: {regime_result["ten_year_rising"]}
- Yield curve inverted: {regime_result["yield_curve_inverted"]}

Latest Canadian Bond Yield Data:
- 2-year Government of Canada yield: {regime_result["latest_two_year_yield"]:.2f}%
- 10-year Government of Canada yield: {regime_result["latest_ten_year_yield"]:.2f}%

Recommended Portfolio Allocation:
"""

    for asset, weight in allocation.items():
        explanation += f"- {asset}: {weight}%\n"

    if regime == "Canadian Recession Risk":
        explanation += "\nRationale: The system prioritizes capital protection, liquidity, and defensive fixed income exposure."
    elif regime == "Canadian Tightening / Inflation Pressure":
        explanation += "\nRationale: The system reduces equity risk and increases inflation-sensitive assets like gold."
    elif regime == "Canadian Easing / Growth Support":
        explanation += "\nRationale: The system increases equity exposure because easing conditions may support risk assets."
    else:
        explanation += "\nRationale: The system uses a balanced allocation because macro signals are not clearly directional."

    return explanation