import requests


QUOTES_API_URL = "https://www.zohoapis.ca/crm/v2/Transport_Offers"


def create_quotes(data,token):
    headers = {
        "Authorization": f"Zoho-oauthtoken {token}",
        "Content-Type": "application/json",
    }

    data = {
        "data":[
            data]
    }

    response = requests.post(QUOTES_API_URL, headers=headers, json=data)
    print(response.status_code)
    if response.status_code == 200:
        return response
    
    return response
