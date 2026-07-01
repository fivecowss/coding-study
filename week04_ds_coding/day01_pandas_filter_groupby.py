
import pandas as pd


def make_users_df() -> pd.DataFrame:
    return pd.DataFrame({
        "user_id": [1, 2, 3, 4, 5, 6, 7, 8],
        "country": ["US", "US", "KR", "KR", "US", "KR", "CA", "CA"],
        "device": ["mobile", "desktop", "mobile", "desktop", "mobile", "mobile", "desktop", "mobile"],
        "revenue": [100, 200, 150, 80, 50, 120, 300, 40],
        "active": [True, True, False, True, False, True, True, False],
        "days_since_signup": [3, 20, 7, 30, 2, 10, 15, 1],
    })


def filter_active_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 1:
    Return only active users.

    Hint:
    - Boolean filtering:
        df[df["active"]]
    - Do not use a for-loop.
    """
    # TODO: return active users only
    return df[df["active"]]


def filter_high_value_recent_users(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 2:
    Return users who satisfy both:
    - revenue >= 100
    - days_since_signup <= 10

    Hint:
    - In pandas, use `&`, not `and`.
    - Each condition must be wrapped in parentheses.
        df[(condition1) & (condition2)]
    """
    # TODO: return high-value recent users
    return df[(df["revenue"] >= 100) & (df["days_since_signup"] <= 10)]


def select_user_country_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 3:
    Return only these columns:
    - user_id
    - country
    - revenue

    Hint:
        df[["col1", "col2"]]
    """
    # TODO: return selected columns
    return df[df.columns.intersection(["user_id", "country", "revenue"])]


def add_revenue_per_day(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 4:
    Add a new column:
        revenue_per_day = revenue / days_since_signup

    Hint:
    - Use .assign(...) if possible.
    - This should return a new DataFrame, not modify in-place.
    """
    # TODO: return DataFrame with revenue_per_day column
    return df.assign(revenue_per_day = df["revenue"] / df["days_since_signup"])


def summarize_revenue_by_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 5:
    For each country, compute:
    - total_revenue
    - avg_revenue
    - n_users

    Then sort by total_revenue descending.

    Hint:
        (
            df.groupby("country")
              .agg(
                  total_revenue=("revenue", "sum"),
                  avg_revenue=("revenue", "mean"),
                  n_users=("user_id", "count"),
              )
              .reset_index()
              .sort_values(...)
        )
    """
    # TODO: return country-level summary
    return (
        df.groupby("country")
        .agg(
            total_revenue = ("revenue", "sum"),
            avg_revenue = ("revenue", "mean"),
            n_users = ("user_id", "count"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending = False)
    )


def summarize_active_rate_by_device(df: pd.DataFrame) -> pd.DataFrame:
    """
    Task 6:
    For each device, compute:
    - n_users
    - active_rate

    """
    # TODO: return device-level active rate
    return (
        df.groupby("device")
        .agg(
            n_users = ("user_id", "count"),
            active_rate = ("active", "mean"),
        )
        .reset_index()
        .sort_values("active_rate", ascending = False)
    )


def run_tasks():
    df = make_users_df()

    print("\nOriginal DataFrame")
    print(df)

    print("\nTask 1: Active users")
    print(filter_active_users(df))

    print("\nTask 2: High-value recent users")
    print(filter_high_value_recent_users(df))

    print("\nTask 3: Selected columns")
    print(select_user_country_revenue(df))

    print("\nTask 4: Add revenue_per_day")
    print(add_revenue_per_day(df))

    print("\nTask 5: Revenue by country")
    print(summarize_revenue_by_country(df))

    print("\nTask 6: Active rate by device")
    print(summarize_active_rate_by_device(df))


# ---------------------------------------------------------------------
# Sample answers
# ---------------------------------------------------------------------
# Try to solve the TODO sections above first.
# Then compare your solution with the sample answers below.
# You can copy these into the TODO functions after checking your attempt.


def filter_active_users_solution(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["active"]]


def filter_high_value_recent_users_solution(df: pd.DataFrame) -> pd.DataFrame:
    return df[(df["revenue"] >= 100) & (df["days_since_signup"] <= 10)]


def select_user_country_revenue_solution(df: pd.DataFrame) -> pd.DataFrame:
    return df[["user_id", "country", "revenue"]]


def add_revenue_per_day_solution(df: pd.DataFrame) -> pd.DataFrame:
    return df.assign(
        revenue_per_day=df["revenue"] / df["days_since_signup"]
    )


def summarize_revenue_by_country_solution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("country")
        .agg(
            total_revenue=("revenue", "sum"),
            avg_revenue=("revenue", "mean"),
            n_users=("user_id", "count"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )


def summarize_active_rate_by_device_solution(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("device")
        .agg(
            n_users=("user_id", "count"),
            active_rate=("active", "mean"),
        )
        .reset_index()
        .sort_values("active_rate", ascending=False)
    )


def run_sample_answers():
    df = make_users_df()

    print("\n[SOLUTION] Task 1: Active users")
    print(filter_active_users_solution(df))

    print("\n[SOLUTION] Task 2: High-value recent users")
    print(filter_high_value_recent_users_solution(df))

    print("\n[SOLUTION] Task 3: Selected columns")
    print(select_user_country_revenue_solution(df))

    print("\n[SOLUTION] Task 4: Add revenue_per_day")
    print(add_revenue_per_day_solution(df))

    print("\n[SOLUTION] Task 5: Revenue by country")
    print(summarize_revenue_by_country_solution(df))

    print("\n[SOLUTION] Task 6: Active rate by device")
    print(summarize_active_rate_by_device_solution(df))


if __name__ == "__main__":
    # Step 1:
    # First, fill in the TODO functions above and run:
    #     run_tasks()
    #
    # Step 2:
    # If you want to check the sample answers, comment out run_tasks()
    # and uncomment run_sample_answers().

    run_tasks()
    # run_sample_answers()