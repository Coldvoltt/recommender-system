import os
import requests
import zipfile


def get_data(url):
    """
    Function: get_data

    Description:
    The `get_data` function is used to download a ZIP file from a given URL, 
    extract its contents to the current working directory, and remove the downloaded 
    ZIP file as part of the cleanup process. This function simplifies the process of 
    obtaining data from a remote source and making it available locally for further use.

    Parameters:
    - url (str): The URL of the ZIP file to be downloaded and extracted.

    Usage Example:
    ```python
    # Specify the URL for the ZIP file
    zip_url = 'https://files.grouplens.org/datasets/movielens/ml-latest-small.zip'

    # Call the function to download and extract the data
    get_data(zip_url)

    """

    # Get the current working directory
    extraction_path = os.getcwd()

    # Download the ZIP file
    response = requests.get(url)
    with open(os.path.join(extraction_path, 'downloaded.zip'), 'wb') as file:
        file.write(response.content)

    # Extract the contents of the ZIP file
    with zipfile.ZipFile(os.path.join(extraction_path, 'downloaded.zip'), 'r') as archive:
        archive.extractall(extraction_path)

    # Clean up: remove the downloaded ZIP file
    os.remove(os.path.join(extraction_path, 'downloaded.zip'))


# Specify the URL for the ZIP file
zip_url = 'https://files.grouplens.org/datasets/movielens/ml-latest-small.zip'

# Call the function to download and extract the data
get_data(zip_url)
