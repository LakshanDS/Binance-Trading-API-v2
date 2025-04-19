import requests
import json

# Replace YOUR_WEBHOOK_URL_HERE with your actual webhook URL - Enter your webhook URL here
webhook_url = "https://n8nlak.duckdns.org/webhook/89614ede-feda-4ec0-aa18-dd9f7632f2cd"

def send_webhook(payload):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(webhook_url, data=json.dumps(payload), headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(f"TG Updated!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook message: {e}")