from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List

class Trader:    
    def run(self, state: TradingState):
        result = {}
        positions_hash = {} # this will store product name and position data
        for product in state.order_depths:
            # if product not in state.market_trades:
            #     volume = 0
            # else:
            #     market_trades = state.market_trades[product]
            #     volume = 0
            #     for trade in market_trades:
            #         volume += abs(trade.quantity)

            # if product in state.own_trades:
            #     own_trades = state.own_trades[product]
            #     for trade in own_trades:
            #         volume += abs(trade.quantity)

            if product in state.position:
                position = state.position[product]
            else:
                position = 0
            
            order_depth: OrderDepth = state.order_depths[product]
            
            orders: List[Order] = []
            
            buy_orders = order_depth.buy_orders
            buy_order_prices = sorted(buy_orders.keys())
            buy_order_price = buy_order_prices[0]
            
            sell_orders = order_depth.sell_orders
            sell_order_prices = sorted(sell_orders.keys())
            sell_order_price = sell_order_prices[0]
 
            limit_width = 20

            buy_order_price += 1
            sell_order_price -= 1

            # if the absolute value of position is equal to the limit width we'll offer better prices
            if position > 0:
                buy_order_price += 2
            
            if position < 0:
                sell_order_price -= 2

            sell_quantity = -limit_width - position
            orders.append(Order(product, sell_order_price, sell_quantity))

            buy_quantity = limit_width - position
            orders.append(Order(product, buy_order_price, buy_quantity))

            result[product] = orders

        # for product in positions_hash we'll put the product name and position count in the traderData string    
        traderData = ""
        conversions = 0
        return result, conversions, traderData