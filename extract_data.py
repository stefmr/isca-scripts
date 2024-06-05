from utils import *
import pandas as pd

xls = pd.ExcelFile('./isca_forms.xlsx')
students_df= pd.read_excel(xls, 'Students')
seniors_df = pd.read_excel(xls, 'Seniors')

#################################################################
##  Extract mentees/mentors from students
#################################################################

masa_mentees_students = []
mass_mentees_students = []
mass_mentors_students = []

masa_mentees_students = students_df.loc[students_df['MaSA Mentee'].isin((
    'Yes. I prefer a mentor from Industry.',
    'Yes. I prefer a mentor from Academia.',
    'Yes. No strong preference on Industry/Academia mentor.'
    ))].copy()

mass_mentees_students = students_df.loc[students_df['MaSS Mentee'] == 'Yes'].copy()

mass_mentors_students = students_df.loc[students_df['MaSS Mentor'].isin((
    'Yes. I can mentor 1 junior student.',
    'Yes. I can mentor 2 junior students.'
    ))].copy()

masa_mentees_students = masa_mentees_students.drop(['MaSS Mentee', 'ResearchAreasMaSS', 'MaSS Mentor', 'ResearchAreasMentors'], axis=1)
mass_mentees_students = mass_mentees_students.drop(['MaSA Mentee', 'ResearchAreasMaSA', 'MaSS Mentor', 'ResearchAreasMentors'], axis=1)
mass_mentors_students = mass_mentors_students.drop(['MaSA Mentee', 'ResearchAreasMaSA', 'MaSS Mentee', 'ResearchAreasMaSS'], axis=1)

mass_mentors_students_oneStudent  = mass_mentors_students.loc[mass_mentors_students['MaSS Mentor'] == 'Yes. I can mentor 1 junior student.']
mass_mentors_students_twoStudents = mass_mentors_students.loc[mass_mentors_students['MaSS Mentor'] == 'Yes. I can mentor 2 junior students.']

masa_mentees_students = masa_mentees_students.drop(['Eulogy'], axis=1)
mass_mentees_students = mass_mentees_students.drop(['Eulogy'], axis=1)
mass_mentors_students_oneStudent = mass_mentors_students_oneStudent.drop(['Eulogy'], axis=1)
mass_mentors_students_twoStudents = mass_mentors_students_twoStudents.drop(['Eulogy'], axis=1)

#################################################################
##  Extract mentors from seniors
#################################################################

masa_mentors_seniors  = []

masa_mentors_seniors = seniors_df.loc[seniors_df['MaSA Mentor'].isin((
    'Yes. I can mentor 1 student.',
    'Yes. I can mentor 2 students.'
    ))].copy()

masa_mentors_senior_oneStudent = seniors_df.loc[seniors_df['MaSA Mentor'] == 'Yes. I can mentor 1 student.']
masa_mentors_senior_twoStudents = seniors_df.loc[seniors_df['MaSA Mentor'] == 'Yes. I can mentor 2 students.']

masa_mentors_senior_oneStudent = masa_mentors_senior_oneStudent.drop(['Eulogy'], axis=1)
masa_mentors_senior_twoStudents = masa_mentors_senior_twoStudents.drop(['Eulogy'], axis=1)

#################################################################
## Extra data
#################################################################

## Eulogy

eulogy = pd.concat([
        students_df.loc[students_df['Eulogy'] == 'Yes'],
        seniors_df.loc[seniors_df['Eulogy'] == 'Yes']
    ], ignore_index=True)

eulogy = eulogy.drop(
    ['Workshops',
    'MaSA Mentee',
    'ResearchAreasMaSA',
    'MaSS Mentee',
    'ResearchAreasMaSS',
    'MaSS Mentor',
    'ResearchAreasMentors',
    'ResearchAreas',
    'index',
    'MaSA Mentor',
    'IndustryOrAcademia']
,axis=1)

## Workshops

students_in_workshops = students_df.loc[
                            ~(students_df['Workshops'] == 'Not applicable (I did not purchase a workshop/tutorials ticket).') & 
                            ~(students_df['Workshops'].isna())]

seniors_in_workshops = seniors_df.loc[
                            ~(seniors_df['Workshops'] == 'Not applicable (I did not purchase a workshop/tutorials ticket).') & 
                            ~(seniors_df['Workshops'].isna())]

students_with_more_than_four_workshops = []
seniors_with_more_than_four_workshops = []

act_with_more_overlap = {}

for idx, student in students_in_workshops.iterrows():
    parsed_workshops = parse_text(student['Workshops'])
    if (len(parsed_workshops) > 4):
           students_with_more_than_four_workshops.append(len(parsed_workshops))
#        print("Student with idx: " + str(idx) + " is registered in: " + str(len(parsed_workshops)) + " workshops")
#        students_with_more_than_four_workshops += 1
    for workshop in parsed_workshops:
        if (len(parsed_workshops) > 4):
            if workshop not in act_with_more_overlap:
                act_with_more_overlap[workshop] = 1
            else:
                act_with_more_overlap[workshop] += 1

        if workshop in workshops_tutorials:
            workshops_tutorials[workshop] += 1
        else:
            print('Not in dict')
            print(workshop)



for idx, senior in seniors_in_workshops.iterrows():
    parsed_workshops = parse_text(senior['Workshops'])
    if (len(parsed_workshops) > 4):
        seniors_with_more_than_four_workshops.append(len(parsed_workshops))
#        print("Senior with idx: " + str(idx) + " is registered in: " + str(len(parsed_workshops)) + " workshops")
#        seniors_with_more_than_four_workshops += 1
    for workshop in parsed_workshops:
        if (len(parsed_workshops) > 4):
            if workshop not in act_with_more_overlap:
                act_with_more_overlap[workshop] = 1
            else:
                act_with_more_overlap[workshop] += 1

        if workshop in workshops_tutorials:
            workshops_tutorials[workshop] += 1
        else:
            print('Not in dict')
            print(workshop)

total_workshops = pd.DataFrame(workshops_tutorials.items(), columns=['Workshops/Tutorials', 'Participants'])

#################################################################
## Export xlsx 
#################################################################
with pd.ExcelWriter('isca_data.xlsx', engine='xlsxwriter') as writer:
    masa_mentees_students.to_excel(writer, sheet_name='MaSA Students')
    mass_mentees_students.to_excel(writer, sheet_name='MaSS Students')
    mass_mentors_students_oneStudent.to_excel(writer, sheet_name='MaSS Mentors - 1 student')
    mass_mentors_students_twoStudents.to_excel(writer, sheet_name='MaSS Mentors - 2 students')
    masa_mentors_senior_oneStudent.to_excel(writer, sheet_name='MaSA Mentors - 1 student')
    masa_mentors_senior_twoStudents.to_excel(writer, sheet_name='MaSA Mentors - 2 students')
    eulogy.to_excel(writer, sheet_name='Eulogy')
    total_workshops.to_excel(writer, sheet_name='Participants per workshop')
