import matplotlib.pyplot as plt
import csv
import pandas as pd
import glob
import os
import signal

def read_csv(csv_file):
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


def print_country_edit_counts(csv_data):
    country_edit_count_dict = csv_data[0]
    for key, value in country_edit_count_dict.items():
        print(key,":",value)


def plot_data(csv_data):
    language_dict = {"en":"English","es":"Spanish","fr":"French","de":"German","ja":"Japanese","pt":"Portuguese","ru":"Russian","NA":"NA"}

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


def get_csv_dates(csv_data):
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




def combine_streaming_csvs():
    csv_files = glob.glob("../CSVs/*-data_streaming.csv")
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
    combined_df.to_csv("streaming_data_total.csv", index=False, header=False)
    print(f"Combined {len(dataframes)} valid files into 'streaming_data_total.csv'.")





def combine_batching_csvs():
    csv_files = glob.glob("../CSVs/*-data_batching.csv")
    dataframes = []

    for file in csv_files:
        if os.path.getsize(file) > 0:  # Skip empty files
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
    combined_df.to_csv("batching_data_total.csv", index=False, header=False)
    print(f"\tCombined {len(dataframes)} valid files into 'batching_data_total.csv'.")



def show_menu():
    os.system("clear")
    options = [
        "en-data_batching.csv",
        "en-data_streaming.csv",
        "fr-data_batching.csv",
        "fr-data_streaming.csv",
        "de-data_batching.csv",
        "de-data_streaming.csv",
        "es-data_batching.csv",
        "es-data_streaming.csv",
        "ja-data_batching.csv",
        "ja-data_streaming.csv",
        "pt-data_batching.csv",
        "pt-data_streaming.csv",
        "ru-data_batching.csv",
        "ru-data_streaming.csv",
        "Combine Streaming CSVs",
        "Combine Batching CSVs",
        "View streaming_data_total.csv",
        "View batching_data_total.csv",
        "Exit"
    ]
    print("\n=== DATA MENU ===")
    for i, option in enumerate(options):
        if option == "Exit":
            print(f"{0}. {option}")
        elif option == "Combine Streaming CSVs":
            print(f"{90}. {option}")
        elif option == "Combine Batching CSVs":
            print(f"{91}. {option}")
        elif option == "View streaming_data_total.csv":
            print(f"{92}. {option}")
        elif option == "View batching_data_total.csv":
            print(f"{93}. {option}")
        elif option == "Exit":
            print(f"{0}. {option}")
        else:
            print(f"\t{i+1}. {option}")
    return input("\nSelect an option: ")




if __name__ == "__main__":

    try:
        while True:
            menu_selection = show_menu()
            selected_csv = int(menu_selection)
            selected_lang = "ALL"
            if selected_csv == 1:
                selected_lang = "en"
                collection_type = "batching"
                print("User Selected en-data_batching.csv")
                csv_data = read_csv('../CSVs/en-data_batching.csv')
                plot_data(csv_data)
            elif selected_csv == 2:
                selected_lang = "en"
                collection_type = "streaming"
                print("User Selected en-data_streaming.csv")
                csv_data = read_csv('../CSVs/en-data_streaming.csv')
                plot_data(csv_data)
            elif selected_csv == 3:
                selected_lang = "fr"
                collection_type = "batching"
                print("User Selected fr-data_batching.csv")
                csv_data = read_csv('../CSVs/fr-data_batching.csv')
                plot_data(csv_data)
            elif selected_csv == 4:
                selected_lang = "fr"
                collection_type = "streaming"
                print("User Selected fr-data_streaming.csv")
                csv_data = read_csv('../CSVs/fr-data_streaming.csv')
                plot_data(csv_data)
            elif selected_csv == 5:
                selected_lang = "de"
                collection_type = "batching"
                print("User Selected de-data_batching.csv")
                csv_data = read_csv('../CSVs/de-data_batching.csv')
                plot_data(csv_data)
            elif selected_csv == 6:
                selected_lang = "de"
                collection_type = "streaming"
                print("User Selected de-data_streaming.csv")
                csv_data = read_csv('../CSVs/de-data_streaming.csv')
                plot_data(csv_data)
            elif selected_csv == 7:
                selected_lang = "es"
                collection_type = "batching"
                print("User Selected es-data_batching.csv")
                csv_data = read_csv('../CSVs/es-data_batching.csv')
                plot_data(csv_data)
            elif selected_csv == 8:
                selected_lang = "es"
                collection_type = "streaming"
                print("User Selected es-data_streaming.csv")
                csv_data = read_csv('../CSVs/es-data_streaming.csv')
                plot_data(csv_data)
            elif selected_csv == 9:
                selected_lang = "ja"
                collection_type = "batching"
                print("User Selected ja-data_batching.csv")
                csv_data = read_csv('../CSVs/ja-data_batching.csv')
                plot_data(csv_data)
            elif selected_csv == 10:
                selected_lang = "ja"
                collection_type = "streaming"
                print("User Selected ja-data_streaming.csv")
                csv_data = read_csv('../CSVs/ja-data_streaming.csv')
                plot_data(csv_data)
            elif selected_csv == 11:
                selected_lang = "pt"
                collection_type = "batching"
                print("User Selected pt-data_batching.csv")
                csv_data = read_csv('../CSVs/pt-data_batching.csv')
                plot_data(csv_data)
            elif selected_csv == 12:
                selected_lang = "pt"
                collection_type = "streaming"
                print("User Selected pt-data_streaming.csv")
                csv_data = read_csv('../CSVs/pt-data_streaming.csv')
                plot_data(csv_data)
            elif selected_csv == 13:
                selected_lang = "ru"
                collection_type = "batching"
                print("User Selected ru-data_batching.csv")
                csv_data = read_csv('../CSVs/ru-data_batching.csv')
                plot_data(csv_data)
            elif selected_csv == 14:
                selected_lang = "ru"
                collection_type = "streaming"
                print("User Selected ru-data_streaming.csv")
                csv_data = read_csv('../CSVs/ru-data_streaming.csv')
                plot_data(csv_data)
        


            elif selected_csv == 90:
                print("Combining streaming data...")
                combine_streaming_csvs()
            elif selected_csv == 91:
                print("Combining batching data...")
                combine_batching_csvs()
            elif selected_csv == 92:
                selected_lang = "NA"
                collection_type = "streaming"
                print("User Selected streaming_data_total.csv")
                csv_data = read_csv('streaming_data_total.csv')
                plot_data(csv_data)
            elif selected_csv == 93:
                selected_lang = "NA"
                collection_type = "batching"
                print("User Selected batching_data_total.csv")
                csv_data = read_csv('batching_data_total.csv')
                plot_data(csv_data)
            elif selected_csv == 0:
                print("Closing Interface")
                os.kill(os.getpid(), signal.SIGINT)
            else:
                continue
    except KeyboardInterrupt:
        print("Program Stopped")
            

