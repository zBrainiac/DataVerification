import time

import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, DateFormatValidation, MatchesPatternValidation

### raw data example
# key       ,sensor_id ,location ,lat     ,lon       ,timestamp           ,pressure ,temperature  ,humidity
# 1         ,2266      ,1140      ,42.738 ,23.272    ,2017-07-01T00:00:07 ,95270.27 ,23.46        ,62.48

start_time = time.time()

schema = Schema([
    Column('key', [MatchesPatternValidation(r'^-?\d{1,16}$')]),  # Number / integer - up to 16
    Column('sensor_id', [MatchesPatternValidation(r'^-?\d{1,16}$')]),  # Number / integer - up to 16
    Column('location', [MatchesPatternValidation(r'^-?\d{1,16}$')]),  # Number / integer - up to 16
    Column('lat', [MatchesPatternValidation(r'^-?\d*\.\d{1,16}$')]),  # Number / decimal with up to 16 decimal place
    Column('lon', [MatchesPatternValidation(r'^-?\d*\.\d{1,16}$')]),  # Number / decimal with up to 16 decimal place
    Column('timestamp', [DateFormatValidation('%Y-%m-%dT%H:%M:%S')]),
    # Timestamp yyyy-MM-dd'T'HH:mm:ss (in Zulu/UTC time zone) e.g. 2017-07-01T00:00:07
    Column('pressure', [MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]),
    # Numbers / / decimal with 1 or 2 decimals (.00)
    Column('temperature', [InRangeValidation(-146, 60), MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]),
    # Number / decimal with upto 2 decimal place
    Column('humidity', [MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')])  # Numbers with 1 or 2 decimals (.00)
])

### get data from File
test_data = pd.read_csv("data/testCSV_short.csv")

### Data Validation
errors = schema.validate(test_data)

# filtering out invalid rows
errors_index_rows = [e.row for e in errors]
data_clean = test_data.drop(index=errors_index_rows)
data_error = test_data.reindex(index=errors_index_rows)

# manipulating column type ('object' -> 'int')
data_clean.sensor_id = data_clean.sensor_id.astype(int)

print('valid raw records:')
print(data_clean)
# execution time
print("--- %s 'Data Cleansing' in seconds ---" % (time.time() - start_time))

### ETL process

start_time = time.time()
data_clean_etl = data_clean.assign(temperature_f=lambda x: x.temperature * 9 / 5 + 32,
                                   temperature_k=lambda x: (x['temperature_f'] + 459.67) * 5 / 9
                                   )
# via function
f = lambda x: x * 2
data_clean_etl['2mal'] = data_clean_etl['temperature_k'].apply(f)

print('ETL output:')
print(data_clean_etl)
# execution time
print("--- %s 'ETL process' in seconds ---" % (time.time() - start_time))

### save data to file
start_time = time.time()
pd.DataFrame({'DataValidationErrors:': errors}).to_csv('data/error_report.txt', index=False)
data_clean.to_csv('data/clean_data.txt', index=False)
data_clean_etl.to_csv('data/clean_data_etl.txt', index=False)
data_error.to_csv('data/error_data.txt', index=False)
# execution time
print("--- %s 'save data to file' in seconds ---" % (time.time() - start_time))

### some details
# data frame info:
data_clean_etl.info()

# correlation between columns
df = data_clean_etl[['location', 'lat', 'lon', 'timestamp', 'pressure', 'temperature', 'humidity']].corr()
print(df)
