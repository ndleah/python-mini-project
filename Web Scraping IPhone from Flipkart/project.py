import os
import smtplib
import pandas as pd
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup

try:
    from password import username, password
except ImportError:
    username = os.environ.get('SMTP_USERNAME', '')
    password = os.environ.get('SMTP_PASSWORD', '')

base_url = 'https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&otracker=categorytree&p%5B%5D=facets.brand%255B%255D%3DAPPLE&page='

def mobile_name(doc_new):
    prase = doc_new.find_all('div', class_='_4rR01T')
    names = []
    for tag in prase:
        names.append(tag.text.strip())
    return names

def prices(doc_new):
    price = doc_new.find_all('div', class_='_30jeq3 _1_WHN1')
    price_link = []
    for i in price:
        price_link.append(i.text.strip())
    return price_link

def percentage_off(doc_new):
    off = doc_new.find_all('div', class_='_3Ay6Sb')
    off_link = []
    for i in off:
        off_link.append({'Percentage off': i.text.strip()})
    return off_link  

def rating(doc_new):
    ratings = doc_new.find_all('div', class_='_3LWZlK')
    all_ratings = []
    for i in ratings:
        all_ratings.append(i.text.strip())
    return all_ratings

def mobile_description(doc_new):
    mobile_description = doc_new.find_all('ul', class_='_1xgFaf')
    mobile_info_link = []
    for i in mobile_description:
        mobile_info_link.append(i.text.strip())
    return mobile_info_link 

def for_all_pages(page_no):
    page_no_url = base_url + str(page_no)
    response = requests.get(page_no_url, timeout=10)
    
    if response.status_code != 200:
        print('Status code:', response.status_code)
        raise Exception('Failed to fetch web page ' + page_no_url)
        
    doc_new = BeautifulSoup(response.text, features='html.parser')
    mobile_names_new = mobile_name(doc_new)
    all_prices_new = prices(doc_new)
    all_ratings_new = rating(doc_new)
    first_page_new = mobile_description(doc_new)

    min_len = min(len(mobile_names_new), len(all_prices_new), len(all_ratings_new), len(first_page_new))
    data_new = {
        'Name': mobile_names_new[:min_len],
        'Prices': all_prices_new[:min_len],
        'ratings': all_ratings_new[:min_len],
        'Description': first_page_new[:min_len]
    }
    
    return pd.DataFrame(data_new)

def all_info(num_of_page):
    all_df = []
    for i in range(1, num_of_page + 1):
        all_df.append(for_all_pages(page_no=i))

    if all_df:
        merge = pd.concat(all_df, ignore_index=True)
        filename = 'all info.csv'
        merge.to_csv(filename, index=False)
        return filename
    return None

def send_email(body):
    if not username or not password:
        print("Notice: SMTP credentials not set in password.py or environment. Skipping email dispatch.")
        return

    emailfrom = 'yb4coding@gmail.com'
    emailto = 'yb4coding@gmail.com'
    fileToSend = "all info.csv"

    if not os.path.exists(fileToSend):
        print(f"Error: {fileToSend} does not exist.")
        return

    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = "Spreadsheet of iPhones present in flipkart containing all information."

    ctype, encoding = mimetypes.guess_type(fileToSend)
    if ctype is None or encoding is not None:
        ctype = "application/octet-stream"

    maintype, subtype = ctype.split("/", 1)

    try:
        with open(fileToSend, "rb" if maintype != "text" else "r") as fp:
            if maintype == "text":
                attachment = MIMEText(fp.read(), _subtype=subtype)
            else:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                encoders.encode_base64(attachment)

        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587", timeout=10)
        server.starttls()
        server.login(username, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        print("Your file has been delivered via email.")
    except Exception as e:
        print(f"SMTP dispatch note: {e}")

if __name__ == "__main__":
    print('Creating dataframe')
    try:
        csv_file = all_info(2)
        print("Generated CSV file:", csv_file)
        if csv_file:
            send_email(csv_file)
    except Exception as err:
        print("Scraper execution note:", err)


