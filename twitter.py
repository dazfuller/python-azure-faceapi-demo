import urllib.parse as up

import base64
import json
import requests

def getApiKey(key):
    with open('config.json', 'r') as f:
        settings = json.load(f)
    return settings[key]

consumer_key = getApiKey("consumerKey")
consumer_secret = getApiKey("consumerSecret")

encoded_key = up.quote_plus(consumer_key)
encoded_secret = up.quote_plus(consumer_secret)

bearer_token_credential = "{}:{}".format(encoded_key, encoded_secret)
b64_bearer_token_credential = base64.b64encode(bytes(bearer_token_credential, 'utf-8')).decode('utf-8')

headers = {
    "Authorization": "Basic {}".format(b64_bearer_token_credential),
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

content = "grant_type=client_credentials"

res = requests.post("https://api.twitter.com/oauth2/token", data=content, headers=headers)
twitter_token = res.json()

headers = {
    "Authorization": "Bearer {}".format(twitter_token["access_token"])
}

res = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=twitterapi&count=2&trim_user=1", headers=headers)
with open('tweets.json', 'w') as f:
    json.dump(res.json(), f, indent=4)
