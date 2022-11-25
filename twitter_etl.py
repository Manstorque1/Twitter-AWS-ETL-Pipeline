import requests
import json
import config
import pandas as pd

bearer_token = config.BEARER_TOKEN

def create_url():
    user_id = 939091
    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def get_params():
    return {"tweet.fields": "created_at"}


def bearer_oauth(r):
    #Method required by bearer token authentication.

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserTweetsPython"
    return r


def connect_to_endpoint(url, params):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)

    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def process_data():
    url = create_url()
    params = get_params()
    json_response = connect_to_endpoint(url, params)
    
    dct = {}

    for i in json_response['data']:
        dct[i['id']] = i['text']


    df = pd.DataFrame([dct])
    df.to_csv('processed_tweet.csv')
    

process_data()