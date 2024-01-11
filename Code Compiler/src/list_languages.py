import requests
import os
import logging
from dotenv import load_dotenv

# Configure logging

logging.basicConfig(filename='bin/logfile.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')


load_dotenv()


# Get API Key from environment path

api_key = os.getenv("API_KEY")


# GET language list from Online Code Compiler API using requests library

def get_language(api_key):

    url = os.getenv("LANGUAGE_LIST_URL")

    host = os.getenv("HOST")
    
    headers = {
        "X-RapidAPI-Key" : api_key,
        "X-RapidAPI-Host" : host
    }

    try:
        response = requests.get(url=url, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        logging.info("Successfully fetched language data.")
        return data
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error making the request: {e}")
        return None
    
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None


# Get the language details in JSON list and define the path to dump the language list

language_extractor = get_language(api_key)

file_path = "input/language_list.txt"


# Truncate the file_path if it exists or create a new one and Write all the Language names from language_extractor

with open(file_path, mode='w') as file:

    for language_detail in language_extractor:
        file.write(language_detail['name']+'\n')
        logging.info(f"Language '{language_detail['name']}' written to file.")