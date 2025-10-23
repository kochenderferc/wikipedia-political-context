import pandas as pd
import matplotlib.pyplot as plt

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
    plt.text(row['v2x_libdem'] + 0.005, row['v2x_freexp_altinf'] + 0.005, row['country_text_id'], fontsize=9)

plt.xlabel('Liberal Democracy Index (0-1)')
plt.ylabel('Freedom of Expression Index (0-1)')
plt.title(f'Democracy vs Freedom of Expression – {year}')
plt.grid(True)
plt.show()