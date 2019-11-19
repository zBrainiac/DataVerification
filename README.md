### Project status

Quality Gate | Status |
--- | --- |
Source Code:| [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=zBrainiac_DataVerification&metric=alert_status)](https://sonarcloud.io/dashboard?id=zBrainiac_DataVerification) |
Build | [![Build Status](https://travis-ci.com/zBrainiac/DataVerification.svg?branch=master)](https://travis-ci.com/zBrainiac/DataVerification) |
  
### Original test data set stored in: _data/fixed_width.txt_
```python
name     title              salary sex date
Ryxlar   Chief Dragon Slayer20000  M   2019-01-31
Tiqla    Assistant Alchemist4000   F   2019-01-31
Brynz    Brute Squad        1000   N   2019-01-31
Mr PotatoMess Cook          35000  M   2019-0231
```


### Console output:
```python
orig dataset
        name                title  salary sex        date
0     Ryxlar  Chief Dragon Slayer   20000   M  2019-01-31
1      Tiqla  Assistant Alchemist    4000   F  2019-01-31
2      Brynz          Brute Squad    1000   N  2019-01-31
3  Mr Potato            Mess Cook   35000   M   2019-0231
```


```python
validation errors in dataset
{row: 2, column: "sex"}: "N" is not in the list of legal options (F, M)
{row: 3, column: "salary"}: "35000" was not in the range [0, 33000)
{row: 3, column: "date"}: "2019-0231" does not match the date format string "%Y-%m-%d"
```


```python
valid records
     name                title  salary sex        date
0  Ryxlar  Chief Dragon Slayer   20000   M  2019-01-31
1   Tiqla  Assistant Alchemist    4000   F  2019-01-31
```

```python
invalid records
        name        title  salary sex        date
2      Brynz  Brute Squad    1000   N  2019-01-31
3  Mr Potato    Mess Cook   35000   M   2019-0231
3  Mr Potato    Mess Cook   35000   M   2019-0231
```
