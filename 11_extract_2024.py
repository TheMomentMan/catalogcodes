# -----------------------------------------------
#  11. Catalog 2024
# 
#  Extract course data from the current 
#  MIT course catalog. After extracting the 
#  text, create a data model and save the 
#  processed data.
# -----------------------------------------------
import requests
from bs4 import BeautifulSoup
import os
import string
import time
import glob
import json
import re

# Base URL for MIT catalog
INDEX_URL = "https://student.mit.edu/catalog/index.cgi"
BASE_URL = "https://student.mit.edu/catalog/"
OUTPUT_DIR = "mit_course_pages4"

# Create directory to store downloaded HTML pages
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_department_links():
    """Scrape the index page to get all department primary links."""
    response = requests.get(INDEX_URL)
    if response.status_code != 200:
        raise Exception("Failed to fetch the index page")
    
    soup = BeautifulSoup(response.text, "html.parser")
    department_links = []
    
    for link in soup.find_all("a", href=True):
        href = link["href"]
        if href.endswith("a.html"):  # Primary department links
            department_links.append(href[:-6])  # Extract base (e.g., 'm1' from 'm1a.html')
    
    return department_links

def download_course_pages(department):
    """Download all course pages for a given department by iterating through tabs."""
    tab_suffix = list(string.ascii_lowercase)  # 'a' to 'z'
    tab_index = 0
    
    while True:
        page_url = f"{BASE_URL}{department}{tab_suffix[tab_index]}.html"
        response = requests.get(page_url)
        
        if response.status_code == 200:
            file_path = os.path.join(OUTPUT_DIR, f"{department}{tab_suffix[tab_index]}.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            print(f"Downloaded: {page_url}")
            tab_index += 1  # Move to next tab
        else:
            print(f"No more pages for {department}, stopping at {tab_suffix[tab_index]}.")
            break  # Stop when a page is not found
        
        time.sleep(1)  # Respectful crawling

if __name__ == "__main__":
    print("Fetching department links...")
    department_links = get_department_links()
    
    for dept in department_links:
        print(f"Processing department: {dept}")
        download_course_pages(dept)
    
    print("All course pages downloaded successfully!")

# merge all the html files in the output folder into one file
output_file = "Mit2024courses.html"

# Get all HTML files in the folder
html_files = glob.glob(OUTPUT_DIR + "/"+ "*.html")

# Merge all HTML files into one
with open(OUTPUT_DIR+"/"+output_file, "w", encoding="utf-8") as outfile:
    for file in html_files:
        with open(file, "r", encoding="utf-8") as infile:
            outfile.write(infile.read() + "\n")  # Read and append content with a newline

print(f"Merged {len(html_files)} HTML files into {output_file}")

#=============================================================================
# CONVERT TO JSON SCRIPT
#=============================================================================

def parse_course_p(p_tag, current_department):
    """
    Parse a single <p> tag containing a course.
    Returns a dictionary with the following keys:
      department, course_code, course_name, Grad_UG, other_info,
      prereq, units, location, description, instructor.
    """
    # Decode the inner HTML and split on <br> tags
    p_html = p_tag.decode_contents()
    parts = re.split(r'<br\s*/?>', p_html)
    # Remove empty parts and strip each
    parts = [BeautifulSoup(part, "html.parser").get_text(" ", strip=True) for part in parts if part.strip()]

    # 1. First part: the <h3> tag containing course code and course name.
    # Parse the first part as HTML to get the text from the h3 tag.
    soup_h3 = BeautifulSoup(parts[0], "html.parser")
    h3 = soup_h3.find("h3")
    if h3:
        header_text = h3.get_text(" ", strip=True)
    else:
        header_text = parts[0]
    m = re.match(r'([\d\.]+)\s+(.*)', header_text)
    if m:
        course_code = m.group(1).strip()
        course_name = m.group(2).strip()
    else:
        course_code = ""
        course_name = header_text

    # 2. Grad_UG: in the next part, find an <img> with title Undergrad or Graduate.
    soup_part1 = BeautifulSoup(parts[1], "html.parser") if len(parts) > 1 else None
    grad_img = None
    if soup_part1:
        grad_img = soup_part1.find("img", attrs={"title": re.compile(r'^(Undergrad|Graduate)$', re.I)})
    Grad_UG = grad_img["title"].strip() if grad_img and grad_img.has_attr("title") else None

    # 3. other_info: next part that contains "Subject meets with" (if any)
    other_info = None
    if len(parts) > 2 and "Subject meets with" in parts[2]:
        other_info = parts[2].strip()

    # 4. prereq: look for part starting with "Prereq:".
    prereq = None
    for part in parts:
        if part.startswith("Prereq:"):
            prereq = part[len("Prereq:"):].strip()
            break

    # 5. units: look for part starting with "Units:".
    units = None
    for part in parts:
        if part.startswith("Units:"):
            units = part[len("Units:"):].strip()
            break

    # 6. location: look for part that includes "Lecture:" or "Lab:".
    location = None
    for part in parts:
        if "Lecture:" in part or "Lab:" in part:
            location = part.strip()
            break

    # 7. description: find the part that comes after a horizontal rule image.
    # We assume one part is exactly a series of underscores (the hr image alt text becomes "______").
    # So take the part immediately after that.
    description = ""
    hr_index = None
    for i, part in enumerate(parts):
        if "______" in part:
            hr_index = i
            break
    if hr_index is not None and hr_index + 1 < len(parts):
        description = parts[hr_index + 1].strip()

    # 8. instructor: look for the part that contains an <i> tag.
    instructor = None
    for part in parts:
        # We use BeautifulSoup to check for an <i> tag.
        soup_part = BeautifulSoup(part, "html.parser")
        i_tag = soup_part.find("i")
        if i_tag:
            instructor = i_tag.get_text(" ", strip=True)
            break

    # Return the course dictionary.
    return {
        "department": current_department,
        "course_code": course_code,
        "course_name": course_name,
        "Grad_UG": Grad_UG,
        "other_info": other_info,
        "prereq": prereq,
        "units": units,
        "location": location,
        "description": description,
        "instructor": instructor
    }

def parse_courses(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    
    # Extract the department from the <h1> header.
    # Example: <h1>Course 1: Civil and Environmental Engineering<br>IAP/Spring 2025</h1>
    h1 = soup.find("h1")
    if h1:
        dept_raw = h1.get_text(" ", strip=True)
        # Remove "Course X:" prefix.
        m_dept = re.search(r'^Course\s+[^:]+:\s*(.*)', dept_raw)
        if m_dept:
            department = m_dept.group(1).strip()
        else:
            department = dept_raw
        # Remove any occurrence of "IAP/Spring" and a year.
        department = re.sub(r'\s*IAP/Spring(\s*\d{4})?', '', department).strip()
    else:
        department = ""

    # For each <p> tag that contains an <h3>, parse a course.
    courses = []
    for p_tag in soup.find_all("p"):
        if p_tag.find("h3"):
            course = parse_course_p(p_tag, department)
            courses.append(course)
    return {"courses": courses}

if __name__ == '__main__':
    html_file = "mit_course_pages3/Mit2024courses.html"  # Replace with your HTML file path
    data = parse_courses(html_file)
    print(json.dumps(data, indent=2))


#save the output to a file
with open("11_mit_2024.json", "w") as f:
    json.dump(data, f, indent=2)

