from pathlib import Path
import json
import pandas as pd
from pprint import pprint
# import re


map_values = {"G26": {"multiplier": 24, "hunters": 2},
              "G27": {"multiplier": 70, "hunters": 4},
              "G28": {"multiplier": 41, "hunters": 3},
              "G29": {"multiplier": 21, "hunters": 2},
              "G30": {"multiplier": 60, "hunters": 4},
              
              "H26": {"multiplier": 47, "hunters": 3},
              "H27": {"multiplier": 82, "hunters": 5},
              "H28": {"multiplier": 87, "hunters": 5},
              "H29": {"multiplier": 80, "hunters": 5},
              "H30": {"multiplier": 35, "hunters": 3},
            
              "I26": {"multiplier": 73, "hunters": 4},
              "I27": {"multiplier": 89, "hunters": 5},
              "I28": {"multiplier": 100, "hunters": 8},
              "I29": {"multiplier": 90, "hunters": 7},
              "I30": {"multiplier": 17, "hunters": 2},
              
              "J26": {"multiplier": 77, "hunters": 5},
              "J27": {"multiplier": 83, "hunters": 5},
              "J28": {"multiplier": 85, "hunters": 5},
              "J29": {"multiplier": 79, "hunters": 5},
              "J30": {"multiplier": 55, "hunters": 4},
              
              "K26": {"multiplier": 12, "hunters": 2},
              "K27": {"multiplier": 27, "hunters": 3},
              "K28": {"multiplier": 52, "hunters": 4},
              "K29": {"multiplier": 15, "hunters": 2},
              "K30": {"multiplier": 30, "hunters": 3},
              }

# print(map_values)

tile_results = []
for tile_key in map_values:
    tile_values = map_values[tile_key]
    basic_value = tile_values["multiplier"] / tile_values["hunters"]
    
    # print(tile_key, basic_value, tile_values)
    tile_results += [[basic_value, tile_key, tile_values]]
    
# print("---")
# print(tile_results)
# for tile_result in sorted(tile_results):
#     print(tile_result)

tile_results_player_pcts = [["Tile", "multiplier", "hunters", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"]]
for tile_key in map_values:
    tile_values = map_values[tile_key]
    multiplier = tile_values["multiplier"]
    hunters = tile_values["hunters"]
    # basic_value = multiplier / hunters
    tile_results = [tile_key, multiplier, hunters]
    for player_pct in range(16):
        result_with_player_pct = multiplier / (hunters + player_pct)
        tile_results += [result_with_player_pct]
    tile_results_player_pcts += [tile_results]


tile_results_player_pcts_df = pd.DataFrame.from_records(tile_results_player_pcts)

with pd.ExcelWriter('round_3_manual_tile_results.xlsx') as writer:
    tile_results_player_pcts_df.to_excel(writer, sheet_name='Round 3 Manual')
