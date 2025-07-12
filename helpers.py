import requests
from datetime import datetime, timedelta, timezone

def _pick_image(images):
    """
    Return one 'best' image URL (16 × 9 >= 640 px if possible,
    otherwise fall back to the first image).
    """
    if not images:
        return None
    for img in images:
        if img.get("ratio") == "16_9" and img.get("width", 0) >= 640:
            return img["url"]
    return images[0]["url"]   # fallback


def get_events(city):
    API_KEY = "o6Ic6NqS51mUeXl3H2wKVyZYSSyzJmT4"
    url = "https://app.ticketmaster.com/discovery/v2/events.json"

    # time window: now → three days ahead
    now   = datetime.now(timezone.utc)
    three = now + timedelta(days=3)

    params = {
        "apikey":        API_KEY,
        "city":          city,
        "startDateTime": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "endDateTime":   three.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "size":          10,
        "sort":          "date,asc"
    }

    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print("Ticketmaster error:", resp.status_code)
        return []

    data = resp.json()
    if "_embedded" not in data:
        return []

    events = []
    for e in data["_embedded"]["events"]:
        start = e["dates"]["start"]
        end   = e["dates"].get("end", {})          

        events.append({
            "id": e["id"],                           
            "name": e["name"],
            "date": start.get("localDate"),            
            "time": start.get("localTime"),            
            "description": e.get("info") or e.get("description") or "",
            "startDateTime": start.get("dateTime"),             
            "endDateTime": end.get("dateTime"),               
            "image": _pick_image(e.get("images", [])),
            "url" : e.get("url", "")
        })

    return events
