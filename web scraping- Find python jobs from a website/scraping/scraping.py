import os
import sys
import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_python_jobs(output_file: str = "jobs.txt", keywords=None):
    if keywords is None:
        keywords = ['python']

    website_url = 'https://infopark.in/companies/jobs-search'
    print(f"Scraping jobs from: {website_url}...")

    try:
        response = requests.get(website_url, verify=False, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching jobs from website: {e}")
        return False

    soup = BeautifulSoup(response.text, 'html.parser')
    jobs = soup.find_all('div', {'class': 'row company-list joblist'})
    print(f"Found {len(jobs)} job listings. Filtering for keywords: {keywords}...")

    matched_jobs = 0
    with open(output_file, 'w', encoding='utf-8') as file:
        for job in jobs:
            title_element = job.find('a')
            if not title_element:
                continue

            title = title_element.text.strip()
            link = title_element.get('href', '')
            comp_elem = job.find('div', {'class': 'jobs-comp-name'})
            company = comp_elem.text.strip() if comp_elem else "N/A"

            date_elem = job.find('div', {'class': 'job-date'})
            last_date = date_elem.text.strip() if date_elem else "N/A"

            if any(word.lower() in title.lower() for word in keywords):
                matched_jobs += 1
                print(f"Match: {title} | {company} | {last_date}")
                file.write(f"{title} {company} {last_date}\n{link}\n\n")

    print(f"Done! {matched_jobs} matching job(s) saved to '{output_file}'.")
    return True

def main():
    fetch_python_jobs()

if __name__ == '__main__':
    main()