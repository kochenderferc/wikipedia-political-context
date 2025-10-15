import requests
import geoip2.database
import ipaddress
import csv

url = "https://en.wikipedia.org/w/api.php"

# Header to simulate user access
headers = {"User-Agent": "WikipediaEditTracker/1.0 dboswell@chapman.edu"}

# Param to navigate to, and access, 250 user IPs
params = {
    "action": "query",
    "list": "recentchanges",
    "rcprop": "user",
    "rclimit": 250,
    "format": "json"
}

# Making request and storing data as json
response = requests.get(url, params=params, headers=headers)
data = response.json()

# Loading the database
reader = geoip2.database.Reader("GeoLite2-Country.mmdb")

# Dictionary to hold IP and Country
ip_country = {}

# Iterating through all recent edits and finding unregistered accounts
for change in data["query"]["recentchanges"]:
    try:
        ip = change["user"] # Getting IP
        response = reader.country(ip) # Getting country from geoip2 database
        ip_country[change['user']] = response.country.name # Storing IP and Country in dictionary
        print(change['user'],"->",response.country.name)
    except:
        print("Registered Account") # In case we encounter an invalid IP/Username

# Writing values to csv
with open("CSVs/data_batching.csv",'w',newline="") as csvFile:
    writer = csv.writer(csvFile)
    for key, value in ip_country.items():
        writer.writerow([key,value])

csvFile.close()
reader.close()



