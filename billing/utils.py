import json

import requests

BASE_URL = 'https://api.paystack.co/'
SECRET_KEY = 'sk_test_7d8221741f69368ac4b0cdd95aa36d17aec9261d'


class PaystackAPI:
    def __init__(self, secret_key=None):
        """Instantiate PaystackAPI."""
        self.secret_key = secret_key

    def create_customer(self, **kwargs):
        endpoint = f'{BASE_URL}customer'
        customer_email = kwargs.get('email')
        payload = json.dumps({
            "email": customer_email
        })
        headers = {
            'Authorization': 'Bearer {SECRET_KEY}'.format(SECRET_KEY=self.secret_key),
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        print(response.text)
        return json.loads(response.content.decode('utf-8'))

    def get_customer(self, **kwargs):
        customer_id = kwargs.get('paystack_cus_id')
        endpoint = f'{BASE_URL}customer/{customer_id}'
        payload = json.dumps({})
        headers = {
            'Authorization': 'Bearer {SECRET_KEY}'.format(SECRET_KEY=self.secret_key),
            'Content-Type': 'application/json',
        }
        response = requests.request("GET", endpoint, headers=headers, data=payload)
        print(response.text)
        return json.loads(response.content.decode('utf-8'))

    def charge(self, **kwargs):
        endpoint = f'{BASE_URL}charge'
        customer_email = kwargs.get('email')
        payload = json.dumps({
            "email": customer_email,
            "amount": kwargs.get('amount'),
            "metadata": {
                "custom_fields": [
                    {
                        "value": kwargs.get('state'),
                        "display_name": f"Socialiga {customer_email}",
                        "variable_name": f"Socialiga {customer_email}"
                    }
                ]
            },
            "card": {
                "cvv": kwargs.get('cvv'),
                "number": kwargs.get('card_number'),
                "expiry_month": kwargs.get('expiry_month'),
                "expiry_year": kwargs.get('expiry_year')
            },
            "pin": kwargs.get('pin'),
        })
        headers = {
            'Authorization': 'Bearer {SECRET_KEY}'.format(SECRET_KEY=self.secret_key),
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", endpoint, headers=headers, data=payload)
        print(response.text)
        return json.loads(response.content.decode('utf-8'))

