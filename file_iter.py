import pandas as pd
import json


def find_header_row(sheet):
    """
    Identify the header row by scanning for the first non-empty row.
    """
    for i, row in sheet.iterrows():
        if row.notna().sum() > 5:  # Assuming headers have at least 5 non-null values
            print(f"✅ Header row found at index: {i}")
            return i
    raise ValueError("❌ Header row not found!")


def extract_transactions(file_path, sheet_name="Transactions"):
    """
    Extract transactions from the given Excel file, considering the correct header row.
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, header=None)  # Read raw data

    header_index = find_header_row(df)  # Detect the header row

    # Assign headers from the correct starting column (skipping first column)
    df_headers = df.iloc[header_index, 1:].values  # Extract header values from row
    df = df.iloc[header_index + 1:, 1:].reset_index(drop=True)  # Remove header row & first column

    # Ensure the number of headers matches the number of columns
    if len(df_headers) != df.shape[1]:
        raise ValueError(f"❌ Header length mismatch: Expected {df.shape[1]} headers, but got {len(df_headers)}")

    df.columns = df_headers  # Assign headers

    # Normalize column names
    df.columns = df.columns.str.strip().str.replace("\n", " ").str.lower()

    print(f"✅ Columns after normalization: {df.columns.tolist()}")  # Debug

    # Ensure required columns exist
    expected_columns = ["number of items", "invoice number", "account number", "invoice date", "invoice amount",
                        "total invoice amount"]
    missing_columns = [col for col in expected_columns if col not in df.columns]

    if missing_columns:
        raise KeyError(f"⚠️ Missing columns: {missing_columns}. Available columns: {df.columns.tolist()}")

    transactions = []
    current_transaction = None

    date_column = next((col for col in df.columns if "date" in col.lower()), None)
    if not date_column:
        raise ValueError("❌ No date column found!")

    for index, row in df.iterrows():
        date_value = str(row[date_column]).strip()

        if date_value.lower() != "nan":  # New transaction starts
            if current_transaction:
                transactions.append(current_transaction)

            # Initialize a new transaction
            current_transaction = {col: row[col] for col in df.columns if col not in expected_columns}
            current_transaction["Invoice Number"] = []
            current_transaction["Account Number"] = []
            current_transaction["Invoice Date"] = []
            current_transaction["Invoice Amount"] = []
            current_transaction["Total Invoice Amount"] = []

        if current_transaction:
            current_transaction["Invoice Number"].append(row.get("invoice number", ""))
            current_transaction["Account Number"].append(row.get("account number", ""))
            current_transaction["Invoice Date"].append(row.get("invoice date", ""))
            current_transaction["Invoice Amount"].append(row.get("invoice amount", ""))
            current_transaction["Total Invoice Amount"].append(row.get("total invoice amount", ""))

    if current_transaction:
        transactions.append(current_transaction)

    return {"Transactions": transactions}


# File path (Update accordingly)
file_path = "C:/Users/Adithya G/formyself/Boost-Qa/Testdata/20250114-PNC.xlsx"

processed_data = extract_transactions(file_path)

print(json.dumps(processed_data, indent=4))

























































# import pandas as pd
# import json
#
# def process_transactions(file_path, sheet_name="Transactions"):
#     """Process transactions and group invoices correctly based on 'Number of items'."""
#
#     df = pd.read_excel(file_path, sheet_name=sheet_name, dtype=str, header=1)  # Read as string
#     df.columns = df.columns.str.strip().str.replace("\n", " ").str.lower()  # Normalize column names
#
#     print("Normalized columns:", df.columns.tolist())  # Debug column names
#
#     date_column = [col for col in df.columns if "date" in col.lower()]
#     if not date_column:
#         raise ValueError("No date column found")
#     date_column = date_column[0]  # Use the correct column name
#
#     transactions = []
#     current_transaction = None
#
#     for index, row in df.iterrows():
#         # Convert to string to prevent AttributeError
#         date_value = str(row[date_column]).strip()
#
#         if date_value.lower() != "nan":  # If it's a valid date row
#             if current_transaction:
#                 transactions.append(current_transaction)
#
#             # Initialize transaction entry
#             current_transaction = {col: row[col] for col in df.columns if col not in
#                                    ["invoice number", "account number", "invoice date", "invoice amount", "total invoice amount"]}
#
#             # Initialize lists for invoice-related fields
#             current_transaction["Invoice Number"] = []
#             current_transaction["Account Number"] = []
#             current_transaction["Invoice Date"] = []
#             current_transaction["Invoice Amount"] = []
#             current_transaction["Total Invoice Amount"] = []
#
#         if current_transaction:
#             current_transaction["Invoice Number"].append(row.get("invoice number", ""))
#             current_transaction["Account Number"].append(row.get("account number", ""))
#             current_transaction["Invoice Date"].append(row.get("invoice date", ""))
#             current_transaction["Invoice Amount"].append(row.get("invoice amount", ""))
#             current_transaction["Total Invoice Amount"].append(row.get("total invoice amount", ""))
#
#     if current_transaction:
#         transactions.append(current_transaction)
#
#     return {"Transactions": transactions}
#
# # File path (Update accordingly)
# file_path = "C:/Users/RAMESH SINGH/PycharmProjects/File_validation/Test_files/20250114-PNC_Original.xlsx"
#
# processed_data = process_transactions(file_path)
#
# print(json.dumps(processed_data, indent=4))
