"""Constants"""
DOMAIN = "wienerlinien"

BASE_URL = "http://www.wienerlinien.at/ogd_realtime/monitor?stopid={}"

DEPARTURES = {
    "first": {"key": 0, "name": "({}) {} first departure"},
    "next": {"key": 1, "name": "({}) {} next departure"},
}

ICONS_URL = f"/{DOMAIN}/icons"
ICONS_PATH = f"custom_components/{DOMAIN}/icons"

METRO_LINES = ["U1", "U2", "U3", "U4", "U6"]
