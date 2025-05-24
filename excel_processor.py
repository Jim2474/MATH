import pandas as pd
import re

# Load the Excel file, using the second row as header (skiprows=1)
file_path = "附件1 校园微农场土壤指标.xlsx"
df = pd.read_excel(file_path, sheet_name='土壤指标', skiprows=1)

# --- Debugging Column Names ---
print("--- Debugging Column Names ---")
print("Raw column names from pandas (after skiprows=1):")
raw_column_names = df.columns.tolist()
print(raw_column_names)

# Clean column names function
def clean_col_name(col_name):
    name = str(col_name) # Ensure it's a string
    # Remove units like ℃, %, mg/kg, g/kg, pH (unit), us/cm
    # Also remove content in parentheses
    name = re.sub(r'\s*\(.*\)|℃|%|mg/kg|g/kg|us/cm', '', name).strip()
    # Specific renaming for clarity or standardisation
    if name == "酸碱度pH": # If original was "酸碱度pH" and "pH" unit was removed
        return "pH"
    if name == "酸碱度": # If original was just "酸碱度" or "酸碱度pH" and "pH" was already stripped by regex
        return "pH"
    return name

cleaned_column_names = [clean_col_name(col) for col in raw_column_names]
print("\nCleaned column names:")
print(cleaned_column_names)
print("--- End Debugging --- \n")

df.columns = cleaned_column_names

# Set the first column '学院' (or its cleaned version) as index
# The first raw column name is raw_column_names[0] which is '学院'
# Its cleaned version is cleaned_column_names[0]
df = df.set_index(cleaned_column_names[0])


# Clean data within cells: remove units and convert to numeric
print("--- Data Cleaning and Conversion ---")
for col in df.columns:
    if df[col].dtype == 'object' or pd.api.types.is_string_dtype(df[col]):
        # Ensure data is string before trying string operations
        df[col] = df[col].astype(str)
        # Remove units from the data itself
        df[col] = df[col].str.replace(r'℃|%|mg/kg|g/kg|us/cm', '', regex=True).str.strip()
        try:
            df[col] = pd.to_numeric(df[col])
            print(f"Successfully converted column '{col}' to numeric.")
        except ValueError:
            print(f"Could not convert column '{col}' to numeric after cleaning. Values like 'nan' or other non-numeric strings might be present.")
            # Attempt to coerce errors, turning unconvertible values into NaNs
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].isnull().any():
                 print(f"Non-numeric values in '{col}' were converted to NaN.")

    elif pd.api.types.is_numeric_dtype(df[col]):
        print(f"Column '{col}' is already numeric.")


print("\nDataFrame shape:", df.shape)
print("\nFinal DataFrame columns:", df.columns.tolist())
print("\nFinal DataFrame head:")
print(df.head())
print("\nFinal DataFrame dtypes:")
print(df.dtypes)

# Identify key columns based on the actual cleaned names
# Expected raw headers that should be cleaned:
# '酸碱度pH' -> 'pH'
# '有机质g/kg' -> '有机质'
# '全氮g/kg' -> '全氮'
# '磷mg/kg' -> '磷'
# '钾mg/kg' -> '钾'

ph_col_expected = 'pH'
organic_matter_expected = '有机质'
total_nitrogen_expected = '全氮'
available_p_expected = '磷'
available_k_expected = '钾'

print("\n--- Identifying Key Columns ---")
print(f"Expected key column names after cleaning: pH='{ph_col_expected}', Organic Matter='{organic_matter_expected}', Total Nitrogen='{total_nitrogen_expected}', Available P='{available_p_expected}', Available K='{available_k_expected}'")

final_columns = df.columns.tolist()
identified_key_cols_dict = {}
missing_key_cols_list = []

# pH
if ph_col_expected in final_columns:
    identified_key_cols_dict['pH'] = ph_col_expected
else:
    missing_key_cols_list.append(f"pH (expected: '{ph_col_expected}')")

# Organic Matter
if organic_matter_expected in final_columns:
    identified_key_cols_dict['Organic Matter'] = organic_matter_expected
else:
    missing_key_cols_list.append(f"Organic Matter (expected: '{organic_matter_expected}')")

# Total Nitrogen
if total_nitrogen_expected in final_columns:
    identified_key_cols_dict['Total Nitrogen'] = total_nitrogen_expected
elif '氮' in final_columns: # Fallback if '全氮' became '氮'
    identified_key_cols_dict['Total Nitrogen'] = '氮'
    print(f"Note: Found '氮' and using it for Total Nitrogen instead of '{total_nitrogen_expected}'.")
else:
    missing_key_cols_list.append(f"Total Nitrogen (expected: '{total_nitrogen_expected}' or '氮')")

# Available P
if available_p_expected in final_columns:
    identified_key_cols_dict['Available P'] = available_p_expected
else:
    missing_key_cols_list.append(f"Available P (expected: '{available_p_expected}')")

# Available K
if available_k_expected in final_columns:
    identified_key_cols_dict['Available K'] = available_k_expected
else:
    missing_key_cols_list.append(f"Available K (expected: '{available_k_expected}')")

print("\nIdentified Key Columns Mapping (Task Requirement):")
for key, val in identified_key_cols_dict.items():
    print(f"- {key}: '{val}'")

if missing_key_cols_list:
    print("\nWarning: The following key columns could NOT be definitively identified based on expected names:")
    for col_info in missing_key_cols_list:
        print(f"- {col_info}")
    print(f"Available DataFrame columns for reference: {final_columns}")
else:
    # Check if all 5 required keys are in identified_key_cols_dict
    required_keys = ['pH', 'Organic Matter', 'Total Nitrogen', 'Available P', 'Available K']
    all_found = all(key in identified_key_cols_dict for key in required_keys)
    if all_found:
        print("\nAll specified key soil indicators have been successfully identified in the DataFrame.")
    else:
        # This case should be caught by missing_key_cols_list, but as a safeguard:
        print("\nThere was an issue identifying all specified key soil indicators. Please review missing column warnings.")

# Farm identifiers are in the index
print("\nFarm Identifiers (Index):")
print(df.index.tolist())
