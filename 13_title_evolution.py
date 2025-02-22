# -----------------------------------------------
#  13. Title Evolution:
# 
#  Conduct a word frequency analysis 
#  on course titles from 1996 and 2024 
#  to explore shifts in academic 
#  terminology and focus areas.
# -----------------------------------------------
# Extracting the course data from json files
import json
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from collections import Counter
import re
from wordcloud import WordCloud

# Read the json files
with open('10_mit_1996.json') as f:
    data_1996 = json.load(f)

# Read from the second json file
with open('11_mit_2024.json') as f:
    data_2024 = json.load(f)

# Convert the data to dataframes
df_1996 = pd.DataFrame(data_1996)
#df_2024 = pd.DataFrame(data_2024)
df_2024 = pd.DataFrame(data_2024["courses"])

# Get the course titlesa
course_titles_1996 = df_1996['title'].dropna()
course_titles_2024 = df_2024['course_name'].dropna()

# Preprocessing the course titles and removing stopwords
stop_words = set(stopwords.words("english"))

# Function to process text
def preprocess_titles(titles):
    word_list = []
    for title in titles:
        words = re.findall(r"\b[a-zA-Z]+\b", title.lower())  # Extract words
        words = [word for word in words if word not in stop_words]  # Remove stopwords
        word_list.extend(words)
    return word_list

# Process words for each year
word_list_1996 = preprocess_titles(course_titles_1996)
word_list_2024 = preprocess_titles(course_titles_2024)

# Perform word frequency count
word_counts_1996 = Counter(word_list_1996)
word_counts_2024 = Counter(word_list_2024)

# Get the top 20 most common words
common_words_1996 = word_counts_1996.most_common(20)
common_words_2024 = word_counts_2024.most_common(20)

# Convert to DataFrame for visualization
df_common_1996 = pd.DataFrame(common_words_1996, columns=["Word", "Frequency"])
df_common_2024 = pd.DataFrame(common_words_2024, columns=["Word", "Frequency"])

# Plot side-by-side bar charts
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

axes[0].barh(df_common_1996["Word"], df_common_1996["Frequency"], color='blue')
axes[0].invert_yaxis()
axes[0].set_title("Top 20 Words in Course Titles (1996)")
axes[0].set_xlabel("Frequency")

axes[1].barh(df_common_2024["Word"], df_common_2024["Frequency"], color='red')
axes[1].invert_yaxis()
axes[1].set_title("Top 20 Words in Course Titles (2024)")
axes[1].set_xlabel("Frequency")

plt.tight_layout()
plt.show()

# Generate word clouds
wordcloud_1996 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts_1996)
wordcloud_2024 = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_counts_2024)

# Display word clouds
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].imshow(wordcloud_1996, interpolation='bilinear')
axes[0].axis("off")
axes[0].set_title("Word Cloud of Course Titles (1996)")

axes[1].imshow(wordcloud_2024, interpolation='bilinear')
axes[1].axis("off")
axes[1].set_title("Word Cloud of Course Titles (2024)")

plt.tight_layout()
plt.show()
#save the plot
plt.savefig('word_clouds.png')

# Compute word frequency changes
df_word_changes = pd.DataFrame.from_dict(word_counts_2024, orient='index', columns=['2024'])
df_word_changes['1996'] = df_word_changes.index.map(lambda word: word_counts_1996.get(word, 0))
df_word_changes['Change'] = df_word_changes['2024'] - df_word_changes['1996']
df_word_changes = df_word_changes.sort_values(by='Change', ascending=False).head(20)

# Plot word frequency changes
plt.figure(figsize=(10, 6))
plt.barh(df_word_changes.index, df_word_changes['Change'], color=['green' if x > 0 else 'red' for x in df_word_changes['Change']])
plt.xlabel("Frequency Change")
plt.ylabel("Word")
plt.title("Top 20 Words with Greatest Change in Frequency (2024 vs. 1996)")
plt.gca().invert_yaxis()
plt.show()
# Save the plot
plt.savefig('word_frequency_changes.png')