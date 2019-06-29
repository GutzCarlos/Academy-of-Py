# Dependencies and Setup
import pandas as pd
import numpy as np

# PyCity Schools Analysis

#* District Schools, apart from being from the lange size schools  group, they tendo to do worse in Math and Reading Scores that Charter schools
#* Regarding the size of the school, it seems that this parameter is related to the performance in subjects scores (math and reading). This is because the data show that Small and Medium Size shcools do better than Large size schools.
#* Finally, budget per student seem to have a negative association with all scores. The "High Budget per Student" group ($ 635.75 - 655.0) is the one with the lowest average scores in math and reading
#---

# Files to Load
school_data_to_load = "Resources/schools_complete.csv"
student_data_to_load = "Resources/students_complete.csv"

# Read School and Student Data File and store into Pandas Data Frames
school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)
school_columns=school_data.columns.values
student_columns=student_data.columns.values

# Combine the data into a single dataset
data = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])
data_columns=data.columns.values

school_data.head()
student_data.head()
data.head()


#####      District Summary
#Calculate the total number of schools
nSchools=len(data["School ID"].unique())
# Calculate the total number of students
nStudents=len(data["Student ID"].unique())
# Calculate the total budget
tBudget=pd.DataFrame(data.groupby("School ID").mean())["budget"].sum()
# Calculate the average math score
aMath=data["math_score"].mean()
# Calculate the average reading score
aReading=data["reading_score"].mean()
# Calculate the percentage of students with a passing math score (70 or greater)
prMath=(data[(data['math_score']>=70)]["Student ID"].count()/data["Student ID"].count())*100
# Calculate the percentage of students with a passing reading score (70 or greater)
prReading=(data[(data['reading_score']>=70)]["Student ID"].count()/data["Student ID"].count())*100
# Calculate the overall passing rate (overall average score), i.e. (avg. math score + avg. reading score)/2
oPR=(aMath+aReading)/2
# Create a dataframe to hold the above results
District_Sumarry=pd.DataFrame({"Total Schools":nSchools,
             "Total Students": nStudents,
             "Total Budget": tBudget,
             "Average Math Score":aMath,
             "Average Reading Score":aReading,
             "% Passing Math":prMath,
             "% Passing Reading": prReading,
             "% Overall Pasing Rate": oPR}, index=[0])

# Optional: give the displayed data cleaner formatting
District_Sumarry.style.format({'Total Schools': "{:,.0f}",
                               'Total Students':"{:,.0f}",
                               "Total Budget": "${:,.2f}",
                               "Average Math Score":"{:,.2f}",
                               "Average Reading Score":"{:,.2f}",
                               "% Passing Math":"{:.2f}%",
                               "% Passing Reading": "{:.2f}%",
                               "% Overall Pasing Rate": "{:.2f}%"})


####  School Summary
##   Create an overview table that summarizes key metrics about each school, including:
# School Name
# School Type
# Total Students
### Obtain data frame from groupby table with students count
SchoolSummary=pd.DataFrame(data.groupby(["School ID","school_name", "type"])["Student ID"].count()) .reset_index()
# Total School Budget
# Per Student Budget
# Average Math Score
# Average Reading Score
### Obtain data frame from groupby table with budget and scores average by school
SchoolSummary=SchoolSummary.merge(pd.DataFrame(data.groupby(["School ID","school_name", "type"])["budget","math_score", "reading_score", "size"].mean()), on="school_name", how="left")
SchoolSummary["Per Student Budget"]=SchoolSummary["budget"]/SchoolSummary["Student ID"]
# % Passing Math
# % Passing Reading
### Obtain data frames from groupby table with students with passing scores count
SchoolSummary=SchoolSummary.merge(pd.DataFrame(data[data["math_score"]>=70].groupby(["School ID","school_name", "type"])["Student ID"].count()), on="school_name", how="left")
SchoolSummary=SchoolSummary.merge(pd.DataFrame(data[data["reading_score"]>=70].groupby(["School ID","school_name", "type"])["Student ID"].count()), on="school_name", how="left")
SchoolSummary=SchoolSummary.rename(columns={"Student ID_x":"Total Students",
                                            "Student ID_y":"% Passing Math",
                                            "Student ID":"% Passing Reading",
                                            "budget": "Total Budget",
                                            "math_score": "Average Math Score",
                                            "reading_score": "Average Reading Score",
                                            "type": "School Type",
                                            "size": "Size"})
### Calculate the % of passing students by subject
SchoolSummary["% Passing Math"]=(SchoolSummary["% Passing Math"]/SchoolSummary["Total Students"])*100
SchoolSummary["% Passing Reading"]=(SchoolSummary["% Passing Reading"]/SchoolSummary["Total Students"])*100
# Overall Passing Rate (Average of the above two)
SchoolSummary["% Overall Passing Rate"]=(SchoolSummary["% Passing Math"]+SchoolSummary["% Passing Reading"])/2
# Create a dataframe to hold the above results. Use "School Name" as index for the df
SchoolSummary=SchoolSummary.set_index("school_name")
SchoolSummary


### Top Performing Schools (By Passing Rate)
#Sort and display the top five schools in overall passing rate

SchoolSummary = SchoolSummary.sort_values("% Overall Passing Rate", ascending=False)
SchoolSummary.head(5)

### Bottom Performing Schools (By Passing Rate)
#Sort and display the five worst-performing schools

SchoolSummary = SchoolSummary.sort_values("% Overall Passing Rate", ascending=True)
SchoolSummary.head(5)



###   Math Scores by Grade
# Create a table that lists the average Math Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# Create a pandas series for each grade. Hint: use a conditional statement.
# Group each series by school
# Combine the series into a dataframe
for gr in list(data["grade"].unique()):
    if(gr==list(data["grade"].unique())[0]):
        MathGrade=pd.DataFrame(data[data["grade"]==gr].groupby(["school_name"])["math_score"].mean())
        MathGrade=MathGrade.rename(columns={"math_score":gr})
    elif(gr!=list(data["grade"].unique())[0]):
        MathGrade=MathGrade.merge(pd.DataFrame(data[data["grade"]==gr].groupby(["school_name"])["math_score"].mean()).reset_index(), on="school_name", how="left")
        MathGrade=MathGrade.rename(columns={"math_score":gr})
# Optional: give the displayed data cleaner formatting
MathGrade=MathGrade[["school_name","9th", "10th", "11th","12th"]].set_index("school_name").style.format({"9th":"{:.2f} %",
                   "10th":"{:.2f} %",
                   "11th":"{:.2f} %",
                   "12th":"{:.2f} %"})
MathGrade

###   Reading Scores by Grade
# Create a table that lists the average Reading Score for students of each grade level (9th, 10th, 11th, 12th) at each school.
# Create a pandas series for each grade. Hint: use a conditional statement.
# Group each series by school
# Combine the series into a dataframe
for gr in list(data["grade"].unique()):
    if(gr==list(data["grade"].unique())[0]):
        ReadingGrade=pd.DataFrame(data[data["grade"]==gr].groupby(["school_name"])["reading_score"].mean())
        ReadingGrade=ReadingGrade.rename(columns={"reading_score":gr})
    elif(gr!=list(data["grade"].unique())[0]):
        ReadingGrade=ReadingGrade.merge(pd.DataFrame(data[data["grade"]==gr].groupby(["school_name"])["reading_score"].mean()).reset_index(), on="school_name", how="left")
        ReadingGrade=ReadingGrade.rename(columns={"reading_score":gr})
# Optional: give the displayed data cleaner formatting
ReadingGrade=ReadingGrade[["school_name","9th", "10th", "11th","12th"]].set_index("school_name").style.format({"9th":"{:.2f} %",
                   "10th":"{:.2f} %",
                   "11th":"{:.2f} %",
                   "12th":"{:.2f} %"})
ReadingGrade


###  Scores by School Spending

# Create a table that breaks down school performances based on average Spending Ranges (Per Student). Use 4 reasonable bins to group school spending. Include in the table each of the following:
# Average Math Score
# Average Reading Score
# % Passing Math
# % Passing Reading
# Overall Passing Rate (Average of the above two)


# Create bins in which to place values based upon Budget per student
# Create labels for these bins
ngroups=4
bins=[]
group=[]
for i in range(ngroups+1):
    bins.append(min(SchoolSummary["Per Student Budget"])+((max(SchoolSummary["Per Student Budget"])-min(SchoolSummary["Per Student Budget"]))/ngroups)*i)
    if (i!=0):
        group.append(str("$ "+ str(bins[i-1])+" - "+str(bins[i])))




SchoolSummary["Spending Ranges (Per Student)"] = pd.cut(SchoolSummary["Per Student Budget"], bins, labels=group)
SchoolSummary.head()

SchoolSummary.groupby("Spending Ranges (Per Student)")['Average Math Score', 'Average Reading Score',
       '% Passing Math', '% Passing Reading',
       '% Overall Passing Rate'].mean()


###  Scores by School Size

#Perform the same operations as above, based on school size

# Sample bins. Feel free to create your own bins.
bins = [0, 1000, 2000, 5000]
group = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]

SchoolSummary["School Size"] = pd.cut(SchoolSummary["Size"], bins, labels=group)
SchoolSummary.head()
SchoolSummary.groupby("School Size")['Average Math Score', 'Average Reading Score',
       '% Passing Math', '% Passing Reading',
       '% Overall Passing Rate'].mean()



# Perform the same operations as above, based on school type.
SchoolSummary.groupby("School Type")['Average Math Score', 'Average Reading Score',
       '% Passing Math', '% Passing Reading',
       '% Overall Passing Rate'].mean()


SchoolSummary.groupby(["School Type","School Size"])['Average Math Score', 'Average Reading Score',
       '% Passing Math', '% Passing Reading',
       '% Overall Passing Rate'].mean()