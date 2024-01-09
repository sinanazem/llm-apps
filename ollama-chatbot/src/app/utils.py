import json
import requests


def call_llama(model, prompt, stream=False):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt":prompt,
        "stream":stream
    }
    json_data = json.dumps(data)
    response = requests.post(url, data=json_data, headers={"Content-Type":"application/json"})
    if response.status_code == 200:
        return response.json()
    else:
        return f"Error: Status code is: {response.status_code}"


    if __name__ == "__main__":
        call_llama('llama2', "hi")['response']