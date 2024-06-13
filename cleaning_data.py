from utils import *
import pandas as pd

#################################################
## Page load
#################################################

xls = pd.ExcelFile('./isca2024_answers_updated.xlsx')
page1 = pd.read_excel(xls, 'Student')
page2 = pd.read_excel(xls, 'Student, member')
page3 = pd.read_excel(xls, 'UArch')
page4 = pd.read_excel(xls, 'senior')
page5 = pd.read_excel(xls, 'senior, member')
page6 = pd.read_excel(xls, 'senior, others')

#xls2 = pd.ExcelFile('~/Downloads/ISCA24_attendee_list.xlsx')
#update_page1 = pd.read_excel(xls2, 'student, nonmember')
#update_page2 = pd.read_excel(xls2, 'student, member')
#update_page3 = pd.read_excel(xls2, 'student, uarch')
#update_page4 = pd.read_excel(xls2, 'seniors, nonmembers')
#update_page5 = pd.read_excel(xls2, 'seniors, member')
#update_page6 = pd.read_excel(xls2, 'seniors, others')

page1.columns = student_categories
page2.columns = studentMember_categories
page3.columns = studentUarch_categories
page4.columns = senior_categories
page5.columns = seniorMember_categories
page6.columns = seniorOthers_categories

page1 = page1.drop([
    'Date', 
    'Location', 
    'Dissability', 
    'Visa', 
    'Postal', 
    'Policy', 
    'Retiring', 
    'First Name (Buyer)', 
    'Last Name(Buyer)', 
    'Email(Buyer)', 
    'Ticket Type'], axis=1)

page2 = page2.drop([
    'Date', 
    'Location', 
    'Dissability', 
    'Visa', 
    'Postal', 
    'ACM/IEEE Number', 
    'Policy', 
    'Retiring', 
    'First Name (Buyer)', 
    'Last Name(Buyer)', 
    'Email(Buyer)', 
    'Ticket Type'], axis=1)

page3 = page3.drop([
    'Date', 
    'Location', 
    'Dissability', 
    'Visa', 
    'Postal', 
    'Policy', 
    'First Name (Buyer)', 
    'Last Name(Buyer)', 
    'Email(Buyer)', 
    'Ticket Type'], axis=1)

page4 = page4.drop([
    'Date', 
    'Location', 
    'Dissability', 
    'Visa', 
    'Postal', 
    'Policy', 
    'Retiring',
    'First Name (Buyer)', 
    'Last Name(Buyer)', 
    'Email(Buyer)', 
    'Ticket Type'], axis=1)

page5 = page5.drop([
    'Date', 
    'Location', 
    'Dissability', 
    'Visa', 
    'Postal', 
    'ACM/IEEE Number', 
    'Policy', 
    'Retiring',
    'First Name (Buyer)', 
    'Last Name(Buyer)', 
    'Email(Buyer)', 
    'Ticket Type'], axis=1)

page6 = page6.drop([
    'Date', 
    'Location', 
    'Dissability',
	'Visa',
	'Postal','Workshop - Saturday',
	'Workshop - Sunday',
	'Workshop - Two days',
	'Policy',
	'Retiring','First Name (Buyer)',
	'Last Name(Buyer)',
	'Email(Buyer)',
	'Ticket Type'],
	axis=1)

page1 = page1.drop_duplicates()
page2 = page2.drop_duplicates()
page3 = page3.drop_duplicates()
page4 = page4.drop_duplicates()
page5 = page5.drop_duplicates()
page6 = page6.drop_duplicates()


#################################################
## Preprocess Seniors
#################################################

page6 = page6.drop(['MaSS/MaSA Mentee', 'MaSS Mentee', 'MaSS Mentor'], axis=1)

seniors= [page4, page5]
seniors_df = pd.concat(seniors, ignore_index=True)

seniors_df['IndustryOrAcademia'] = seniors_df['IndustryOrAcademia'].fillna(seniors_df['IndustryOrAcademia2'])
seniors_df['ResearchAreas'] = seniors_df['ResearchAreas'].fillna(seniors_df['ResearchAreasMentors/Mentees'])

seniors_df = seniors_df.drop(['IndustryOrAcademia2', 'ResearchAreasMentors/Mentees'], axis=1)

seniors_df = pd.concat([seniors_df, page6], ignore_index=True)


## Extracting students that signed up as seniors.
students_as_seniors = pd.concat([ 
                        seniors_df.loc[seniors_df['Job Title'] =='Graduate Student'],
                        seniors_df.loc[seniors_df['Job Title'] =='PhD Student']
                        ], ignore_index=True)

students_as_seniors = students_as_seniors.drop(['MaSA Mentor','IndustryOrAcademia','ResearchAreas'], axis=1)

seniors_df = seniors_df.drop(seniors_df.loc[seniors_df['Job Title'] =='Graduate Student'].index)
seniors_df = seniors_df.drop(seniors_df.loc[seniors_df['Job Title'] =='PhD Student'].index)

seniors_df.reset_index(inplace=True)

#################################################
## Preprocess Students
#################################################

page3['MaSS Mentor'] = pd.NA
page3['ResearchAreasMentors'] = pd.NA
page3['ResearchAreasGeneral'] = pd.NA

students = [page1, page2, page3]
students_df = pd.concat(students, ignore_index=True)

## Collapse research areas into one column
students_df['ResearchAreasMaSA'] = students_df['ResearchAreasMaSA'].fillna(students_df['ResearchAreas2MaSA'])
students_df['ResearchAreasMaSA'] = students_df['ResearchAreasMaSA'].fillna(students_df['ResearchAreas3MaSA'])
students_df.loc[students_df['ResearchAreasMaSS'] == 'Same as before', 'ResearchAreasMaSS'] = students_df['ResearchAreasMaSA']
students_df['ResearchAreasMentors'] = students_df['ResearchAreasMentors'].fillna(students_df['ResearchAreasGeneral'])
students_df.loc[students_df['ResearchAreasMentors'] == 'Same as before', 'ResearchAreasMentors'] = students_df['ResearchAreasMaSA']

## Drop empty columns
students_df = students_df.drop(['ResearchAreas2MaSA', 'ResearchAreas3MaSA', 'ResearchAreasGeneral'], axis=1)

## Add students that registered as seniors into the students dataframe.
students_df = pd.concat([students_df, students_as_seniors], ignore_index = True)

students_df = students_df.drop_duplicates()
seniors_df= seniors_df.drop_duplicates()

#################################################
## Export
#################################################

with pd.ExcelWriter('isca_forms.xlsx', engine='xlsxwriter') as writer:
    students_df.to_excel(writer, sheet_name='Students')
    seniors_df.to_excel(writer, sheet_name='Seniors')
