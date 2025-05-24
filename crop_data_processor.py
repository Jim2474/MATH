import pandas as pd
import re

file_path = "附件3 微农作物产量.xlsx" # Corrected filename from previous error log if any, or ensure it's right

# Read both sheets
try:
    df_data = pd.read_excel(file_path, sheet_name='2024年数据')
    df_cycle = pd.read_excel(file_path, sheet_name='蔬菜生长周期')
except Exception as e:
    print(f"Error reading sheets from {file_path}: {e}")
    # Fallback to the filename used in successful prior execution if there's an error
    file_path = "附件3 微农场农作物产量.xlsx"
    try:
        df_data = pd.read_excel(file_path, sheet_name='2024年数据')
        df_cycle = pd.read_excel(file_path, sheet_name='蔬菜生长周期')
    except Exception as e_fallback:
        print(f"Fallback error reading sheets from {file_path}: {e_fallback}")
        exit()


# Merge the two dataframes on '蔬菜名称' (Crop Name) and '蔬菜序号' (ID)
df_merged = pd.merge(df_data, df_cycle[['蔬菜名称', '蔬菜序号', '生长周期']], on=['蔬菜名称', '蔬菜序号'], how='left')

# Rename columns for clarity
column_rename_map = {
    '蔬菜序号': 'ID',
    '蔬菜名称': 'Crop_Name',
    '生长季节': 'Planting_Season',
    '产量（斤/㎡）': 'Yield_jin_per_m2',
    '种植成本（元/㎡）': 'Cost_Yuan_per_m2',
    '销售单价(元/公斤)': 'Selling_Price_Range_Yuan_per_kg',
    '生长周期': 'Growth_Cycle_days'
}
df_merged = df_merged.rename(columns=column_rename_map)

# --- Data Transformations ---
if 'Yield_jin_per_m2' in df_merged.columns:
    df_merged['Yield_kg_per_m2'] = df_merged['Yield_jin_per_m2'] * 0.5

if 'Selling_Price_Range_Yuan_per_kg' in df_merged.columns:
    def parse_price(price_range_str):
        if isinstance(price_range_str, (int, float)):
            return float(price_range_str), float(price_range_str), float(price_range_str)
        if isinstance(price_range_str, str):
            numbers = re.findall(r'\d+\.?\d*', price_range_str)
            if numbers:
                prices = [float(n) for n in numbers]
                return min(prices), max(prices), sum(prices) / len(prices) if prices else None
        return None, None, None
    parsed_prices = df_merged['Selling_Price_Range_Yuan_per_kg'].apply(parse_price)
    df_merged['Min_Selling_Price_Yuan_per_kg'] = parsed_prices.apply(lambda x: x[0])
    df_merged['Max_Selling_Price_Yuan_per_kg'] = parsed_prices.apply(lambda x: x[1])
    df_merged['Avg_Selling_Price_Yuan_per_kg'] = parsed_prices.apply(lambda x: x[2])

final_columns = [
    'ID', 'Crop_Name', 'Planting_Season', 'Growth_Cycle_days', 
    'Yield_kg_per_m2', 'Cost_Yuan_per_m2', 
    'Min_Selling_Price_Yuan_per_kg', 'Max_Selling_Price_Yuan_per_kg', 'Avg_Selling_Price_Yuan_per_kg'
]
final_columns = [col for col in final_columns if col in df_merged.columns] # Ensure columns exist
df_final = df_merged[final_columns]

# --- Output DataFrame as CSV to stdout ---
print(df_final.to_csv(index=False))
