import requests


class Up_Data():
    def __init__(self):
        pass

    def get_authtoken(self):
        endpoint = "http://ee7e3592.ngrok.io/api/authenticate"
        data = {"password": "admin", "username": "admin"}
        headers = {"Content-Type": "application/json"}
        tokenid = requests.post(endpoint, json=data, headers=headers).json()
        return tokenid['id_token']

    def mine_post_data(self,token,receiveddata):
        endpoint = "http://ee7e3592.ngrok.io/api/mines"
        to = "Bearer " + token;
        headers = {"Authorization": to}
        data = requests.post(endpoint,json=receiveddata, headers=headers).json()
        return data

# token = get_authtoken()

# data = mine_get_data(token)
