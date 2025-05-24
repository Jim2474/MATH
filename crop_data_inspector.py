import pandas as pd

file_path = "附件3 微农场农作物产量.xlsx"

# Load the Excel file
try:
    excel_file = pd.ExcelFile(file_path)
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# Print sheet names
print("Sheet names:", excel_file.sheet_names)

# Inspect all sheets
for sheet_name in excel_file.sheet_names:
    print(f"\n--- Inspecting sheet: '{sheet_name}' ---")
    try:
        df_sheet = excel_file.parse(sheet_name)
        print("\nSheet head:")
        print(df_sheet.head())
        print("\nSheet columns:")
        print(df_sheet.columns.tolist())
        print("\nSheet shape:")
        print(df_sheet.shape)
        if '蔬菜名称' in df_sheet.columns:
            print("\nUnique crop names in this sheet (sample):")
            print(df_sheet['蔬菜名称'].unique()[:10]) # Print up to 10 unique names
    except Exception as e:
        print(f"Error parsing sheet '{sheet_name}': {e}")
