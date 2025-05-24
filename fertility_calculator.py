import pandas as pd
import numpy as np
import io

# --- 1. Parse Soil Data ---
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

# Use StringIO to simulate reading from a file, splitting by tab
data = io.StringIO(raw_soil_data_text)
# Columns based on typical structure: Farm, Temp, Moisture, Conductivity, pH, N, P, K, Fertility
# We only need Farm, pH, N, P, K for this task
# Indices: Farm (0), pH (4), N (5), P (6), K (7)
parsed_data = []
for line in data:
    parts = line.strip().split('\t')
    farm_name = parts[0]
    ph_val = float(parts[4])
    # Extract numeric part of N, P, K and convert
    n_val_mg_kg = float(parts[5].replace('mg/kg', ''))
    p_val_mg_kg = float(parts[6].replace('mg/kg', ''))
    k_val_mg_kg = float(parts[7].replace('mg/kg', ''))
    parsed_data.append({
        'Farm_Name': farm_name,
        'pH_value': ph_val,
        'N_mg_per_kg': n_val_mg_kg,
        'P_mg_per_kg': p_val_mg_kg,
        'K_mg_per_kg': k_val_mg_kg
    })
soil_df = pd.DataFrame(parsed_data)

# --- 2. Define Standard Values (Sᵢ) and pH Pᵢ Scoring ---
S_values = {
    'Organic_Matter_g_per_kg': 12.5, # Not used in calculation as C_i is missing
    'Total_Nitrogen_g_per_kg': 1.0,
    'Available_Phosphorus_mg_per_kg': 7.5,
    'Available_Potassium_mg_per_kg': 80.0
}

def calculate_ph_pi(ph):
    if ph <= 5.8: # Covers ≤5.0 and 5.0<pH≤5.8, both Pᵢ=1.0
        return 1.0
    elif 5.8 < ph <= 6.0:
        return 1.5
    elif 6.0 < ph <= 7.0:
        return 2.0
    elif 7.0 < ph <= 7.5:
        return 2.5
    elif 7.5 < ph <= 8.0:
        return 3.0
    elif ph > 8.0: # pH > 8.0
        return 1.0
    return np.nan # Should not happen with valid pH

# --- 3. Calculations ---
results = []
N_indicators = 4 # pH, N, P, K

for index, row in soil_df.iterrows():
    farm_name = row['Farm_Name']
    
    # Pᵢ for pH
    ph_value = row['pH_value']
    p_ph = calculate_ph_pi(ph_value)
    
    # Prepare Cᵢ for N, P, K
    c_nitrogen_mg_kg = row['N_mg_per_kg']
    c_nitrogen_g_kg = c_nitrogen_mg_kg / 1000.0 # Convert N from mg/kg to g/kg
    
    c_phosphorus_mg_kg = row['P_mg_per_kg']
    c_potassium_mg_kg = row['K_mg_per_kg']
    
    # Calculate Pᵢ for N, P, K (Cᵢ/Sᵢ, capped at 3)
    p_nitrogen = min(c_nitrogen_g_kg / S_values['Total_Nitrogen_g_per_kg'], 3.0)
    p_phosphorus = min(c_phosphorus_mg_kg / S_values['Available_Phosphorus_mg_per_kg'], 3.0)
    p_potassium = min(c_potassium_mg_kg / S_values['Available_Potassium_mg_per_kg'], 3.0)
    
    # Compile Pᵢ values
    pi_values = [p_ph, p_nitrogen, p_phosphorus, p_potassium]
    
    # Calculate P_min and P_avg
    p_min = min(pi_values)
    p_avg = sum(pi_values) / len(pi_values)
    
    # Calculate P综
    # P综 = ((P_min)^2 + (P_avg)^2) / 2 * sqrt((N-1)/N)
    p_comprehensive = ((p_min**2) + (p_avg**2)) / 2 * np.sqrt((N_indicators - 1) / N_indicators)
    
    # Assign Fertility Grades
    fertility_grade = ''
    if p_comprehensive > 1.7:
        fertility_grade = 'I'
    elif 0.9 <= p_comprehensive <= 1.7:
        fertility_grade = 'II'
    else: # P综 < 0.9
        fertility_grade = 'III'
        
    results.append({
        'Farm_Name': farm_name,
        'pH_value': ph_value,
        'P_pH': p_ph,
        'N_g_per_kg_Ci': round(c_nitrogen_g_kg, 4), # Store C_i for N
        'S_Nitrogen_g_per_kg': S_values['Total_Nitrogen_g_per_kg'],
        'P_Nitrogen': round(p_nitrogen, 2),
        'P_mg_per_kg_Ci': c_phosphorus_mg_kg, # Store C_i for P
        'S_Phosphorus_mg_per_kg': S_values['Available_Phosphorus_mg_per_kg'],
        'P_Phosphorus': round(p_phosphorus, 2),
        'K_mg_per_kg_Ci': c_potassium_mg_kg, # Store C_i for K
        'S_Potassium_mg_per_kg': S_values['Available_Potassium_mg_per_kg'],
        'P_Potassium': round(p_potassium, 2),
        'P_min': round(p_min, 2),
        'P_avg': round(p_avg, 2),
        'P_Comprehensive': round(p_comprehensive, 2),
        'Fertility_Grade': fertility_grade
    })

output_df = pd.DataFrame(results)

# --- 4. Output DataFrame ---
print("--- Calculated Soil Fertility Indices and Grades ---")
print(output_df.to_string())

# --- 5. Textual Summary ---
print("\n--- Summary and Limitations ---")
print("1. Organic Matter: The Pᵢ for Organic Matter was not included in the P综 calculation as its measured value (Cᵢ) is missing from the provided soil data.")
print(f"2. Number of Indicators (N): The P综 was calculated using N={N_indicators} indicators (pH, Nitrogen, Phosphorus, Potassium). This is less than the N>=10 guideline mentioned in '附件2.txt'. The formula was applied as specified with N=4.")
print("3. Pᵢ Capping: Pᵢ values for Nitrogen, Phosphorus, and Potassium were capped at 3.0 as per standard practice when Pᵢ > 3 (from 附件2.txt Section 7.2.2 description for P_min and P_avg calculation).")
print("4. pH Pᵢ Scoring: pH Pᵢ values were determined using the provided Table C.2 scoring rules.")
print("5. Nitrogen Unit Conversion: Nitrogen values from soil data (mg/kg) were converted to g/kg before calculating Pᵢ, aligning with the unit of its Sᵢ value.")

# Further analysis of results (optional, can be done by inspecting the DataFrame)
avg_p_comprehensive = output_df['P_Comprehensive'].mean()
grade_counts = output_df['Fertility_Grade'].value_counts().to_dict()

print(f"\nOverall Average P_Comprehensive: {avg_p_comprehensive:.2f}")
print(f"Distribution of Fertility Grades: {grade_counts}")

# Check for any P_i consistently being the P_min
min_contributors = []
for index, row in output_df.iterrows():
    pis = {'P_pH': row['P_pH'], 'P_Nitrogen': row['P_Nitrogen'], 
           'P_Phosphorus': row['P_Phosphorus'], 'P_Potassium': row['P_Potassium']}
    current_p_min_val = row['P_min']
    for name, val in pis.items():
        if round(val,2) == current_p_min_val: # Compare rounded values
            min_contributors.append(name)
            break # Count first one only for simplicity or count all if needed

from collections import Counter
min_contributor_counts = Counter(min_contributors)
print(f"Factors most often being P_min: {min_contributor_counts}")
