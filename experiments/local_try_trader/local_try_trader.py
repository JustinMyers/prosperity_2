import argparse
import importlib

from pathlib import Path
# import json
# import pandas as pd

# path = Path('prosperity_2.log.txt')
# log_file = path.read_text()

parser = argparse.ArgumentParser( description="getting file name from command line" )
parser.add_argument("--trader_filename", required=True, type=str)
args = parser.parse_args()
trader_filename = args.trader_filename

print("local_try_trader.py: trader_filename = ", trader_filename)
# path = Path(trader_filename)

# import subprocess
# # subprocess.Popen('touch __init__.py', shell=True)
# relative_path_to_trader = "/".join(trader_filename.split("/")[0:-1])
# print("local_try_trader.py: relative_path_to_trader = ", relative_path_to_trader)

# subprocess.Popen("touch " + relative_path_to_trader + "/__init__.py", shell=True)
# # <Popen: returncode: None args: 'touch ../steven_demo_trader/__init__.py'>

# # https://stackoverflow.com/questions/49039436/how-to-import-a-module-from-a-different-folder/49039555#49039555
# import sys
# import os

# print("sys.path = ", sys.path)

# # print("os.path = ", os.path)

# sys.path.insert(0, os.path.abspath(relative_path_to_trader))

# print("sys.path = ", sys.path)

# # https://stackoverflow.com/questions/14071135/import-file-using-string-as-name
# # demo_trader = __import__(trader_filename)

# # # File "/home/stevenmyers/py_projects/prosperity_2/experiments/local_try_trader/local_try_trader.py", line 36, in <module>
# # trader = __import__("/home/stevenmyers/py_projects/prosperity_2/experiments/local_try_trader/local_try_trader.py")

# # from trader_filename import Trader
# trader = __import__(trader_filename)

trader = importlib.import_module(trader_filename, package=None)

Trader = trader.Trader

# from trader_filename import Trader

# from demo_trader import Trader
test_trader = Trader()

import datamodel
from datamodel import TradingState

# sample_trading_state = {"listings": {"AMETHYSTS": {"denomination": 1, "product": "AMETHYSTS", "symbol": "AMETHYSTS"},
#                                      "STARFRUIT": {"denomination": 1, "product": "STARFRUIT", "symbol": "STARFRUIT"}}, 
#                         "market_trades": {}, 
#                         "observations": {"conversionObservations": {}, "plainValueObservations": {}},
#                         "order_depths": {"AMETHYSTS": {"buy_orders": {"9995": 29, "9996": 2, "10002": 1},
#                                                        "sell_orders": {"10004": -2, "10005": -29}},
#                                          "STARFRUIT": {"buy_orders": {"4997": 31, "5002": 1},
#                                                        "sell_orders": {"5003": -31}}}, 
#                         "own_trades": {},
#                         "position": {},
#                         "timestamp": 0,
#                         "traderData": "SAMPLE"}

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

# order_depths = {"AMETHYSTS": OrderDepth({9995: 29, 9996: 2, 10002: 1},
#                                         {10004: -2, 10005: -29}),
#                 "STARFRUIT": OrderDepth({4997: 31, 5002: 1},
#                                         {5003: -31})}

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
