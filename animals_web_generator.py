import json
import requests



"""creates the string of all the info for each 
animal that will be added to the json and displayed on the website"""
def serialize_animal(animal):
    output = ' '
    output += "<li class='cards__item'>\n"
    output += f"<div class='card__title'>{animal.get('name', 'Unknown')}</div><br/>\n"
    output += "<div class='card__text'>\n"
    output += "<ul class='info_block'\n>"
    output += f"<li class='diet'><strong>Diet:</strong> {animal.get('characteristics', 'Unknown')['diet']}<br/>\n"
    output += f"<li class='location'><strong>Location:</strong> {' and '.join(animal.get('locations', 'Unknown'))}<br/>\n"
    if "type" in animal['characteristics']:
        output += f"<li class='type'><strong>Type:</strong> {animal['characteristics']['type']}\n"
    output += "</ul>"
    output += "</div>"
    output += "</li>"
    return output

def get_user_input():
    user_input = input("Please enter the animal you want to search for: ")
    return user_input

def get_info_from_API(api_url, user_animal):
    response = requests.get(api_url, headers={'X-Api-Key': 'q9r48ssh7l6bFIW9jifEIQ==L3BwmkN4TTAnt5Qg'})
    if response.status_code == requests.codes.ok:
        animals = response.json()
        return animals
    else:
        error_message = "Error:", response.status_code, response.text
        return error_message

def main():
    user_animal = get_user_input()
    api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(user_animal)

    with open("animals_template.html", 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    animals_data = get_info_from_API(api_url, user_animal)
    print("Website was successfully generated to the file animals.html.")
    print(animals_data)


    output = ''
    for animal in animals_data:
        output += serialize_animal(animal)

    html_content = html_content.replace("__REPLACE_ANIMALS_INFO__", output)

    with open("animals.html", 'w') as new_file:
        new_file.write(html_content)

if __name__ == "__main__":
    main()
