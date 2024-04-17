import pandas as pd

prices_round_2_day_m1 = pd.read_csv("prices_round_2_day_-1.csv", sep=";")
prices_round_2_day_0 = pd.read_csv("prices_round_2_day_0.csv", sep=";")
prices_round_2_day_1 = pd.read_csv("prices_round_2_day_1.csv", sep=";")

# list(prices_round_2_day_1.to_dict().keys())
# ['timestamp', 'ORCHIDS', 'TRANSPORT_FEES', 'EXPORT_TARIFF', 'IMPORT_TARIFF', 'SUNLIGHT', 'HUMIDITY', 'DAY']

# Summarizing trading microstructure of ORCHIDs:
# 1. ConversionObservation (https://imc-prosperity.notion.site/Writing-an-Algorithm-in-Python-658e233a26e24510bfccf0b1df647858#44efb36257b94733887ae00f46a805f1) shows quotes of ORCHID offered by the ducks from South Archipelago
# 2. If you want to purchase 1 unit of ORCHID from the south, you will purchase at the askPrice, pay the TRANSPORT_FEES, IMPORT_TARIFF 
# 3. If you want to sell 1 unit of ORCHID to the south, you will sell at the bidPrice, pay the TRANSPORT_FEES, EXPORT_TARIFF
# 4. You can ONLY trade with the south via the conversion request with applicable conditions as mentioned in the wiki
# 5. For every 1 unit of ORCHID net long position you hold, you will pay 0.1 Seashells per timestamp you hold that position. No storage cost applicable to net short position
# 6. Negative ImportTariff would mean you would receive premium for importing ORCHIDs to your island
# 7. Each Day in ORCHID trading is equivalent to 12 hours on the island. You can assume the ORCHID quality doesn’t deteriorate overnight
# 8. Sunlight unit: Average sunlight per hour is 2500 units. The data/plot shows instantaneous rate of sunlight on any moment of the day

# steven/round_2/round_2_notes/round_2_algo.odt
# Orchid position linit 100
# Sunlight: under 7 hours, decrease production 4% for every 10 minutes
# Humidity: outside of 60% to 80%, decrease production 2% for every 5% bad humidity
# Storage Space:  5,000 maximum, cost 0.1 Seashell per Orchid per timestamp.

def sunlight_production(sunlight_value):
    sunlight_70 = (10000 / 24 * 7)  # 2916.666666666667
    minutes_10 = (10000 / 24 / 6)  # 69.44444444444444
    sunlight_production = 1.0
    if (sunlight_value < sunlight_70):
        sunlight_deficit_pct = (sunlight_70 - sunlight_value) / minutes_10
        sunlight_penalty_pct = sunlight_deficit_pct * 4
        sunlight_production -= sunlight_penalty_pct / 100
    return sunlight_production

# https://pandas.pydata.org/docs/getting_started/intro_tutorials/05_add_columns.html
# https://saturncloud.io/blog/how-to-create-new-values-in-a-pandas-dataframe-column-based-on-values-from-another-column/#:~:text=To%20create%20the%20new%20column,and%20returns%20the%20corresponding%20category.

prices_round_2_day_m1['sunlight_production'] = prices_round_2_day_m1['SUNLIGHT'].apply(sunlight_production)
prices_round_2_day_0['sunlight_production'] = prices_round_2_day_0['SUNLIGHT'].apply(sunlight_production)
prices_round_2_day_1['sunlight_production'] = prices_round_2_day_1['SUNLIGHT'].apply(sunlight_production)

def humidity_production(humidity_value):
    humidity_production = 1.0
    if (humidity_value > 80):
        bad_humidity_pct = humidity_value - 80.0
        humidity_penalty_pct = bad_humidity_pct / 5 * 2
        humidity_production -= humidity_penalty_pct / 100
    elif (humidity_value < 60):
        bad_humidity_pct = 60 - humidity_value
        humidity_penalty_pct = bad_humidity_pct / 5 * 2
        humidity_production -= humidity_penalty_pct / 100
    return humidity_production

prices_round_2_day_m1['humidity_production'] = prices_round_2_day_m1['HUMIDITY'].apply(humidity_production)
prices_round_2_day_0['humidity_production'] = prices_round_2_day_0['HUMIDITY'].apply(humidity_production)
prices_round_2_day_1['humidity_production'] = prices_round_2_day_1['HUMIDITY'].apply(humidity_production)

prices_round_2_day_m1['production_penalty'] = (prices_round_2_day_m1['sunlight_production'] * prices_round_2_day_m1['humidity_production'])
prices_round_2_day_0['production_penalty'] = (prices_round_2_day_0['sunlight_production'] * prices_round_2_day_0['humidity_production'])
prices_round_2_day_1['production_penalty'] = (prices_round_2_day_1['sunlight_production'] * prices_round_2_day_1['humidity_production'])

##############

prices_round_2_day_m1['buy_penalty'] = (prices_round_2_day_m1['TRANSPORT_FEES'] + prices_round_2_day_m1['IMPORT_TARIFF'])
prices_round_2_day_0['buy_penalty'] = (prices_round_2_day_0['TRANSPORT_FEES'] + prices_round_2_day_0['IMPORT_TARIFF'])
prices_round_2_day_1['buy_penalty'] = (prices_round_2_day_1['TRANSPORT_FEES'] + prices_round_2_day_1['IMPORT_TARIFF'])

prices_round_2_day_m1['sell_penalty'] = (prices_round_2_day_m1['TRANSPORT_FEES'] + prices_round_2_day_m1['EXPORT_TARIFF'])
prices_round_2_day_0['sell_penalty'] = (prices_round_2_day_0['TRANSPORT_FEES'] + prices_round_2_day_0['EXPORT_TARIFF'])
prices_round_2_day_1['sell_penalty'] = (prices_round_2_day_1['TRANSPORT_FEES'] + prices_round_2_day_1['EXPORT_TARIFF'])

##############
# ['timestamp', 'ORCHIDS', 'TRANSPORT_FEES', 'EXPORT_TARIFF', 'IMPORT_TARIFF', 'SUNLIGHT', 'HUMIDITY', 'DAY']

prices_round_2_day_m1['orchids_minus_bp'] = (prices_round_2_day_m1['ORCHIDS'] - prices_round_2_day_m1['buy_penalty'])
prices_round_2_day_0['orchids_minus_bp'] = (prices_round_2_day_0['ORCHIDS'] - prices_round_2_day_0['buy_penalty'])
prices_round_2_day_1['orchids_minus_bp'] = (prices_round_2_day_1['ORCHIDS'] - prices_round_2_day_1['buy_penalty'])

prices_round_2_day_m1['orchids_plus_bp'] = (prices_round_2_day_m1['ORCHIDS'] + prices_round_2_day_m1['buy_penalty'])
prices_round_2_day_0['orchids_plus_bp'] = (prices_round_2_day_0['ORCHIDS'] + prices_round_2_day_0['buy_penalty'])
prices_round_2_day_1['orchids_plus_bp'] = (prices_round_2_day_1['ORCHIDS'] + prices_round_2_day_1['buy_penalty'])

prices_round_2_day_m1['orchids_minus_sp'] = (prices_round_2_day_m1['ORCHIDS'] - prices_round_2_day_m1['sell_penalty'])
prices_round_2_day_0['orchids_minus_sp'] = (prices_round_2_day_0['ORCHIDS'] - prices_round_2_day_0['sell_penalty'])
prices_round_2_day_1['orchids_minus_sp'] = (prices_round_2_day_1['ORCHIDS'] - prices_round_2_day_1['sell_penalty'])

prices_round_2_day_m1['orchids_plus_sp'] = (prices_round_2_day_m1['ORCHIDS'] + prices_round_2_day_m1['sell_penalty'])
prices_round_2_day_0['orchids_plus_sp'] = (prices_round_2_day_0['ORCHIDS'] + prices_round_2_day_0['sell_penalty'])
prices_round_2_day_1['orchids_plus_sp'] = (prices_round_2_day_1['ORCHIDS'] + prices_round_2_day_1['sell_penalty'])

##############

prices_round_2_day_m1['orchids_minus_900'] = (prices_round_2_day_m1['ORCHIDS'] - 900 )
prices_round_2_day_0['orchids_minus_900'] = (prices_round_2_day_0['ORCHIDS'] - 900 )
prices_round_2_day_1['orchids_minus_900'] = (prices_round_2_day_1['ORCHIDS'] - 900 )

##############

prices_round_2_day_m1[['ORCHIDS','orchids_minus_900','production_penalty','sunlight_production','humidity_production','buy_penalty','sell_penalty']].corr()
prices_round_2_day_0[['ORCHIDS','orchids_minus_900','production_penalty','sunlight_production','humidity_production','buy_penalty','sell_penalty']].corr()
prices_round_2_day_1[['ORCHIDS','orchids_minus_900','production_penalty','sunlight_production','humidity_production','buy_penalty','sell_penalty']].corr()

##############



##############



##############



##############



##############
