import requests
import re
from dotenv import load_dotenv
import os, sys

from .models.association import Association
from .models.company import Company
from .models.product import Product
from .models.sales_network import SalesNetwork

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


def get_products(date, expired=False):
    if not is_valid_date(date):
        raise ValueError("Date must be in yyyy-MM-dd format")

    client_id = os.getenv('STROMPRIS_CLIENT_ID')
    client_secret = os.getenv('STROMPRIS_CLIENT_SECRET')

    access_token = get_access_token(client_id, client_secret)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    expired_flag = 'true' if expired else 'false'

    print(f'{BASE_URL}/feed/{date}?expired={expired_flag}')  # Include expired flag in the URL
    response = requests.get(f'{BASE_URL}/feed/{date}?expired={expired_flag}', headers=headers)

    if response.status_code == 200:
        companies_data  = response.json()
        companies = []

        for company_data in companies_data:
            products = []

            for product_data in company_data.get('products', []):
                sales_networks = [SalesNetwork(**sales_network) for sales_network in product_data.get('salesNetworks', [])]
                associations = [Association(**association) for association in product_data.get('associations', [])]

                filtered_product_data = {k: v for k, v in product_data.items() if
                                        k not in ['salesNetworks', 'associations',
                                                  'linkedProduct']}
                product = Product(
                    **filtered_product_data,
                    salesNetworks=sales_networks,
                    associations=associations
                )
                products.append(product)

            company = Company(
                id=company_data['id'],
                name=company_data['name'],
                organizationNumber=company_data['organizationNumber'],
                pricelistUrl=company_data['pricelistUrl'],
                products=products
            )
            companies.append(company)

        return companies

    else:
        print(f"Error Details: {response.text}")
        raise Exception(f"Failed to fetch data: {response.status_code}")
