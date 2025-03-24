from data_fetcher import fetch_data


def get_user_input():
    """Gets the name of the animal from the user."""
    return input("Please enter the animal you want to search for: ")


def create_html_element(tag, content, class_name=None):
    """Creates an HTML element with optional class."""
    class_attr = f" class='{class_name}'" if class_name else ""
    return f"<{tag}{class_attr}>{content}</{tag}>"


def format_info_item(label, value):
    """Creates a formatted list item for an animal attribute."""
    return f"<li class='{label.lower()}'><strong>{label}:</strong> {value}<br/>\n"


def get_safe_diet(animal):
    """Safely extracts diet information from animal data."""
    characteristics = animal.get('characteristics', {})
    if isinstance(characteristics, dict) and 'diet' in characteristics:
        return characteristics['diet']
    return 'Unknown'


def get_safe_location(animal):
    """Safely extracts location information from animal data."""
    locations = animal.get('locations', ['Unknown'])
    if isinstance(locations, list):
        return ' and '.join(locations)
    return 'Unknown'


def get_safe_type(animal):
    """Safely extracts type information from animal data."""
    characteristics = animal.get('characteristics', {})
    if isinstance(characteristics, dict) and 'type' in characteristics:
        return characteristics['type']
    return None


def serialize_simple_animal(animal_str):
    """Creates HTML for a non-dictionary animal."""
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


def serialize_animal(animal):
    """Creates HTML content for an animal."""
    # Handle non-dictionary animal
    if not isinstance(animal, dict):
        return serialize_simple_animal(str(animal))

    # Start building the card
    output = "<li class='cards__item'>\n"
    output += f"<div class='card__title'>{animal.get('name', 'Unknown')}</div><br/>\n"
    output += "<div class='card__text'>\n"
    output += "<ul class='info_block'>\n"

    # Add animal information
    output += format_info_item('Diet', get_safe_diet(animal))
    output += format_info_item('Location', get_safe_location(animal))

    # Add type if available
    animal_type = get_safe_type(animal)
    if animal_type:
        output += format_info_item('Type', animal_type)

    # Close tags
    output += "</ul>\n</div>\n</li>"
    return output


def generate_html_file(html_template, animal_content):
    """Generates the final HTML file with animal content."""
    final_html = html_template.replace("__REPLACE_ANIMALS_INFO__", animal_content)
    with open("animals.html", 'w', encoding='utf-8') as new_file:
        new_file.write(final_html)


def process_animal_data(animals_data, user_animal):
    """Processes valid animal data and returns HTML content."""
    # Validate data
    if not isinstance(animals_data, list) or len(animals_data) == 0:
        print(f"Error: Unfortunately {user_animal} was not found in the list of animals. Try again.")
        return None

    # Check if valid data (not an error string)
    if not isinstance(animals_data[0], dict) or str(animals_data[0]).startswith('ERROR'):
        print(f"Error: The data for {user_animal} seems invalid. Please try again.")
        return None

    # Generate HTML for all animals
    output = ''
    for animal in animals_data:
        output += serialize_animal(animal)

    return output


def main():
    """Main function to control the program flow."""
    # Load HTML template
    with open("animals_template.html", 'r', encoding='utf-8') as html_file:
        html_template = html_file.read()

    while True:
        try:
            # Get user input and fetch data
            user_animal = get_user_input()
            api_url = f'https://api.api-ninjas.com/v1/animals?name={user_animal}'
            animals_data = fetch_data(api_url, user_animal)

            # Process animal data
            animal_content = process_animal_data(animals_data, user_animal)
            if animal_content:
                # Generate HTML file
                generate_html_file(html_template, animal_content)
                print(f"\nWebsite for {user_animal} was successfully generated to the file animals.html.")
                break  # Success! Exit the loop

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again with a different animal name.")


if __name__ == "__main__":
    main()