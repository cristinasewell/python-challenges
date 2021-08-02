#!/usr/bin/env python
# coding: utf-8

# In[90]:


import pandas as pd
import os

data_purchase = "./data/purchase_data.csv"
data_schools = "./data/schools_complete.csv"
data_students = "./data/students_complete.csv"

purchase_file = os.path.abspath(data_purchase)
schools_file = os.path.abspath(data_schools)
students_file = os.path.abspath(data_students)

schools_df = pd.read_csv(schools_file)
students_df = pd.read_csv(students_file)

df = pd.merge(students_df, schools_df, how="left", on=["school_name"])

print(schools_df.head())


# In[ ]:





# In[91]:


total_schools = schools_df["school_name"].count()
total_students = students_df["student_name"].count()
total_students, total_schools
total_budget = schools_df["budget"].sum()

average_reading_score = students_df["reading_score"].mean()
average_math_score = students_df["math_score"].mean()
average_math_score, average_reading_score
passing_math = df.loc[df['math_score'] >= 70].count()
passing_math = passing_math / total_students * 100

passing_reading = df.loc[df['reading_score'] >= 70].count()
passing_reading = passing_reading / total_students * 100

passing_math['math_score'], passing_reading['reading_score']

passing_math = passing_math['math_score']
passing_reading = passing_reading['reading_score']
passing_math_and_reading = df.loc[(df['math_score'] >= 70) & (df['reading_score'] >= 70)].count()
passing_math_and_reading = passing_math_and_reading / total_students * 100
passing_math_and_reading['student_name']

my_table = pd.DataFrame({"math": ["{0:.2f}%".format(passing_math)], "reading": [passing_reading]})
print(my_table.head())


# 

# In[92]:

schools_df = schools_df.sort_values(by='school_name')

school_type = schools_df['type']

student_counts = df['school_name'].value_counts()

final = student_counts.to_frame()
final.rename(columns={'school_name': 'Total Students'})
final = final.sort_index()
df = df.sort_values(by='school_name')
final.insert(loc=0, column='School Type', value=list(school_type))


budget = schools_df['budget']
final.insert(loc=1, column='School Budget', value=list(budget))
final_budget = final["School Budget"]/final["school_name"]

final['Final Budget'] = list(final_budget)

final['School Budget'] = final['School Budget'].map("${:,.2f}".format)

final['Final Budget'] = final['Final Budget'].map("${:,.2f}".format)

schools_groupby = df.groupby(['school_name'])

average_math_score = schools_groupby['math_score'].mean()
final['Average Math Score'] = average_math_score

average_reading_score = schools_groupby['reading_score'].mean()
final['Average Reading Score'] = average_reading_score


# passing scores by filterling
passing_math = df[(df['math_score']) >= 70]
passing_reading = df[(df['reading_score']) >= 70]
passing_both = df[(df['math_score'] >= 70) & (df["reading_score"] >= 70)]

school_passing_math = passing_math.groupby(['school_name']).count()['student_name'] / student_counts * 100
school_passing_reading = passing_reading.groupby(['school_name']).count()['student_name'] / student_counts * 100

final["Passing Math %"] = school_passing_math
final['Passing Reading %'] = school_passing_reading

overall_passing = passing_both.groupby(['school_name']).count()['student_name'] / student_counts * 100

final['% Overall passing score'] = overall_passing

school_summary = final
print(school_summary)


# In[93]:


# Top performing schools
top_performing = school_summary.sort_values(['% Overall passing score'], ascending=False)
print(top_performing.head(5))


# In[94]:


# Buttom performing schools
top_performing = school_summary.sort_values(['% Overall passing score'], ascending=True)
print(top_performing.head(5))


# In[95]:


# Math Scores by Grade
grade9 = df[(df['grade']) == '9th']
grade10 = df[(df['grade']) == '10th']
grade11 = df[(df['grade']) == '11th']
grade12 = df[(df['grade']) == '12th']

score_grade9 = grade9.groupby(['school_name']).mean()['math_score'] 
score_grade10 = grade10.groupby(['school_name']).mean()['math_score']
score_grade11 = grade11.groupby(['school_name']).mean()['math_score']
score_grade12 = grade12.groupby(['school_name']).mean()['math_score']

math_score_grade = pd.DataFrame({"9th": score_grade9})

math_score_grade.index.name = None
print(math_score_grade)


# In[125]:


# Reading Scores by Grade

# get the max and min per student spending to find the ranges
final_budget.max(), final_budget.min()

bins = [0, 590, 628, 640, 670]

labels = ['$0 to 590', '$591 to 615', '$616 to 640', '$641 to 670']


# spending = pd.DataFrame()
school_summary['Spending Stuff'] =  pd.cut(final_budget, bins, labels=labels).head()

math = school_summary.groupby(['Spending Stuff']).mean()['Average Math Score']
reading = school_summary.groupby(['Spending Stuff']).mean()['Average Reading Score']

spending = pd.DataFrame({"something": math})
print(spending)
