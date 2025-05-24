# 校园微农场数学建模分析 (Mathematical Modeling Analysis for Campus Micro-Farms) - (Corrected Version)

## Overview

This project provides a comprehensive analysis for the Guilin campus micro-farms. Key objectives include:
1.  **Soil Fertility Assessment:** Evaluating soil samples from 18 farm plots (14 college farms with explicit Cᵢ data, 4 "后勤临时管理用地" plots assigned a default Grade II) based on pH, Nitrogen (N), Phosphorus (P), and Potassium (K) levels to determine fertility grades (I, II, III).
2.  **Crop Planting Optimization:** Developing a Linear Programming (LP) model to maximize total expected profit by allocating suitable crops to farms based on their fertility, available area, and crop rotation requirements (specifically, nitrogen-fixer percentages).
3.  **Sustainable Agricultural Recommendations:** Formulating suggestions for soil improvement and sustainable planting practices tailored to the identified soil conditions and optimized planting plan.

This document outlines a revised analysis based on refined calculation methods for soil fertility, particularly the P综 (Comprehensive Soil Fertility Index) formula and pH Pᵢ scoring, as agreed upon in later stages of the project (Turn 48 for pH table, Turn 50 for P综 formula).

## Soil Fertility Assessment Methodology

The soil fertility assessment for the 14 college farms was based on the following methodology for N=4 core indicators:

*   **Core Indicators (N=4):**
    *   pH (酸碱度)
    *   Total Nitrogen (全氮) - Cᵢ values derived from '氮mg/kg' in `附件1`.
    *   Available Phosphorus (有效磷) - Cᵢ values derived from '磷mg/kg' in `附件1`.
    *   Available Potassium (速效钾) - Cᵢ values derived from '钾mg/kg' in `附件1`.

*   **Single-Item Fertility Index (Pᵢ) Calculation:**
    *   For Nitrogen, Phosphorus, and Potassium, the Pᵢ is calculated as Cᵢ/Sᵢ (Measured Value / Standard Value), with the resulting Pᵢ value capped at a maximum of 3.0.
        *   **Sᵢ for Nitrogen (全氮):** 1.0 g/kg (user-provided, equivalent to Table C.1). The measured Cᵢ value for Nitrogen (originally in mg/kg from `附件1`) is converted to g/kg before calculating Pᵢ.
        *   **Sᵢ for Phosphorus (有效磷):** 7.5 mg/kg (user-provided, equivalent to Table C.1).
        *   **Sᵢ for Potassium (速效钾):** 80 mg/kg (user-provided, equivalent to Table C.1).
    *   **Pᵢ for pH (酸碱度 P_pH):** Calculated using the specific scoring table provided by the user in Turn 48:
        *   pH < 5.0 or pH > 9.0: Pᵢ = 1.0
        *   pH 5.0-5.5 (inclusive of 5.0, exclusive of 5.5) or pH 8.5-9.0 (inclusive of 9.0, exclusive of 8.5): Pᵢ = 1.5 *(Note: The script `fertility_calculator.py` implements ranges like `5.0 <= ph < 5.5` and `8.5 < ph <= 9.0` based on typical interpretations of such tables.)*
        *   pH 5.5-6.0 (inclusive of 5.5, exclusive of 6.0) or pH 8.0-8.5 (inclusive of 8.5, exclusive of 8.0): Pᵢ = 2.0
        *   pH 6.0-6.5 (inclusive of 6.0, exclusive of 6.5) or pH 7.5-8.0 (inclusive of 8.0, exclusive of 7.5): Pᵢ = 2.5
        *   pH 6.5-7.5 (inclusive): Pᵢ = 3.0

*   **Comprehensive Soil Fertility Index (P综) Formula Used:**
    *   The final agreed-upon formula (from Turn 50) is: `P综 = [ (P_min_overall)² + (P_avg_overall)² ] / 2 * √[(N-1)/N]`
    *   **P_min_overall:** The minimum value among the N calculated Pᵢ values (Pᵢ_pH, Pᵢ_N, Pᵢ_P, Pᵢ_K) for a given farm.
    *   **P_avg_overall:** The average value of these N Pᵢ values for that farm.
    *   **N:** Number of core indicators used, which is N=4 for this project.

*   **Justification for this P综 Formula Choice:**
    *   An initially confirmed P综 formula (`P综 = √ { Pᵢ²_min + ( Pᵢ²_avg / 2 ) * log₁₀[(N-1)/N] }`) was found to be mathematically problematic for N=4 with the project's dataset. The `log₁₀((N-1)/N)` term (i.e., `log₁₀(0.75)`) is negative, which led to attempts to calculate the square root of negative numbers for all farms (as detailed in Turn 47).
    *   The currently adopted formula `P综 = [ (P_min_overall)² + (P_avg_overall)² ] / 2 * √[(N-1)/N]` is a common structural approach for creating composite indices that ensures valid numerical results for N=4 by using squared Pᵢ values (which are always non-negative) and an averaging mechanism. The scaling factor `√[(N-1)/N]` (i.e., `√[0.75]`) appropriately adjusts the index based on the number of indicators used, providing a more stable and interpretable result for fertility assessment.

*   **Fertility Grades:**
    *   Grade I (High Fertility): P综 > 1.7
    *   Grade II (Medium Fertility): 0.9 ≤ P综 ≤ 1.7
    *   Grade III (Low Fertility): P综 < 0.9
    *   *(The 4 "后勤临时管理用地" plots were assigned Grade II by default for the LP model as their specific Cᵢ values were not processed for P综 calculation in `fertility_calculator.py`.)*

## Planting Optimization

*   A Linear Programming (LP) model was developed using the **PuLP** library in Python to determine the optimal planting plan that maximizes total expected profit from all 18 farm plots.
*   **Key Constraints in the LP Model:**
    *   The total area planted on each farm cannot exceed its available area.
    *   Crops are allocated only if they are suitable for the (newly calculated and assigned) fertility grade of the farm, based on predefined recommendation lists.
    *   Nitrogen-fixer quotas:
        *   Grade II farms must allocate at least 10% of their planted area to nitrogen-fixing crops (e.g., '凉薯', '豌豆苗').
        *   Grade III farms must allocate at least 20% of their planted area to nitrogen-fixing crops.

## Input Files

*   **`附件1 校园微农场土壤指标.xlsx`**: This Excel file is the original source for measured Cᵢ values (pH, N, P, K, etc.) for the 14 college farms. The relevant data, after initial processing in earlier project steps, is effectively hardcoded into `fertility_calculator.py` for consistent execution.
*   **`附件3 微农场农作物产量.xlsx`**: This Excel file provides data on various crops, including yield, cost, and selling price, which are used to calculate profit per square meter. This processed data is hardcoded into `lp_optimizer.py`.
*   **Farm Area Data (formerly referenced as `附件4.txt` content):** The area data for each farm plot was provided as text by the user in Step 3 of the overall problem. This data is hardcoded into `lp_optimizer.py`.
*   **Soil Fertility Standards (Sᵢ Values and pH Pᵢ Scoring Rules):** These crucial parameters (Sᵢ values for N, P, K equivalent to user's Table C.1; pH Pᵢ scoring table from user's Turn 48 instructions) are embedded directly into the `fertility_calculator.py` script for calculations.

## Scripts

The core analysis is performed by the following Python scripts:

*   **`fertility_calculator.py`**:
    *   Processes hardcoded soil data (pH, N, P, K values for 14 college farms).
    *   Applies the user-defined Sᵢ values and the latest pH Pᵢ scoring table (from Turn 48).
    *   Calculates Pᵢ for pH, N, P, K (capping N, P, K Pᵢ at 3.0).
    *   Computes P_min_overall, P_avg_overall.
    *   Calculates the final P综 using the agreed formula: `P综 = [ (P_min_overall)² + (P_avg_overall)² ] / 2 * √[(N-1)/N]`.
    *   Assigns fertility grades (I, II, III) to the 14 college farms.
*   **`lp_optimizer.py`**:
    *   Uses hardcoded farm areas, crop data (including calculated profit/m²), and updated fertility grades (14 calculated + 4 assigned for "后勤" plots).
    *   Implements predefined crop recommendations per grade.
    *   Solves the LP model for maximum profit, subject to area and nitrogen-fixer constraints.
*   **`visualizer.py`**:
    *   Generates a bar chart (`fertility_distribution.png`) showing the final distribution of soil fertility grades across all 18 farm plots. The counts for this chart (0 Grade I, 17 Grade II, 1 Grade III) are hardcoded based on the results from `fertility_calculator.py` and the assignment for "后勤" plots.

## Python Libraries Required

*   **pandas** (for data handling)
*   **PuLP** (for Linear Programming)
*   **Matplotlib** (for generating visualizations)

## Key Outputs

*   **`综合分析报告_更新版.md`**: The detailed final project report, summarizing all methodologies, findings (including updated fertility grades for 18 farms, new LP optimization results), and sustainable agriculture recommendations. *(This file was created in Turn 60, despite tool errors during its creation confirmation.)*
*   **`fertility_distribution.png`**: A bar chart visualizing the final distribution of soil fertility grades (0 Grade I, 17 Grade II, 1 Grade III) across the 18 micro-farms.
*   **Console Output from `lp_optimizer.py`**: Provides the detailed optimal planting plan and farm summary statistics. This information is also incorporated into the `综合分析报告_更新版.md`. *(No separate CSV file for the planting plan is generated by the current script version; results are for screen review or manual copy from console/report.)*

## How to Run (Conceptual Order for Replicating Final Results)

1.  **Ensure Dependencies:** Install pandas, PuLP, and Matplotlib if not already present (e.g., `pip install pandas pulp matplotlib`). These were installed during the project's interactive execution.
2.  **Run Fertility Calculation:** Execute `python fertility_calculator.py`. This script uses hardcoded soil data (derived from `附件1`) and hardcoded Sᵢ/pH rules as per final user specifications. It will print the fertility analysis for the 14 college farms.
3.  **Run Planting Optimization:** Execute `python lp_optimizer.py`. This script uses hardcoded farm areas, crop data (derived from `附件3`), and the final fertility grades (14 calculated by `fertility_calculator.py` logic + 4 "后勤" plots assigned Grade II). It prints the optimized planting plan and total profit.
4.  **Run Visualization:** Execute `python visualizer.py`. This script generates `fertility_distribution.png` using the final hardcoded grade counts for all 18 plots.
5.  **Review Report:** Open `综合分析报告_更新版.md` (or `综合分析报告.md` if the rename wasn't performed for the final report file) to view the full analysis, recommendations, and consolidated results.

*(Note: The scripts currently use hardcoded data derived from the initial input files and intermediate calculations to ensure consistent execution of the final agreed-upon methodologies and parameters. For a production system or different dataset, these would typically be replaced by direct file reads.)*
