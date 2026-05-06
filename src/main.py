from src.boc_client import fetch_canadian_yields
from src.regime_engine import detect_canadian_regime
from src.allocation_engine import recommend_allocation
from src.explanation_engine import generate_explanation


def main():
    print("Fetching Canadian macro data...")

    yield_df = fetch_canadian_yields(start_date="2020-01-01")
    yield_df.to_csv("data/canadian_yields.csv")

    regime_result = detect_canadian_regime(yield_df)
    allocation = recommend_allocation(regime_result["regime"])
    explanation = generate_explanation(regime_result, allocation)

    print(explanation)


if __name__ == "__main__":
    main()