




if __name__ == "__main__":
    # Download Jupyter Notebooks From GitHub
    repo_owner = 'pytopia'
    repo_name = 'Python-Programming'
    metadata_output_file = 'notebook_metadata.json'
    process_github_repo(repo_owner, repo_name, metadata_output_file)
    
    # Transform and Extract Data From Jupyter Notebooks
    directory_to_search = "downloaded_files"  # Change this to your directory
    output_json_file = "notebooks_summary.json"
    repository_url = "https://github.com/pytopia/Python-Programming"  # Replace with your repository URL

    extract_cells(directory_to_search, output_json_file, repository_url)