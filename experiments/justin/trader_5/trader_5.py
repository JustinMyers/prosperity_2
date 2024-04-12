from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle

class BestPriceTracker:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths[product]
        
        orders: List[Order] = []
        
        buy_orders = order_depth.buy_orders
        buy_order_prices = sorted(buy_orders.keys())
        lowest_buy_order_price = buy_order_prices[0]
        highest_buy_order_price = buy_order_prices[-1]
        
        sell_orders = order_depth.sell_orders
        sell_order_prices = sorted(sell_orders.keys())
        lowest_sell_order_price = sell_order_prices[0]
        highest_sell_order_price = sell_order_prices[-1]

        if data["worst_buy"] is None or lowest_buy_order_price > data["worst_buy"]:
            data["worst_buy"] = lowest_buy_order_price

        if data["best_buy"] is None or highest_buy_order_price > data["best_buy"]:
            data["best_buy"] = highest_buy_order_price

        if data["worst_sell"] is None or highest_sell_order_price < data["worst_sell"]:
            data["worst_sell"] = highest_sell_order_price
        
        if data["best_sell"] is None or lowest_sell_order_price < data["best_sell"]:
            data["best_sell"] = lowest_sell_order_price
        
        limit_width = 20

        position = state.position[product] if product in state.position else 0

        buy_gap = highest_buy_order_price - data["worst_buy"]
        sell_gap = data["worst_sell"] - lowest_sell_order_price

        if sell_gap > buy_gap:
            target_portfolio = sell_gap / (data["worst_sell"] - data["best_sell"])

        if highest_buy_order_price > 10000:
            orders.append(Order(product, 10000, -limit_width - current_holdings))
        elif lowest_sell_order_price < 10000:
            orders.append(Order(product, 10000, limit_width - current_holdings))
    
        return orders, 0, data

class MarketMaker:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths[product]
        
        orders: List[Order] = []
        
        if product in state.position:
            position = state.position[product]
        else:
            position = 0
        
        order_depth: OrderDepth = state.order_depths[product]
        
        orders: List[Order] = []
        
        buy_orders = order_depth.buy_orders
        buy_order_prices = sorted(buy_orders.keys())
        lowest_buy_order_price = buy_order_prices[0]
        highest_buy_order_price = buy_order_prices[-1]
        
        sell_orders = order_depth.sell_orders
        sell_order_prices = sorted(sell_orders.keys())
        lowest_sell_order_price = sell_order_prices[0]
        highest_sell_order_price = sell_order_prices[-1]

        limit_width = 20

        mid_price = int((highest_buy_order_price + lowest_sell_order_price) / 2)

        buy_price = mid_price - 1
        sell_price = mid_price + 1

        sell_quantity = -limit_width - position
        orders.append(Order(product, sell_price, sell_quantity))

        buy_quantity = limit_width - position
        orders.append(Order(product, buy_price, buy_quantity))

        return orders, 0, data

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
                }
            }

        conversions = 0

        for product in state.order_depths:
            if product == "AMETHYSTS":
                trader = MarketMaker()
                result[product], conversions, traderData[product] = trader.run(state, product, traderData[product])
            if product == "STARFRUIT":
                trader = MarketMaker()
                result[product], conversions, traderData[product] = trader.run(state, product, traderData[product])

        traderData = jsonpickle.encode(traderData)
        conversions = 0
        return result, conversions, traderData