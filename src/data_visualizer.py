import matplotlib.pyplot as plt
import csv
import pandas as pd
import glob
import os
import signal
import SpeechAnalysis
import time 
from collections import defaultdict
import numpy as np

import requests



# Colors for console output
def make_text_blue(text) -> str:
    return f"\033[94m{text}\033[0m"
def make_text_red(text) -> str:
    return f"\033[91m{text}\033[0m"
def make_text_green(text) -> str:
    return f"\033[92m{text}\033[0m"
def make_text_pink(text) -> str:
    return f"\033[95m{text}\033[0m"
def make_text_yellow(text) -> str:
    return f"\033[93m{text}\033[0m"


# Helpers
def read_csv(csv_file) -> tuple:
    try:
        country_edit_dict = {}
        # Reading from the csv and creating a dictionary with their values
        with open(csv_file,'r') as csvFile:
            print("File Opened: ",csv_file)
            reader = csv.reader(csvFile,delimiter=",")
            edits = list(reader) # creating a list of edits from the reader iterables
            
            total_edit_count = len(edits)
            start_date = 0
            end_date = 1

            # Grabbing the country from edit to set as the key in a country:IP dict.
            for edit in edits: 
                country = edit[1]
                if country in country_edit_dict:
                    country_edit_dict[country] = country_edit_dict[country] + 1
                else:
                    country_edit_dict[country] = 1
          
        return (country_edit_dict, total_edit_count,start_date,end_date)    
    except:
        print("\n\tERROR READING FROM CSV FILE: '",csv_file,"'\n\n")
        exit()
        return None

def get_language_and_collection(file_name) -> tuple[str, str]:
    parts = file_name.split('-')
    language = parts[0]
    collection_type = parts[1].split('.')[0].replace('data_','')
    return language, collection_type

def prepare_plot_data(language,collection_type) -> tuple[tuple,str,str]:
    print(f"User Selected {language}-data_{collection_type}.csv")

    if language != "NA":
        csv_data = read_csv(f'../data/{language}-data_{collection_type}.csv')
    else:
        csv_data = read_csv(f'../data/aggregate_csv_data/{collection_type}_data_total.csv')
    return (csv_data,language,collection_type)

def get_user_input(options_map) -> tuple[int, str, dict]:
    user_input = input("\n Select Option: ")

    # Weeding out non-integer inputs
    try:
        selection = int(user_input)
    except:
        print("Invalid Input, Please enter a number from the options list.")
        time.sleep(2)
        return -1, "Invalid", options_map
    

    # For catching invalid, numeric inputs
    if selection not in options_map.keys():
        print("Invalid Entry",selection)
        time.sleep(2)
        return -1, "Invalid", options_map
    
    print(selection, options_map[selection])
    return selection, options_map[selection], options_map

def get_country_edit_counts(csv_path):
    counts = defaultdict(int)

    with open(csv_path, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # if there *is* a header; remove this if NO header at all

        for row in reader:
            # Country is always the second item in the row
            if len(row) > 1:
                country = row[1]
                counts[country] += 1

    return counts

def get_edit_count_of_all_countries():
    csv_paths = glob.glob("../data/*-data_streaming.csv")
    total_counts = defaultdict(int)

    for path in csv_paths:
        per_file_counts = get_country_edit_counts(path)

        for country, count in per_file_counts.items():
            total_counts[country] += count

    return dict(total_counts)

def get_country_populations() -> dict[str,int]:
   
    # Using this method just to get a list of countries
    countries = get_edit_count_of_all_countries()
    countries["United States of America"] = countries["United States"] # Have to mannually change United States -> United States of America
    country_pop_dict = {}
    """
    Russia [{'population': 146028325}]
    Belarus [{'population': 9109280}]
    """
    for country, edit in countries.items():
        data = requests.get(f"https://restcountries.com/v3.1/name/{country}?fullText=true&fields=population").json()
        try:
            population = data[0]["population"]
            country_pop_dict[country] = population
            print(country,country_pop_dict[country])
        except:
            print(country,data)


    # Adjusting population sizes by a factor of 1000, we want ot plot edit counts of each country per 1000 people in the population.
    for country, population in country_pop_dict.items():
        # Getting how many sets of 1000 people are in a population. 42,521 // 1000 = 42
        country_pop_dict[country] = population // 1000

    return country_pop_dict
    

# Function Options
def plot_data(data) -> None:
    # Unpacking Data
    csv_data = data[0]
    selected_lang = data[1]
    collection_type = data[2]

    language_dict = {"en":"English","es":"Spanish","hu":"Hungarian","ru":"Russian","NA":"Available"}

    country_ip_dict = csv_data[0]
    total_edit_count = csv_data[1]
    # start_date = csv_data[2]
    # end_date = csv_data[3]
    plt.figure(figsize=(10,6))  # making the figure wider to fit labels

    for key, value in country_ip_dict.items():
        bars = plt.bar(key, value)
        # Adding numbers above bars
        for bar in bars:
            height = bar.get_height()
            plt.text(
                bar.get_x() + bar.get_width()/2,   # x position (center of bar)
                height,                            # y position (top of bar)
                str(height),                       # text (the number)
                ha='center', va='bottom', fontsize=8
            )
    
    # Rotating x-tick labels diagonally to fit all countries
    plt.xticks(rotation=45, ha='right', fontsize=8)

    # Labels
    plt.ylabel("Edit Counts")
    plt.title(f"{collection_type.capitalize()} -- {language_dict[selected_lang]} Wikipedia, Country vs Edit Counts")

    # Adding caption at the bottom
    plt.figtext(0.5, 0.01, f"Figure 1:  Count of edits made to {language_dict[selected_lang]} Wikipedia by country, N={total_edit_count}.", ha="center", fontsize=9, style="italic")
    plt.tight_layout()  # fitting labels
    plt.show()

def combine_streaming_data() -> None:
    csv_files = glob.glob("../data/*-data_streaming.csv")
    dataframes = []

    for file in csv_files:
        if os.path.getsize(file) > 0:  # Skip empty files
            try:
                df = pd.read_csv(file, header=None)
                dataframes.append(df)
            except pd.errors.EmptyDataError:
                print(f"Skipping empty or invalid file: {file}")
        else:
            print(f"Skipping empty file: {file}")

    if not dataframes:
        print("No valid CSV files found to combine.")
        return

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv("../data/aggregate_csv_data/streaming_data_total.csv", index=False, header=False)
    print(f"Combined {len(dataframes)} valid files into 'streaming_data_total.csv'.")

def combine_batching_data() -> None:
    csv_files = glob.glob("../data/*-data_batching.csv")
    dataframes = []

    for file in csv_files:
        if os.path.getsize(file) > 0:  # Skipping empty files
            try:
                df = pd.read_csv(file, header=None)
                dataframes.append(df)
            except pd.errors.EmptyDataError:
                print(f"\tSkipping empty or invalid file: {file}")
        else:
            print(f"\tSkipping empty file: {file}")

    if not dataframes:
        print("No valid CSV files found to combine.")
        return

    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv("../data/aggregate_csv_data/batching_data_total.csv", index=False, header=False)
    print(f"\tCombined {len(dataframes)} valid files into 'batching_data_total.csv'.")

def rank_countries_by_speech_freedom(csv_data) -> None:
    SpeechAnalysis.rank_countries_by_speech_freedom(csv_data)

def plot_edits_and_speech(analysis):
    # {country : population}, population has been adjusted by a factor of 1,000
    population_dict = get_country_populations()

    # ranked_countries -> [(country, magnitude, angle), ...]
    ranked_countries = analysis.sort_countries_by_speech()

    # Convert magnitude list into dictionary for lookup
    ranked_dict = {country: magnitude for (country, magnitude, angle) in ranked_countries}

    # Get edit counts
    country_edits = get_edit_count_of_all_countries()
    country_edits["United States of America"] = country_edits["United States"] # Exception, have to mannually change United States to United States of America

    # Only plot countries that appear in BOTH datasets
    common_countries = [c for c in country_edits if c in ranked_dict]
    

    # Extract values aligned by country and adjust them by population size
    edits = []
    for country in common_countries:
        edit_count = country_edits[country]
        adjusted_edit_count = edit_count  # / population_dict[country] need more data before we do this
        edits.append(adjusted_edit_count)

    magnitudes = []
    for country in common_countries:
        magnitudes.append(ranked_dict[country])


    # Create x positions for countries
    x = np.arange(len(common_countries))
    width = 0.35   # bar width

    plt.figure(figsize=(14, 7))

    # Bars
    plt.bar(x - width/2, edits, width, label="Edits")
    plt.bar(x + width/2, magnitudes, width, label="Freedom Of Speech")

    # Labels & formatting
    plt.xticks(x, common_countries, rotation=90)
    plt.ylabel("Value")
    plt.title("Edits and Speech Magnitude per Country")
    plt.legend()
    plt.tight_layout()

    plt.show()


# Interface
def show_menu(csv_files) -> dict:
    os.system("clear")

    header = "=== Data Visualizer Menu ==="
    print(make_text_green(header))
    
    # Putting CSV options in a map
    CSVs_map = {}
    for option in csv_files: # Using enumerate to print/get index of options in incremental order
        CSVs_map[len(CSVs_map)+1] = option
       
    # Printing CSV options
    for index, csv in CSVs_map.items():
        print(make_text_yellow(f"{index}. {csv}"))

    # Printing additional functions
    additional_functions_map = {
        90:"View Speech Analysis Plot",
        91:"View Combined Streaming Data",
        92:"View Combined Batching Data",
        93:"Rank Countries by Fredom of Speech Scores",
        94:"Plot Edits and Speech",
        0: "Exit"
    }
    for index, function in additional_functions_map.items():
        if function == "Exit": # Red text for Exit option
            print(make_text_red(f"{index}. {function}"))
        else:
            print(make_text_pink(f"{index}. {function}"))
       
    # Joinning maps
    options_map = CSVs_map | additional_functions_map

    return options_map

def exit_interface() -> None:
    print("Closing Interface")
    os.kill(os.getpid(), signal.SIGINT)

def handle_individual_dataset(selection) -> None:
    selected_lang, collection_type = get_language_and_collection(selection)
    data = prepare_plot_data(selected_lang,collection_type)
    plot_data(data)

def handle_additional_function(selection,analysis) -> None:
    if selection == "View Speech Analysis Plot":
            analysis.make_plot()
            return
    elif selection == "View Combined Streaming Data":
        combine_batching_data()
        # Setting parameters
        selected_lang = "NA"
        collection_type = "streaming"
        print("User Selected streaming_data_total.csv")
        data = prepare_plot_data(selected_lang,collection_type)
        plot_data(data)
        return
    elif selection == "View Combined Batching Data":
        combine_streaming_data()
        selected_lang = "NA"
        collection_type = "batching"
        print("User Selected batching_data_total.csv")
        data = prepare_plot_data(selected_lang,collection_type)
        plot_data(data)
        return
    elif selection == "Rank Countries by Fredom of Speech Scores":
        # Console Output Loop
        while True:
            os.system("clear")
            analysis.rank_countries_by_speech_freedom()
            exit_signal = input(make_text_blue("\n\nEnter 0 to exit: "))
            if exit_signal == '0':
                break
        return
    
def run_interface(analysis,csv_files) -> None:

    language_dict = {"en":"English","es":"Spanish","hu":"Hungarian","ru":"Russian","NA":"Available"}
    os.system("clear")

    # Showing Menu 
    options = show_menu(csv_files)

    # Getting User Input
    index_selection, selection, options_map  = get_user_input(options)

    # ===== Handling User Selection =====
        # Create function handler/assigner
    # For Invalid Input
    if index_selection == -1:
        return
    
    # For Exiting Program, 0.) Exit
    if index_selection == 0:
        exit_interface()
        return
    
    if index_selection == 94:
        plot_edits_and_speech(analysis)
        return

    # Displaying Individual Datasets, 1 - 8
    valid_options_count = len(language_dict)**2-2 # 2 CSVs per language, minus 2 for NA option
    if index_selection < valid_options_count:
        handle_individual_dataset(selection)
        return
    
    # Additional Functions, 90.) - 93.)
    if selection in options_map.values():
        handle_additional_function(selection,analysis)


if __name__ == "__main__":
    try:

        os.system("clear")
        
        # Loading Speech Analysis
        print("Loading Data...")
        analysis = SpeechAnalysis.SpeechAnalysis('V-Dem-CY-Full+Others-v15.csv')

        # Loading CSV Files
        data_path = '../data/'
        data = os.listdir(data_path)
        csv_files = []
        for file in data:
            if file.endswith('.csv'):
                print(file)
                csv_files.append(file)
        csv_files.sort() # Putting corresponding batching and streaming files together.

        # -- Main Interface Loop --
        while True:
            run_interface(analysis,csv_files)

    except KeyboardInterrupt:
        print("Program Stopped")
            
