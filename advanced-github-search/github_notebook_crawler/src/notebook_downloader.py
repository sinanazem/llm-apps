import os
import requests
import json

def fetch_repo_content(repo_owner, repo_name, path=''):
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{path}"
    headers = {'Accept': 'application/vnd.github.v3+json'}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch repo content: {e}")
        return None

def download_file(file_url, local_file_path):
    try:
        response = requests.get(file_url)
        response.raise_for_status()
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        with open(local_file_path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded: {file_url} to {local_file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download file {file_url}: {e}")

def process_github_repo(repo_owner, repo_name, metadata_output_path):
    contents = fetch_repo_content(repo_owner, repo_name)
    if contents is None:
        return

    base_raw_url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main"
    base_main_github_url = f"https://github.com/{repo_owner}/{repo_name}/blob/main"
    metadata = {}

    stack = [('', contents)]
    while stack:
        current_path, directory_contents = stack.pop()
        for item in directory_contents:
            if item['type'] == 'file' and item['name'].endswith('.ipynb'):
                file_path = item['path']
                raw_file_url = f"{base_raw_url}/{file_path.replace(' ', '%20')}"
                github_url = f"{base_main_github_url}/{file_path.replace(' ', '%20')}"
                local_file_path = os.path.join("downloaded_files", file_path)

                # Download the notebook
                download_file(raw_file_url, local_file_path)

                # Store both raw and main GitHub URLs in metadata
                metadata[local_file_path] = {
                    "raw_url": raw_file_url,
                    "github_url": github_url
                }
            
            elif item['type'] == 'dir':
                # Fetch contents of the directory
                sub_dir_contents = fetch_repo_content(repo_owner, repo_name, item['path'])
                if sub_dir_contents:
                    stack.append((item['path'], sub_dir_contents))

    # Save metadata to a JSON file
    with open(metadata_output_path, 'w', encoding='utf-8') as metadata_file:
        json.dump(metadata, metadata_file, ensure_ascii=False, indent=4)

    print(f"Metadata saved to {metadata_output_path}")


if __name__ == "__main__":
    # Usage
    repo_owner = 'pytopia'
    repo_name = 'Python-Programming'
    metadata_output_file = 'notebook_metadata.json'
    process_github_repo(repo_owner, repo_name, metadata_output_file)