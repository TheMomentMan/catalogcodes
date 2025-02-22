# -----------------------------------------------
#  5. Data Extraction:
# 
#  Objective: Extract course titles from 
#  the data you cleaned.
# -----------------------------------------------
import json
import os

# Load the cleaned JSON file
cleaned_file = os.environ.get("Cleaned_JSON", "04_cleaned_courses.json")
#cleaned_file = "cleaned_courses.json"
with open("output_folder/"+cleaned_file, "r", encoding="utf-8") as file:
    cleaned_courses = json.load(file)

# Extract course titles
course_titles = [course["title"] for course in cleaned_courses if "title" in course]

# Save extracted course titles to a text file
output_file = "05_course_titles.txt"
with open('output_folder/'+output_file, "w", encoding="utf-8") as file:
    for title in course_titles:
        file.write(title + "\n")
os.environ['Output_TXT'] = output_file
print(f"Course titles extracted and saved to {output_file}")
