import requests

def get_rules() -> dict[str, str]:
    response = requests.get("http://service-c:8080/api/rules")
    return response.json()

        