import matplotlib
matplotlib.use('Agg') # Use a non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd

# Data for Soil Fertility Distribution
# Based on Step 4/6 outputs: 1 Grade I, 1 Grade III, 16 Grade II (12 original + 4 '后勤' assumed II)
fertility_grades_counts = {'Grade I': 1, 'Grade II': 16, 'Grade III': 1}
grades = list(fertility_grades_counts.keys())
counts = list(fertility_grades_counts.values())

# Create Bar Chart
plt.figure(figsize=(8, 6))
bars = plt.bar(grades, counts, color=['#4CAF50', '#FFC107', '#F44336']) # Green, Amber, Red

# Add titles and labels
plt.title('Soil Fertility Grade Distribution Across Micro-Farms', fontsize=16)
plt.xlabel('Fertility Grade', fontsize=12)
plt.ylabel('Number of Farms', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(range(0, max(counts) + 2, 2), fontsize=10) # Adjust y-axis ticks

# Add count labels on top of bars
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=10)

# Add a grid for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the chart
file_path = 'fertility_distribution.png'
plt.savefig(file_path)
plt.close() # Close the figure to free memory

print(f"Bar chart saved to {file_path}")

# Data for Optimized Planting Plan Table (to be used in the report text)
# This part is more for structuring the data for the text report
# Actual data will be taken from Step 6 output directly in the report generation phase.
# Here's a conceptual representation of how it would be enriched:

crop_details_data = {
    '西蓝花': {'Planting_Season': '秋季', 'Growth_Cycle_days': '80~100天'},
    '凉薯': {'Planting_Season': '春季', 'Growth_Cycle_days': '120~150天'},
    '蒜': {'Planting_Season': '秋季', 'Growth_Cycle_days': '青蒜：30~50天；蒜头：90~120天'}
    # Add other crops from the optimized plan as needed
}

# Example of how the planting plan might be enriched (actual enrichment in the main report text)
# planting_plan_from_step6 = [
# {'Farm_Name': '学院1', 'Fertility_Grade': 'I', 'Crop_Name': '西蓝花', 'Area_m2_Allocated': 610.0, 'Expected_Profit_from_Crop': 30271.25},
# ... (other plan data)
# ]

# enriched_plan = []
# for item in planting_plan_from_step6:
#     crop_info = crop_details_data.get(item['Crop_Name'], {'Planting_Season': 'N/A', 'Growth_Cycle_days': 'N/A'})
#     item.update(crop_info)
#     enriched_plan.append(item)

# enriched_df = pd.DataFrame(enriched_plan)
# print("\nEnriched Planting Plan (Conceptual for Text Report):")
# print(enriched_df.to_string())
# This part is illustrative; the actual table will be built in the report text.
print("Visualizer script finished conceptual data structuring for report.")
