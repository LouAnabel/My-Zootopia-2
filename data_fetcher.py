import os
from dotenv import load_dotenv
import requests

#loading variables from .env
load_dotenv()

#access environment variables from .env file
API_KEY = os.getenv('API_KEY')

def fetch_data(api_url, animal_name):
    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    if response.status_code == requests.codes.ok:
        animals = response.json()
        print(animals)
        return animals
    else:
        error_message = "Error:", response.status_code, response.text
        return error_message

