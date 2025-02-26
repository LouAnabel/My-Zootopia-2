from data_fetcher import fetch_data
# or in main: animals_data = data_fetcher.fetch_data(animal_name)


def get_user_input():
    user_input = input("Please enter the animal you want to search for: ")
    return user_input

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


def main():
    with open("animals_template.html", 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

        user_animal = get_user_input()
        api_url = 'https://api.api-ninjas.com/v1/animals?name={}'.format(user_animal)

        animals_data = fetch_data(api_url, user_animal)
        if len(animals_data) > 0:
            output = ''
            for animal in animals_data:
                output += serialize_animal(animal)

            html_content = html_content.replace("__REPLACE_ANIMALS_INFO__", output)

            with open("animals.html", 'w') as new_file:
                new_file.write(html_content)
            print("\nWebsite was successfully generated to the file animals.html.")

        else:
            error_message = f"<h2>Error! The animal {user_animal} doesn't exist. Please check if it's correctly written and in english!</h2>"
            html_content = html_content.replace("__REPLACE_ANIMALS_INFO__", error_message)

            with open("animals.html", 'w') as new_file:
                new_file.write(html_content)

            print(f"Error: Unfortunately {user_animal} was not found in the list of animals. Try again.")


if __name__ == "__main__":
    main()
