import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = 'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DAPPLE&page='

def mobile_name(doc_new):
    prase = doc_new.find_all('div', class_='_4rR01T')
    names = []
    for tag in prase:
        names.append(tag.text.strip())
    return names

def prices(doc_new):
    price = doc_new.find_all('div',class_='_30jeq3 _1_WHN1')
    price_link = []
    for i in price:
        price_link.append(i.text.strip())
    return price_link

def percentage_off(doc_new):
    off = doc_new.find_all('div',class_='_3Ay6Sb')
    off_link =[]
    for i in off:
        off_link.append({'Percentage off':i.text.strip()})
    return off_link  

def rating(doc_new):
    ratings = doc_new.find_all('div', class_='_3LWZlK')
    all_ratings = []
    for i in ratings:
        all_ratings.append(i.text.strip())
    return all_ratings

def mobile_description(doc_new):
    mobile_description = doc_new.find_all('ul', class_='_1xgFaf')
    mobile_info_link=[]
    for i in mobile_description:
        mobile_info_link.append(i.text.strip())
    return mobile_info_link 

def for_all_pages(page_no):
    page_no_url = base_url +  str(page_no)
    response = requests.get(page_no_url)
    
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ' + page_no_url)
        
    doc_new =  BeautifulSoup(response.text)
    mobile_names_new = mobile_name(doc_new)
    all_prices_new = prices(doc_new)
    all_ratings_new = rating(doc_new)
    first_page_new = mobile_description(doc_new)
    data_new = {'Name': mobile_names_new,  #getting all the information in a dictionary
       'Prices':all_prices_new,
       'ratings':all_ratings_new,
       'Description':first_page_new}
    
    return pd.DataFrame(data_new)   #return directly a dataframe.

#Below is our helper function to add all data frames.

def all_info(num_of_page):
    all_df = []
    for i in range(1, num_of_page + 1):
        all_df.append(for_all_pages(page_no=i))

    if all_df:
        merge = pd.concat(all_df, ignore_index=True)
        merge.to_csv('all info.csv', index=False)
        return 'all info.csv'
    return None


