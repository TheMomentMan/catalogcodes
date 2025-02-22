# -----------------------------------------------
#  1. Data Acquisition:
# 
#  Objective: Download all the public course 
#  catalog data in raw HTML format from a 
#  university website.
# 
#  Tools/Resources: Extract all the course 
#  catalog data from one of the follow 
#  three universities:
#     Harvard: https://courses.my.harvard.edu
#     BU: https://www.bu.edu/academics/cas/courses
#     NE: https://catalog.northeastern.edu/course-descriptions
# -----------------------------------------------
# Importing required libraries
import os
import requests
from bs4 import BeautifulSoup

# Base URL structure
base_url = "https://www.bu.edu"
course_pages_base = "https://www.bu.edu/academics/cas/courses/"

# Directory to store downloaded course HTML files
output_dir = "bu_courses"
os.makedirs(output_dir, exist_ok=True)

os.environ['OUTPUT_DIR'] = output_dir # Set the environment variable so other scripts can access it

# Function to get course links from a page
def get_course_links(page_url):
    """Extracts all course page links from a course listing page."""
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to fetch {page_url}, Status: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    course_links = []
    
    for link in soup.select("ul.course-feed a"):  # Ensure this selector matches the website
        href = link.get("href")
        if href and href.startswith("/academics/cas/courses/"):
            course_links.append(base_url + href)

    return course_links

# Function to save course pages
def save_course_page(course_url):
    """Downloads and saves a course page as an HTML file."""
    response = requests.get(course_url)
    if response.status_code == 200:
        course_code = course_url.rstrip("/").split("/")[-1]
        file_path = os.path.join(output_dir, f"{course_code}.html")
        
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        
        print(f"Saved: {file_path}")
    else:
        print(f"Failed to fetch {course_url}, Status: {response.status_code}")

# Loop through course listing pages
page_num = 1
while True:
    page_url = f"{course_pages_base}{page_num}/"
    print(f"Fetching course list from: {page_url}")

    course_links = get_course_links(page_url)

    if not course_links:
        print(f"No more courses found. Stopping at page {page_num}.")
        break  # Stop if no course links are found

    for course_url in course_links:
        save_course_page(course_url)

    page_num += 1  # Move to the next page

print("All course pages have been downloaded.")

