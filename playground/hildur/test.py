import json
import requests

webhookurl = "https://discord.com/api/webhooks/1446479214629883997/Ct682I4szno9aF4mpskSHVoeCpXA37IfWddC1SVycmI-CYbHmbrFsmQNhAxEC2yCu1mT"
headers = {"User-Agent": "hildur", "Content-Type": "application/json"}
message = "test"
data = json.dumps({"content": message})
requests.post(webhookurl, headers=headers, data=data)
