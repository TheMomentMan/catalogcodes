# -----------------------------------------------
#  14. New and Discontinued Subjects:
# 
#  Identify subjects that were offered in 
#  1996 but no longer exist in 2024, as 
#  well as new subjects introduced in 2024. 
#  Explore possible reasons for these changes.
# -----------------------------------------------
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib_venn import venn2

# Read the JSON files
with open('10_mit_1996.json') as f:
    data_1996 = json.load(f)

with open('11_mit_2024.json') as f:
    data_2024 = json.load(f)

# Convert the data to DataFrames
df_1996 = pd.DataFrame(data_1996)
df_2024 = pd.DataFrame(data_2024["courses"])

# Extract the department names
departments_1996 = set(df_1996['department'])
departments_2024 = set(df_2024['department'])

# Identify discontinued subjects (in 1996 but not in 2024)
discontinued_subjects = departments_1996 - departments_2024

# Identify new subjects (in 2024 but not in 1996)
new_subjects = departments_2024 - departments_1996

# Identify common subjects
common_subjects = departments_1996 & departments_2024

# Assign scores to each department
department_scores = {}
for dept in discontinued_subjects:
    department_scores[dept] = -1  # Red
for dept in new_subjects:
    department_scores[dept] = 1  # Green
for dept in common_subjects:
    department_scores[dept] = 0.5  # Blue

# Prepare data for the bar chart
departments = list(department_scores.keys())
scores = list(department_scores.values())

# Ensure sorting follows the order: Discontinued (-1, red), Common (0.5, blue), New (1, green)
sorted_departments, sorted_scores = zip(*sorted(zip(departments, scores), key=lambda x: x[1]))

# Define colors based on values
sorted_colors = ['red' if score == -1 else 'blue' if score == 0.5 else 'green' for score in sorted_scores]

# Plot the column chart
plt.figure(figsize=(12, 8))
bars = plt.bar(sorted_departments, sorted_scores, color=sorted_colors)
plt.ylabel("Score")
plt.xlabel("Department")
plt.title("Department Presence: 1996 vs 2024")
plt.xticks(rotation=90)  # Rotate department names for better readability

# Create a legend manually
patches = [
    mpatches.Patch(color='red', label='Discontinued (1996 Only) -1'),
    mpatches.Patch(color='blue', label='Common 0.5'),
    mpatches.Patch(color='green', label='New (2024 Only) 1')
]
plt.legend(handles=patches)

# Save the plot
plt.savefig('14_ChangeOverTime.png')
plt.show()

# Display the results
print(f"Discontinued subjects (1996 but not in 2024): {len(discontinued_subjects)}")
print(discontinued_subjects)
print(f"New subjects (2024 but not in 1996): {len(new_subjects)}")
print(new_subjects)

# Plot a Venn diagram to visualize the overlap and differences.
plt.figure(figsize=(8, 8))
venn2(subsets=(len(discontinued_subjects), len(new_subjects), len(common_subjects)),
      set_labels=('1996 Subjects', '2024 Subjects'),
      set_colors=('red', 'green'))
plt.title("Subject Changes: 1996 vs 2024")
plt.savefig('14_subj_chng_venn.png')
plt.show()

# Save the results to JSON files
with open('discontinued_subjects.json', 'w') as f:
    json.dump(list(discontinued_subjects), f, indent=4)

with open('new_subjects.json', 'w') as f:
    json.dump(list(new_subjects), f, indent=4)
