# -----------------------------------------------
#   4. Data Cleaning:
# 
#   Objective: Clean and preprocess the 
#   extracted data for analysis.
# 
#   Tools/Resources: Use Regular Expressions 
#   or string manipulation functions in 
#   your programming language.
# -----------------------------------------------
import json
import re
import os
from bs4 import BeautifulSoup

# Load the raw parsed JSON file
parsed_file = os.environ.get("Output_JSON", "03_parsed_courses.json")
#parsed_file = "parsed_courses.json"
with open("output_folder/"+parsed_file, "r", encoding="utf-8") as file:
    raw_courses = json.load(file)

# Function to clean HTML tags
def clean_html_tags(text):
    """Removes HTML tags and trims spaces from text.""" 
    if not text:
        return "N/A"
    return re.sub(r"<.*?>", "", text).strip()

# Process and clean data
cleaned_courses = []

for course in raw_courses:
    cleaned_course = {
        "title": clean_html_tags(course["title"]),
        "code": clean_html_tags(course["code"]).upper(),
        "description": clean_html_tags(course["description"]),
        "units": int(clean_html_tags(course["units"])) if course["units"].isdigit() else "N/A",
        "schedule": []
    }

    # Process the schedule data
    for row in course["schedule"]:
        cleaned_course["schedule"].append({
            "section": clean_html_tags(row["section"]),
            "instructor": clean_html_tags(row["instructor"]),
            "location": clean_html_tags(row["location"]),
            "schedule": clean_html_tags(row["schedule"]),
            "notes": clean_html_tags(row["notes"])
        })

    cleaned_courses.append(cleaned_course)

# Save the cleaned data to a new JSON file
cleaned_file = "04_cleaned_courses.json"
with open('output_folder/'+cleaned_file, "w", encoding="utf-8") as file:
    json.dump(cleaned_courses, file, indent=4)

os.environ['Cleaned_JSON'] = cleaned_file
print(f"Data cleaning complete. Cleaned data saved to {cleaned_file}")
