import requests

def get_rules() -> dict[str, str]:
    response = requests.get("http://service-a:8000/api/rules")
    return response.json()

        