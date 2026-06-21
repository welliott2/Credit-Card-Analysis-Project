from load_cc_data import load_credit_data

X, y, metadata, variables = load_credit_data()

# Check the documented vs. actual values in the demographic columns
print("EDUCATION value counts:")
print(X["X3"].value_counts().sort_index())

print("\nMARRIAGE value counts:")
print(X["X4"].value_counts().sort_index())

print("\nSEX value counts:")
print(X["X2"].value_counts().sort_index())

print("\nAGE range:")
print(X["X5"].min(), "to", X["X5"].max())

print("\nPAY_0 (first repayment status) value counts:")
print(X["X6"].value_counts().sort_index())