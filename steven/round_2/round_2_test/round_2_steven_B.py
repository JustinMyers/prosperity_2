from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle

class OrchidTrader:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths[product]
        
        orders: List[Order] = []

        position = state.position[product] if product in state.position else 0

        conversions = -position

        # sunlight = state.observations.conversionObservations["ORCHIDS"].sunlight
        # humidity = state.observations.conversionObservations["ORCHIDS"].humidity
        bidPrice = state.observations.conversionObservations["ORCHIDS"].bidPrice
        askPrice = state.observations.conversionObservations["ORCHIDS"].askPrice
        transportFees = state.observations.conversionObservations["ORCHIDS"].transportFees
        exportTariff = state.observations.conversionObservations["ORCHIDS"].exportTariff
        importTariff =  state.observations.conversionObservations["ORCHIDS"].importTariff

        cost_of_import = int(askPrice + transportFees + importTariff)
        # cost_of_export = int(bidPrice - transportFees - exportTariff)
        cost_of_export = int(bidPrice + transportFees + exportTariff)

        limit_width = 100
        buy_quantity = limit_width - position
        buy_orders = order_depth.buy_orders
        buy_order_prices = sorted(buy_orders.keys())
        lowest_buy_order_price = buy_order_prices[0]
        highest_buy_order_price = buy_order_prices[-1]
        
        sell_quantity = -limit_width - position
        sell_orders = order_depth.sell_orders
        sell_order_prices = sorted(sell_orders.keys())
        lowest_sell_order_price = sell_order_prices[0]
        highest_sell_order_price = sell_order_prices[-1]

        if highest_buy_order_price > cost_of_import:
            # orders.append(Order(product, cost_of_import, -100))
            orders.append(Order(product, cost_of_import, buy_quantity))
        elif lowest_sell_order_price < cost_of_export:
            # orders.append(Order(product, cost_of_export, 100))
            orders.append(Order(product, cost_of_export, sell_quantity))

        # sunlight_delta = sunlight - data.get("prev_sunlight", 0)
        # humidity_delta = humidity - data.get("prev_humidity", 0)

        # data["prev_sunlight"] = sunlight
        # data["prev_humidity"] = humidity
        # data["prev_sunlight_delta"] = sunlight_delta
        # data["prev_humidity_delta"] = humidity_delta
       
        return orders, conversions, data

class AmethystsTrader:    
    def run(self, state: TradingState, product: str):
        result = {}
    # for product in state.order_depths:

        # if product in state.position:
        #     position = state.position[product]
        # else:
        #     position = 0
        position = state.position[product] if product in state.position else 0

        order_depth: OrderDepth = state.order_depths[product]
        
        limit_width = 20

        orders: List[Order] = []
    
        sell_quantity = -limit_width - position
        orders.append(Order(product, 10002, sell_quantity))
        buy_quantity = limit_width - position
        orders.append(Order(product, 9998, buy_quantity))

        result[product] = orders

        traderData = "SAMPLE"         
        conversions = 0
        return result, conversions, traderData
    
class BasicTrader:    
    def run(self, state: TradingState, product: str):
        result = {}
    # for product in state.order_depths:

        # if product in state.position:
        #     position = state.position[product]
        # else:
        #     position = 0
        position = state.position[product] if product in state.position else 0

        order_depth: OrderDepth = state.order_depths[product]
        
        limit_width = 20

        orders: List[Order] = []
    
        buy_orders = order_depth.buy_orders
        buy_order_prices = sorted(buy_orders.keys())
        buy_order_price = buy_order_prices[0]
        buy_order_price += 1
        
        sell_orders = order_depth.sell_orders
        sell_order_prices = sorted(sell_orders.keys(), reverse=True)
        sell_order_price = sell_order_prices[0]
        sell_order_price -= 1

        # limit_width = 20

        sell_quantity = -limit_width - position
        orders.append(Order(product, sell_order_price, sell_quantity))

        buy_quantity = limit_width - position
        orders.append(Order(product, buy_order_price, buy_quantity))

        result[product] = orders

        traderData = "SAMPLE"         
        conversions = 0
        return result, conversions, traderData
    
class Trader:    
    def run(self, state: TradingState):
        result = {}

        if state.traderData:
            traderData = jsonpickle.decode(state.traderData)
        else:
            traderData = {
                "AMETHYSTS": {
                    "worst_buy": None,
                    "best_buy": None,
                    "worst_sell": None,
                    "best_sell": None
                },
                "STARFRUIT": {
                },
                "ORCHIDS": {
                }
            }

        conversions = 0

        for product in state.order_depths:
            if product == "ORCHIDS":
                trader = OrchidTrader()
                result[product], orchid_conversions, traderData[product] = trader.run(state, product, traderData[product])
                conversions = orchid_conversions
            elif product == "AMETHYSTS":
                trader = AmethystsTrader()
                # result[product], conversions, traderData[product] = trader.run(state, product, traderData[product])
                result[product], amethysts_conversions, traderData[product] = trader.run(state, product)
            elif product == "STARFRUIT":
                trader = BasicTrader()
                # result[product], conversions, traderData[product] = trader.run(state, product, traderData[product])
                result[product], starfruit_conversions, traderData[product] = trader.run(state, product)

        traderData = jsonpickle.encode(traderData)
        return result, conversions, traderData