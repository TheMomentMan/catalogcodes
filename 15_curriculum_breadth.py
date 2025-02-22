# -----------------------------------------------
#  15. Curriculum Breadth:
# 
#  Compare the breadth of topics in the 
#  1996 and 2024 catalogs to assess whether 
#  the curriculum has become more 
#  interdisciplinary or specialized.
# -----------------------------------------------
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from wordcloud import WordCloud

# Load course data
with open('10_mit_1996.json') as f:
    data_1996 = json.load(f)

with open('11_mit_2024.json') as f:
    data_2024 = json.load(f)

# Convert to DataFrames
df_1996 = pd.DataFrame(data_1996)
df_2024 = pd.DataFrame(data_2024["courses"])

# Extract course titles and departments
titles_1996 = df_1996['title'].dropna().tolist()
titles_2024 = df_2024['course_title'].dropna().tolist()

departments_1996 = df_1996['department'].dropna().tolist()
departments_2024 = df_2024['department'].dropna().tolist()

# Define interdisciplinary categories
interdisciplinary_keywords = {
    'AI': ['machine learning', 'artificial intelligence', 'deep learning', 'neural network'],
    'Sustainability': ['climate', 'sustainability', 'renewable', 'environment'],
    'Healthcare': ['biomedical', 'health', 'medicine', 'neuroscience'],
    'Energy': ['energy', 'power systems', 'nuclear'],
    'Policy': ['policy', 'law', 'governance', 'regulation']
}

# Function to classify courses based on keywords
def classify_courses(titles):
    category_counts = Counter()
    for title in titles:
        for category, keywords in interdisciplinary_keywords.items():
            if any(keyword in title.lower() for keyword in keywords):
                category_counts[category] += 1
    return category_counts

# Classify courses
categories_1996 = classify_courses(titles_1996)
categories_2024 = classify_courses(titles_2024)

# Convert classification to DataFrame
df_categories = pd.DataFrame([categories_1996, categories_2024], index=['1996', '2024']).fillna(0)

# Compute word diversity using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
word_matrix_1996 = vectorizer.fit_transform(titles_1996)
word_matrix_2024 = vectorizer.fit_transform(titles_2024)

word_diversity_1996 = len(vectorizer.get_feature_names_out())
word_diversity_2024 = len(vectorizer.get_feature_names_out())

# Plot interdisciplinary category comparison
plt.figure(figsize=(10, 6))
df_categories.T.plot(kind='bar', figsize=(12, 6))
plt.title("Interdisciplinary Course Presence: 1996 vs. 2024")
plt.xlabel("Category")
plt.ylabel("Number of Courses")
plt.xticks(rotation=45)
plt.legend(title="Year")
plt.savefig("interdisciplinary_trends.png")
plt.savefig("15_breadth_visual.png")
plt.show()

# Plot word cloud of course titles
wordcloud_1996 = WordCloud(width=800, height=400, background_color='white').generate(" ".join(titles_1996))
wordcloud_2024 = WordCloud(width=800, height=400, background_color='white').generate(" ".join(titles_2024))

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].imshow(wordcloud_1996, interpolation='bilinear')
axes[0].axis("off")
axes[0].set_title("Word Cloud of Course Titles (1996)")

axes[1].imshow(wordcloud_2024, interpolation='bilinear')
axes[1].axis("off")
axes[1].set_title("Word Cloud of Course Titles (2024)")

plt.savefig("wordcloud_comparison.png")
plt.show()

# Print diversity results
print(f"Unique Words in Course Titles (1996): {word_diversity_1996}")
print(f"Unique Words in Course Titles (2024): {word_diversity_2024}")

# Save results to JSON
results = {
    "word_diversity": {
        "1996": word_diversity_1996,
        "2024": word_diversity_2024
    },
    "interdisciplinary_categories": {
        "1996": categories_1996,
        "2024": categories_2024
    }
}

with open('curriculum_breadth_analysis.json', 'w') as f:
    json.dump(results, f, indent=4)

print("Analysis saved to curriculum_breadth_analysis.json")
