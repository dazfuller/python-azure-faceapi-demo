import json
import requests
import uuid

TEXT_ANALYTICS_API = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/sentiment"

def getApiKey():
    with open('config.json', 'r') as f:
        settings = json.load(f)
    return settings['textAnalyticsKey']

def run():
    headers = {
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Key": getApiKey()
    }

    content = {
        "documents": [
            {
                "language": "en",
                "id": str(uuid.uuid4()),
                "text": "I'm going to mess you up"
            },
            {
                "language": "en",
                "id": str(uuid.uuid4()),
                "text": "You have a beautiful face and your poop smell of roses"
            }
        ]
    }

    res = requests.post(TEXT_ANALYTICS_API, data=json.dumps(content), headers=headers)
    resBody = res.json()
    print(json.dumps(resBody, indent=4))

if __name__ == "__main__":
    run()
