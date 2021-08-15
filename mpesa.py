from requests.auth import HTTPBasicAuth
from datetime import datetime
import requests
import json
import base64

class MpesaCredentials:
    '''
        mpesa credentials

        get consumer_key, consumer_secret, pass_key, business_short_code from mpesa daraja
        by creating an app

        the passkey is given in your app credentials

        the api_url is used to give authorization token

        consumer_key (string)
        consumer_secret (string)
        token_api_url (string)
        business_short_code (integer)
        pass_key (string)
    '''
    consumer_key = ''
    consumer_secret = ''
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    business_short_code = 174379
    pay_time = datetime.now().strftime('%Y%m%d%H%M%S')
    pass_key = ''
    data = str(business_short_code) + str(pass_key) + pay_time
    passwd = base64.b64encode(data.encode())
    password = passwd.decode('utf8')

# get time limited access token
def get_token():
    consumer_key = MpesaCredentials.consumer_key
    consumer_secret = MpesaCredentials.consumer_secret
    api_url = MpesaCredentials.api_url
    token = requests.get(
        api_url,
        auth=HTTPBasicAuth(consumer_key, consumer_secret)
    )
    access_token = token.json()['access_token']
    return access_token

# perfom a lipa na mpesa online stk push
def lipa_na_mpesa():
    access_token = get_token()
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    headers = {
        "Authorization": "Bearer %s" % access_token,
    }
    # amount (integer)
    amount = 1
    # customer telephone in 254712345678 format (integer)
    telephone = 0
    payload = {
        "BusinessShortCode": MpesaCredentials.business_short_code,
        "Password": MpesaCredentials.password,
        "Timestamp": MpesaCredentials.pay_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": telephone,
        "PartyB": MpesaCredentials.business_short_code,
        "PhoneNumber": telephone,
        # CallBackUrl must be HTTPS
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "CompanyXLTD",
        "TransactionDesc": "Payment of Test"
    }
    response = requests.post(
        api_url,
        json=payload,
        headers=headers,
    )
    return response.text
