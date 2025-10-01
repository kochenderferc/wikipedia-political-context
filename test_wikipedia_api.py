import requests
import geoip2.database


url = "https://en.wikipedia.org/w/api.php"
params = {
    "action": "query",
    "list": "recentchanges",
    "rcprop": "title|user|timestamp|comment|flags",
    "rclimit": 5,
    "format": "json"
}

headers = {"User-Agent": "WikipediaEditTracker/1.0 dboswell@chapman.edu"}

response = requests.get(url, params=params, headers=headers)
data = response.json()

for change in data["query"]["recentchanges"]:
    print(change)
