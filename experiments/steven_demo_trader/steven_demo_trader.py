from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))
        
        # Orders to be placed on exchange matching engine
        result = {}
        for product in state.order_depths:
            order_depth: OrderDepth = state.order_depths[product]
            if product in state.position.keys ():
                position = state.position[product]
            else:
                position = 0
            
            base_price = {"AMETHYSTS" : 10000, "STARFRUIT" : 5000}[product]
            
            print(product + " position: " + str(position))
            orders: List[Order] = []
            # acceptable_price = 10  # Participant should calculate this value
            # print("Acceptable price : " + str(acceptable_price))
            print("Buy Order depth : " + str(len(order_depth.buy_orders)) + ", Sell order depth : " + str(len(order_depth.sell_orders)))
            
            
            
            best_current_sell_price = list(order_depth.sell_orders.keys())[0]
            best_current_buy_price = list(order_depth.buy_orders.keys())[0]
            
            try_hard_to_sell_price = best_current_buy_price
            try_to_sell_price = best_current_buy_price + 2
            try_hard_to_buy_price = best_current_sell_price 
            try_to_buy_price = best_current_sell_price - 1
            
            buy_sell_price_diff = best_current_sell_price - best_current_buy_price
            seventy_pct_of_price_diff = buy_sell_price_diff * 0.7
            
            
            if len(order_depth.sell_orders) != 0:
                # best_ask, best_ask_amount = list(order_depth.sell_orders.items())[0]
                # if int(best_ask) < acceptable_price:
                #     print("BUY", str(-best_ask_amount) + "x", best_ask)
                #     orders.append(Order(product, best_ask, -best_ask_amount))
    
                if position < -19:
                    # try hard to sell more
                    print("BUY " + str(product), str(try_hard_to_buy_price) + "x", "1")
                    buy_price, buy_quantity = [try_hard_to_buy_price, 1]
                    orders.append(Order(product, buy_price, -buy_quantity))
                
                elif position < -15:
                    # try to sell more
                    print("BUY " + str(product), str(try_to_buy_price) + "x", "1")
                    buy_price, buy_quantity = [try_to_buy_price, 1]
                    orders.append(Order(product, buy_price, -buy_quantity))
                
                elif (position < 0) and (seventy_pct_of_price_diff > 0):
                    acceptable_price = best_current_sell_price - int( seventy_pct_of_price_diff )
                    how_many = -int(position / 2)
                    print("BUY " + str(product), str(acceptable_price) + "x", str(how_many))
                    buy_price, buy_quantity = [acceptable_price, how_many]
                    orders.append(Order(product, buy_price, -buy_quantity))
                    
                elif position < 15:
                    # sell if great price
                    good_price = best_current_sell_price - 2
                    print("BUY " + str(product), str(good_price) + "x", "1")
                    buy_price, buy_quantity = [good_price, 3]
                    orders.append(Order(product, buy_price, -buy_quantity))
                    
                elif position < 20:
                    # sell if great price
                    great_price = best_current_sell_price - 4
                    print("BUY " + str(product), str(great_price) + "x", "1")
                    buy_price, buy_quantity = [great_price, 1]
                    orders.append(Order(product, buy_price, -buy_quantity))
                    
            if len(order_depth.buy_orders) != 0:
                # best_bid, best_bid_amount = list(order_depth.buy_orders.items())[0]
                # if int(best_bid) > acceptable_price:
                #     print("SELL", str(best_bid_amount) + "x", best_bid)
                #     orders.append(Order(product, best_bid, -best_bid_amount))
            
                if position > 19:
                    # try hard to sell more
                    print("SELL " + str(product), str(try_hard_to_sell_price) + "x", "1")
                    sell_price, sell_quantity = [try_hard_to_sell_price, 1]
                    orders.append(Order(product, sell_price, -sell_quantity))
                    
                elif position > 15:
                    # try to sell more
                    print("SELL " + str(product), str(try_to_sell_price) + "x", "1")
                    sell_price, sell_quantity = [try_to_sell_price, 1]
                    orders.append(Order(product, sell_price, -sell_quantity))
                    
                elif (position > 0) and (seventy_pct_of_price_diff > 0):
                    acceptable_price = best_current_buy_price + int( seventy_pct_of_price_diff )
                    how_many = int(position / 2)
                    print("SELL " + str(product), str(acceptable_price) + "x", str(how_many))
                    sell_price, sell_quantity = [acceptable_price, how_many]
                    orders.append(Order(product, sell_price, -sell_quantity))
                    
                elif position > -15:
                    # sell if great price
                    good_price = best_current_buy_price + 2
                    print("SELL " + str(product), str(good_price) + "x", "1")
                    sell_price, sell_quantity = [good_price, 3]
                    orders.append(Order(product, sell_price, -sell_quantity))
                
                elif position > -20:
                    # sell if great price
                    great_price = best_current_buy_price + 4
                    print("SELL " + str(product), str(great_price) + "x", "1")
                    sell_price, sell_quantity = [great_price, 1]
                    orders.append(Order(product, sell_price, -sell_quantity))
                
                    
            result[product] = orders
    
		    # String value holding Trader state data required. 
				# It will be delivered as TradingState.traderData on next execution.
        traderData = "SAMPLE" 
        
				# Sample conversion request. Check more details below. 
        conversions = 1
        return result, conversions, traderData
