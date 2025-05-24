import pandas as pd
import numpy as np
import io
import math

# --- 1. Parse Soil Data (for 14 college farms) ---
# Data based on previous processing of 附件1
raw_soil_data_text = """学院1	17.7℃	22.6%	1003.0us/cm	8.0	50mg/kg	70mg/kg	160mg/kg	551mg/kg
学院2	17.4℃	20.3%	379us/cm	8.0	18mg/kg	26mg/kg	60mg/kg	208mg/kg
学院3	14.6℃	21.8%	306.0us/cm	8.0	15mg/kg	21mg/kg	48mg/kg	168mg/kg
学院4	16.8℃	33.5%	602.1us/cm	8.1	31mg/kg	43mg/kg	97mg/kg	332mg/kg
学院5	17.8℃	23.0%	430.0us/cm	8.0	21mg/kg	30mg/kg	68mg/kg	236mg/kg
学院6	15.1℃	28.1%	439.0us/cm	8.0	21mg/kg	30mg/kg	70mg/kg	241mg/kg
学院7	17.4℃	20.3%	317.0us/cm	8.0	15mg/kg	22mg/kg	50mg/kg	174mg/kg
学院8	19.2℃	29.3%	457.0us/cm	8.0	22mg/kg	31mg/kg	73mg/kg	251mg/kg
学院9	15.6℃	19.9%	283.0us/cm	8.0	14mg/kg	19mg/kg	45mg/kg	155mg/kg
学院10	15.5℃	28.6%	763.0us/cm	8.0	38mg/kg	53mg/kg	122mg/kg	419mg/kg
学院11	14.7℃	26.8%	722.0us/cm	8.0	36mg/kg	50mg/kg	115mg/kg	397mg/kg
学院12	18.8℃	36.7%	605.0us/cm	8.0	30mg/kg	42mg/kg	96mg/kg	332mg/kg
学院13	15.8℃	18.3%	294.0us/cm	8.0	14mg/kg	20mg/kg	47mg/kg	161mg/kg
学院14	15.1℃	26.3%	438.0us/cm	8.0	21mg/kg	30mg/kg	70mg/kg	240mg/kg
"""

data = io.StringIO(raw_soil_data_text)
parsed_data = []
for line in data:
    parts = line.strip().split('\t')
    farm_name = parts[0]
    ph_val = float(parts[4])
    n_val_mg_kg = float(parts[5].replace('mg/kg', ''))
    p_val_mg_kg = float(parts[6].replace('mg/kg', ''))
    k_val_mg_kg = float(parts[7].replace('mg/kg', ''))
    parsed_data.append({
        'Farm_Name': farm_name,
        'pH': ph_val, # Original pH value
        'N_mg_per_kg': n_val_mg_kg, # Original N value
        'P_mg_per_kg': p_val_mg_kg, # Original P value
        'K_mg_per_kg': k_val_mg_kg  # Original K value
    })
soil_df = pd.DataFrame(parsed_data)

# --- 2. Define Standard Values (Sᵢ) and NEW pH Pᵢ Scoring ---
S_values = {
    'Total_Nitrogen_g_per_kg': 1.0,
    'Available_Phosphorus_mg_per_kg': 7.5,
    'Available_Potassium_mg_per_kg': 80.0
}

def calculate_ph_pi_new(ph): # New pH Pᵢ table from Turn 48
    if ph < 5.0 or ph > 9.0:
        return 1.0
    elif (5.0 <= ph < 5.5) or (8.5 < ph <= 9.0): # pH 5.0-5.5 or 8.5-9.0
        return 1.5
    elif (5.5 <= ph < 6.0) or (8.0 < ph <= 8.5): # pH 5.5-6.0 or 8.0-8.5
        return 2.0
    elif (6.0 <= ph < 6.5) or (7.5 < ph <= 8.0): # pH 6.0-6.5 or 7.5-8.0
        return 2.5
    elif 6.5 <= ph <= 7.5: # pH 6.5-7.5 (inclusive)
        return 3.0
    return np.nan # Should ideally not be reached if pH is always valid

# --- 3. Calculations ---
results = []
N_indicators = 4 # pH, N, P, K
sqrt_term = math.sqrt((N_indicators - 1) / N_indicators) # sqrt(0.75)

for index, row in soil_df.iterrows():
    farm_name = row['Farm_Name']
    ph_value = row['pH']
    
    # Pᵢ for pH using new table
    p_ph = calculate_ph_pi_new(ph_value)
    
    # Cᵢ for N, P, K
    n_mg_kg_ci = row['N_mg_per_kg']
    n_g_kg_ci = n_mg_kg_ci / 1000.0 # Convert N from mg/kg to g/kg for Pᵢ calculation
    
    p_mg_kg_ci = row['P_mg_per_kg']
    k_mg_kg_ci = row['K_mg_per_kg']
    
    # Pᵢ for N, P, K (Cᵢ/Sᵢ, capped at 3)
    p_nitrogen = min(n_g_kg_ci / S_values['Total_Nitrogen_g_per_kg'], 3.0)
    p_phosphorus = min(p_mg_kg_ci / S_values['Available_Phosphorus_mg_per_kg'], 3.0)
    p_potassium = min(k_mg_kg_ci / S_values['Available_Potassium_mg_per_kg'], 3.0)
    
    # P_min_overall and P_avg_overall
    pi_values = [p_ph, p_nitrogen, p_phosphorus, p_potassium]
    p_min_overall = min(pi_values)
    p_avg_overall = sum(pi_values) / len(pi_values)
    
    # Calculate P综 using the agreed formula: P综 = [ (P_min_overall)² + (P_avg_overall)² ] / 2 * √[(N-1)/N]
    p_comprehensive = ((p_min_overall**2) + (p_avg_overall**2)) / 2.0 * sqrt_term
    
    # Assign Fertility Grades
    fertility_grade = 'N/A'
    if not pd.isna(p_comprehensive):
        if p_comprehensive > 1.7:
            fertility_grade = 'I'
        elif 0.9 <= p_comprehensive <= 1.7:
            fertility_grade = 'II'
        else: # P综 < 0.9
            fertility_grade = 'III'
        
    results.append({
        'Farm_Name': farm_name,
        'pH': ph_value, # Original pH
        'Pᵢ_pH': round(p_ph, 2),
        'N_g_kg': n_g_kg_ci, # Cᵢ value for N in g/kg
        'Pᵢ_N': round(p_nitrogen, 2),
        'P_mg_kg': p_mg_kg_ci, # Cᵢ value for P in mg/kg
        'Pᵢ_P': round(p_phosphorus, 2),
        'K_mg_kg': k_mg_kg_ci, # Cᵢ value for K in mg/kg
        'Pᵢ_K': round(p_potassium, 2),
        'P_min_overall': round(p_min_overall, 2),
        'P_avg_overall': round(p_avg_overall, 2),
        'P综': round(p_comprehensive, 2),
        'Fertility_Grade': fertility_grade
    })

output_df = pd.DataFrame(results)

# --- 4. Output DataFrame ---
print("--- Recalculated Soil Fertility Indices and Grades (Agreed P综 Formula & New pH Table) ---")
print(output_df.to_string())

# --- 5. Note on "后勤临时管理用地" plots ---
print("\n--- Note on Excluded Plots ---")
print("The 4 '后勤临时管理用地' plots were excluded from this specific calculation because their explicit Cᵢ values (measured soil indicator values for pH, N, P, K) were not available in the provided '附件1' soil data snippets used for the 14 college farms.")
print("To include them in this fertility grading, their specific soil test data would be required.")

print("\nCalculation Details Summary:")
print("- Pᵢ_pH calculated using the new pH Pᵢ table from Turn 48.")
print("- Pᵢ for N, P, K calculated as Cᵢ/Sᵢ (capped at 3.0), with N converted to g/kg.")
print("- P_min_overall is the minimum of (Pᵢ_pH, Pᵢ_N, Pᵢ_P, Pᵢ_K).")
print("- P_avg_overall is the average of (Pᵢ_pH, Pᵢ_N, Pᵢ_P, Pᵢ_K).")
print("- P综 calculated using the formula: P综 = [ (P_min_overall)² + (P_avg_overall)² ] / 2 * √[(N-1)/N], with N=4.")
print("- Fertility grades based on P综 (I: >1.7, II: 0.9-1.7, III: <0.9).")
