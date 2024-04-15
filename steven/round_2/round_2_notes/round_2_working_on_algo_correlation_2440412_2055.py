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
    sunlight_production = 100
    if (sunlight_value < sunlight_70):
        sunlight_deficit = sunlight_70 - sunlight_value
        sunlight_penalty_pct = sunlight_deficit / minutes_10 * 4
        sunlight_production -= sunlight_penalty_pct
    return sunlight_production

# https://pandas.pydata.org/docs/getting_started/intro_tutorials/05_add_columns.html
# https://saturncloud.io/blog/how-to-create-new-values-in-a-pandas-dataframe-column-based-on-values-from-another-column/#:~:text=To%20create%20the%20new%20column,and%20returns%20the%20corresponding%20category.

prices_round_2_day_m1['sunlight_production'] = prices_round_2_day_m1['SUNLIGHT'].apply(sunlight_production)

def humidity_production(humidity_value)
    humidity_production = 100
    if (humidity value > 80)
