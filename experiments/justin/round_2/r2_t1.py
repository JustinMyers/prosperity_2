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
        cost_of_export = int(bidPrice - transportFees - exportTariff)

        buy_orders = order_depth.buy_orders
        buy_order_prices = sorted(buy_orders.keys())
        lowest_buy_order_price = buy_order_prices[0]
        highest_buy_order_price = buy_order_prices[-1]
        
        sell_orders = order_depth.sell_orders
        sell_order_prices = sorted(sell_orders.keys())
        lowest_sell_order_price = sell_order_prices[0]
        highest_sell_order_price = sell_order_prices[-1]

        if highest_buy_order_price > cost_of_import:
            orders.append(Order(product, cost_of_import, -100))
        elif lowest_sell_order_price < cost_of_export:
            orders.append(Order(product, cost_of_export, 100))

        # sunlight_delta = sunlight - data.get("prev_sunlight", 0)
        # humidity_delta = humidity - data.get("prev_humidity", 0)

        # data["prev_sunlight"] = sunlight
        # data["prev_humidity"] = humidity
        # data["prev_sunlight_delta"] = sunlight_delta
        # data["prev_humidity_delta"] = humidity_delta
       
        return orders, conversions, data

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
                conversions += orchid_conversions

        traderData = jsonpickle.encode(traderData)
        return result, conversions, traderData