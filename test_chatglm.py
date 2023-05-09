import requests
import json
from evaluation.utils import SSEClient

prompt = "你现在在正常工作吗？"
seed = 2333
url = "http://10.50.212.248:8001/completion/stream"

payload = json.dumps({
    "prompt": prompt,
    "seed": seed,
    "history": []
})
headers = {
    'Authorization': '85577713-4c52-48bd-bf65-57112ce337d2',
    'Content-Type': 'application/json; charset=utf-8'
}
response = requests.request("POST", url, headers=headers, data=payload)
client = SSEClient(response)
for event in client.events():
    if event.event == "add":
        continue
    elif event.event == "finish":
        print(event.data)