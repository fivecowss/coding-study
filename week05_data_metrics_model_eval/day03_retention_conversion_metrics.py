import pandas as pd


def build_events() -> pd.DataFrame:
    """
    Each row is one event.
    Grain: one row = one user event.
    """
    return pd.DataFrame({
        "user_id": [1, 1, 1, 2, 2, 3, 4, 4, 5, 6, 6],
        "event_date": pd.to_datetime([
            "2026-07-01",
            "2026-07-02",
            "2026-07-04",
            "2026-07-01",
            "2026-07-03",
            "2026-07-02",
            "2026-07-03",
            "2026-07-04",
            "2026-07-04",
            "2026-07-01",
            "2026-07-02",
        ]),
        "event_type": [
            "visit",
            "visit",
            "purchase",
            "visit",
            "purchase",
            "visit",
            "visit",
            "purchase",
            "visit",
            "visit",
            "visit",
        ],
    })


def build_experiment_assignments() -> pd.DataFrame:
    """
    Each row is one user assignment.
    Grain: one row = one user in experiment.
    """
    return pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6],
        "treatment_group": ["control", "control", "treatment", "treatment", "control", "treatment"],
        "assigned_date": pd.to_datetime([
            "2026-07-01",
            "2026-07-01",
            "2026-07-02",
            "2026-07-03",
            "2026-07-04",
            "2026-07-01",
        ]),
    })


def main() -> None:
    events = build_events()
    assignments = build_experiment_assignments()

    print("\n=== Events ===")
    print(events)

    print("\n=== Experiment assignments ===")
    print(assignments)

    print("\n=== Grain checks ===")
    print("event rows:", len(events), "| unique users in events:", events["user_id"].nunique())
    print("assignment rows:", len(assignments), "| unique assigned users:", assignments["user_id"].nunique())

    # ------------------------------------------------------------------
    # TODO 1:
    # Find each user's first event date.
    #
    # Required columns:
    # - user_id
    # - first_event_date
    #
    # Hint:
    # groupby("user_id")["event_date"].min()
    # ------------------------------------------------------------------

    first_event = (
        events
        .groupby("user_id")["event_date"]
        .min()
        .reset_index()
        .rename(columns={"event_date": "first_event_date"})
    )

    print("\n=== First event date by user ===")
    print(first_event)

    # ------------------------------------------------------------------
    # TODO 2:
    # Compute days_since_first_event for each event.
    #
    # Required:
    # - Merge first_event back to events.
    # - Create days_since_first_event.
    #
    # Hint:
    # (event_date - first_event_date).dt.days
    # ------------------------------------------------------------------

    events_with_first = events.merge(
        first_event,
        on = "user_id",
        how = "left",
    )
    events_with_first["days_since_first_event"] = (
        events_with_first["event_date"] - events_with_first["first_event_date"]
    ).dt.days

    print("\n=== Events with days since first event ===")
    print(events_with_first)

    # ------------------------------------------------------------------
    # TODO 3:
    # Compute D1 retention.
    #
    # Definition:
    # A user is D1 retained if they have at least one event
    # exactly 1 day after their first event.
    #
    # Required output:
    # - one row per user
    # - d1_retained: 0/1
    #
    # Then compute overall D1 retention rate.
    # ------------------------------------------------------------------

    user_d1 = (
        events_with_first
        .groupby("user_id")["days_since_first_event"]
        .apply(lambda x:int(1 in set(x)))
        .reset_index()
        .rename(columns = {"days_since_first_event": "d1_retained"})
    )

    d1_retention_rate = user_d1["d1_retained"].mean()

    print("\n=== D1 retained by user ===")
    print(user_d1)

    print("\nD1 retention rate:", d1_retention_rate)

    # ------------------------------------------------------------------
    # TODO 4:
    # Compute whether each user converted.
    #
    # Definition:
    # converted = 1 if the user has at least one purchase event.
    #
    # Required output:
    # - user_id
    # - converted
    # ------------------------------------------------------------------

    user_conversion = (
        events
        .assign(is_purchase = lambda df: (df["event_type"] == "purchase").astype(int))
        .groupby("user_id")["is_purchase"]
        .max()
        .reset_index()
        .rename(columns = {"is_purchase": "converted"})
    )

    print("\n=== User-level conversion ===")
    print(user_conversion)

    # ------------------------------------------------------------------
    # TODO 5:
    # Join experiment assignments with user_conversion.
    #
    # Required:
    # - all assigned users should remain
    # - missing converted should become 0
    #
    # Then compute conversion rate by treatment_group.
    # ------------------------------------------------------------------

    experiment_outcomes = assignments.merge(
        user_conversion,
        on = "user_id",
        how = "left",
    )

    conversion_by_group = (
        experiment_outcomes
        .groupby("treatment_group")
        .agg(
            n_users = ("user_id", "nunique"),
            n_converted = ("converted", "sum"),
            conversion_rate = ("converted", "mean"),
        )
        .reset_index()
    )

    print("\n=== Experiment outcomes ===")
    print(experiment_outcomes)

    print("\n=== Conversion rate by group ===")
    print(conversion_by_group)


if __name__ == "__main__":
    main()


# ----------------------------------------------------------------------
# SAMPLE ANSWER
# ----------------------------------------------------------------------
#
# first_event = (
#     events
#     .groupby("user_id")["event_date"]
#     .min()
#     .reset_index()
#     .rename(columns={"event_date": "first_event_date"})
# )
#
# events_with_first = events.merge(
#     first_event,
#     on="user_id",
#     how="left",
# )
#
# events_with_first["days_since_first_event"] = (
#     events_with_first["event_date"] - events_with_first["first_event_date"]
# ).dt.days
#
# user_d1 = (
#     events_with_first
#     .groupby("user_id")["days_since_first_event"]
#     .apply(lambda x: int(1 in set(x)))
#     .reset_index()
#     .rename(columns={"days_since_first_event": "d1_retained"})
# )
#
# d1_retention_rate = user_d1["d1_retained"].mean()
#
# user_conversion = (
#     events
#     .assign(is_purchase=lambda df: (df["event_type"] == "purchase").astype(int))
#     .groupby("user_id")["is_purchase"]
#     .max()
#     .reset_index()
#     .rename(columns={"is_purchase": "converted"})
# )
#
# experiment_outcomes = assignments.merge(
#     user_conversion,
#     on="user_id",
#     how="left",
# )
#
# experiment_outcomes["converted"] = experiment_outcomes["converted"].fillna(0).astype(int)
#
# conversion_by_group = (
#     experiment_outcomes
#     .groupby("treatment_group")
#     .agg(
#         n_users=("user_id", "nunique"),
#         n_converted=("converted", "sum"),
#         conversion_rate=("converted", "mean"),
#     )
#     .reset_index()
# )