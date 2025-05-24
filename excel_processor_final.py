import pandas as pd
import re

# Load the Excel file, using the second row as header (skiprows=1)
file_path = "附件1 校园微农场土壤指标.xlsx"
df = pd.read_excel(file_path, sheet_name='土壤指标', skiprows=1)

# Raw column names from pandas (after skiprows=1)
raw_column_names = df.columns.tolist()

# Clean column names function
def clean_col_name(col_name):
    name = str(col_name)
    name = re.sub(r'\s*\(.*\)|℃|%|mg/kg|g/kg|us/cm', '', name).strip()
    if name == "酸碱度pH" or name == "酸碱度": # Handles if original is '酸碱度pH' or just '酸碱度'
        return "pH"
    return name

cleaned_column_names = [clean_col_name(col) for col in raw_column_names]
df.columns = cleaned_column_names

# Set the first column (cleaned '学院') as index
df = df.set_index(cleaned_column_names[0])

# Clean data within cells: remove units and convert to numeric
for col in df.columns:
    if df[col].dtype == 'object' or pd.api.types.is_string_dtype(df[col]):
        df[col] = df[col].astype(str)
        # Corrected regex to avoid accidentally removing parts of valid numbers if units are absent
        df[col] = df[col].str.replace(r'(℃|%|mg/kg|g/kg|us/cm)', '', regex=True).str.strip()
        df[col] = pd.to_numeric(df[col], errors='coerce') # Coerce errors to NaN

# Remove the erroneous row from the index if it exists
if '注：2024年11月采样' in df.index:
    df = df.drop('注：2024年11月采样')
    # print("Note: Removed row with index '注：2024年11月采样'.") # Suppress this for CSV output

# --- Output DataFrame as CSV to stdout ---
# print("--- Final Soil DataFrame (CSV) ---") # Suppress header for direct parsing
print(df.to_csv())

# --- Key Soil Indicator Columns ---
# (Original print statements for key columns are suppressed for this step)
