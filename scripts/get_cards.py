import os
import zipfile

import requests


def get_cards():
    # Use Hugging Face Spaces path
    data_dir = "/home/user/app/data"
    os.makedirs(data_dir, exist_ok=True)

    # Correct Kaggle API URL
    url = "https://www.kaggle.com/api/v1/datasets/download/lsind18/tarot-json"
    zip_file = os.path.join(data_dir, "tarot-json.zip")

    try:
        # Download with curl-like headers
        response = requests.get(
            url,
            allow_redirects=True,
            headers={"User-Agent": "curl/7.64.1", "Accept": "*/*"},
        )
        response.raise_for_status()

        with open(zip_file, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(data_dir)

        os.remove(zip_file)
        print("Files downloaded and extracted successfully!")

    except Exception as e:
        print(f"Error downloading/extracting files: {e}")
        raise


if __name__ == "__main__":
    get_cards()
