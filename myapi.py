import requests

class HuggingFaceNLP:
    def __init__(self, api_token):
        self.api_token = api_token
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def query(self, model, text):
        api_url = f"https://api-inference.huggingface.co/models/{model}"
        payload = {"inputs": text}

        try:
            response = requests.post(api_url, headers=self.headers, json=payload)

            # Check HTTP status code
            if response.status_code == 503:
                return [{"label": "MODEL_LOADING", "score": 0.0}]
            elif response.status_code != 200:
                return [{"label": f"HTTP_{response.status_code}", "score": 0.0}]

            # Try to parse JSON response
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"❌ Network error: {e}")
            return [{"label": "NETWORK_ERROR", "score": 0.0}]

        except requests.exceptions.JSONDecodeError:
            print("❌ JSON decode error")
            print("🔎 Raw response:", response.text)
            return [{"label": "INVALID_RESPONSE", "score": 0.0}]

    def sentiment_analysis(self, text):
        model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
        return self.query(model, text)

    def named_entity_recognition(self, text):
        model = "dbmdz/bert-large-cased-finetuned-conll03-english"
        return self.query(model, text)

    def emotion_detection(self, text):
        model = "j-hartmann/emotion-english-distilroberta-base"
        return self.query(model, text)

def query(self, model, text):
    api_url = f"https://api-inference.huggingface.co/models/{model}"
    payload = {"inputs": text}

    try:
        response = requests.post(api_url, headers=self.headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Raw Text Response: {response.text}")
        return response.json()
    except Exception as e:
        print("❌ Exception occurred:", str(e))
        return {"error": str(e)}

