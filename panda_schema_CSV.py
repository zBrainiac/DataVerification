import time

import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, DateFormatValidation, MatchesPatternValidation

# key       ,sensor_id ,location ,lat     ,lon       ,timestamp           ,pressure ,temperature  ,humidity
# 1         ,2266      ,1140      ,42.738 ,23.272    ,2017-07-01T00:00:07 ,95270.27 ,23.46        ,62.48

start_time = time.time()

schema = Schema([
    Column('key', [MatchesPatternValidation(r'^-?\d{1,16}$')]),            # Number / integer - up to 16
    Column('sensor_id', [MatchesPatternValidation(r'^-?\d{1,16}$')]),      # Number / integer - up to 16
    Column('location', [MatchesPatternValidation(r'^-?\d{1,16}$')]),       # Number / integer - up to 16
    Column('lat', [MatchesPatternValidation(r'^-?\d*\.\d{1,16}$')]),       # Number / decimal with up to 16 decimal place
    Column('lon', [MatchesPatternValidation(r'^-?\d*\.\d{1,16}$')]),       # Number / decimal with up to 16 decimal place
    Column('timestamp', [DateFormatValidation('%Y-%m-%dT%H:%M:%S')]),      # Timestamp yyyy-MM-dd'T'HH:mm:ss (in Zulu/UTC time zone) e.g. 2017-07-01T00:00:07
    Column('pressure', [MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]),   # Numbers / / decimal with 1 or 2 decimals (.00)
    Column('temperature', [InRangeValidation(-146, 60), MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]),  # Number / decimal with upto 2 decimal place
    Column('humidity', [MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')])    # Numbers with 1 or 2 decimals (.00)
])

### get data from File
print('load orig dataset from file')

test_data = pd.read_csv("data/testCSV_short.csv")
print('orig dataset')
print(test_data)

# data verification
print('start data verification on orig dataset')

errors = schema.validate(test_data)

# print verification errors to console
print('validation errors in dataset')
for error in errors:
    print(error)

# filtering out invalid rows
errors_index_rows = [e.row for e in errors]
data_clean = test_data.drop(index=errors_index_rows)
data_error = test_data.reindex(index=errors_index_rows)

print('valid records')
print(data_clean)
# execution time
print("--- %s 'Data Cleansing' in seconds ---" % (time.time() - start_time))

# save data to file
start_time = time.time()
pd.DataFrame({'DataValidationErrors:': errors}).to_csv('data/error_report.txt', index=False)
data_clean.to_csv('data/clean_data.txt', index=False)
data_error.to_csv('data/error_data.txt', index=False)
# execution time
print("--- %s 'save data to file' in seconds ---" % (time.time() - start_time))

