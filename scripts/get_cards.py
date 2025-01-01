import os
import shutil
import zipfile

import requests


def get_cards():
    # Create data directory
    os.makedirs('./data', exist_ok=True)
    
    # Download zip file
    url = 'https://www.kaggle.com/api/v1/datasets/download/lsind18/tarot-json'
    zip_file = './tarot-json.zip'
    
    response = requests.get(url)
    with open(zip_file, 'wb') as f:
        f.write(response.content)
    
    # Extract contents
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('./data')
    
    # Remove zip file
    os.remove(zip_file)

if __name__ == '__main__':
    get_cards()
