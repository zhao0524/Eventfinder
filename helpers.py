import requests

def get_events(city, keyword=None):
    API_KEY = "o6Ic6NqS51mUeXl3H2wKVyZYSSyzJmT4"
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "city": city,
        "keyword": keyword,  # optional
        "size": 10,          # number of events to return
        "sort": "date,asc"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["_embedded"]["events"] if "_embedded" in data else []
    else:
        print("Error:", response.status_code)
        return []
    