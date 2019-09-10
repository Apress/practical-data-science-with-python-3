import pandas as pd

df = pd.read_csv('GHCND_sample_csv.csv',
                 usecols = [3, 4, 5, 6, 7], 
                 index_col = 2,
                 parse_dates = True, 
                 infer_datetime_format = True)
df['TMIN'] = df['TMIN'] / 10
df['TMAX'] = df['TMAX'] / 10
print(df.head())

from plot_stations import plot_stations
plot_stations(df['LONGITUDE'].tolist()[0], df['LATITUDE'].tolist()[0])

min_temp = df['TMIN'].min()
max_temp = df['TMAX'].max()
print("\nMinimum temperature: %g\nMaximum temperature: %g\n" % (min_temp, max_temp))

LIMIT_HIGH = 0
LIMIT_LOW = -30

extreme_high_temps = df['TMAX'][df['TMAX'] > LIMIT_HIGH]
extreme_low_temps = df['TMIN'][df['TMIN'] < LIMIT_LOW]

print('Extreme low temperatures\n', extreme_low_temps)
print('\nExtreme high temperatures\n', extreme_high_temps)

from plot_temps import plot_temps
plot_temps(df, min_temp, max_temp, extreme_low_temps, extreme_high_temps)
