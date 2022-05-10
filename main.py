# These are the imports necessary for the code to run
import requests
import re
from bs4 import BeautifulSoup
import csv
# This opens a CSV file that is called file.csv
csv_file=open("file.csv", 'w')
csv_writer= csv.writer(csv_file)
csv_writer.writerow(["Eligibilty","Location","State", "Country", "Zip Code", "Study Type", "Study Design", "Conditions","Interventions","Enrollment"'Number of Baseline Participants', 'Analysis Population Description', 'Age', ''," ","(Age)Number Analyzed","Mean of Age", "Standard Deviation of Age","","(Sex)Number Analyzed","Female", "Female Percent", "Male", "Male Percent", '',"(Ethnicity)Number Analyzed" , "Hispanic/Latino", "Hispanic/latino percent","Not Hispanic", "Not Hispanic Percent","Unknown", "Unknown percent", "", "(Race)Number Analyzed", "American Indian or Alaska Native","American Indian or Alaska Native %","Asian", "Asian %","Native Hawaiian or Other Pacific Islander", "Native Hawaiian or Other Pacific Islander %", "Black or African American","Black or African American %","White","White %","More than one race", "More than one race %","Unknown or Not Reported","Unknown or Not Reported %", "", "URL"] )
# The line above allows you to write the headers of the CSV file and correlate it to the data that will be scraped
url="https://www.clinicaltrials.gov/ct2/show/study/NCT02831998?recrs=e&rslt=With&cntry=US&draw=2&rank=2762"

count=0

for i in range(3000):
#you can change the range to the amount of pages you want scraped    
                        
    
            
    source=requests.get(url).text
    #the line above changes the data recieved into text or string type    
        
    soup = BeautifulSoup(source, "html5lib")
    #line above initializes the beautiful soup library, here is a tutorial on it you will need to be familiar with it: https://www.youtube.com/watch?v=ng2o98k983k
    
    next= soup.find(class_="tr-next-link", href=True)
    # this line gets the link to the next page
    
    next=next['href']
    # makes the link equal the "next" variable
    
    # empty arrays for storage     
    results=[]
    study_r=[]
    results_2=[] 
    r=[]
    locat=[]
     #make sure you watch the tutorial in the comment above or you won't understand the loops below!
    for location in soup.find_all("table", class_= "ct-layout_table tr-indent2"):
        location1=location.text
        location1=" ".join(location1.split())
        locat.append(location1)
        # for the line below I am removing uncessary strings to make the data cleaner
        new_set = [x.replace('Layout table for location information United States, ', '') for x in locat]
     # This removes the second index all we need is location    
    locat= new_set
    if len(locat)== 2:    
        locat.pop(1)
    
     # I create an empty array and split locat array based on commas    
    b=[]
    for i in locat:
        b+=i.split(", ")

    locat=b
    # for the block of code below I store the data for eligibilty in the array m
    m=[]
    for crit in soup.find_all("table", class_= "ct-layout_table tr-tableStyle tr-studyInfo"):
        crit1=crit.text
        crit1=" ".join(crit1.split())
        m.append(crit1)
    
    m.pop(0)#remove unecessary data
    
    # now that the location and eligibilty data is collected we need to go to the study results page so I replace the strings in the URL
    url = url.replace("study", "results")
    
    source=requests.get(url).text
    
        
        
    soup = BeautifulSoup(source, "html5lib")
    # Gets the link for the next page on the new page we are on
    next= soup.find(class_="tr-next-link", href=True)
    
    
    next=next['href']
    
    # the loop below gets all the study details data and stores it in results   
    for study in soup.find_all("td", class_= "ct-body3"):
        study1=study.text
        study1=" ".join(study1.split())
        study_r.append(study1)
     
    #This loop scrapes all baseline characteristics and cleans it
    for demo in soup.find_all("td", class_= "de-numValue_baselineDataCell"):
        demo1= demo.text
        demo1=" ".join(demo1.split())
        results.append(demo1)
        new_set = [x.replace(' participants', '') for x in results]
        w= [x.replace('[Not Specified]', 'N/A') for x in new_set]
        results=w
    for i in results:
        x=i.split(" ", 1)
        
        results_2.append(x)
    results = [item for sublist in results_2 for item in sublist]
    
    
    # The block of code below gets rid of unwanted data in the results array
    if len(results) >= 37:
        results= results[:38]
    results.append(url)
    if results[3] != '':
        results= results[0:3]+results[4:]


     # The line below makes the url equal the url of the next page after getting all the data
    url="https://www.clinicaltrials.gov"+next
    
    # The line below replace strings in the url to go to the study details page
    url= url.replace("results", "study")
    
    #adds location data, study detail data, and eligibilty to the results array
    results= study_r+results
    results= locat+results
    results= m+ results
    
    count+=1

    # This loops gets all the character data in baseline characteristics so pages can be skipped if it is not the format desired
    for demo in soup.find_all("td", class_= "de-baselineLabelCell"):
        titles=demo.text
        titles=" ".join(titles.split())
        r.append(titles)
     # The block of code below can be changed based on the patterns seen on pages and the format you want scraped 
    if len(locat) > 4:
        continue
        
    if "Asian" not in r:
        continue    
    if "0.0%" not in results:
        continue
    
    if "Total of all reporting groups" in r:
        continue
    
    if "Between 18 and 65 years" in r:
        continue
    if "Not Hispanic or Latino" not in r:
        continue
    if "Age 17" in r:
        continue
        
        
        
           
     #adds results to the CSV file      
    csv_writer.writerow(results)
    
        
    
            
        
        
                
    
    
    print(results)
    print("page"+str(count))
    print(len(results))
    print("\n")
    
#closes the CSV file    
csv_file.close()


