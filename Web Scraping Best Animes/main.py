import requests
from bs4 import BeautifulSoup

list_challenges_url = "https://www.listchallenges.com/top-100-anime-of-all-time-according-to-the"
# list_challenges_url2 = "https://www.listchallenges.com/top-100-anime-of-all-time-according-to-the/list/2"
# list_challenges_url3 = "https://www.listchallenges.com/top-100-anime-of-all-time-according-to-the/list/3"

response = requests.get(url=list_challenges_url)
response.raise_for_status()
# response2 = requests.get(url=list_challenges_url2)
# response2.raise_for_status()
# response3 = requests.get(url=list_challenges_url3)
# response3.raise_for_status()

list_challenges_html = response.text
list_challenges_soup = BeautifulSoup(list_challenges_html, 'html.parser')
# list_challenges_html2 = response2.text
# list_challenges_soup2 = BeautifulSoup(list_challenges_html2, 'html.parser')
# list_challenges_html3 = response3.text
# list_challenges_soup3 = BeautifulSoup(list_challenges_html3, 'html.parser')

title_anchors = list_challenges_soup.find_all(name="div", class_="item-name")
# title_anchors2 = list_challenges_soup2.find_all(name="div", class_="item-name")
# title_anchors3 = list_challenges_soup3.find_all(name="div", class_="item-name")

titles = [title.getText() for title in title_anchors]
# titles2 = [title.getText() for title in title_anchors2]
# titles3 = [title.getText() for title in title_anchors3]
# titles += titles2 + titles3

with open("best_animes", "w", encoding="utf-8") as file:
    for title in titles:
        file.write(title + "\n")