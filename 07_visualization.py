# -----------------------------------------------
#  7. Data Visualization:
#  Objective: Visualize the word frequencies
#  using a visualization library.
# 
#  Tools/Resources: Examples of visualization 
#  libraries D3, Plotly, and Chart.JS.
#     D3, https://d3js.org/
#     Plotly, https://plotly.com/
#     Chart.JS, https://www.chartjs.org/
#     Google Charts, https://developers.google.com/chart/
# -----------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns
from wordcloud import WordCloud

# Load word frequency data
file_path = os.environ.get("WordFreq", "06_word_frequencies.csv")
#file_path = "word_frequencies.csv"
df = pd.read_csv("output_folder/"+file_path)

# Sort data to show the most frequent words
df = df.sort_values(by="Frequency", ascending=False)

# ----------- BAR CHART -----------
plt.figure(figsize=(12, 6)) # Set the figure size
#sns.barplot(x=df["Frequency"][:15], y=df["Word"][:15], palette="viridis") # Create the bar plot
sns.barplot(x=df["Frequency"][:15], y=df["Word"][:15], hue=df["Word"][:15], palette="viridis", legend=False) # Create the bar plot
plt.xlabel("Frequency") # Set the x-axis label
plt.ylabel("Word") # Set the y-axis label
plt.title("Top 15 Most Common Words in Course Titles") # Set the title
plt.grid(axis="x", linestyle="--", alpha=0.7) # Add gridlines for better readability
plt.show()

# ----------- WORD CLOUD -----------
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate_from_frequencies(dict(zip(df["Word"], df["Frequency"])))

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")  # Hide axes
plt.title("Word Cloud of Most Common Words in Course Titles")
plt.show()

#---------------------SAVE VISUALIZATIONS---------------------
# Save bar chart
plt.figure(figsize=(12, 6))
#sns.barplot(x=df["Frequency"][:15], y=df["Word"][:15], palette="viridis")
sns.barplot(x=df["Frequency"][:15], y=df["Word"][:15], hue=df["Word"][:15], palette="viridis", legend=False)
plt.xlabel("Frequency")
plt.ylabel("Word")
plt.title("Top 15 Most Common Words in Course Titles")
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.savefig("output_folder/07_word_freq_bar_chart.png")  # Save instead of showing
plt.close()  # Close figure to prevent overlap

# Save word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="viridis").generate_from_frequencies(dict(zip(df["Word"], df["Frequency"])))

plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud of Most Common Words in Course Titles")
plt.savefig("output_folder/07_wordcloud_freq.png")  # Save instead of showing
plt.close()