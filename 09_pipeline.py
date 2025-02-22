# -----------------------------------------------
#  9. Data pipeline:
# 
#  Write a program that automates the 
#  sequential execution of previously created 
#  script files, ensuring that each script 
#  runs to completion before the next begins. 
#  This program aims to streamline the 
#  generation of outputs from all your 
#  previous files, consolidating the 
#  results into one sequence.
# -----------------------------------------------
# import required libraries
import subprocess
import sys

# Function to install nltk if not already installed
def install_nltk():
    try:
        import nltk
    except ImportError:
        print("Installing nltk...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
        import nltk

    # Download necessary nltk data
    nltk.download('stopwords')
    nltk.download('punkt')
    nltk.download('wordnet')

# Install nltk if necessary
install_nltk()

# Define the sequence of scripts to run
scripts = [
    "01_pull.py",       # Scrapes raw HTML from the website
    "02_combine.py",        # Merges multiple scraped files
    "03_parse.py",        # Parses merged HTML and extracts raw course data
    "04_clean.py",        # Cleans and standardizes the extracted data
    "05_extract.py", # Extracts course titles specifically
    "06_frequency.py",    # Performs word frequency analysis
    "07_visualization.py", # Generates visualizations for the analysis
    "08_export.py"        # Formats and exports the final dataset
]

# Function to run each script sequentially
def run_pipeline():
    for script in scripts:
        print(f"\n🚀 Running {script}...")
        # Run the script using the Python interpreter
        result = subprocess.run([sys.executable, script], capture_output=True, text=True)

        # Print script output for debugging
        print(result.stdout)
        if result.stderr:
            print(f"❌ Error in {script}:\n{result.stderr}")
            sys.exit(1)  # Stop the pipeline if any script fails

    print("\n✅ Data pipeline completed successfully!")

# Run the pipeline
if __name__ == "__main__":
    run_pipeline()