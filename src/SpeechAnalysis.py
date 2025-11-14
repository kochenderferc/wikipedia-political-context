
import pandas as pd
import matplotlib.pyplot as plt
import math


class SpeechAnalysis:
    def __init__ (self,csv_file_path) -> None:
        # -- Processing To Get Country Speech and Expression Data --

        # load csv
        csv = pd.read_csv(csv_file_path, low_memory=False)

        # Filter for year 2023
        year_df = csv[csv['year'] == 2023]

        # Filter for Freedom of Expression and Liberal Democracy variables
        speech_df = year_df[['country_name', 'country_text_id', 'v2x_freexp_altinf', 'v2x_libdem']].dropna()

        # Filter for specific countries
        countries = ['United States', 'Canada', 'Germany', 'India', 'Brazil', 'China', 'Russia', 'South Africa', 'Japan', 'Australia']
        self.country_df = speech_df[speech_df['country_name'].isin(countries)]

    def get_country_data(self) -> list:
        countries_list = []
        for i, row in self.country_df.iterrows():
            x = row['v2x_libdem']
            y = row['v2x_freexp_altinf']
            # Calculating Values
            r = math.sqrt(x**2 + y**2) # Magnitude/Length
            m = y/x if x != 0 else float('inf') # Angle/Slope
            countries_list.append((row['country_name'], r, m))
        return countries_list

    def compute_delta(self,country_data) -> tuple:
        country, r, m = country_data
        dx = r / math.sqrt(1 + m**2)
        dy = m * dx
        return (country, dx, dy)

    def plot_country(self,country_data) -> None:
        country_name, dx, dy = self.compute_delta(country_data)
        # Plotting Lines
        end_point_x = [0, dx] # From origin to x
        end_point_y = [0, dy] # From origin to y
        plt.plot(end_point_x, end_point_y, 'o-',label=f"{country_name} - Magnitude {float(country_data[1]):.3f}") # Label param is for legend
    
    def make_plot(self) -> None:
        plt.figure(figsize=(8,6))
        plt.scatter(self.country_df['v2x_libdem'], self.country_df['v2x_freexp_altinf'], s=50)

        for country_data in self.get_country_data():
            self.plot_country(country_data)
        
        plt.axis('equal')
        plt.xlabel('Liberal Democracy Index (0-1)')
        plt.ylabel('Freedom of Expression Index (0-1)')
        plt.title(f'Liberal Democracy vs Freedom of Expression – {2023}')
        plt.legend()
        plt.grid(True)
        plt.show()

    def rank_countries_by_speech_freedom(self) -> list:
        ranked_countries = self.get_country_data()
        # Should be sorting in decending order based on magnitude r

        ranked_countries.sort(key=lambda x: x[1], reverse=True) # x[1] is the magnitude r

        print("\033[92m--- Countries ranked by Freedom of Speech Magnitude (Descending) ---\033[0m") # Its green text
        i = 1
        for country in ranked_countries:

            print(f"{i}.) {country[0]} - Magnitude \033[94m{country[1]:.3f}\033[0m")
            i += 1
        return ranked_countries

if __name__ == "__main__":
    analysis = SpeechAnalysis('V-Dem-CY-Full+Others-v15.csv')
    analysis.make_plot()