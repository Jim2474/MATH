import pandas as pd
import re

raw_text_data = """
学院4 465㎡
学院10 430㎡
学院9 340㎡
学院8 341㎡
学院12 423 ㎡
学院14 360㎡
学院11 364㎡
学院5 473 ㎡
后勤临时管理用地 408㎡
后勤临时管理用地 336㎡
学院6 350㎡
学院13 390㎡
学院1 610㎡
后勤临时管理用地 472㎡
后勤临时管理用地 113 ㎡
学院3 328㎡
学院7 407 ㎡
学院2 522㎡
"""

lines = raw_text_data.strip().split('\n')

farm_names = []
areas = []
logistics_counter = 1

# Regex to capture name and area.
# It looks for:
# (anything not a digit, not a space at the end) (optional space) (digits) (optional space) ㎡
# Pattern: r"^(.*?)(\s*)(\d+)\s*㎡$"
# Refined pattern: r"^(.*?)\s*(\d+)\s*㎡$"
# Name part: (.+?) captures the farm name (non-greedy).
# Area part: (\d+) captures the area digits.
# \s* handles optional spaces.
# ㎡ is the area unit.
pattern = re.compile(r"^(.*?)\s*(\d+)\s*㎡$")

for line in lines:
    match = pattern.match(line)
    if match:
        name_part = match.group(1).strip()
        area_part = int(match.group(2))

        if name_part == "后勤临时管理用地":
            farm_names.append(f"{name_part}{logistics_counter}")
            logistics_counter += 1
        else:
            farm_names.append(name_part)
        areas.append(area_part)
    else:
        print(f"Warning: Could not parse line: '{line}'")

# Create DataFrame
df_areas = pd.DataFrame({
    'Farm_Name': farm_names,
    'Area_m2': areas
})

# --- Output Summary ---
print("--- Farm Area DataFrame Summary ---")
print("\nDataFrame Shape:")
print(df_areas.shape)

print("\nColumn Names:")
print(df_areas.columns.tolist())

print("\nFirst 5 Rows of DataFrame:")
print(df_areas.head())

print("\nFull DataFrame:")
print(df_areas)
