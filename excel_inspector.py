import pandas as pd

# Load the Excel file
excel_file = pd.ExcelFile("附件1 校园微农场土壤指标.xlsx")

# Print sheet names
print("Sheet names:", excel_file.sheet_names)

# Load the first sheet into a DataFrame (assuming the first sheet is relevant for now)
# If multiple sheets, this will need adjustment after inspecting sheet names
df = excel_file.parse(excel_file.sheet_names[0])

# Print some info about the DataFrame
print("\nDataFrame head:")
print(df.head())

print("\nDataFrame columns:")
print(df.columns)

print("\nDataFrame shape:")
print(df.shape)
