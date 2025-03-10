import os
import zipfile

import requests


def get_cards():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    print(f"Base directory: {base_dir}")
    print(f"Data directory: {data_dir}")

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

        # Extract and rename if necessary
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            # List all files in the ZIP
            files = zip_ref.namelist()
            json_files = [f for f in files if f.endswith(".json")]

            if json_files:
                # Extract all files
                zip_ref.extractall(data_dir)

                old_path = os.path.join(data_dir, json_files[0])
                new_path = os.path.join(data_dir, "tarot-images.json")

                if old_path != new_path:
                    if os.path.exists(old_path):
                        os.rename(old_path, new_path)

            else:
                raise Exception("No JSON file found in the ZIP archive")

        os.remove(zip_file)


    except Exception as e:
        print(f"Error downloading/extracting files: {e}")
        raise


if __name__ == "__main__":
    get_cards()
