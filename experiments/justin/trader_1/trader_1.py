from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    def run(self, state: TradingState):
        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            # find the volume of trades for this product
            # see if this product is in the market_trades keys
            if product not in state.market_trades:
                print("product not in market_trades keys. volume = 0.")
                volume = 0
            else:
                market_trades = state.market_trades[product]
                volume = 0
                for trade in market_trades:
                    volume += trade.quantity
                print("product in market_trades keys. volume = sum of trade quantities = " + str(volume))

            if product in state.position:
                position = state.position[product]
                print("product in position keys. position = " + str(position))
            else:
                print("product not in position keys. position = 0.")
                position = 0

            order_depth: OrderDepth = state.order_depths[product]
            
            orders: List[Order] = []
            
            # first we'll do our sell orders.
            # we'll see what the order depth is for the buy orders in the market
            buy_orders = order_depth.buy_orders
            print("buy_orders count = " + str(len(buy_orders)))
            # sort the buy orders by price, and then find the price where the total quantity is greater than the volume of trades
            buy_order_prices = sorted(buy_orders.keys())
            buy_order_prices.reverse()
            print("buy_order_prices = " + str(buy_order_prices))
            buy_order_quantity = 0
            buy_order_price = 0
            max_buy_order_price = 0
            for price in buy_order_prices:
                if price > max_buy_order_price:
                    max_buy_order_price = price
                buy_order_quantity += buy_orders[price]
                if buy_order_quantity > volume:
                    buy_order_price = price
                    print("buy order price = " + str(buy_order_price))
                    break
            
            if buy_order_price == 0:
                buy_order_price = max_buy_order_price + 1
                print("buy order price = " + str(buy_order_price))
            
            # do the same for the sell orders
            sell_orders = order_depth.sell_orders
            print("sell_orders count = " + str(len(sell_orders)))
            sell_order_prices = sorted(sell_orders.keys())
            print("sell_order_prices = " + str(sell_order_prices))
            sell_order_quantity = 0
            sell_order_price = 0
            max_sell_order_price = 0
            for price in sell_order_prices:
                if price > max_sell_order_price:
                    max_sell_order_price = price
                sell_order_quantity += sell_orders[price]
                if sell_order_quantity > volume:
                    sell_order_price = price
                    print("sell order price = " + str(sell_order_price))
                    break
            
            if sell_order_price == 0:
                sell_order_price = max_sell_order_price - 1
                print("sell order price = " + str(sell_order_price))
            
            # now we will place orders at the buy_order_price and sell_order_price
            # we will attempt to max out our position in each direction

            # first we'll do the sell orders
            sell_quantity = -20 - position
            print("sell_quantity = " + str(sell_quantity))
            orders.append(Order(product, sell_order_price, sell_quantity))

            # now we'll do the buy orders
            buy_quantity = 20 - position
            print("buy_quantity = " + str(buy_quantity))
            orders.append(Order(product, buy_order_price, buy_quantity))

            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 0
        return result, conversions, traderData