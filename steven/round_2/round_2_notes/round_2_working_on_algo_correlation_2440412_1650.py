import pandas as pd

# list(prices_round_2_day_1.to_dict().keys())
# ['timestamp', 'ORCHIDS', 'TRANSPORT_FEES', 'EXPORT_TARIFF', 'IMPORT_TARIFF', 'SUNLIGHT', 'HUMIDITY', 'DAY']

def csv_to_dict_by_row_index(filename)
    # dict_by_column_index = pd.read_csv("prices_round_2_day_1.csv", sep=";").to_dict()
    dict_by_column_index = pd.read_csv(filename, sep=";").to_dict()
    column_keys = list(dict_by_column_index.keys())
    row_timestamp_to_row_dicts = {}
    row_indexes = dict_by_column_index[column_keys[0]].keys()
    for row_index in row_indexes:
        row_dict = {}
        for column_key in column_keys:
            row_dict[column_key] = dict_by_column_index[column_key][row_index]
        row_timestamp_to_row_dicts[row_dict['timestamp']] = row_dict
    return row_timestamp_to_row_dicts

# row_timestamp_to_row_dicts[1000000]
# {'timestamp': 1000000, 'ORCHIDS': 1035.25, 'TRANSPORT_FEES': 0.9, 'EXPORT_TARIFF': 9.5, 'IMPORT_TARIFF': -5.0, 'SUNLIGHT': 2300.0, 'HUMIDITY': 70.0, 'DAY': 1}

# row_timestamp_to_row_dicts = csv_to_dict_by_row_index("prices_round_2_day_1.csv")
