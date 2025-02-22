# -----------------------------------------------
#  10. Catalog 1996
# 
#  Extract course data from the scanned 
#  1996 MIT course catalog. After extracting 
#  the text, create a data model and save the 
#  processed data. This task emphasizes 
#  working with raw, scanned documents 
#  and aims to teach you how to extract 
#  information from non-digitized sources.
# -----------------------------------------------

#==============================================================================
#JSON SCRIPT
#==============================================================================

"""
10_extract_1996.py

Extracts course data from the merged scanned 1996 MIT course catalog.
Adds a department field to each course by looking up the alphanumeric
prefix before the '.' in the course code (e.g. "21W" from "21W.794") 
in a JSON lookup table (lookuptable.json).

Now updated to handle alphanumeric course codes such as "21h.101", 
"21w.794", "18.01A", or "21W.101-21W.102".
"""

import os
import re
import json
import sys
import fitz  # PyMuPDF

# Folder where the merged PDF is stored.
input_folder = "step10_catalog_1996"
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
    print(f"Created folder: {input_folder}")
else:
    print(f"Folder exists: {input_folder}")

# Input PDF file (merged.pdf) and output JSON file path.
pdf_file = os.path.join(input_folder, "merged.pdf")
output_json = os.path.join(input_folder, "10_mit_1996H.json")

if not os.path.exists(pdf_file):
    print(f"Error: PDF file '{pdf_file}' not found.")
    sys.exit(1)

# Load the lookup table that maps course prefix -> department name.
lookup_file = "lookuptable.json"  # Adjust path if needed
if not os.path.exists(lookup_file):
    print(f"Error: Lookup table file '{lookup_file}' not found.")
    sys.exit(1)

with open(lookup_file, "r", encoding="utf-8") as f:
    department_lookup_data = json.load(f)

# Convert lookup data into a dictionary for quick access.
department_map = {}
for item in department_lookup_data:
    course_number = item["Course Number"].strip()
    department_title = item["Course Title"].strip()
    # Store it in a dictionary, key = "21W", value = "Program in Writing..."
    department_map[course_number.upper()] = department_title

def extract_text(pdf_path):
    """
    Extracts text from the PDF using PyMuPDF.
    Returns the full extracted text as a string.
    """
    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF '{pdf_path}': {e}")
        sys.exit(1)
    
    full_text = ""
    for page_num, page in enumerate(doc, start=1):
        page_text = page.get_text("text")
        if not page_text.strip():
            print(f"Warning: No text extracted from page {page_num} of {pdf_path}")
        full_text += page_text + "\n"
    doc.close()
    return full_text

def parse_courses(text):
    """
    Splits the text into course blocks and extracts course data.
    Handles course headers that span multiple lines.
    
    For each block, the first line (plus any subsequent short lines)
    is merged into a header. Then, the header is trimmed so that any text
    starting with an open bracket "(" or the word "Prereq" (case-insensitive)
    is removed. This ensures that no bracket appears in the course title.
    """
    # Split text into blocks where each block begins with a course code.
    # This pattern now supports alphanumeric prefixes (e.g., 21W, 21h),
    # a dot, then alphanumeric again, optionally with a dash for ranges.
    blocks = re.split(r"(?=^[A-Za-z0-9]+\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+\.[A-Za-z0-9]+)?\s)", 
                      text, flags=re.MULTILINE)
    courses = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.splitlines()
        if not lines:
            continue

        # Start with the first line as the header.
        header_line = lines[0].strip()
        description_lines = lines[1:]
        
        # Merge subsequent lines if they are short (<=10 words) and do not start with "Prereq.:"
        i = 0
        while i < len(description_lines):
            curr_line = description_lines[i].strip()
            if curr_line.startswith("Prereq.:") or len(curr_line.split()) > 10:
                break
            header_line += " " + curr_line
            i += 1
        # The remaining lines are the description.
        description_lines = description_lines[i:]
        
        # Trim header_line at the first occurrence of "(" or "Prereq"
        header_line_clean = re.split(r"\(|Prereq", header_line, flags=re.IGNORECASE)[0].strip()
        
        # Updated regex to capture alphanumeric course codes like 21w.794, 21h.101, 18.01A, etc.
        header_match = re.match(
            r"^(?P<code>[A-Za-z0-9]+\.[A-Za-z0-9]+(?:-[A-Za-z0-9]+\.[A-Za-z0-9]+)?)\s+(?P<title>.+)$",
            header_line_clean
        )
        if not header_match:
            continue
        course_code = header_match.group("code").strip()
        title = header_match.group("title").strip()
        
        # Determine department by extracting everything before the first dot in course_code
        # E.g., from "21W.794" -> "21W"
        dept_key = re.match(r"^[^.]+", course_code)
        department_name = "Unknown"
        if dept_key:
            dept_key_str = dept_key.group(0).upper()
            department_name = department_map.get(dept_key_str, "Unknown")

        # Look for a line that contains "Prereq.:"
        prereq = "None"
        for line in description_lines:
            prereq_match = re.search(r"Prereq\.:\s*(.*)", line)
            if prereq_match:
                prereq = prereq_match.group(1).strip()
                break
        
        # Build the description by joining all lines (excluding any "Prereq.:" line).
        desc_lines = [line for line in description_lines if not line.startswith("Prereq.:")]
        description = " ".join(desc_lines).strip()
        description = re.sub(r"\s+", " ", description)
        
        courses.append({
            "course_code": course_code,
            "department": department_name,
            "title": title,
            "prerequisites": prereq,
            "description": description
        })
    return courses

def main():
    # Step 1: Extract raw text from the merged PDF.
    raw_text = extract_text(pdf_file)
    
    # Step 2: Parse the text to extract course data.
    courses = parse_courses(raw_text)
    if not courses:
        print("No courses found. Please check the PDF extraction or adjust the parsing rules.")
        sys.exit(1)
    
    # Step 3: Save the structured course data as JSON.
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(courses, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Extracted {len(courses)} courses from '{pdf_file}'.")
    print(f"Course data (with department) saved to '{output_json}'.")

if __name__ == "__main__":
    main()