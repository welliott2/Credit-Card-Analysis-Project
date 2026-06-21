import pandas as pd
from load_cc_data import load_credit_data
from clean_taiwan_cc_data import clean_credit_data

pd.set_option("display.float_format", "{:.3f}".format)


def default_rate_by(df, group_cols):
    """
    Returns default rate and group size for one or more grouping columns.
    """
    summary = df.groupby(group_cols)["default"].agg(
        default_rate="mean",
        n="count"
    )
    return summary.sort_values("default_rate", ascending=False)


if __name__ == "__main__":
    X, y, metadata, variables = load_credit_data()
    df = clean_credit_data(X, y)

    print("=== Overall default rate ===")
    print(f"{df['default'].mean():.3f} across {len(df)} accounts\n")

    print("=== Default rate by PAY_0 (behavioral) ===")
    print(default_rate_by(df, "pay_0"))

    print("\n=== Default rate by Education (demographic) ===")
    print(default_rate_by(df, "education_label"))

    print("\n=== Default rate by Marriage (demographic) ===")
    print(default_rate_by(df, "marriage_label"))

    print("\n=== Default rate by Sex (demographic) ===")
    print(default_rate_by(df, "sex_label"))

    print("\n=== Default rate by PAY_0 x Education (combined) ===")
    print(default_rate_by(df, ["pay_0", "education_label"]))