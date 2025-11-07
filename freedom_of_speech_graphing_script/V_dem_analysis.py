import pandas as pd
import matplotlib.pyplot as plt
import math

# --- load data ---
# update the file paths/URLs as appropriate
vdem = pd.read_csv('V-Dem-CY-Full+Others-v15.csv', low_memory=False)

# select year
year = 2023
df = vdem[vdem['year'] == year]

# pick variables: freedom of expression + liberal democracy
df2 = df[['country_name', 'country_text_id', 'v2x_freexp_altinf', 'v2x_libdem']].dropna()

# optional: filter a subset of countries
countries = ['United States', 'Canada', 'Germany', 'India', 'Brazil', 'China', 'Russia', 'South Africa', 'Japan', 'Australia']
df3 = df2[df2['country_name'].isin(countries)]

def get_country_data(dataframe):
    countries_list = []
    for i, row in dataframe.iterrows():
        x = row['v2x_libdem']
        y = row['v2x_freexp_altinf']
        # Calculating Values
        r = math.sqrt(x**2 + y**2) # Magnitude/Length
        m = y/x if x != 0 else float('inf') # Angle/Slope
        countries_list.append((row['country_text_id'], r, m))
    return countries_list

def compute_delta(country_data):
    country, r, m = country_data
    dx = r / math.sqrt(1 + m**2)
    dy = m * dx
    return (country, dx, dy)

def plot_data(country_data):
    country_name, dx, dy = compute_delta(country_data)
    # Plotting Lines
    end_point_x = [0, dx] # From origin to x
    end_point_y = [0, dy] # From origin to y
    plt.plot(end_point_x, end_point_y, 'o-',label=f"{country_name} - Magnitude {float(country_data[2]):.3f}") # Label param is for legend

def make_plot(dataframe):
    plt.figure(figsize=(8,6))
    plt.scatter(df3['v2x_libdem'], df3['v2x_freexp_altinf'], s=50)

    for country_data in get_country_data(dataframe):
        plot_data(country_data)

    plt.xlabel('Liberal Democracy Index (0-1)')
    plt.ylabel('Freedom of Expression Index (0-1)')
    plt.title(f'Liberal Democracy vs Freedom of Expression – {year}')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    make_plot(df3)