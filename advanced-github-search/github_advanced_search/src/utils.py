import json

def read_json_file(file_path):
    """
    Reads JSON data from a file and returns it as a Python dictionary.

    :param file_path: Path to the JSON file.
    :return: Parsed JSON data as a dictionary or list.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_path} contains invalid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")