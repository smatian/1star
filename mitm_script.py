from mitmproxy import http
import json

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
