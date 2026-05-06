def recommend_allocation(regime: str) -> dict:
    allocations = {
        "Canadian Recession Risk": {
            "Canadian Equities": 25,
            "Short-Term Canadian Bonds": 35,
            "Gold": 15,
            "Cash": 25
        },
        "Canadian Tightening / Inflation Pressure": {
            "Canadian Equities": 35,
            "Short-Term Canadian Bonds": 25,
            "Gold": 25,
            "Cash": 15
        },
        "Canadian Easing / Growth Support": {
            "Canadian Equities": 65,
            "Short-Term Canadian Bonds": 20,
            "Gold": 5,
            "Cash": 10
        },
        "Canadian Mixed Macro Regime": {
            "Canadian Equities": 45,
            "Short-Term Canadian Bonds": 30,
            "Gold": 10,
            "Cash": 15
        }
    }

    return allocations.get(regime, allocations["Canadian Mixed Macro Regime"])