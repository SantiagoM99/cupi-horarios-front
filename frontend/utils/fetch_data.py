# data_fetcher.py
import requests
import json

# Leer datos locales
def load_local_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# Obtener datos del endpoint
def fetch_chosen_schedule(mock_data, url='http://localhost:8003/v1.0/official_schedule/'):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return mock_data
    

def fetch_assistants(url='http://localhost:8003/v1.0/assistant/'):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return []
    
def fetch_availability(assistant_code):
    response = requests.get(f"http://localhost:8003/v1.0/assistant-availability/assistant/{assistant_code}")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching availability: {response.status_code}")
        return []

def fetch_time_slots():
    response = requests.get("http://localhost:8003/v1.0/time-slot/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching time slots: {response.status_code}")
        return []
