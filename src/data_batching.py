import requests
import geoip2.database
import csv
import sys
import time
from datetime import datetime

def make_text_red(text) -> str:
    return f"\033[91m{text}\033[0m"

def make_text_green(text) -> str:
    return f"\033[92m{text}\033[0m"

def collect_data_from_json(json_data) -> tuple:

    # Opening database
    reader = geoip2.database.Reader("../GeoLite2-Country.mmdb") # Loading the database

    ip_country_tuple_list = [] # Dictionary to hold IP and Country
    request_number = 0
    unregistered_count = 0
    registered_count = 0
    past_ip = "2804:7F3:404:9426:14FD:82D8:898D:CABE"

    try:
        # Iterating through all recent edits, finding unregistered accounts, and collecting response data
        for change in json_data["query"]["recentchanges"]:
            request_number += 1
            ip = change["user"] # Getting IP
            if past_ip != ip:
                try:
                    
                    response = reader.country(ip) # Getting country from geoip2 database
                    country = response.country.name # Storing IP and Country in dictionary

                    print(ip, country) # Printing country name via its ip pairing
                    ip_country_tuple_list.append((ip,country)) # Adding to tuple_list

                    time.sleep(0.5)
                    print(make_text_green(f"Unregistered Account - {ip} -> {country} #{unregistered_count+1}"))
                    unregistered_count += 1

                    # Tracking ip to make sure its not a duplicate edit from one ip.
                    past_ip = ip
                except:
                    print(make_text_red(f"Registered Account - {request_number}")) # In case we encounter an invalid IP/Username
                    registered_count += 1
    except Exception as e:
        print("Error Collecting Data from JSON:",lang_select,"\n",e)

    # Closing database
    reader.close()
    
    return (ip_country_tuple_list,request_number,unregistered_count,registered_count)

def print_edit_distribution(unregistered_count,registered_count,request_number) -> None:
    print(make_text_red(f"\tResgistered Accounts: {registered_count}"))
    print(make_text_green(f"\tUnregistered Accounts: {unregistered_count}"))
    print(f"\tTotal Requests Made: {request_number}")    

def write_to_csv(lang_select,ip_country_tuples) -> None:
    # Printing out how many unregistered accounts there are in the dictionary
    print(len(ip_country_tuples)) 
    
    row_number = 1
    with open(f"../data/{lang_select}-data_batching.csv",'w',newline="") as csvFile:
        writer = csv.writer(csvFile)
        for pair in ip_country_tuples:
            ip = pair[0]
            country = pair[1]
            writer.writerow([ip,country])
            print("Writing",country,ip,row_number)
            row_number += 1
    csvFile.close()

def run_batching(url,parameters,headers,language) -> None:
    # Making request and storing data as json
    response = requests.get(url, params=parameters, headers=headers) 
    data = response.json()
    
    # Collecting data from json
    ip_country,request_number,unregistered_count,registered_count = collect_data_from_json(data)

    # Printing out data distribution
    print_edit_distribution(unregistered_count=unregistered_count,registered_count=registered_count,request_number=request_number)
    
    # Making CSV
    write_to_csv(language,ip_country)

if __name__ == "__main__":
    if len(sys.argv) == 2: 
        print("Language Selected",sys.argv[1])

        lang_select = sys.argv[1] # language specification
        url = f"https://{lang_select}.wikipedia.org/w/api.php" # Constructing url
        # Header to simulate user access
        headers = {"User-Agent": "WikipediaEditTracker/1.0 dboswell@chapman.edu"}
        # Param to navigate to, and access, 250 user IPs
        parameters = {
            "action": "query",
            "list": "recentchanges",
            "rcprop": "timestamp|user",
            "rclimit": 500,
            "format": "json"
        }
        
        run_batching(url,parameters,headers,lang_select)
    else:
        print("Incorrect Arguments Provided\n Arguments Expected <program-name> <language-specification>\n Arguments given:")
        # Printing out the received arguments
        for i in range(len(sys.argv)):
            print("\t",i,sys.argv[i])

