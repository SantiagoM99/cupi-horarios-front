# data_fetcher.py
import requests
import json

# Leer datos locales
def load_local_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Obtener datos del endpoint
def fetch_chosen_schedule(mock_data, url='http://localhost:8003/v1.0/fixed_schedule/'):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return mock_data
