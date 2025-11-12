import matplotlib.pyplot as plt
import csv
import pandas as pd
import glob
import os
import signal
import SpeechAnalysis
import time # Remove this

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

def print_country_edit_counts(csv_data) -> None:
    country_edit_count_dict = csv_data[0]
    for key, value in country_edit_count_dict.items():
        print(key,":",value)

def rank_countries_by_speech_freedom(csv_data) -> None:
    SpeechAnalysis.rank_countries_by_speech_freedom(csv_data)

def plot_data(csv_data,selected_lang,collection_type) -> None:
    language_dict = {"en":"English","es":"Spanish","hu":"Hungarian","ru":"Russian","NA":"NA"}

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

def get_csv_dates(csv_data) -> list:
    try:
        dates = []
        with open(csv_data,'r') as csvFile:
                reader = csv.reader(csvFile,delimiter=',')
                
                for row in reader:
                    date = row[2].split()[0]
                    dates.append(date)
        csvFile.close()
        return dates
    except:
        print("\n\tERROR READING FROM CSV FILE: '",csv_data,"'\n\n")
        exit()
        return None

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

def show_menu(csv_files) -> tuple:
    os.system("clear")

    header = "=== Data Visualizer Menu ==="
    print(make_text_green(header))
    
    # Printing CSV file options
    csv_map = {}
    for i, option in enumerate(csv_files): # Using enumerate to print/get index of options in incremental order
        index = i+1
        csv_map [index] = option
        print(make_text_yellow(f"{index}. {csv_map[index]}"))
    
    # Printing Aggregate Data Options
    aggregates = ["View Speech Analysis Plot"]

    # Checking to see if aggregate files exist
    if os.path.exists("../data/aggregate_csv_data/streaming_data_total.csv"):
        aggregates.append("View streaming_data_total.csv")
    if os.path.exists("../data/aggregate_csv_data/batching_data_total.csv"):
        aggregates.append("View batching_data_total.csv")

    # Printing aggregate options
    aggregate_map = {}
    for j, aggregate in enumerate(aggregates):
        index = len(csv_files)+j+1
        aggregate_map[index] = aggregate
        print(make_text_blue(f"{index}. {aggregate_map[index]}"))

    # Printing additional functions
    additional_functions = [
        "Combine Streaming data",
        "Combine Batching data",
        "Rank Countries by Fredom of Speech Scores"
    ]
    additional_function_map = {}
    for i, function in enumerate(additional_functions):
        index = i+90
        additional_function_map[index] = function
        print(make_text_pink(f"{index}. {additional_function_map[index]}"))

    # Joinning all dictionaries
    options_map = csv_map | aggregate_map | additional_function_map | {0: "Exit"}
    print(make_text_red("\n0. Exit"))

    # Weeding out non-integer inputs
    try:
        selection = int(input("\nSelect an option: "))
    except:
        print("Invalid Input, Please enter a number corresponding to the options.")
        time.sleep(2)
        return -1, "Invalid", options_map
    

    # For catching invalid, numeric inputs
    if selection not in options_map.keys():
        print("Invalid Entry",selection)
        time.sleep(2)
        return -1, "Invalid", options_map
    
    print(selection, options_map[selection])
    return selection, options_map[selection], options_map

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

def display_data(language,collection_type) -> None:
    print(f"User Selected {language}-data_{collection_type}.csv")
    csv_data = read_csv(f'../data/{language}-data_{collection_type}.csv')
    plot_data(csv_data,language,collection_type)

def run_interface(analysis,csv_files) -> None:

    os.system("clear")

    # Showing Menu and Getting User Input
    index_selection, selection, options_map = show_menu(csv_files)
    selected_lang = "ALL"

    # For Invalid Input
    if index_selection == -1:
        return
    
    # For Exiting Program
    if index_selection < 1:
        print("Closing Interface")
        os.kill(os.getpid(), signal.SIGINT)
        return
    
    # Individual Datasets
    if index_selection < len(options_map) - 6: # Removing aggregate and additional function options
        selected_lang, collection_type = get_language_and_collection(selection)
        display_data(selected_lang,collection_type)
        return
    
    # Speech Plot
    if index_selection == 9: # Speech Analysis Plot
        analysis.make_plot() # Fix this
        return
    
    # Aggregate Datasets
    if selection in options_map.values():
        if selection == "View streaming_data_total.csv":
            selected_lang = "NA"
            collection_type = "streaming"
            print("User Selected streaming_data_total.csv")
            csv_data = read_csv('../data/aggregate_csv_data/streaming_data_total.csv')
            plot_data(csv_data,selected_lang,collection_type)
            return
        elif selection == "View batching_data_total.csv":
            selected_lang = "NA"
            collection_type = "batching"
            print("User Selected batching_data_total.csv")
            csv_data = read_csv('../data/aggregate_csv_data/batching_data_total.csv')
            plot_data(csv_data,selected_lang,collection_type)
            return

    # Combining Data Functions
    if index_selection == 90:
        print("Combining streaming data...")
        combine_streaming_data()
        return
    elif index_selection == 91:
        print("Combining batching data...")
        combine_batching_data()
        return
    elif index_selection == 92:
 
        os.system("clear")

        # Console Output Loop
        while True:
            os.system("clear")
            analysis.rank_countries_by_speech_freedom()
            exit_signal = input(make_text_blue("\n\nEnter 0 to exit: "))
            if exit_signal == '0':
                break
        return

def get_language_and_collection(file_name) -> tuple[str, str]:
    parts = file_name.split('-')
    language = parts[0]
    collection_type = parts[1].split('.')[0].replace('data_','')
    return language, collection_type

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
            
