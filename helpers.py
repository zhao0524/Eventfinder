import requests
from datetime import datetime, timedelta, timezone

def get_events(city):
    API_KEY = "o6Ic6NqS51mUeXl3H2wKVyZYSSyzJmT4"
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    # Get the current time in UTC
    now = datetime.now(timezone.utc)

    # Get the time 3 days from now in UTC
    three_days_later = now + timedelta(days=3)

    start_time = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_time = three_days_later.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Set up the API parameters
    params = {
        "apikey": API_KEY,
        "city": city,
        "startDateTime": start_time,
        "endDateTime": end_time,
        "size": 10,
        "sort": "date,asc" 
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if "_embedded" in data:
            return data["_embedded"]["events"]
        else:
            return []
    else:
        print("Error:", response.status_code)
        return []
