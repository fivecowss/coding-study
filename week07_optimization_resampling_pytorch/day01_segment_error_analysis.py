from typing import List, Dict, Any

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)


def summarize_by_group(
    results: pd.DataFrame,
    group_col: str,
) -> pd.DataFrame:
    """
    Compute classification metrics separately for each group.
    """

    # TODO: Validate that the required columns exist.
    required_columns = {
        group_col,
        "y_true",
        "y_pred",
    }

    # TODO: Create an empty list for group summaries.
    missing_columns = required_columns - set(results.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )
    summaries = []

    # TODO: Group the DataFrame using group_col.
    for group_value, group_frame in results.groupby( 
        group_col,
        dropna = False,
        sort = True,
    ):
        y_true = group_frame["y_true"]
        y_pred = group_frame["y_pred"] 

        # TODO: Compute sample size.
        summaries.append({
            group_col: group_value,
            "n": len(group_frame),
            "positive_rate": y_true.mean(),
            "predicted_positive_rate": y_pred.mean(),
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(
                y_true,
                y_pred,
                zero_division = 0,
            ),
            "recall": recall_score(
                y_true,
                y_pred,
                zero_division = 0,
            ),
            "f1": f1_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
        })
        
    return pd.DataFrame(summaries)


def build_example_data() -> pd.DataFrame:
    data: Dict[str, List[Any]] = {
        "segment": [
            "A", "A", "A", "A",
            "B", "B", "B", "B",
            "C", "C",
        ],
        "y_true": [
            1, 1, 0, 0,
            1, 1, 1, 0,
            0, 0,
        ],
        "y_pred": [
            1, 0, 1, 0,
            1, 1, 0, 0,
            0, 0,
        ],
    }

    return pd.DataFrame(data)


def main() -> None:
    results = build_example_data()

    print("Input data:")
    print(results)

    summary = summarize_by_group(
        results=results,
        group_col="segment",
    )

    print("\nSegment summary:")
    print(summary)


if __name__ == "__main__":
    main()