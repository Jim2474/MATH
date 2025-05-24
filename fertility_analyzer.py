import pandas as pd
import io

csv_data = """学院,温度,水分,电导率,pH,氮,磷,钾,肥力
学院1,17.7,22.6,1003.0,8.0,50.0,70.0,160.0,551.0
学院2,17.4,20.3,379.0,8.0,18.0,26.0,60.0,208.0
学院3,14.6,21.8,306.0,8.0,15.0,21.0,48.0,168.0
学院4,16.8,33.5,602.1,8.1,31.0,43.0,97.0,332.0
学院5,17.8,23.0,430.0,8.0,21.0,30.0,68.0,236.0
学院6,15.1,28.1,439.0,8.0,21.0,30.0,70.0,241.0
学院7,17.4,20.3,317.0,8.0,15.0,22.0,50.0,174.0
学院8,19.2,29.3,457.0,8.0,22.0,31.0,73.0,251.0
学院9,15.6,19.9,283.0,8.0,14.0,19.0,45.0,155.0
学院10,15.5,28.6,763.0,8.0,38.0,53.0,122.0,419.0
学院11,14.7,26.8,722.0,8.0,36.0,50.0,115.0,397.0
学院12,18.8,36.7,605.0,8.0,30.0,42.0,96.0,332.0
学院13,15.8,18.3,294.0,8.0,14.0,20.0,47.0,161.0
学院14,15.1,26.3,438.0,8.0,21.0,30.0,70.0,240.0
"""

soil_df = pd.read_csv(io.StringIO(csv_data))
soil_df = soil_df.set_index('学院')

print("--- Soil Fertility Analysis Report ---")
print("Based on '附件1 校园微农场土壤指标.xlsx' data and '附件2.txt' (南方地区耕地土壤肥力诊断与评价标准)")

print("\n1. Available Soil Data for Key Indicators:")
key_indicators_df = soil_df[['pH', '氮', '磷', '钾']]
print(key_indicators_df)
print("\n   Units: 氮 (Nitrogen mg/kg), 磷 (Phosphorus mg/kg), 钾 (Potassium mg/kg)")

print("\n2. Consultation of '附件2.txt' Standard:")
print("   - The standard '附件2.txt' primarily describes a Soil Fertility Comprehensive Index (P综).")
print("   - Calculation of P综 requires a minimum of N=10 soil indicators. Our data provides 4 key indicators for this purpose (pH, N, P, K).")
print("   - The P综 formula also relies on single-item fertility indices (Pᵢ = Cᵢ/Sᵢ), where Sᵢ are standard values. These Sᵢ values are not provided in the text of '附件2.txt'.")
print("   - '附件2.txt' lists '有机质' (Organic Matter), '阳离子交换量' (CEC), and '质地' (Texture) as part of the '最小通用数据集' (minimal universal dataset) which must be measured. These are MISSING from our soil data.")
print("   - The standard DOES NOT PROVIDE explicit classification tables (e.g., low/medium/high thresholds) for individual raw values of pH, Total Nitrogen (mg/kg), Available Phosphorus (mg/kg), or Available Potassium (mg/kg) outside the context of Pᵢ calculation for P综.")

print("\n3. Classification of Individual Indicators (pH, N, P, K):")
print("   - Due to the lack of specific classification thresholds or Sᵢ values in '附件2.txt' for individual indicators, we CANNOT classify the measured pH, Nitrogen, Phosphorus, and Potassium values into fertility levels (e.g., low, medium, high) or calculate Pᵢ scores based SOLELY on this standard.")
print("   - Any such classification would require external standards or assumptions not present in '附件2.txt'.")

print("\n4. Conclusion on P综 Calculation and Overall Fertility Assessment:")
print("   - The Soil Fertility Comprehensive Index (P综) CANNOT be calculated because:")
print("     1. The number of available key indicators (N=4: pH, N, P, K) is less than the required minimum of N=10.")
print("     2. Critical data from the minimal dataset, most notably '有机质' (Organic Matter), is missing.")
print("     3. Standard values (Sᵢ) required for calculating individual fertility indices (Pᵢ) are not defined in the provided text of '附件2.txt'.")
print("   - '附件2.txt' does not offer an alternative assessment method when P综 cannot be calculated or when essential data is missing.")

print("\n5. Regarding the '肥力' column in soil data:")
print("   - The '肥力' column from '附件1 校园微农场土壤指标.xlsx' is not defined in '附件2.txt'. Therefore, its interpretation or use in fertility assessment according to this standard is not possible.")

print("\n6. Summary of Limitations:")
print("   - The primary limitation is that '附件2.txt' is geared towards a comprehensive P综 index, for which our current dataset is insufficient due to:")
print("     a) Missing several 'must-measure' indicators (Organic Matter, CEC, Texture).")
print("     b) An insufficient number of total indicators (4 available vs. 10 required for P综).")
print("     c) Lack of defined 'standard values' (Sᵢ) in the provided text for the available indicators.")
print("   - Without these, or alternative classification tables within '附件2.txt', a quantitative or qualitative fertility assessment as per this specific standard cannot be completed for individual indicators or overall fertility.")
print("   - Further assessment would require either making assumptions outside the provided standard, using a different standard, or collecting the missing soil data.")

print("\nReport End.")
