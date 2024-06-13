debug = False 
from utils import *
import pandas as pd
import numpy as np

xls = pd.ExcelFile('./isca_forms.xlsx')
students_df= pd.read_excel(xls, 'Students')
seniors_df = pd.read_excel(xls, 'Seniors')

#################################################################
##  Extract mentees/mentors from students
#################################################################

masa_mentees_students = []

masa_mentees_students = students_df.loc[students_df['MaSA Mentee'].isin((
    'Yes. I prefer a mentor from Industry.',
    'Yes. I prefer a mentor from Academia.',
    'Yes. No strong preference on Industry/Academia mentor.'
    ))].copy()


masa_mentees_students = masa_mentees_students.drop(['MaSS Mentee', 'ResearchAreasMaSS', 'MaSS Mentor', 'ResearchAreasMentors'], axis=1)


masa_mentees_students = masa_mentees_students.drop(['Eulogy'], axis=1)

#################################################################
##  Extract mentors from seniors
#################################################################

masa_mentors_seniors  = []

masa_mentors_seniors = seniors_df.loc[seniors_df['MaSA Mentor'].isin((
    'Yes. I can mentor 1 student.',
    'Yes. I can mentor 2 students.'
    ))].copy()

masa_mentors_oneStudent = seniors_df.loc[seniors_df['MaSA Mentor'] == 'Yes. I can mentor 1 student.']
masa_mentors_twoStudents = seniors_df.loc[seniors_df['MaSA Mentor'] == 'Yes. I can mentor 2 students.']

masa_mentors_oneStudent = masa_mentors_oneStudent.drop(['Eulogy'], axis=1)
masa_mentors_twoStudents = masa_mentors_twoStudents.drop(['Eulogy'], axis=1)

masa_mentors = pd.concat([masa_mentors_oneStudent, masa_mentors_twoStudents, masa_mentors_twoStudents], ignore_index=True)

#################################################################
##  Extract mentors from seniors
#################################################################

masa_mentors_by_area = {}
for area in research_areas:
    masa_mentors_by_area[area] = masa_mentors[masa_mentors['ResearchAreas'].str.contains(area,regex=False)]

masa_mentors_industry = {}
masa_mentors_academia = {}
for area in research_areas:
    masa_mentors_industry[area] = masa_mentors_by_area[area][masa_mentors_by_area[area]['IndustryOrAcademia'].isin(["Industry.", 'Both Industry and Academia.'])]
    masa_mentors_academia[area] = masa_mentors_by_area[area][masa_mentors_by_area[area]['IndustryOrAcademia'].isin(["Academia.", 'Both Industry and Academia.'])]

## Initialize variables for Matching.
mentee_count=0
num_mentor_commitments = masa_mentors['Email'].count()
masa_mentees_students.loc[:,'MentorAllocated']   = np.nan
masa_mentees_students.loc[:,'MentorName']        = np.nan
masa_mentees_students.loc[:,'MentorEmail']       = np.nan
masa_mentees_students.loc[:,'MentorAffiliation'] = np.nan
masa_mentors.loc[:,'MenteeAllocated']   = np.nan
masa_mentors.loc[:,'MenteeName']        = np.nan
masa_mentors.loc[:,'MenteeEmail']       = np.nan
masa_mentors.loc[:,'MenteeAffiliation'] = np.nan

## Stats for tracking research area and industry/academia preference match success
# For research area preference
num_mentees_want_areamatch = 0  
num_mentees_got_areamatch = 0 
# For Industry/academia preference
num_mentees_want_affiliationtype = 0 
num_mentees_got_affiliationtype = 0





##############################################################
## Function: Research-Area Based Matching with Mentor.
## Inputs: Mode (0 - Industry, 1-Academia, 2-Indifferent)
## Inputs: mentee_index 
## Inputs: mentee
##############################################################

def match_research_area(mode):
    global num_mentees_want_areamatch 
    global num_mentees_got_areamatch  
    global num_mentees_want_affiliationtype
    global num_mentees_got_affiliationtype 

    ## Shuffle mentees
    masa_mentees = masa_mentees_students.sample(frac=1)
 #   masa_mentees = masa_mentees_students

    ## Choose Mentor Pool from which mentors chosen.
    mentors_pool = masa_mentors_by_area
    if(mode == "Industry"):   # industry preference of mentee
        mentors_pool = masa_mentors_industry
    elif(mode == "Academia"): # academia preference of mentee
        mentors_pool = masa_mentors_academia 
    else :
        mentors_pool = masa_mentors_by_area 
      
    ## Get Mentee Preference for Industry/Academia
    if(mode == "Industry."):
        mentee_affiliation_type_pref = 'Yes. I prefer a mentor from Industry.'
    elif (mode == "Academia."):
        mentee_affiliation_type_pref = 'Yes. I prefer a mentor from Academia.'
           
    ## Match using research area
    mentee_count = 0
    for mentee_index, mentee in masa_mentees.iterrows():
        mentee_count=mentee_count+1
    
        ## Bools for tracking stats of research area match
        mentee_wants_areamatch = False
        mentee_got_areamatch = False
        
        ## Check if Mentee prefers Industry or Academia as per the mode
        if(((mode == "Industry.") and (masa_mentees.loc[int(mentee_index),'MaSA Mentee'] == mentee_affiliation_type_pref)) |
           ((mode == "Academia.") and (masa_mentees.loc[int(mentee_index),'MaSA Mentee'] == mentee_affiliation_type_pref)) |
           ((mode in ["Industry.","Academia."]) != True)):

            #Check if mentee is not allocated:
            if(masa_mentees.loc[int(mentee_index),'MentorAllocated'] != True) :                           
                ## Iterate over mentees research area
                for area in research_areas:
                    if(area in mentee['ResearchAreasMaSA']):
                        if debug: print ("MenteeResearchArea: ",area)
                        mentee_wants_areamatch = True

                        #Check if Mentor available in mentee's research area
                        if(not mentors_pool[area].empty):                
                            #Get first available mentor from mentee's research area
                            mentor_chosen = mentors_pool[area].iloc[0] 
                            mentor_chosen_index = int(mentors_pool[area].index[0])
                            if debug: print("Chosen Mentor Index: "+str(mentor_chosen_index))
                            if debug: print(mentor_chosen['First Name'] + " "+mentor_chosen['Last Name'] + " MentorResearchAreas: "+mentor_chosen['ResearchAreas'])

                            #Mark mentor as allocated in mentees_df and mentors_replicated_df
                            masa_mentees_students.loc[int(mentee_index),'MentorAllocated']   = True
                            masa_mentees_students.loc[int(mentee_index),'MentorName']        = mentor_chosen['First Name'] + " " + mentor_chosen['Last Name']
                            masa_mentees_students.loc[int(mentee_index),'MentorEmail']       = mentor_chosen['Email'] 
                            masa_mentees_students.loc[int(mentee_index),'MentorAffiliation'] = mentor_chosen['Affiliation']     
                            masa_mentors.loc[mentor_chosen_index,'MenteeAllocated'] = True
                            masa_mentors.loc[mentor_chosen_index,'MenteeName']      = mentee['First Name'] + " " + mentee['Last Name']
                            masa_mentors.loc[mentor_chosen_index,'MenteeEmail']     = mentee['Email']
                            masa_mentors.loc[mentor_chosen_index,'MenteeAffiliation']     = mentee['Affiliation']                            

                            #Delete matched mentor from all mentors_by_area, to prevent future hit on matched mentor-entry
                            for temp_area in research_areas:
                                if(mentor_chosen_index in masa_mentors_by_area[temp_area].index):
                                    masa_mentors_by_area[temp_area] = masa_mentors_by_area[temp_area].drop(index=mentor_chosen_index)
                                if(mentor_chosen_index in masa_mentors_industry[temp_area].index):
                                    masa_mentors_industry[temp_area] = masa_mentors_industry[temp_area].drop(index=mentor_chosen_index)
                                if(mentor_chosen_index in masa_mentors_academia[temp_area].index):
                                    masa_mentors_academia[temp_area] = masa_mentors_academia[temp_area].drop(index=mentor_chosen_index)

                            #Mentee is matched
                            mentee_got_areamatch = True

                            #Update industry/academia preference match:
                            if (((mentee['MaSA Mentee'] == 'Yes. I prefer a mentor from Academia.') and (mentor_chosen['IndustryOrAcademia'] in ['Academia','Both Industry and Academia'])) or
                               ((mentee['MaSA Mentee'] == 'Yes. I prefer a mentor from Industry.') and (mentor_chosen['IndustryOrAcademia'] in ['Industry','Both Industry and Academia']))):
                                num_mentees_got_affiliationtype += 1
                            break                        
                ## Update Research Area Match Stats
                if mentee_got_areamatch == True: num_mentees_got_areamatch += 1    
    
        ## Stop matching once we hit the number of commitments from mentors
        if(mentee_count >= num_mentor_commitments):
            break            
        
##############################################################

##############################################################
## Function: Random research-area based Matching with Mentor.
## Inputs: Mode (0 - Industry, 1-Academia, 2-Indifferent)
## Inputs: mentors_remaining_df -> list of unallocated mentors.
##############################################################

def match_random_area(mode):
    global num_mentees_want_affiliationtype
    global num_mentees_got_affiliationtype 
    
    ## Get remaining mentors that are not allocated yet.
    mentors_remaining_df = masa_mentors[masa_mentors['MenteeAllocated']!= True]    
    
    ## Filter Remaining Mentors from Industry/Academia as per mode
    if(mode == "Industry."):
        mentors_remaining_df = mentors_remaining_df[mentors_remaining_df['IndustryOrAcademia'].isin(["Industry.", 'Both Industry and Academia.'])]
    elif(mode == "Academia."):
        mentors_remaining_df = mentors_remaining_df[mentors_remaining_df['IndustryOrAcademia'].isin(["Academia.", 'Both Industry and Academia.'])]

    #Shuffle leftovers
    mentors_remaining_df = mentors_remaining_df.sample(frac=1) 

    ## Get Mentee Preference for Industry/Academia
    if(mode == "Industry."):
        mentee_affiliation_type_pref = 'Yes. I prefer a mentor from Industry.'
    elif (mode == "Academia."):
        mentee_affiliation_type_pref = 'Yes. I prefer a mentor from Academia.'
        
    #Start Matching    
    mentee_count=0
    for mentee_index, mentee in masa_mentees_students.iterrows():
        mentee_count=mentee_count+1    
        
        ## Check if Mentee prefers Industry or Academia as per the mode
        if(((mode == "Industry.") and (masa_mentees_students.loc[int(mentee_index),'MaSA Mentee'] == mentee_affiliation_type_pref)) |
           ((mode == "Academia.") and (masa_mentees_students.loc[int(mentee_index),'MaSA Mentee'] == mentee_affiliation_type_pref)) |
           ((mode in ["Industry.","Academia."]) != True)):

            #If leftover mentee: Match with first leftover mentor
            if((masa_mentees_students.loc[int(mentee_index),'MentorAllocated'] != True)  and len(mentors_remaining_df.index)):
                mentor_chosen = mentors_remaining_df.iloc[0]
                mentor_chosen_index = int(mentors_remaining_df.index[0])

                #Mark mentor as allocated in mentees_df and mentors_replicated_df
                masa_mentees_students.loc[int(mentee_index),'MentorAllocated']   = True
                masa_mentees_students.loc[int(mentee_index),'MentorName']        = mentor_chosen['First Name'] + " " + mentor_chosen['Last Name']
                masa_mentees_students.loc[int(mentee_index),'MentorEmail']       = mentor_chosen['Email'] 
                masa_mentees_students.loc[int(mentee_index),'MentorAffiliation'] = mentor_chosen['Affiliation']     
                masa_mentors.loc[mentor_chosen_index,'MenteeAllocated'] = True
                masa_mentors.loc[mentor_chosen_index,'MenteeName']      = mentee['First Name'] + " " + mentee['Last Name']
                masa_mentors.loc[mentor_chosen_index,'MenteeEmail']     = mentee['Email']
                masa_mentors.loc[mentor_chosen_index,'MenteeAffiliation']     = mentee['Affiliation']                            

                #Remove matched mentor from leftover list
                mentors_remaining_df = mentors_remaining_df.drop(index=mentor_chosen_index)

                #Remove matched mentor from all area-specific lists.
                for temp_area in research_areas:
                    if(mentor_chosen_index in masa_mentors_by_area[temp_area].index):
                        masa_mentors_by_area[temp_area] = masa_mentors_by_area[temp_area].drop(index=mentor_chosen_index)
                    if(mentor_chosen_index in masa_mentors_industry[temp_area].index):
                        masa_mentors_industry[temp_area] = masa_mentors_industry[temp_area].drop(index=mentor_chosen_index)
                    if(mentor_chosen_index in masa_mentors_academia[temp_area].index):
                        masa_mentors_academia[temp_area] = masa_mentors_academia[temp_area].drop(index=mentor_chosen_index)

                #Update industry/academia preference match:

                if (((mentee['MaSA Mentee'] == 'Yes. I prefer a mentor from Academia.') and (mentor_chosen['IndustryOrAcademia'] in ['Academia.','Both Industry and Academia.'])) or
                   ((mentee['MaSA Mentee'] == 'Yes. I prefer a mentor from Industry.') and (mentor_chosen['IndustryOrAcademia'] in ['Industry.','Both Industry and Academia.']))):
                    num_mentees_got_affiliationtype += 1
                break                        

        ## Stop matching once we hit the number of commitments from mentors
        if(mentee_count >= num_mentor_commitments):
            break

##############################################################

## Match by Research Area
print("Matching Mentees Preferring Industry-Mentor: By Research Area")
match_research_area("Industry.")

## Match by Random Area    
print("Matching Mentees Preferring Industry-Mentor: By Random Area")
match_random_area("Industry.")
        
##############################################################
## MENTEES PREFRRING ACADEMIA MENTORS : Match Mentors By Reserach Area, then Random-Area
##############################################################

## Match by Research Area
print("Matching Mentees Preferring Academia-Mentor: By Research Area")
match_research_area("Academia.")

## Match by Random Area    
print("Matching Mentees Preferring Academia-Mentor: By Random Area")
match_random_area("Academia.")
        

##############################################################
## ALL REMAINING : Match Mentors By Reserach Area, then Random-Area
##############################################################
## Match by Research Area
print("Matching Mentees without strict-mentor preference: By Research Area")
match_research_area("ALL")

## Match by Random Area    
print("Matching Mentees without strict-mentor Preference: By Random Area")
match_random_area("ALL")

#masa_mentees_students.to_csv("masa_mentees.csv", index=False)






#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################
#########################################################################################################

mass_mentees = students_df.loc[students_df['MaSS Mentee'] == 'Yes'].copy()
mass_mentors = students_df.loc[students_df['MaSS Mentor'].isin((
    'Yes. I can mentor 1 junior student.',
    'Yes. I can mentor 2 junior students.'
    ))].copy()

mass_mentors_oneStudent  = mass_mentors.loc[mass_mentors['MaSS Mentor'] == 'Yes. I can mentor 1 junior student.']
mass_mentors_twoStudents = mass_mentors.loc[mass_mentors['MaSS Mentor'] == 'Yes. I can mentor 2 junior students.']

mass_mentors = pd.concat([mass_mentors_oneStudent, mass_mentors_twoStudents, mass_mentors_twoStudents], ignore_index=True)

mass_mentees= mass_mentees.drop(['Eulogy'], axis=1)
mass_mentors= mass_mentors.drop(['Eulogy'], axis=1)

mass_mentees = mass_mentees.drop(['MaSA Mentee', 'ResearchAreasMaSA', 'MaSS Mentor', 'ResearchAreasMentors'], axis=1)
mass_mentors= mass_mentors.drop(['MaSA Mentee', 'ResearchAreasMaSA', 'MaSS Mentee', 'ResearchAreasMaSS'], axis=1)

##
## Hasta aca tengo los dos arrays listos
##


mass_mentors_by_area = {}
for area in research_areas:
    mass_mentors_by_area[area] = mass_mentors[mass_mentors['ResearchAreasMentors'].str.contains(area,regex=False)]


mass_mentees.loc[:,'MentorAllocated']   = np.nan
mass_mentees.loc[:,'MentorName']        = np.nan
mass_mentees.loc[:,'MentorEmail']       = np.nan
mass_mentees.loc[:,'MentorAffiliation'] = np.nan

mass_mentors.loc[:,'MenteeAllocated']   = np.nan
mass_mentors.loc[:,'MenteeName']        = np.nan
mass_mentors.loc[:,'MenteeEmail']       = np.nan
mass_mentors.loc[:,'MenteeAffiliation'] = np.nan

num_mentor_commitments = mass_mentors['Email'].count()

def mass_match_research_area():
    global num_mentees_want_areamatch 
    global num_mentees_got_areamatch  
    global num_mentees_want_affiliationtype
    global num_mentees_got_affiliationtype 

    ## Shuffle mentees
    mass_mentees_df = mass_mentees.sample(frac=1)

    ## Choose Mentor Pool from which mentors chosen.
    mentors_pool = mass_mentors_by_area

    ## Match using research area
    mentee_count = 0
    for mentee_index, mentee in mass_mentees_df.iterrows():
        
        ## Bools for tracking stats of research area match
        mentee_wants_areamatch = False
        mentee_got_areamatch = False
        
        #Check if mentee is not allocated:
        if(mass_mentees_df.loc[int(mentee_index),'MentorAllocated'] != True) :                           
            ## Iterate over mentees research area
            for area in research_areas:
                if(area in mentee['ResearchAreasMaSS']):
                    if debug: print ("MenteeResearchArea: ",area)
                    mentee_wants_areamatch = True

                    #Check if Mentor available in mentee's research area
                    if(not mentors_pool[area].empty):                
                        #Get first available mentor from mentee's research area
                        mentor_chosen = mentors_pool[area].iloc[0] 
                        mentor_chosen_index = int(mentors_pool[area].index[0])
                        if debug: print("Chosen Mentor Index: "+str(mentor_chosen_index))
                        if debug: print(mentor_chosen['First Name'] + " "+mentor_chosen['Last Name'] + " MentorResearchAreas: "+mentor_chosen['ResearchAreasMentors'])

                        #Mark mentor as allocated in mentees_df and mentors_replicated_df
                        mass_mentees.loc[int(mentee_index),'MentorAllocated']   = True
                        mass_mentees.loc[int(mentee_index),'MentorName']        = mentor_chosen['First Name'] + " " + mentor_chosen['Last Name']
                        mass_mentees.loc[int(mentee_index),'MentorEmail']       = mentor_chosen['Email'] 
                        mass_mentees.loc[int(mentee_index),'MentorAffiliation'] = mentor_chosen['Affiliation']     

                        mass_mentors.loc[mentor_chosen_index,'MenteeAllocated'] = True
                        mass_mentors.loc[mentor_chosen_index,'MenteeName']      = mentee['First Name'] + " " + mentee['Last Name']
                        mass_mentors.loc[mentor_chosen_index,'MenteeEmail']     = mentee['Email']
                        mass_mentors.loc[mentor_chosen_index,'MenteeAffiliation']     = mentee['Affiliation']                            

                        #Delete matched mentor from all mentors_by_area, to prevent future hit on matched mentor-entry
                        for temp_area in research_areas:
                            if(mentor_chosen_index in mass_mentors_by_area[temp_area].index):
                                mass_mentors_by_area[temp_area] = mass_mentors_by_area[temp_area].drop(index=mentor_chosen_index)

                        mentee_count=mentee_count+1
                        #Mentee is matched
                        mentee_got_areamatch = True
                        break

                ## Update Research Area Match Stats
                if mentee_got_areamatch == True: num_mentees_got_areamatch += 1    
    
        ## Stop matching once we hit the number of commitments from mentors
        if(mentee_count >= num_mentor_commitments):
            break            
        
##############################################################

##############################################################
## Function: Random research-area based Matching with Mentor.
## Inputs: Mode (0 - Industry, 1-Academia, 2-Indifferent)
## Inputs: mentors_remaining_df -> list of unallocated mentors.
##############################################################

def mass_match_random_area():
    global num_mentees_want_affiliationtype
    global num_mentees_got_affiliationtype 
    
    ## Get remaining mentors that are not allocated yet.
    mentors_remaining_df = mass_mentors[mass_mentors['MenteeAllocated']!= True]    
    mentees_remaining_df = mass_mentees[mass_mentees['MentorAllocated']!= True]    
    
    #Shuffle leftovers
    mentors_remaining_df = mentors_remaining_df.sample(frac=1) 

    #Start Matching    
    mentee_count=0
    for mentee_index, mentee in mentees_remaining_df.iterrows():
        
        #If leftover mentee: Match with first leftover mentor
        if((mass_mentees.loc[int(mentee_index),'MentorAllocated'] != True)  and len(mentors_remaining_df.index)):
            mentor_chosen = mentors_remaining_df.iloc[0]
            mentor_chosen_index = int(mentors_remaining_df.index[0])

            #Mark mentor as allocated in mentees_df and mentors_replicated_df
            masa_mentees_students.loc[int(mentee_index),'MentorAllocated']   = True
            masa_mentees_students.loc[int(mentee_index),'MentorName']        = mentor_chosen['First Name'] + " " + mentor_chosen['Last Name']
            masa_mentees_students.loc[int(mentee_index),'MentorEmail']       = mentor_chosen['Email'] 
            masa_mentees_students.loc[int(mentee_index),'MentorAffiliation'] = mentor_chosen['Affiliation']     
            masa_mentors.loc[mentor_chosen_index,'MenteeAllocated'] = True
            masa_mentors.loc[mentor_chosen_index,'MenteeName']      = mentee['First Name'] + " " + mentee['Last Name']
            masa_mentors.loc[mentor_chosen_index,'MenteeEmail']     = mentee['Email']
            masa_mentors.loc[mentor_chosen_index,'MenteeAffiliation']     = mentee['Affiliation']                            

            #Remove matched mentor from leftover list
            mentors_remaining_df = mentors_remaining_df.drop(index=mentor_chosen_index)

            #Remove matched mentor from all area-specific lists.
            for temp_area in research_areas:
                if(mentor_chosen_index in mass_mentors_by_area[temp_area].index):
                    mass_mentors_by_area[temp_area] = mass_mentors_by_area[temp_area].drop(index=mentor_chosen_index)

            mentee_count=mentee_count+1    

        ## Stop matching once we hit the number of commitments from mentors
        if(mentee_count >= num_mentor_commitments):
            break

## Match by Research Area
print("Matching Mentees Preferring Industry-Mentor: By Research Area")
mass_match_research_area()

## Match by Random Area    
print("Matching Mentees Preferring Industry-Mentor: By Random Area")
mass_match_random_area()


mass_mentees_notselected = mass_mentees.loc[mass_mentees['MentorAllocated'].isnull()]
masa_mentees_notselected = masa_mentees_students.loc[masa_mentees_students['MentorAllocated'].isnull()]


#
#with pd.ExcelWriter('mass_matching.xlsx', engine='xlsxwriter') as writer:
#    mass_mentors.to_excel(writer, sheet_name='Mentors & Students')
#    mass_mentees_notselected.to_excel(writer, sheet_name='Students - Not assigned')


with pd.ExcelWriter('masa_matching.xlsx', engine='xlsxwriter') as writer:
    masa_mentors.to_excel(writer, sheet_name='Mentors & Students')
    masa_mentees_notselected.to_excel(writer, sheet_name='Students - Not assigned')

#mass_mentors.to_excel("mass_mentors.xlsx", sheet_name='masa_mentors')
#mass_mentors.to_excel("mass_mentors.xlsx", sheet_name='masa_mentors')


#mass_mentees.to_csv("mass_mentees.csv", index=False)
