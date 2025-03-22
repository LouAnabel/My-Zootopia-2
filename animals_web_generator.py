from data_fetcher import fetch_data


def get_user_input():
    user_input = input("Please enter the animal you want to search for: ")
    return user_input


def serialize_animal(animal):
    """creates the string of all the info for each
    animal that will be added to the json and displayed on the website"""

    # Check if animal is a dictionary
    if not isinstance(animal, dict):
        animal_str = str(animal)
        return f"""
        <li class='cards__item'>
            <div class='card__title'>{animal_str}</div><br/>
            <div class='card__text'>
                <ul class='info_block'>
                    <li class='diet'><strong>Diet:</strong> Unknown<br/>
                    <li class='location'><strong>Location:</strong> Unknown<br/>
                </ul>
            </div>
        </li>
        """

    output = ' '
    output += "<li class='cards__item'>\n"
    output += f"<div class='card__title'>{animal.get('name', 'Unknown')}</div><br/>\n"
    output += "<div class='card__text'>\n"
    output += "<ul class='info_block'>\n"

    # Safely get diet
    characteristics = animal.get('characteristics', {})
    if isinstance(characteristics, dict) and 'diet' in characteristics:
        diet = characteristics['diet']
    else:
        diet = 'Unknown'
    output += f"<li class='diet'><strong>Diet:</strong> {diet}<br/>\n"

    # Safely get location
    locations = animal.get('locations', ['Unknown'])
    if isinstance(locations, list):
        location_str = ' and '.join(locations)
    else:
        location_str = 'Unknown'
    output += f"<li class='location'><strong>Location:</strong> {location_str}<br/>\n"

    # Safely add type if it exists
    if isinstance(characteristics, dict) and "type" in characteristics:
        output += f"<li class='type'><strong>Type:</strong> {characteristics['type']}\n"

    output += "</ul>"
    output += "</div>"
    output += "</li>"
    return output


def main():
    with open("animals_template.html", 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()

    while True:
        try:
            # Get user input
            user_animal = get_user_input()
            api_url = f'https://api.api-ninjas.com/v1/animals?name={user_animal}'

            # Fetch data
            animals_data = fetch_data(api_url, user_animal)

            # Check if we have valid animal data
            if isinstance(animals_data, list) and len(animals_data) > 0:
                # Check if the first item is a dictionary (not an error string)
                if isinstance(animals_data[0], dict) and not str(animals_data[0]).startswith('ERROR'):
                    output = ''
                    for animal in animals_data:
                        output += serialize_animal(animal)

                    # Generate HTML file
                    html_content = html_content.replace("__REPLACE_ANIMALS_INFO__", output)
                    with open("animals.html", 'w', encoding='utf-8') as new_file:
                        new_file.write(html_content)

                    print(f"\nWebsite for {user_animal} was successfully generated to the file animals.html.")
                    break  # Success! Exit the loop
                else:
                    print(f"Error: The data for {user_animal} seems invalid. Please try again.")
                    continue  # Try again
            else:
                print(f"Error: Unfortunately {user_animal} was not found in the list of animals. Try again.")
                continue  # Try again

        except Exception as e:
            # Handle any exceptions
            print(f"An error occurred: {str(e)}")
            print("Please try again with a different animal name.")
            continue  # Try again

if __name__ == "__main__":
    main()
