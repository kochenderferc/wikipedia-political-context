import requests
import geoip2.database
import csv

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
user_ip = {}

for change in data["query"]["recentchanges"]:
    if change["user"][0].isdigit():
        try:
            ip = change["user"]
            response = reader.country(ip)
            user_ip[change['user']] = response.country.name
            print(change['user'],"->",response.country.name)
        except:
            print("Not Real")


with open("user_ip_data.csv",'w',newline="") as csvFile:
    writer = csv.writer(csvFile)
    for key, value in user_ip.items():
        writer.writerow([key,value])

csvFile.close()
    

reader.close()



