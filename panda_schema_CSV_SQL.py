import time

import pandas as pd
import pandasql
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, DateFormatValidation, MatchesPatternValidation

start_time = time.time()

pattern_id = r'^-?\d{1,16}$'
pattern_dec = r'^-?\d*\.\d{1,2}$'
pattern_geo = r'^-?\d*\.\d{1,16}$'

schema = Schema([
    Column('key', [MatchesPatternValidation(pattern_id)]),  # Number / integer - up to 16
    Column('sensor_id', [MatchesPatternValidation(pattern_id)]),  # Number / integer - up to 16
    Column('location', [MatchesPatternValidation(pattern_id)]),  # Number / integer - up to 16
    Column('lat', [MatchesPatternValidation(pattern_geo)]),  # Number / decimal with up to 16 decimal place
    Column('lon', [MatchesPatternValidation(pattern_geo)]),  # Number / decimal with up to 16 decimal place
    Column('timestamp', [DateFormatValidation('%Y-%m-%dT%H:%M:%S')]),
    # Timestamp yyyy-MM-dd'T'HH:mm:ss (in Zulu/UTC time zone) e.g. 2017-07-01T00:00:07
    Column('pressure', [MatchesPatternValidation(pattern_dec)]),  # Numbers / / decimal with 1 or 2 decimals (.00)
    Column('temperature', [InRangeValidation(-146, 60), MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]),
    # Number / decimal with upto 2 decimal place
    Column('humidity', [MatchesPatternValidation(pattern_dec)])  # Numbers with 1 or 2 decimals (.00)
])

### get data from File
print('load orig dataset from file')

df_test_data_iot = pd.read_csv("data-input/testCSV.csv")
print('orig iot dataset')
print(df_test_data_iot)

df_OrderBy = pandasql.sqldf("SELECT sensor_id, count() as No, lat, lon "
                            "FROM df_test_data_iot "
                            "GROUP BY sensor_id ORDER BY "
                            "count() DESC")

df_OrderBy_10 = df_OrderBy.head(10)
print("First 10 rows of the DataFrame:")
print(df_OrderBy_10)

df_test_data_geoloc = pd.read_csv("data-input/geolocation_ch.csv")
print('orig geoloc dataset')
print(df_test_data_geoloc)


df_Join = pandasql.sqldf("SELECT iot.key, iot.sensor_id, geoloc.city "
                         "FROM df_test_data_geoloc AS geoloc "
                         "JOIN df_test_data_iot AS iot "
                         "ON iot.key = geoloc.sensor_id")


df_Join_10 = df_Join.head(10)
print("First 10 rows of the DataFrame:")
print(df_Join_10)

# save data to file
df_Join.to_csv('data-output/output_df_join.txt', index=False)

start_time = time.time()
# data_clean.to_csv('data-output/clean_data.txt', index=False)

# execution time
print("--- %s 'save data to file' in seconds ---" % (time.time() - start_time))
