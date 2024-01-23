# This file was kindly provided by the mighty ChatGPT

import requests
import urllib.request
import json

def download_oracle_cards_json(api_url, save_path):
    # Send a GET request to the Scryfall API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Get the download URI for Oracle Cards
        oracle_cards_uri = next((item['download_uri'] for item in data['data'] if item['name'] == 'Oracle Cards'), None)

        if oracle_cards_uri:
            # Download the Oracle Cards JSON file
            urllib.request.urlretrieve(oracle_cards_uri, save_path)
            print(f"Downloaded Oracle Cards JSON file to {save_path}")
        else:
            print("Oracle Cards URI not found in the API response.")
    else:
        print(f"Error: Unable to fetch data from the API. Status code: {response.status_code}")


def main():
    api_url = "https://api.scryfall.com/bulk-data"
    save_path = "oracle-cards.json"

    download_oracle_cards_json(api_url, save_path)


if __name__ == '__main__':
    main()
