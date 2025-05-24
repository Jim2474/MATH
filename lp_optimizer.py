import pandas as pd
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, value, LpStatus
import io

# --- 1. Prepare Input Data ---

# Farm Area Data (Consistent with previous LP run)
farm_area_data_dict = {
    '学院4': 465, '学院10': 430, '学院9': 340, '学院8': 341, '学院12': 423,
    '学院14': 360, '学院11': 364, '学院5': 473, '后勤临时管理用地1': 408,
    '后勤临时管理用地2': 336, '学院6': 350, '学院13': 390, '学院1': 610,
    '后勤临时管理用地3': 472, '后勤临时管理用地4': 113, '学院3': 328,
    '学院7': 407, '学院2': 522
}
farm_areas_df = pd.DataFrame(list(farm_area_data_dict.items()), columns=['Farm_Name', 'Area_m2'])

# Crop Data (Consistent with previous LP run)
crop_csv_data = """ID,Crop_Name,Planting_Season,Growth_Cycle_days,Yield_kg_per_m2,Cost_Yuan_per_m2,Min_Selling_Price_Yuan_per_kg,Max_Selling_Price_Yuan_per_kg,Avg_Selling_Price_Yuan_per_kg
1,莴笋,春季,60~90天,10.0,4,6.0,7.0,6.5
2,灯笼椒,春季,90~120天,4.0,6,4.0,5.5,4.75
3,水果黄瓜,春季,50~70天,8.0,4,2.5,3.0,2.75
4,甜玉米,春季,70~100天,6.5,4,5.0,6.5,5.75
5,香瓜,春季,70~100天,7.0,3,4.5,6.5,5.5
6,地瓜,春季,叶用30~50天，块根100~180天,9.0,3,2.0,3.0,2.5
7,空心菜,春季,25~40天,3.0,4,5.5,6.5,6.0
8,圣女果,春季,90~120天,6.0,5,6.0,7.5,6.75
9,南瓜,春季,嫩瓜50~70天，老瓜90~120天,10.0,6,2.5,3.5,3.0
10,凉薯,春季,120~150天,9.5,3,4.5,6.5,5.5
11,薄荷,春季,扦插30~50天，播种60~90天,2.0,3,5.5,7.5,6.5
12,小芋头,春季,180~240天,9.0,3,3.5,4.5,4.0
13,萝卜,秋季,40~60天,8.5,5,1.4,2.0,1.7
14,豌豆苗,秋季,15~30天,3.5,5,9.5,12.5,11.0
15,胡萝卜,秋季,70~100天,8.0,3,3.5,4.5,4.0
16,大白菜,秋季,60~90天,6.5,6,2.5,4.0,3.25
17,菠菜,秋季,30~50天,4.0,6,4.0,5.0,4.5
18,芥兰,秋季,50~70天,6.0,4,3.5,4.5,4.0
19,茼蒿,秋季,30~45天,5.5,3,4.0,5.0,4.5
20,西蓝花,秋季,80~100天,9.5,5,5.0,6.5,5.75
21,生菜,秋季,40~60天,5.0,3,4.0,5.5,4.75
22,上海青,秋季,25~40天,5.0,6,2.0,3.4,2.7
23,甘蓝,秋季,70~100天,7.5,4,3.5,5.0,4.25
24,蒜,秋季,青蒜：30~50天；蒜头：90~120天,5.5,6,11.5,13.0,12.25
25,芹菜,秋季,80~120天,5.5,3,3.5,4.5,4.0
26,葱,秋季,小葱：30~50天；大葱：90~150天,7.0,3,3.0,4.0,3.5
27,香菜,秋季,30~50天,5.0,3,17.0,19.5,18.25
28,油麦菜,双季,30~45天,4.5,5,3.5,4.5,4.0
29,韭菜,双季,首茬60~80天，之后20~30天/茬,3.0,4,2.6,3.5,3.05
30,茄子,双季,90~120天,8.0,3,4.0,6.0,5.0
"""
crop_df = pd.read_csv(io.StringIO(crop_csv_data))
crop_df['Profit_per_m2'] = (crop_df['Yield_kg_per_m2'] * crop_df['Avg_Selling_Price_Yuan_per_kg']) - crop_df['Cost_Yuan_per_m2']

# ** NEW Farm Fertility Grades (from Turn 52 output for colleges, default Grade II for 后勤) **
# Output from Turn 52:
# 学院1: P综=1.54, Grade II
# 学院2: P综=1.06, Grade II
# 学院3: P综=0.95, Grade II
# 学院4: P综=1.06, Grade II (Previously Grade III)
# 学院5: P综=1.10, Grade II
# 学院6: P综=1.11, Grade II
# 学院7: P综=1.00, Grade II
# 学院8: P综=1.12, Grade II
# 学院9: P综=0.85, Grade III (Previously Grade II)
# 学院10: P综=1.35, Grade II
# 学院11: P综=1.32, Grade II
# 学院12: P综=1.23, Grade II
# 学院13: P综=0.90, Grade II
# 学院14: P综=1.11, Grade II

new_farm_fertility_grades = {
    '学院1': 'II',  # Changed from I
    '学院2': 'II',
    '学院3': 'II',
    '学院4': 'II',  # Changed from III
    '学院5': 'II',
    '学院6': 'II',
    '学院7': 'II',
    '学院8': 'II',
    '学院9': 'III', # Changed from II
    '学院10': 'II',
    '学院11': 'II',
    '学院12': 'II',
    '学院13': 'II',
    '学院14': 'II',
    '后勤临时管理用地1': 'II', # Default as per instruction
    '后勤临时管理用地2': 'II', # Default
    '后勤临时管理用地3': 'II', # Default
    '后勤临时管理用地4': 'II'  # Default
}

# Crop Recommendations per Grade (Consistent with previous LP run)
nitrogen_fixers = ['凉薯', '豌豆苗']
recommendations = {
    'I': ['甜玉米', '茄子', '南瓜', '灯笼椒', '西蓝花', '豌豆苗', '凉薯'], # Still define for completeness
    'II': ['地瓜', '空心菜', '莴笋', '萝卜', '蒜', '豌豆苗', '凉薯'],
    'III': ['凉薯', '豌豆苗', '空心菜', '薄荷', '地瓜']
}

# Filter farms to only those with grades and areas
farm_areas_df = farm_areas_df[farm_areas_df['Farm_Name'].isin(new_farm_fertility_grades.keys())]

# --- 2. Create LP Model ---
prob = LpProblem("Crop_Planting_Optimization_New_Grades", LpMaximize)

plant_vars = {}
for _, farm_row in farm_areas_df.iterrows():
    farm_name = farm_row['Farm_Name']
    farm_grade = new_farm_fertility_grades.get(farm_name) # Use new grades
    if not farm_grade: continue
    recommended_crop_names = recommendations.get(farm_grade, [])
    for _, crop_row in crop_df.iterrows():
        crop_name = crop_row['Crop_Name']
        if crop_name in recommended_crop_names:
            var_name = f"Area_{farm_name.replace(' ', '_')}_{crop_name.replace(' ', '_')}"
            plant_vars[(farm_name, crop_name)] = LpVariable(var_name, lowBound=0, cat='Continuous')

total_profit_terms = []
for (farm_name, crop_name), var in plant_vars.items():
    profit = crop_df[crop_df['Crop_Name'] == crop_name]['Profit_per_m2'].iloc[0]
    total_profit_terms.append(var * profit)
prob += lpSum(total_profit_terms), "Total_Profit"

# Constraints (logic remains the same)
for _, farm_row in farm_areas_df.iterrows():
    farm_name = farm_row['Farm_Name']
    farm_total_area = farm_row['Area_m2']
    farm_crop_vars = [plant_vars[(f, c)] for (f, c) in plant_vars if f == farm_name]
    if farm_crop_vars:
        prob += lpSum(farm_crop_vars) <= farm_total_area, f"Area_Constraint_{farm_name.replace(' ', '_')}"

for _, farm_row in farm_areas_df.iterrows():
    farm_name = farm_row['Farm_Name']
    farm_grade = new_farm_fertility_grades.get(farm_name) # Use new grades
    if not farm_grade: continue
    all_crops_on_farm_vars = [plant_vars[(f, c)] for (f, c) in plant_vars if f == farm_name]
    n_fixing_crops_on_farm_vars = [
        plant_vars[(f, c)] for (f, c) in plant_vars 
        if f == farm_name and c in nitrogen_fixers
    ]
    if not all_crops_on_farm_vars: continue
    
    # Grade I farms have no N-fixer constraint in this setup
    if farm_grade == 'II' and n_fixing_crops_on_farm_vars:
        prob += lpSum(n_fixing_crops_on_farm_vars) - 0.10 * lpSum(all_crops_on_farm_vars) >= 0, f"N_Fixer_II_{farm_name.replace(' ', '_')}"
    elif farm_grade == 'III' and n_fixing_crops_on_farm_vars:
        prob += lpSum(n_fixing_crops_on_farm_vars) - 0.20 * lpSum(all_crops_on_farm_vars) >= 0, f"N_Fixer_III_{farm_name.replace(' ', '_')}"

# --- 3. Solve LP Problem ---
prob.solve()

# --- 4. Output Results ---
print("--- LP Model Results (with Updated Fertility Grades) ---")
print(f"Status: {LpStatus[prob.status]}")

if LpStatus[prob.status] == 'Optimal':
    total_profit_value = value(prob.objective)
    print(f"New Total Expected Profit: {total_profit_value:.2f} Yuan")

    planting_plan_data = []
    for (farm_name, crop_name), var in plant_vars.items():
        if var.varValue is not None and var.varValue > 0:
            area_planted = var.varValue
            profit_per_m2 = crop_df[crop_df['Crop_Name'] == crop_name]['Profit_per_m2'].iloc[0]
            crop_profit = area_planted * profit_per_m2
            farm_grade = new_farm_fertility_grades.get(farm_name, "N/A") # Use new grades
            planting_plan_data.append({
                'Farm_Name': farm_name,
                'Fertility_Grade': farm_grade,
                'Crop_Name': crop_name,
                'Area_m2_Allocated': round(area_planted, 2),
                'Expected_Profit_from_Crop': round(crop_profit, 2)
            })
    
    planting_plan_df = pd.DataFrame(planting_plan_data)
    print("\nNew Planting Plan:")
    if not planting_plan_df.empty:
        print(planting_plan_df.to_string())
    else:
        print("No crops allocated in the optimal plan.")

    print("\nSummary per Farm (New Grades):")
    summary_data = []
    farm_names_in_plan = planting_plan_df['Farm_Name'].unique() if not planting_plan_df.empty else []
    
    processed_farms_summary = set()

    if not planting_plan_df.empty:
        for farm_name_grp, group_df in planting_plan_df.groupby('Farm_Name'):
            processed_farms_summary.add(farm_name_grp)
            total_planted_on_farm = group_df['Area_m2_Allocated'].sum()
            farm_total_capacity = farm_areas_df[farm_areas_df['Farm_Name'] == farm_name_grp]['Area_m2'].iloc[0]
            
            n_fixer_area_on_farm = 0
            for index, row in group_df.iterrows():
                if row['Crop_Name'] in nitrogen_fixers:
                    n_fixer_area_on_farm += row['Area_m2_Allocated']
            
            n_fixer_percentage = (n_fixer_area_on_farm / total_planted_on_farm * 100) if total_planted_on_farm > 0 else 0
            
            summary_data.append({
                'Farm_Name': farm_name_grp,
                'Fertility_Grade': group_df['Fertility_Grade'].iloc[0], # Use new grade
                'Total_Area_Planted_m2': round(total_planted_on_farm,2),
                'Farm_Capacity_m2': farm_total_capacity,
                'N_Fixer_Area_m2': round(n_fixer_area_on_farm,2),
                'N_Fixer_Percentage': round(n_fixer_percentage, 2)
            })

    # Add farms that might not have any crops allocated but have area and grade
    for _, farm_row in farm_areas_df.iterrows():
        farm_name_iter = farm_row['Farm_Name']
        if farm_name_iter not in processed_farms_summary:
            farm_grade_iter = new_farm_fertility_grades.get(farm_name_iter, "N/A")
            farm_total_capacity_iter = farm_row['Area_m2']
            summary_data.append({
                'Farm_Name': farm_name_iter,
                'Fertility_Grade': farm_grade_iter,
                'Total_Area_Planted_m2': 0,
                'Farm_Capacity_m2': farm_total_capacity_iter,
                'N_Fixer_Area_m2': 0,
                'N_Fixer_Percentage': 0
            })

    farm_summary_df = pd.DataFrame(summary_data)
    # Sort summary by Farm_Name to match original farm_areas_df order as much as possible
    farm_summary_df = farm_summary_df.set_index('Farm_Name').reindex(farm_areas_df['Farm_Name'].unique().tolist()).reset_index() # Reindex based on actual order in farm_areas_df
    print(farm_summary_df.to_string())

else:
    print("LP problem could not be solved to optimality.")

print("\n--- End of Updated LP Model Script ---")
