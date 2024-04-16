from pathlib import Path
import json
import pandas as pd
from pprint import pprint
import re

path = Path('prosperity_2.log.txt')
log_file = path.read_text()

log_lines = log_file.splitlines()

activities_log_start = log_lines.index('Activities log:')
trade_history_start = log_lines.index('Trade History:')

sandbox_logs_lines = log_lines[1:activities_log_start]
activities_log_lines = log_lines[(activities_log_start + 1):trade_history_start]
trade_history_lines = log_lines[(trade_history_start + 1):-1]

def pop_json_from_list(log_lines):
# read lines until close brace is found and remove them from the list and return the json string
    json_string = ''
    while log_lines:
        line = log_lines.pop(0)
        json_string += line
        if line == '}':
            break
    return json_string

sandbox_json_objects = []
while sandbox_logs_lines:
    json_string = pop_json_from_list(sandbox_logs_lines)
    if json_string != '':
        # sandbox_json_objects += [json.loads(pop_json_from_list(sandbox_logs_lines))]
        sandbox_json_objects += [json.loads(json_string)]

# sandbox_json_objects[0].keys()
# dict_keys(['sandboxLog', 'lambdaLog', 'timestamp'])

if trade_history_lines:
    trade_history_json_objects = json.loads(''.join(trade_history_lines) + ']')
else:
    trade_history_json_objects = []

# trade_history_json_objects[0].keys()
# dict_keys(['timestamp', 'buyer', 'seller', 'symbol', 'currency', 'price', 'quantity'])

# json.loads(sandbox_json_objects[0])
# {'sandboxLog': '', 'lambdaLog': 'traderData: \nObservations: (plainValueObservations: {}, conversionObservations: {})\nAcceptable price : 10\nBuy Order depth : 3, Sell order depth : 2\nSELL 1x 10002\nAcceptable price : 10\nBuy Order depth : 2, Sell order depth : 1\nSELL 1x 5002', 'timestamp': 0}

sandbox_logs_header = ['sandboxLog', 'timestamp', 'lambdaLog']

orchids_info__lines = []

sandbox_logs_array = [sandbox_logs_header]
for json_row in sandbox_json_objects:
    row_array = []
    for row_key in sandbox_logs_header:
        row_value = json_row[row_key]
        row_array += [row_value]
        # if row_key == "lambdaLog":
            
        #     pattern = re.compile('^ORCHIDS_INFO')
        #     row_lines = row_value.splitlines()
        #     for line in row_lines:
        #         if pattern.match(line):
        #             orchids_info__lines += [line]

    sandbox_logs_array += [row_array]
    
    
# with open('orchids_info.csv', 'w') as file:
#     for line in orchids_info__lines:
#         file.write(f"{line}\n")


activities_log_array = []
activities_products_to_log_array = {}
activities_header = []
for scsv_row in activities_log_lines:
    scsv_row_split = scsv_row.split(';')
    activities_log_array += [scsv_row_split]
    if (len(scsv_row_split) > 2):
        product_name = scsv_row_split[2]
        if product_name == "product":
            activities_header = activities_log_array
        elif product_name in activities_products_to_log_array.keys():
            activities_products_to_log_array[product_name] += [scsv_row_split]
        else:
            activities_products_to_log_array[product_name] = [[activities_header]]
            activities_products_to_log_array[product_name] += [scsv_row_split]
        

trade_history_array = []
trade_history_products_to_log_array = {}
if trade_history_json_objects != []:
    trade_history_header = list(trade_history_json_objects[0].keys())
    trade_history_array = [trade_history_header]
    for json_row in trade_history_json_objects:
        row_array = []
        for row_key in trade_history_header:
            row_array += [json_row[row_key]]
        trade_history_array += [row_array]
            
        if (len(row_array) > 3):
            product_name = row_array[3]
            if product_name in trade_history_products_to_log_array.keys():
                trade_history_products_to_log_array[product_name] += [row_array]
            else:
                trade_history_products_to_log_array[product_name] = [[trade_history_header]]
                trade_history_products_to_log_array[product_name] += [row_array]
            

# import pandas
# writer = pd.ExcelWriter('prosperity_log.xlsx', engine='xlsxwriter')

sandbox_logs_df = pd.DataFrame.from_records(sandbox_logs_array)
activities_log_df = pd.DataFrame.from_records(activities_log_array)
trade_history_df = pd.DataFrame.from_records(trade_history_array)


with pd.ExcelWriter('prosperity_log_product_activities.xlsx') as writer:
    sandbox_logs_df.to_excel(writer, sheet_name='Sandbox logs')
    activities_log_df.to_excel(writer, sheet_name='Activities log')
    trade_history_df.to_excel(writer, sheet_name='Trade History')
    for product_name in sorted(trade_history_products_to_log_array.keys()):
        product_log_df = pd.DataFrame.from_records(trade_history_products_to_log_array[product_name])
        product_log_df.to_excel(writer, sheet_name=(product_name+'_History'))
    for product_name in sorted(activities_products_to_log_array.keys()):
        product_log_df = pd.DataFrame.from_records(activities_products_to_log_array[product_name])
        product_log_df.to_excel(writer, sheet_name=(product_name+'_Activities'))
    
# writer.close()

