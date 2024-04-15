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

print(map_values)

tile_results = []
for tile_key in map_values:
    tile_values = map_values[tile_key]
    basic_value = tile_values["multiplier"] / tile_values["hunters"]
    
    print(tile_key, basic_value, tile_values)
    tile_results += [[basic_value, tile_key, tile_values]]
    
print("---")
# print(tile_results)
for tile_result in sorted(tile_results):
    print(tile_result)

    