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

# --- plot ---
plt.figure(figsize=(8,6))
plt.scatter(df3['v2x_libdem'], df3['v2x_freexp_altinf'], s=50)

for i, row in df3.iterrows():
    # Setting variables
    x = row['v2x_libdem']
    y = row['v2x_freexp_altinf']

    # Getting values for plotting lines
    r = math.sqrt(x**2 + y**2) # Magnitude/Length
    m = y/x if x != 0 else float('inf') # Angle/Slope

    # Computing deltas for line plotting
    dx = r / math.sqrt(1 + m**2)
    dy = m * dx

    # Plotting Lines
    end_point_x = [0, dx] # From origin to x
    end_point_y = [0, dy] # From origin to y
    plt.plot(end_point_x, end_point_y, 'o-',label=f"{row['country_text_id']} - Magnitude {r:.3f}") # Label param is for legend
    
    # Console Output
    print('---')
    print(row['country_text_id'])
    print("x=",x, "y=",y)
    print('Slope:', m)
    print('Magnitude:', r)

plt.xlabel('Liberal Democracy Index (0-1)')
plt.ylabel('Freedom of Expression Index (0-1)')
plt.title(f'Liberal Democracy vs Freedom of Expression – {year}')
plt.legend()
plt.grid(True)
plt.show()