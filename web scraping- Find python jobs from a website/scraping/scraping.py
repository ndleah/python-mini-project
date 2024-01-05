import requests
from bs4 import BeautifulSoup


# to find python jobs from  infopark website

website_url='https://infopark.in/companies/jobs-search'
keywords=['python']
file=open('jobs.txt','w')
response=requests.get(website_url,verify=False)
soup=BeautifulSoup(response.text,'lxml')
jobs=soup.find_all('div',{'class':'row company-list joblist'})



# store data in a file as txt format
for job in jobs:
    title_elment=job.find('a')
    title=title_elment.text
    link=title_elment['href']
    company=job.find('div',{'class':'jobs-comp-name'}).text
    last_date=job.find('div',{'class':'job-date'}).text
    if any(word.lower() in title.lower() for word in keywords ):

        print(title,company,last_date,link)
        file.write(title + ' '+company + ' '+last_date +'\n '+ link +'\n\n' )