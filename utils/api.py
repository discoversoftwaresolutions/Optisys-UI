import requests

BASE_URL = "https://optisys-agent-production.up.railway.app"

def fetch_products():
    res = requests.get(f"{BASE_URL}/api/products/")
    res.raise_for_status()
    return res.json()
