import matplotlib.pyplot as plt
import csv

country_edit_counts = {}
country_edit_counts_size = 0
total_edit_count = 0

# Reading from the csv and creating a dictionary with their values
with open('user_ip_data_continuous.csv','r') as csvFile:
    reader = csv.reader(csvFile,delimiter=",")
    for edit in reader:
        total_edit_count += 1
        country = edit[1]
        if country in country_edit_counts:
            country_edit_counts[country] = country_edit_counts[country] + 1
            country_edit_counts_size += 1
        else:
            country_edit_counts[country] = 1
    

for key, value in country_edit_counts.items():
    print(key,":",value)



plt.figure(figsize=(10,6))  # making the figure wider to fit labels
bars = plt.bar(country_edit_counts.keys(), country_edit_counts.values())

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
plt.title("Edit Counts by Country")


# Adding caption at the bottom
plt.figtext(0.5, 0.01, f"Figure 1:  Count of edits made to english Wikipedia from dataset of edits made by registered accounts, N={total_edit_count}", ha="center", fontsize=9, style="italic")

plt.tight_layout()  # fitting labels

plt.show()