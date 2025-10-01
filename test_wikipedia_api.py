import requests
import geoip2.database


url = "https://en.wikipedia.org/w/api.php"
params = {
    "action": "query",
    "list": "recentchanges",
    "rcprop": "title|user|timestamp|comment|flags",
    "rclimit": 250,
    "format": "json"
}

headers = {"User-Agent": "WikipediaEditTracker/1.0 dboswell@chapman.edu"}

response = requests.get(url, params=params, headers=headers)
data = response.json()

# Load the database
reader = geoip2.database.Reader("GeoLite2-Country.mmdb")

for change in data["query"]["recentchanges"]:
    if change["user"][0].isdigit():
        ip = change["user"]
        response = reader.country(ip)
        print(ip, "→", response.country.name)  # Should print "United States"

reader.close()


