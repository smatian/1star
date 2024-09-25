from mitmproxy import http
import json

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
        print(data["Number"])
        
        # check if data["number"] is in a line on allowed.txt
        with open("allowed.txt", "r") as f:
            allowed_numbers = f.read().splitlines()
            if data["Number"] in allowed_numbers:
                 data["Badges"] = badge_data
                 flow.response.content = json.dumps(data).encode()
            
            else :
                data["Badges"] = []
        
       
