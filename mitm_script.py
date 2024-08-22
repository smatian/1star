from mitmproxy import http
import json

badge_data = [
    {
        "ImageFileName": "aab9dfbd119b45e089660bf16cb8569d.png",
        "Name": "OFF CAMPUS 1A",
        "Type": "Activity"
    }
]

def set_all_true(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, bool) and not v:
                data[k] = True
            elif isinstance(v, (dict, list)):
                data[k] = set_all_true(v)
    elif isinstance(data, list):
        for i in range(len(data)):
            if isinstance(data[i], bool) and not data[i]:
                data[i] = True
            elif isinstance(data[i], (dict, list)):
                data[i] = set_all_true(data[i])
    return data

def response(flow: http.HTTPFlow) -> None:
    # Define the URLs you want to intercept
    urls_to_intercept = [
        "https://oneroster.lvusd.org/oneroster/mobileapi/v1//student/20112478/classsummary",
        "https://api.5starstudents.com/person/identity",
        "https://api.5starstudents.com/configuration/5f9274c6e5f245bfbfe59c92345bcb5f"
    ]
    # Define the IP address to ignore
    ip_to_ignore = "3.107.45.216"
    
    # Check if the request comes from the specific IP
    if flow.client_conn.address[0] == ip_to_ignore:
        # Do not process further
        flow.kill()

    # Check if the request URL is in the list of URLs to intercept
    if flow.request.pretty_url not in urls_to_intercept:
        return  # If not, do nothing and exit the function

    # Process the response for the specific URLs
    if flow.request.pretty_url == "https://oneroster.lvusd.org/oneroster/mobileapi/v1//student/20112478/classsummary":
        data = json.loads(flow.response.text)
        if 'ClassSummary' in data[0]:
            for j in range(len(data[0]['ClassSummary'])):
                if 'CurrentMark' in data[0]['ClassSummary'][j]:
                    data[0]['ClassSummary'][j]['CurrentMark'] = "A+"
                if 'Percent' in data[0]['ClassSummary'][j]:
                    data[0]['ClassSummary'][j]['Percent'] = 100.0
        flow.response.text = json.dumps(data)
        
    elif "https://api.5starstudents.com/person/identity" in flow.request.pretty_url:
        data = json.loads(flow.response.content)
        data["Badges"] = badge_data
        flow.response.content = json.dumps(data).encode()
        
    elif "https://api.5starstudents.com/configuration/5f9274c6e5f245bfbfe59c92345bcb5f" in flow.request.pretty_url:
        data = json.loads(flow.response.content)
        data = set_all_true(data)
        flow.response.content = json.dumps(data).encode()
