# -----------------------------------------------
#  2. Data Preparation:
# 
#  Objective: Combine multiple HTML files into 
#  a single document.
# 
#  Tools/Resources: Concatenate HTML text using 
#  python or javascript.
# -----------------------------------------------
# import libraries
import glob
import os

# Define folder and output file
# folderptah = output_dir
folderpath = os.environ.get("OUTPUT_DIR", "bu_courses")+"/"
#folderpath = "bu_courses2/"
output_file = "02_mergedhtmlsbu.html"
os.environ['OUTPUT_FILE'] = output_file # Set the environment variable so other scripts can access it

# Get all HTML files in the folder
html_files = glob.glob(folderpath + "*.html")

# Merge all HTML files into one
with open(folderpath+output_file, "w", encoding="utf-8") as outfile:
    for file in html_files:
        with open(file, "r", encoding="utf-8") as infile:
            outfile.write(infile.read() + "\n")  # Read and append content with a newline

print(f"Merged {len(html_files)} HTML files into {output_file}")