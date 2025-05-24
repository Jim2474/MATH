import matplotlib
matplotlib.use('Agg') # Use a non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd

# NEW Data for Soil Fertility Distribution (18 farms total)
# Grade I: 0
# Grade II: 17 (13 original colleges + 4 '后勤' plots)
# Grade III: 1 ('学院9')
new_fertility_grades_counts = {'Grade I': 0, 'Grade II': 17, 'Grade III': 1}
grades = list(new_fertility_grades_counts.keys())
counts = list(new_fertility_grades_counts.values())

# Create Bar Chart
plt.figure(figsize=(8, 6))
bars = plt.bar(grades, counts, color=['#4CAF50', '#FFC107', '#F44336']) # Green, Amber, Red

# Add titles and labels
plt.title('New Soil Fertility Grade Distribution Across 18 Micro-Farms', fontsize=16)
plt.xlabel('Fertility Grade', fontsize=12)
plt.ylabel('Number of Farms', fontsize=12)
plt.xticks(fontsize=10)
plt.yticks(range(0, max(counts) + 2, 2), fontsize=10) # Adjust y-axis ticks

# Add count labels on top of bars
for bar in bars:
    yval = bar.get_height()
    if yval > 0: # Only add label if count is > 0
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.1, int(yval), ha='center', va='bottom', fontsize=10)

# Add a grid for better readability
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Save the chart
file_path = 'fertility_distribution.png' # Overwrite existing
plt.savefig(file_path)
plt.close() # Close the figure to free memory

print(f"New bar chart saved to {file_path}")

# The rest of the script (conceptual data structuring) is not needed for actual execution.
print("Visualizer script finished generating new chart.")
