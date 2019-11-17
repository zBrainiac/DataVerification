import pandas as pd
import pandas_schema
from pandas_schema import Column
from pandas_schema.validation import CustomElementValidation, LeadingWhitespaceValidation, TrailingWhitespaceValidation, \
    InRangeValidation, DateFormatValidation, InListValidation
from decimal import *


def check_decimal(dec):
    try:
        Decimal(dec)
    except InvalidOperation:
        return False
    return True


def do_validation():
    # read the data
    widths = [
        9,  # name
        19,  # title
        6,  # salary
        4,  # sex
        11,  # date
    ]

    # read source data
    test_data = pd.read_fwf("data/fixed_width.txt", widths=widths)

    print(test_data)

    # define validation elements
    decimal_validation = [CustomElementValidation(lambda d: check_decimal(d), 'is not decimal')]

    # define validation schema
    schema = pandas_schema.Schema([
        Column('name', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]),
        Column('title', [LeadingWhitespaceValidation(), TrailingWhitespaceValidation()]),
        Column('salary', decimal_validation, [InRangeValidation(0, 33000)]),
        Column('sex', [InListValidation(['F', 'M'])]),
        Column('date', [DateFormatValidation('%Y-%m-%d')])
    ])

    # apply validation
    errors = schema.validate(test_data)

    # print verification errors to console
    print('validation errors in data set')
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


if __name__ == '__main__':
    do_validation()
