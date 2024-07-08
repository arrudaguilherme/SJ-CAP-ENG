# Classe de conexão com a API

from dotenv import load_dotenv
import os
import base64
import json
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes),"utf-8")

    url="https://accounts.spotify.com/api/token"

    headers = {
        "Authorization":"Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers,data=data)
    json_result = json.loads(result.content)

    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization":"Bearer " + token}

def search_artist(token,artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url,headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if (json_result) == 0:
        print("We didn't find the searched artist")
        return None
    
    return json_result[0]


token = get_token()
result = search_artist(token,"Ed Sheeran")
print(result["name"])