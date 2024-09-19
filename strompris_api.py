import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = 'https://strom-api.forbrukerradet.no'

def is_valid_date(date_str):
    return bool(re.match(r'\d{4}-\d{2}-\d{2}', date_str))

def get_access_token(client_id, client_secret):
    if not client_id or not client_secret or not isinstance(client_id, str) or not isinstance(client_secret, str):
        raise ValueError("client_id and client_secret must be non-empty strings")

    payload = {
        "grantType": "client_credentials",
        "clientId": client_id,
        "clientSecret": client_secret
    }

    response = requests.post(f'{BASE_URL}/auth/token', json=payload)

    if response.status_code == 200:
        token_info = response.json()
        return token_info['accessToken']
    else:
        raise Exception(f"Failed to obtain token: {response.status_code} {response.text}")


def get_products(date):
    if not is_valid_date(date):
        raise ValueError("Date must be in yyyy-MM-dd format")

    client_id = os.getenv('CLIENT_ID')
    client_secret = os.getenv('CLIENT_SECRET')

    access_token = get_access_token(client_id, client_secret)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    response = requests.get(f'{BASE_URL}/feed/{date}', headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error Details: {response.text}")
        raise Exception(f"Failed to fetch data: {response.status_code}")
