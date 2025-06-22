import requests

API_URL = "https://optisys-agent-production.up.railway.app"

def trigger_full_integration(stack_description):
    res = requests.post(f"{API_URL}/api/trigger/full", json={"stack_description": stack_description})
    res.raise_for_status()
    return res.json().get("result", {})
