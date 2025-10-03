import matplotlib.pyplot as plt
import csv

def read_csv(csv_file):
    try:
        country_edit_dict = {}
        total_edit_count = 0
        country_edit_dict_size = 0
        # Reading from the csv and creating a dictionary with their values
        with open(csv_file,'r') as csvFile:
            reader = csv.reader(csvFile,delimiter=",")
            for edit in reader:
                total_edit_count += 1
                country = edit[1]
                if country in country_edit_dict:
                    country_edit_dict[country] = country_edit_dict[country] + 1
                    country_edit_dict_size += 1
                else:
                    country_edit_dict[country] = 1
                    country_edit_dict_size += 1

        return (country_edit_dict, total_edit_count, country_edit_dict_size)    
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
    total_edit_count = csv_data[2]
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
    plt.figtext(0.5, 0.01, f"Figure 1:  Count of edits made to english Wikipedia from dataset of edits made by registered accounts, N={total_edit_count}", ha="center", fontsize=9, style="italic")
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
        print("\n\tERROR READING FROM CSV FILE: '",csv_file,"'\n\n")
        exit()
        return None


if __name__ == "__main__":
    csv_data = read_csv('user_ip_data_continuous.csv')
    print_country_edit_counts(csv_data)
    plot_data(csv_data)
