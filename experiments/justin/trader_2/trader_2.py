from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List

class Trader:    
    def run(self, state: TradingState):
        result = {}
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
            buy_order_price += 1
            
            sell_orders = order_depth.sell_orders
            sell_order_prices = sorted(sell_orders.keys())
            sell_order_price = sell_order_prices[0]
            sell_order_price -= 1

            sell_quantity = -20 - position
            orders.append(Order(product, sell_order_price, sell_quantity))

            buy_quantity = 20 - position
            orders.append(Order(product, buy_order_price, buy_quantity))

            result[product] = orders
    
        traderData = "SAMPLE"         
        conversions = 0
        return result, conversions, traderData