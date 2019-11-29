import pandas as pd
from pandas_schema import Column, Schema
from pandas_schema.validation import InRangeValidation, DateFormatValidation, MatchesPatternValidation

# key       ,sensor_id ,location ,lat     ,lon       ,timestamp           ,pressure ,temperature  ,humidity
# 1         ,2266      ,1140      ,42.738 ,23.272    ,2017-07-01T00:00:07 ,95270.27 ,23.46        ,62.48

schema = Schema([
    Column('key', [MatchesPatternValidation(r'^-?\d{1,16}$')]),
    Column('sensor_id', [MatchesPatternValidation(r'^-?\d{1,16}$')]),
    Column('location', [MatchesPatternValidation(r'^-?\d{1,16}$')]),
    Column('lat', [MatchesPatternValidation(r'^-?\d*\.\d{1,16}$')]), # Numbers with upto 16 decimals
    Column('lon', [MatchesPatternValidation(r'^-?\d*\.\d{1,16}$')]), # Numbers with upto 16 decimals
    Column('timestamp', [DateFormatValidation('%Y-%m-%dT%H:%M:%S')]),
    Column('pressure', [MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]), # Numbers with 1 or 2 decimals (.00)
    Column('temperature', [InRangeValidation(-146, 60), MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]),
    Column('humidity', [MatchesPatternValidation(r'^-?\d*\.\d{1,2}$')]) # Numbers with 1 or 2 decimals (.00)
])
# read source data
test_data = pd.read_csv("data/testCSV_short.csv")
print('orig dataset')
print(test_data)

# data verification
errors = schema.validate(test_data)

# print verification errors to console
print('validation errors in dataset')
for error in errors:
    print(error)

# filtering out invalid rows
errors_index_rows = [e.row for e in errors]
data_clean = test_data.drop(index=errors_index_rows)
data_error = test_data.reindex(index=errors_index_rows)

# save data to file
pd.DataFrame({'DataValidationErrors:': errors}).to_csv('data/error_report.txt', index=False)
data_clean.to_csv('data/clean_data.txt', index=False)
data_error.to_csv('data/error_data.txt', index=False)

print('valid records')
print(data_clean)


print('invalid records')
print(data_error)
