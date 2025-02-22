# -----------------------------------------------
#  12. Course Offerings Over Time
# 
#  After extracting the course data from 
#  both the 1996 and present catalogs, 
#  analyze the number of courses offered 
#  in various departments. Are there any 
#  departments that have significantly 
#  expanded or reduced their course offerings? 
#  If so, identify them and discuss possible 
#  reasons for these changes.
# -----------------------------------------------
#extracting the course data from json files
import json
import pandas as pd
import matplotlib.pyplot as plt

#read the json files
with open('10_mit_1996.json') as f:
    data_1996 = json.load(f)

#read from the second json file
with open('11_mit_2024.json') as f:
    data_2024 = json.load(f)

#convert the data to dataframes
df_1996 = pd.DataFrame(data_1996)
#df_2024 = pd.DataFrame(data_2024)
df_2024=pd.DataFrame(data_2024["courses"])

course_count_1996 = df_1996.groupby('department').size().rename('1996')
course_count_2024 = df_2024.groupby('department').size().rename('2024')

#merge the two dataframes
course_count = pd.merge(course_count_1996, course_count_2024, on='department', how='outer')
course_count.columns = ['1996', '2024']
course_count.fillna(0, inplace=True)

#calculate the change in the number of courses
course_count['Change'] = course_count['2024'] - course_count['1996']

#sort the data by the change in the number of courses
course_count = course_count.sort_values(by='Change', ascending=False)

#display the data
print(course_count)
#save the data to a csv file
course_count.to_csv('course_count.csv')
#plot the data
course_count.plot(kind='bar', y='Change', title='Change in Number of Courses by Department', figsize=(10, 6))
plt.ylabel('Change in Number of Courses')
plt.show()
#save the plot
plt.savefig('course_change.png')