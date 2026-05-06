def detect_canadian_regime_from_window(yield_window):
    clean_df = yield_window.dropna()

    if len(clean_df) < 60:
        return "Canadian Mixed Macro Regime"

    latest = clean_df.iloc[-1]
    previous = clean_df.iloc[-60]

    two_year_rising = latest["two_year_yield"] > previous["two_year_yield"]
    ten_year_rising = latest["ten_year_yield"] > previous["ten_year_yield"]
    yield_curve_inverted = latest["two_year_yield"] > latest["ten_year_yield"]

    if yield_curve_inverted and two_year_rising:
        return "Canadian Recession Risk"
    elif two_year_rising and ten_year_rising:
        return "Canadian Tightening / Inflation Pressure"
    elif not two_year_rising and not ten_year_rising:
        return "Canadian Easing / Growth Support"
    else:
        return "Canadian Mixed Macro Regime"


def detect_canadian_regime(yield_df):
    clean_df = yield_df.dropna()

    latest = clean_df.iloc[-1]
    previous = clean_df.iloc[-60]

    two_year_rising = latest["two_year_yield"] > previous["two_year_yield"]
    ten_year_rising = latest["ten_year_yield"] > previous["ten_year_yield"]
    yield_curve_inverted = latest["two_year_yield"] > latest["ten_year_yield"]

    if yield_curve_inverted and two_year_rising:
        regime = "Canadian Recession Risk"
    elif two_year_rising and ten_year_rising:
        regime = "Canadian Tightening / Inflation Pressure"
    elif not two_year_rising and not ten_year_rising:
        regime = "Canadian Easing / Growth Support"
    else:
        regime = "Canadian Mixed Macro Regime"

    return {
        "regime": regime,
        "two_year_rising": two_year_rising,
        "ten_year_rising": ten_year_rising,
        "yield_curve_inverted": yield_curve_inverted,
        "latest_two_year_yield": latest["two_year_yield"],
        "latest_ten_year_yield": latest["ten_year_yield"]
    }