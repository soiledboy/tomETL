import requests


def generate_new_token():
    url = 'https://api.tcgplayer.com/token'
    res = requests.post(url,
        data=dict(
            grant_type='client_credentials', 
            client_id='',
            client_secret=''))
    
    data = res.json()
    return data['access_token']