import pandas as pd
from load_cc_data import load_credit_data


def clean_credit_data(X, y):
    """
    Cleans and recodes the Default of Credit Card Clients dataset.

    Handles undocumented category codes found during exploration:
      - EDUCATION (X3): values 0, 5, 6 are not in the official 1-4 scheme.
        Recoded into an explicit "Unknown" category (5) rather than
        merged into an existing label or dropped.
      - MARRIAGE (X4): value 0 is not in the official 1-3 scheme.
        Recoded into an explicit "Unknown" category (4).
      - PAY_0 (X6) and related PAY_2-PAY_6 columns: value -2 is not
        documented (official scale starts at -1 = "pay duly"). Kept as
        its own distinct category rather than merged into -1, since its
        true meaning (e.g. "no balance that month") isn't confirmed by
        the source and merging it would obscure a potentially different
        customer behavior pattern.

    Returns a single combined DataFrame (features + target) with
    human-readable column names.
    """
    df = X.copy()
    df["default"] = y["Y"]

    # Rename columns to be self-explanatory instead of X1, X2, etc.
    df = df.rename(columns={
        "X1": "limit_bal",
        "X2": "sex",
        "X3": "education",
        "X4": "marriage",
        "X5": "age",
        "X6": "pay_0", "X7": "pay_2", "X8": "pay_3",
        "X9": "pay_4", "X10": "pay_5", "X11": "pay_6",
        "X12": "bill_amt1", "X13": "bill_amt2", "X14": "bill_amt3",
        "X15": "bill_amt4", "X16": "bill_amt5", "X17": "bill_amt6",
        "X18": "pay_amt1", "X19": "pay_amt2", "X20": "pay_amt3",
        "X21": "pay_amt4", "X22": "pay_amt5", "X23": "pay_amt6",
    })

    # EDUCATION: fold undocumented codes (0, 5, 6) into a single
    # explicit "Unknown" bucket, coded as 5.
    df["education"] = df["education"].replace({0: 5, 6: 5})
    education_labels = {
        1: "Graduate School",
        2: "University",
        3: "High School",
        4: "Other",
        5: "Unknown",
    }
    df["education_label"] = df["education"].map(education_labels)

    # MARRIAGE: fold undocumented code (0) into an explicit "Unknown"
    # bucket, coded as 4.
    df["marriage"] = df["marriage"].replace({0: 4})
    marriage_labels = {
        1: "Married",
        2: "Single",
        3: "Other",
        4: "Unknown",
    }
    df["marriage_label"] = df["marriage"].map(marriage_labels)

    # SEX: clean, just adding readable labels.
    sex_labels = {1: "Male", 2: "Female"}
    df["sex_label"] = df["sex"].map(sex_labels)

    # PAY_0 / PAY_2-6: no recoding needed. The undocumented -2 value
    # is intentionally left as-is (see docstring above) rather than
    # merged into -1.

    return df


if __name__ == "__main__":
    X, y, metadata, variables = load_credit_data()
    df_clean = clean_credit_data(X, y)

    print("Cleaned data shape:", df_clean.shape)
    print("\nColumns:", list(df_clean.columns))

    print("\nEducation labels after cleaning:")
    print(df_clean["education_label"].value_counts())

    print("\nMarriage labels after cleaning:")
    print(df_clean["marriage_label"].value_counts())

    print("\nSample rows:")
    print(df_clean.head())