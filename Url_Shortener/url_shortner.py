import requests
import json

UI = input("Enter the long link: ")
api_key = 'You api key here'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

data = {"long_url": UI}
for i in range(3): 
    result = requests.post("https://api-ssl.bitly.com/v4/shorten", headers=headers, data=json.dumps(data))
    if result.status_code == 200:
        break
if result.status_code == 200:
    link = json.loads(result.content)['link']
    print(f"\nYour shortened link: {link}")
else:
    print("error occured")

