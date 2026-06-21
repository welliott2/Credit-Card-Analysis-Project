from ucimlrepo import fetch_ucirepo
import pandas as pd

def load_credit_data():
    """
    Pulls the Default of Credit Card Clients dataset from the UCI ML Repository.
    Returns features (X) and target (y) as pandas DataFrames.
    """
    dataset = fetch_ucirepo(id=350)

    X = dataset.data.features
    y = dataset.data.targets

    return X, y, dataset.metadata, dataset.variables


if __name__ == "__main__":
    X, y, metadata, variables = load_credit_data()

    print("Features shape:", X.shape)
    print("Target shape:", y.shape)
    print("\nFirst few rows of features:")
    print(X.head())
    print("\nFirst few rows of target:")
    print(y.head())