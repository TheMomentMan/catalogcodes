# -----------------------------------------------
#  6. Word Frequency Analysis:
# 
#  Objective: Perform a word frequency count 
#  on the course titles.
# 
#  Tools/Resources: You can use a “map reduce” 
#  style word counting approach.
# -----------------------------------------------
import re
import os
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
import nltk

# Ensure stopwords are downloaded
#nltk.download('stopwords')

# Load the course titles from the text file
course_titles_file = os.environ.get("Output_TXT", "05_course_titles.txt")
#course_titles_file = "course_titles.txt"  # Update the path as needed

with open("output_folder/"+course_titles_file, "r", encoding="utf-8") as file:
    course_titles = file.readlines()

# Use NLTK stopwords for a more comprehensive list
stop_words = set(stopwords.words("english"))

# Preprocessing: Convert to lowercase, remove punctuation, and split into words
word_list = []
for title in course_titles:
    words = re.findall(r"\b[a-zA-Z]+\b", title.lower())  # Extract words
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    word_list.extend(words)

# Perform word frequency count using a MapReduce-style approach
word_counts = Counter(word_list)

# Convert to a sorted list of tuples (word, count) ordered by frequency
sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

# Save results to a CSV file
output_csv_file = "06_word_frequencies.csv"
df_word_freq = pd.DataFrame(sorted_word_counts, columns=["Word", "Frequency"])
df_word_freq.to_csv('output_folder/'+output_csv_file, index=False)

# Display top 10 most common words
""" print("\nTop 10 Most Common Words in Course Titles:")
for word, count in sorted_word_counts[:10]:
    print(f"{word}: {count}") """

os.environ['WordFreq'] = output_csv_file
print(f"\nWord frequency analysis complete.")
print(f"- CSV saved as: {output_csv_file}")
