import matplotlib.pyplot as plt
import csv
import sys

def read_csv(csv_file):
    try:
        country_edit_dict = {}
        # Reading from the csv and creating a dictionary with their values
        with open(csv_file,'r') as csvFile:
            reader = csv.reader(csvFile,delimiter=",")
            edits = list(reader) # creating a list of edits from the reader iterables
            total_edit_count = len(edits)
            start_date = edits[0][2].split()[0]
            end_date = edits[total_edit_count-1][2].split()[0]

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
    country_ip_dict = csv_data[0]
    total_edit_count = csv_data[1]
    start_date = csv_data[2]
    end_date = csv_data[3]
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
    plt.title("Country vs Edit Counts")
    # Adding caption at the bottom
    plt.figtext(0.5, 0.01, f"Figure 1:  Count of edits made to english Wikipedia by country from {start_date} to {end_date},N={total_edit_count}.", ha="center", fontsize=9, style="italic")
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


if __name__ == "__main__":
    if len(sys.argv) < 2: # If there is no csv file provided as a command line argument
        csv_data = read_csv('CSVs/data_streaming.csv')
        print_country_edit_counts(csv_data)
        plot_data(csv_data)
    elif len(sys.argv) == 2:
        csv_data = read_csv(sys.argv[1])
        print(csv_data)
        print_country_edit_counts(csv_data)
        plot_data(csv_data)
    else:
        print("Incorrect Arguments Provided:",end="")
        for i in range(len(sys.argv)):
            print(sys.argv[i] + " ")
        print()
    

