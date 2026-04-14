import time
import random
import requests
import json
import hashlib
import hmac
import base64
from datetime import datetime

# ?? Replace these with your actual values
workspace_id = "YOUR_WORKSPACE_ID"
shared_key = "YOUR_PRIMARY_KEY"
log_type = "CustomAppLogs"

def build_signature(date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(
        hmac.new(decoded_key, bytes_to_hash, hashlib.sha256).digest()
    ).decode()
    return f"SharedKey {workspace_id}:{encoded_hash}"

def post_data(body):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    
    rfc1123date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(body)

    signature = build_signature(rfc1123date, content_length, method, content_type, resource)

    uri = f"https://{workspace_id}.ods.opinsights.azure.com{resource}?api-version=2016-04-01"

    headers = {
        "Content-Type": content_type,
        "Authorization": signature,
        "Log-Type": log_type,
        "x-ms-date": rfc1123date
    }

    response = requests.post(uri, data=body, headers=headers)
    print(f"Log sent with status: {response.status_code}")

# ?? Continuous log generation
while True:
    log_data = [{
        "TimeGenerated": str(datetime.now()),
        "Status": random.choice(["Success", "Error"]),
        "ResponseTime": random.randint(100, 1000)
    }]

    body = json.dumps(log_data)
    post_data(body)

    time.sleep(5)