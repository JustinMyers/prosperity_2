import argparse
import importlib

parser = argparse.ArgumentParser( description="getting file name from command line" )
parser.add_argument("--trader_filename", required=True, type=str)
args = parser.parse_args()
trader_filename = args.trader_filename

print("local_try_trader.py: trader_filename = ", trader_filename)

trader = importlib.import_module(trader_filename, package=None)

Trader = trader.Trader

test_trader = Trader()

import datamodel
from datamodel import Listing, OrderDepth, Trade, TradingState

traderData = "SAMPLE"

timestamp = 1100

listings = {"AMETHYSTS": Listing(denomination= 1, product= "AMETHYSTS", symbol= "AMETHYSTS"),
            "STARFRUIT": Listing(denomination= 1, product= "STARFRUIT", symbol= "STARFRUIT")}

# order_depths = {
# 	"PRODUCT1": OrderDepth(
# 		buy_orders={10: 7, 9: 5},
# 		sell_orders={12: -5, 13: -3}
# 	),
# 	"PRODUCT2": OrderDepth(
# 		buy_orders={142: 3, 141: 5},
# 		sell_orders={144: -5, 145: -8}
# 	),	
# }

# order_depths = {
#     "AMETHYSTS": OrderDepth(
#         buy_orders={9995: 29, 9996: 2, 10002: 1}, 
#         sell_orders={10004: -2, 10005: -29}
#     ),
#     "STARFRUIT": OrderDepth(
#         buy_orders={4997: 31, 5002: 1}, 
#         sell_orders={5003: -31}
#     )
# }

amethysts_od = OrderDepth()
amethysts_od.buy_orders={9995: 29, 9996: 2, 10002: 1}
amethysts_od.sell_orders={10004: -2, 10005: -29}

starfruit_od = OrderDepth()
starfruit_od.buy_orders={4997: 31, 5002: 1}
starfruit_od.sell_orders={5003: -31}

order_depths = {
    "AMETHYSTS": amethysts_od,
    "STARFRUIT": starfruit_od
}

own_trades = {'AMETHYSTS': [Trade(buyer= '', price= 10002.0, quantity= 1, seller= 'SUBMISSION', symbol= 'AMETHYSTS', timestamp= 0), 
                            Trade(buyer= '', price= 10002.0, quantity= 1, seller= 'SUBMISSION', symbol= 'AMETHYSTS', timestamp= 0)], 
              'STARFRUIT': [Trade(buyer= '', price= 5002.0, quantity= 1, seller= 'SUBMISSION', symbol= 'STARFRUIT', timestamp= 0), 
                            Trade(buyer= '', price= 5001.0, quantity= 2, seller= 'SUBMISSION', symbol= 'STARFRUIT', timestamp= 0)]}

market_trades = {
	"AMETHYSTS": [],
	"STARFRUIT": []
}

position = {
	"PRODUCT1": 10,
	"PRODUCT2": -7
}

observations = {}

sample_trading_state = TradingState(
	traderData,
	timestamp,
    listings,
	order_depths,
	own_trades,
	market_trades,
	position,
	observations
)

result = Trader.run(test_trader, sample_trading_state)
print("RESULT = ", result)

############################################################

# https://medium.com/@evaGachirwa/running-python-script-with-arguments-in-the-command-line-93dfa5f10eff
# import argparse

# def get_sum_of_nums(num1,num2,num3):
#   return(int(num1)+int(num2)+int(num3))

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(
#         description="Script that adds 3 numbers from CMD"
#     )
#     parser.add_argument("--num1", required=True, type=int)
#     parser.add_argument("--num2", required=True, type=int)
#     parser.add_argument("--num3", required=True, type=int)
#     args = parser.parse_args()

#     num1 = args.num1
#     num2 = args.num2
#     num3 = args.num3

#     print(get_sum_of_nums(num1, num2, num3))

############################################################

# https://blog.devjunction.in/how-to-import-modules-from-string-in-python
# import importlib

# module_name = 'math'
# module = importlib.import_module(module_name)

############################################################
