#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz

KDWP_URL = "https://ksoutdoors.com/KDWP-Info/Kansas-Outdoor-Events"
TZ       = pytz.timezone("America/Chicago")

def fetch_events():
    resp = requests.get(KDWP_URL)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    cal  = Calendar()
    cal.add("prodid", "-//Fall River Lake Rentals//KDWP Feed//EN")
    cal.add("version", "2.0")

    # Each event link is an <a class="fc-daygrid-event">
    for a in soup.select("a.fc-daygrid-event"):
        title = a.select_one(".fc-event-title").get_text(strip=True)
        date_td = a.find_parent("td", attrs={"data-date": True})
        date_str = date_td["data-date"]  # "YYYY-MM-DD"
        start_dt = TZ.localize(datetime.fromisoformat(f"{date_str}T00:00:00"))
        evt = Event()
        evt.add("summary", title)
        evt.add("dtstart", start_dt)
        evt.add("dtend", start_dt + timedelta(days=1))
        cal.add_component(evt)

    with open("events.ics", "wb") as f:
        f.write(cal.to_ical())

if __name__ == "__main__":
    fetch_events()
