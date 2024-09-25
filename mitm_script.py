from mitmproxy import http
import json
import requests

badge_data = [
    {
        "ImageFileName": "aab9dfbd119b45e089660bf16cb8569d.png",
        "Name": "OFF CAMPUS 1A",
        "Type": "Activity",
    },
    {
        "Type": "Activity",
        "Name": "ASB CARD",
        "ImageFileName": "cc3f97dd82b04109a9cd608334508bb3.png",
    },
]

def response(flow: http.HTTPFlow) -> None:
    # Define the URLs you want to intercept
    
    if "https://api.5starstudents.com/person/identity" in flow.request.pretty_url:
        data = json.loads(flow.response.content)
        print(data)

        # Load the allowed numbers from the GitHub URL
        url = "https://raw.githubusercontent.com/smatian/1star/main/allowed.txt"
        response = requests.get(url)
        if response.status_code == 200:
            allowed_numbers = response.text.splitlines()
        else:
            allowed_numbers = []

        # Check if the number is in the allowed list
        if data["Number"] in allowed_numbers:
            data["Badges"] = badge_data
        else:
            data["Badges"] = []

        flow.response.content = json.dumps(data).encode()
