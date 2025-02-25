import json
import requests

def fetch_data(api_url, animal_name):
    response = requests.get(api_url, headers={'X-Api-Key': 'q9r48ssh7l6bFIW9jifEIQ==L3BwmkN4TTAnt5Qg'})
    if response.status_code == requests.codes.ok:
        animals = response.json()
        print(animals)
        return animals
    else:
        error_message = "Error:", response.status_code, response.text
        return error_message


