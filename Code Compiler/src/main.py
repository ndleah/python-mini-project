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


# Compile the code by sending POST request to Online Code Compiler API

def compile_code(language_id, api_key):

    # Grab the User input from input.txt and read it.
    
    input_path = "input/input.txt"

    with open(input_path, mode='r') as file:
        user_input = file.read()

    
    # Grab the user code from code.txt file

    code_path = "input/code.txt"

    with open(code_path, mode='r') as file:
        code = file.read()


    # Grab the host and url from Environment file

    host = os.getenv("HOST")
    url = os.getenv("COMPILE_CODE_URL")


    # Define the headers for the api call

    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": host
    }


    # Define the body for the api call

    payload = {
        "language": language_id,
        "version": "latest",
        "code": code,
        "input": user_input
    }


    try:
        # Hit the API to compile the code
        response = requests.post(url=url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()
        logging.info("Successfully compiled the code.")
        return data
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Error making the compile request: {e}")
        return None
    
    except Exception as e:
        logging.error(f"An unexpected error occurred during compilation: {e}")
        return None


# Get the language details in JSON list and get the language_id from User input of language name. Return an exception if it doesn't exist.

language_extractor = get_language(api_key)

language_name = input("Enter your choice of language. You can refer to language_list.txt in input folder for reference :  ")

language_id = None  # Initialize language_id to None

for language_detail in language_extractor:
    if language_detail['name'].lower() == language_name.lower():
        language_id = language_detail['id']
        break

else:
    # This block is executed when the loop completes without finding a match
    error_message = f"Language '{language_name}' not found in the language list. Available languages are: {[lang['name'] for lang in language_extractor]}"
    logging.error(error_message)
    raise ValueError(error_message)


# Compile the code and write the result into /bin in output.txt

output = compile_code(language_id, api_key)

with open("bin/output.txt", mode='w') as file:
    file.write(output['output'])
    logging.info("Output written to bin/output.txt.")