# -----------------------------------------------
#  8. Export a Clean Formatted Dataset
#  of the Entire University Catalog:
# 
#  Export a Clean Formatted Dataset of 
#  the Entire University Catalog: The 
#  dataset you would have liked when you 
#  started. Prepare and export a clean, 
#  well-formatted dataset encompassing 
#  the entire university catalog. This 
#  dataset should be in a form that is 
#  readily usable for analysis and 
#  visualization, reflecting the cleaned 
#  and consolidated data you've worked 
#  with throughout the project. Document 
#  the structure of your dataset, including 
#  a description of columns, data types, and 
#  any assumptions or decisions made during 
#  the data preparation process.
# -----------------------------------------------
import json
import os

# Load the existing cleaned courses JSON file
input_file = os.environ.get("Cleaned_JSON", "04_cleaned_courses.json")
#input_file = "cleaned_courses.json"  # Update this if needed

with open('output_folder/'+input_file, "r", encoding="utf-8") as f:
    courses = json.load(f)

# Helper function to extract department from course code
def extract_department(code):
    parts = code.split()
    if len(parts) >= 2:
        return parts[1]  # Extracting second part as the department
    return "Unknown"

# Process and refine the dataset
processed_courses = []
for course in courses:
    # Standardizing units field (convert "N/A" to None, ensure numeric values)
    course["units"] = None if course["units"] == "N/A" else int(course["units"])

    # Extracting department from course code
    course["department"] = extract_department(course["code"])

    # Removing redundant white spaces in description
    course["description"] = " ".join(course["description"].split())

    # Deduplicating schedules
    unique_schedules = []
    seen_schedules = set()
    for schedule in course.get("schedule", []):
        schedule_tuple = (schedule["section"], schedule["instructor"], schedule["location"], schedule["schedule"])
        if schedule_tuple not in seen_schedules:
            seen_schedules.add(schedule_tuple)
            unique_schedules.append(schedule)

    course["schedule"] = unique_schedules

    # Append processed course
    processed_courses.append(course)

# Save the refined dataset in JSON format
output_file = "08_refined_courses.json"
with open('output_folder/'+output_file, "w", encoding="utf-8") as f:
    json.dump(processed_courses, f, indent=4, ensure_ascii=False)

print(f"Dataset exported successfully as {output_file}")