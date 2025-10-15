import requests
import geoip2.database
import csv
from datetime import datetime

def make_text_red(text):
    return f"\033[91m{text}\033[0m"

def make_text_green(text):
    return f"\033[92m{text}\033[0m"

def make_csv(url,parameters,headers):
    # Default dummy variable used to compare to new edits
    previous_timestamp = "2025-09-30T09:34:21Z"
    # Replace "Z" with "+00:00" so Python knows it's UTC
    previous_timestamp = datetime.fromisoformat(previous_timestamp.replace("Z", "+00:00"))
    while True:
        try:
            # Making request and storing data as json
            response = requests.get(url, params=parameters, headers=headers)
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
                    ip = data["query"]["recentchanges"][0]["user"] # Getting IP
                    # Getting country from geoip2 database based on IP
                    response = reader.country(ip)
                    country = response.country.name

                    # Adding IP, Country, and Timestamp to csv
                    with open("CSVs/data_streaming.csv",'a',newline="") as csvFile:
                        writer = csv.writer(csvFile)
                        writer.writerow([ip,country,current_timestamp])

                    # Green console output
                    print(make_text_green(f"Unregistered Account ------- {ip} : {country}\n"))
                
                except KeyboardInterrupt:
                    print("Program terminating..")
                    break
                except:
                    # Red console output
                    print(make_text_red(f"Registered Account ------- {ip}\n"))
        # For SIGINT/Ctrl + C
        except KeyboardInterrupt:
            print("Program Exited...")
            csvFile.close()
            reader.close()
            break
        except:
            print("Program Stalling")
        
if __name__ == "__main__":
    url = "https://en.wikipedia.org/w/api.php"

    # Header to simulate user access
    headers = {"User-Agent": "WikipediaEditTracker/1.0 dboswell@chapman.edu"}
    # Param to navigate to, and access, 250 user IPs
    parameters = {
        "action": "query",
        "list": "recentchanges",
        "rcprop": "timestamp|user",
        "rclimit": 1,
        "format": "json"
    }

    make_csv(url,parameters,headers)

