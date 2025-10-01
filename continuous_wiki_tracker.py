import requests
import geoip2.database
import csv
from datetime import datetime

url = "https://en.wikipedia.org/w/api.php"


# Dummy variable used to compare to new edits
previous_timestamp = "2025-09-30T09:34:21Z"
# Replace "Z" with "+00:00" so Python knows it's UTC
previous_timestamp = datetime.fromisoformat(previous_timestamp.replace("Z", "+00:00"))


# Header to simulate user access
headers = {"User-Agent": "WikipediaEditTracker/1.0 dboswell@chapman.edu"}
# Param to navigate to, and access, 250 user IPs
params = {
    "action": "query",
    "list": "recentchanges",
    "rcprop": "timestamp|user",
    "rclimit": 1,
    "format": "json"
}


while True:
    try:
        # Making request and storing data as json
        response = requests.get(url, params=params, headers=headers)
        data = response.json()

        # Loading the database
        reader = geoip2.database.Reader("GeoLite2-Country.mmdb")

        # Converting timestamp of recent edit into comparable value
        current_timestamp = data["query"]["recentchanges"][0]["timestamp"]
        current_timestamp = datetime.fromisoformat(current_timestamp.replace("Z", "+00:00"))

        # Checks to see if the current edit is new via its timestamp
        if current_timestamp > previous_timestamp:
            print("New Entry Found -",current_timestamp,end=" - ")
            # Update timestamp marker
            previous_timestamp = current_timestamp
            try:
                ip = ip = data["query"]["recentchanges"][0]["user"] # Getting IP
                response = reader.country(ip) # Getting country from geoip2 database
                country = response.country.name
                # Writing to csv
                with open("user_ip_data.csv",'a',newline="") as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow([ip,country,current_timestamp])
                print(f"Valid IP ------- {ip} : {country}\n")
            except:
                print(f"Invalid IP --- {ip}\n")
    except KeyboardInterrupt:
        print("Program Exited...")
        break


csvFile.close()
reader.close()



