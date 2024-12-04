import os
import json
import nbformat
import re

def clean_toc(content):
    """
    Cleans up the "Table of Contents" content by extracting plain text headings.
    
    Parameters:
    - content (str): The raw markdown content of the TOC cell.
    
    Returns:
    - list of str: A list containing the plain text titles of each TOC entry.
    """
    lines = content.splitlines()
    cleaned_lines = []
    
    # Regular expression to find markdown list items with links
    toc_regex = re.compile(r'^\s*[-*]\s*\[(.*?)\]\(.*?\)\s*$')
    
    for line in lines:
        match = toc_regex.match(line)
        if match:
            cleaned_lines.append(match.group(1))
    
    return cleaned_lines

def clean_exercise(content):
    """
    Cleans the "Practice Exercise" content by removing markdown syntax and excess whitespace.
    
    Parameters:
    - content (str): The raw content of the exercise cell.
    
    Returns:
    - str: Cleaned content as plain text.
    """
    # Remove markdown links and other formatting
    cleaned_content = re.sub(r'\[.*?\]\(.*?\)', '', content)  # Remove markdown links
    cleaned_content = re.sub(r'^\s*[-*]\s*', '', cleaned_content, flags=re.MULTILINE)  # Remove list markers
    cleaned_content = re.sub(r'\s+', ' ', cleaned_content).strip()  # Reduce whitespace
    return cleaned_content

def extract_cells(directory, json_output_path, notebook_metadata):
    """
    Extracts "Table of Contents" and "Practice Exercise" cells from all Jupyter notebooks in a directory,
    cleans them, and saves the information to a JSON file.
    
    Parameters:
    - directory (str): The directory path to search for Jupyter notebooks.
    - json_output_path (str): The path to save the output JSON file.
    - repo_url (str): The repository URL to include in the JSON output.
    """
    notebook_data = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb"):
                notebook_path = os.path.join(root, file)

                try:
                    with open(notebook_path, 'r', encoding='utf-8') as nb_file:
                        nb = nbformat.read(nb_file, as_version=4)

                        toc_content = ""
                        practice_exercises = []
                        capturing_exercise = False

                        for cell in nb.cells:
                            if cell.cell_type == 'markdown':
                                cell_text = cell.source.lower()

                                if "table of contents" in cell_text:
                                    toc_content = clean_toc(cell.source)
                                elif "practice exercise" in cell_text or "Exercise:" in cell_text:
                                    capturing_exercise = True
                                    practice_exercises.append(clean_exercise(cell.source))
                                elif capturing_exercise and re.match(r'^\s*#', cell.source):
                                    capturing_exercise = False

                            if capturing_exercise:
                                practice_exercises.append(clean_exercise(cell.source))

                        notebook_data.append({
                            "local_path": notebook_path,
                            "name": os.path.splitext(file)[0],
                            "table_of_content": toc_content,
                            "practice_exercises": practice_exercises,
                            "github_link": notebook_metadata[notebook_path]['github_url']
                        })
                except (nbformat.reader.NotJSONError, json.JSONDecodeError) as e:
                    print(f"Error reading {notebook_path}: {e}")

    with open(json_output_path, 'w', encoding='utf-8') as json_file:
        json.dump(notebook_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Notebook data saved to {json_output_path}")

if __name__ == "__main__":
    directory_to_search = "downloaded_files"  # Change this to your directory
    output_json_file = "notebooks_summary.json"
    repository_url = "https://github.com/pytopia/Python-Programming"  # Replace with your repository URL

    extract_cells(directory_to_search, output_json_file, repository_url)