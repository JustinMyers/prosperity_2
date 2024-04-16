from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle

# class AmethystTrader:
#     def run(self, state: TradingState, product: str, data: dict):
#         orders: List[Order] = []

#         position = state.position[product] if product in state.position else 0

#         limit_width = 20

#         orders: List[Order] = []

#         sell_quantity = -limit_width - position
#         orders.append(Order(product, 10002, sell_quantity))
#         buy_quantity = limit_width - position
#         orders.append(Order(product, 9998, buy_quantity))

#         return orders, 0, data

# class StarfruitTrader:
#     def run(self, state: TradingState, product: str, data: dict):
#         order_depth: OrderDepth = state.order_depths[product]

#         orders: List[Order] = []

#         position = state.position[product] if product in state.position else 0

#         limit_width = 20

#         orders: List[Order] = []

#         buy_orders = order_depth.buy_orders
#         buy_order_prices = sorted(buy_orders.keys())
#         buy_order_price = buy_order_prices[0]
#         buy_order_price += 1
        
#         sell_orders = order_depth.sell_orders
#         sell_order_prices = sorted(sell_orders.keys(), reverse=True)
#         sell_order_price = sell_order_prices[0]
#         sell_order_price -= 1

#         sell_quantity = -limit_width - position
#         orders.append(Order(product, sell_order_price, sell_quantity))

#         buy_quantity = limit_width - position
#         orders.append(Order(product, buy_order_price, buy_quantity))

#         return orders, 0, data

# class OrchidTrader:
#     def run(self, state: TradingState, product: str, data: dict):
#         order_depth: OrderDepth = state.order_depths[product]
        
#         orders: List[Order] = []

#         position = state.position[product] if product in state.position else 0

#         # sunlight = state.observations.conversionObservations["ORCHIDS"].sunlight
#         # humidity = state.observations.conversionObservations["ORCHIDS"].humidity
#         bidPrice = state.observations.conversionObservations["ORCHIDS"].bidPrice
#         askPrice = state.observations.conversionObservations["ORCHIDS"].askPrice
#         transportFees = state.observations.conversionObservations["ORCHIDS"].transportFees
#         exportTariff = state.observations.conversionObservations["ORCHIDS"].exportTariff
#         importTariff =  state.observations.conversionObservations["ORCHIDS"].importTariff

#         cost_of_import = int(askPrice + transportFees + importTariff)
#         cost_of_export = int(bidPrice - transportFees - exportTariff)

#         buy_orders = order_depth.buy_orders
#         buy_order_prices = sorted(buy_orders.keys())
#         lowest_buy_order_price = buy_order_prices[0]
#         highest_buy_order_price = buy_order_prices[-1]
        
#         sell_orders = order_depth.sell_orders
#         sell_order_prices = sorted(sell_orders.keys())
#         lowest_sell_order_price = sell_order_prices[0]
#         highest_sell_order_price = sell_order_prices[-1]

#         mid_price = int((highest_buy_order_price + lowest_sell_order_price) / 2)

#         limit_width = 100

#         print(f"Position: {position}, Cost of Import: {cost_of_import}, Cost of Export: {cost_of_export}")
#         print(f"Lowest Sell: {lowest_sell_order_price}, Highest Buy: {highest_buy_order_price}")

#         orders.append(Order(product, mid_price - 1, -limit_width))
#         conversions = -position

#         # sunlight_delta = sunlight - data.get("prev_sunlight", 0)
#         # humidity_delta = humidity - data.get("prev_humidity", 0)

#         # data["prev_sunlight"] = sunlight
#         # data["prev_humidity"] = humidity
#         # data["prev_sunlight_delta"] = sunlight_delta
#         # data["prev_humidity_delta"] = humidity_delta
       
#         return orders, conversions, data

# class ItemTrader:
#     def run(self, state: TradingState, product: str, data: dict):
#         order_depth: OrderDepth = state.order_depths[product]

#         orders: List[Order] = []

#         position = state.position[product] if product in state.position else 0

#         limit_width = 20

#         orders: List[Order] = []

#         buy_orders = order_depth.buy_orders
#         buy_order_prices = sorted(buy_orders.keys())
#         buy_order_price = buy_order_prices[0]
#         buy_order_price += 1
        
#         sell_orders = order_depth.sell_orders
#         sell_order_prices = sorted(sell_orders.keys(), reverse=True)
#         sell_order_price = sell_order_prices[0]
#         sell_order_price -= 1

#         sell_quantity = -limit_width - position
#         orders.append(Order(product, sell_order_price, sell_quantity))

#         buy_quantity = limit_width - position
#         orders.append(Order(product, buy_order_price, buy_quantity))

#         return orders, 0, data

class BasketTrader:
    def run(self, state: TradingState):
        
        result = []
        
        
                
#         # class TradingState(object):
#         # def __init__(self,
#         #             traderData: str,
#         #             timestamp: Time,
#         #             listings: Dict[Symbol, Listing],
#         #             order_depths: Dict[Symbol, OrderDepth],
#         #             own_trades: Dict[Symbol, List[Trade]],
#         #             market_trades: Dict[Symbol, List[Trade]],
#         #             position: Dict[Product, Position],
#         #             observations: Observation):
#         #     self.traderData = traderData
#         #     self.timestamp = timestamp
#         #     self.listings = listings
#         #     self.order_depths = order_depths
#         #     self.own_trades = own_trades
#         #     self.market_trades = market_trades
#         #     self.position = position
#         #     self.observations = observations
        
        timestamp = state.timestamp
        timestamp_str = str(timestamp)
        
        print("TRADER_LOG:"+timestamp_str+"  "+"traderData: " + str(state.traderData))
        print("TRADER_LOG:"+timestamp_str+"  "+"listings: " + str(state.listings))
        # for pname in ["AMETHYSTS", "STARFRUIT", "ORCHIDS"]:
        for pname in ["CHOCOLATE", "STRAWBERRIES", "ROSES", "GIFT_BASKET"]:
            # print("TRADER_LOG:"+timestamp_str+"  "+"order_depths: " + pname +": " + str(state.order_depths[pname]))
            print("TRADER_LOG:"+timestamp_str+"  "+"order_depths: " + pname +": " + "buy_orders:" +": " + str(state.order_depths[pname].buy_orders))
            print("TRADER_LOG:"+timestamp_str+"  "+"order_depths: " + pname +": " + "sell_orders:" +": " + str(state.order_depths[pname].sell_orders))
        print("TRADER_LOG:"+timestamp_str+"  "+"own_trades: " + str(state.own_trades))
        print("TRADER_LOG:"+timestamp_str+"  "+"market_trades: " + str(state.market_trades))
        print("TRADER_LOG:"+timestamp_str+"  "+"position: " + str(state.position))
        print("TRADER_LOG:"+timestamp_str+"  "+"Observations: " + str(state.observations))
        
        
        
        
        
        
        
        
        
        def simple_buy_order_price(order_depth):
            buy_orders = order_depth.buy_orders
            buy_order_prices = sorted(buy_orders.keys())
            buy_order_price = buy_order_prices[0]
            buy_order_price += 1
            return buy_order_price
        
        def simple_sell_order_price(order_depth):
            sell_orders = order_depth.sell_orders
            sell_order_prices = sorted(sell_orders.keys(), reverse=True)
            sell_order_price = sell_order_prices[0]
            sell_order_price -= 1
            return sell_order_price

        def add_gb_component_prices(chocolate_price: int, strawberries_price: int, roses_price: int):
            gift_basket_price = (4 * chocolate_price) + (6 * strawberries_price) + roses_price
            return gift_basket_price
        
        def get_positions(state_position: dict):
            position_dict = {}
            position_dict["chocolate_position"] = state.position["CHOCOLATE"] if "CHOCOLATE" in state.position else 0
            position_dict["strawberries_position"] = state.position["STRAWBERRIES"] if "STRAWBERRIES" in state.position else 0
            position_dict["roses_position"] = state.position["ROSES"] if "ROSES" in state.position else 0
            position_dict["gb_position"] = state.position["GIFT_BASKET"] if "GIFT_BASKET" in state.position else 0

            # position_limits = {"CHOCOLATE": 250, "STRAWBERRIES": 350, "ROSES": 60, "GIFT_BASKET": 60}
            # maybe because int(350 / 6) is 58, GIFT_BASKET limit is 58
            position_limits = {"CHOCOLATE": 250, "STRAWBERRIES": 350, "ROSES": 60, "GIFT_BASKET": 60}
            position_dict["chocolate_limit"] = position_limits["CHOCOLATE"]
            position_dict["strawberries_limit"] = position_limits["STRAWBERRIES"]
            position_dict["roses_limit"] = position_limits["ROSES"]
            position_dict["gb_limit"] = position_limits["GIFT_BASKET"]
            
            gb_chocolate_position = int(position_dict["chocolate_position"] / 4)
            gb_strawberries_position = int(position_dict["strawberries_position"] / 4)
            gb_roses_position = int(position_dict["roses_position"] / 4)
            
            gb_min_neg_comp_position = min(gb_chocolate_position, gb_strawberries_position, gb_roses_position)
            position_dict["gb_min_neg_position"] = max(-58, gb_min_neg_comp_position)
            gb_max_pos_comp_position = min(gb_chocolate_position, gb_strawberries_position, gb_roses_position)
            position_dict["gb_max_pos_position"] = max(58, gb_max_pos_comp_position)
            
            return position_dict
        
        # ["CHOCOLATE", "STRAWBERRIES", "ROSES"]
        chocolate_order_depth: OrderDepth    = state.order_depths["CHOCOLATE"]
        strawberries_order_depth: OrderDepth = state.order_depths["STRAWBERRIES"]
        roses_order_depth: OrderDepth        = state.order_depths["ROSES"]
        
        chocolate_buy_order_price    = simple_buy_order_price(chocolate_order_depth)
        strawberries_buy_order_price = simple_buy_order_price(strawberries_order_depth)
        roses_buy_order_price        = simple_buy_order_price(roses_order_depth)
        
        gb_components_buy_order_price = add_gb_component_prices(chocolate_buy_order_price, strawberries_buy_order_price, roses_buy_order_price)
        
        chocolate_sell_order_price    = simple_sell_order_price(chocolate_order_depth)
        strawberries_sell_order_price = simple_sell_order_price(strawberries_order_depth)
        roses_sell_order_price        = simple_sell_order_price(roses_order_depth)
        
        gb_components_sell_order_price = add_gb_component_prices(chocolate_sell_order_price, strawberries_sell_order_price, roses_sell_order_price)
        
        
        
        # if product in state.position gb_position = state.position[product] else 0
        position_dict = get_positions(state.position)
        
    
        chocolate_position = position_dict["chocolate_position"]
        strawberries_position = position_dict["strawberries_position"]
        roses_position = position_dict["roses_position"]
        gb_position = position_dict["gb_position"]
        chocolate_limit = position_dict["chocolate_limit"]
        strawberries_limit = position_dict["strawberries_limit"]
        roses_limit = position_dict["roses_limit"]
        gb_limit = position_dict["gb_limit"]
        gb_min_neg_position = position_dict["gb_min_neg_position"]
        gb_max_pos_position = position_dict["gb_max_pos_position"]
        
        # limit_width = 20

        print("TRADER_LOG:"+timestamp_str+"  "+"chocolate_limit: " + str(chocolate_limit))
        print("TRADER_LOG:"+timestamp_str+"  "+"strawberries_limit: " + str(strawberries_limit))
        print("TRADER_LOG:"+timestamp_str+"  "+"roses_limit: " + str(roses_limit))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_limit: " + str(gb_limit))

        order_depth: OrderDepth = state.order_depths["GIFT_BASKET"]

        # orders: List[Order] = []
        chocolate_orders: List[Order] = []
        strawberries_orders: List[Order] = []
        roses_orders: List[Order] = []
        gb_orders: List[Order] = []
        

        # buy_orders = order_depth.buy_orders
        # buy_order_prices = sorted(buy_orders.keys())
        # buy_order_price = buy_order_prices[0]
        # buy_order_price += 1
        gb_buy_order_price = simple_buy_order_price(order_depth)
    
        # sell_orders = order_depth.sell_orders
        # sell_order_prices = sorted(sell_orders.keys(), reverse=True)
        # sell_order_price = sell_order_prices[0]
        # sell_order_price -= 1
        gb_sell_order_price = simple_sell_order_price(order_depth)
        
        print("TRADER_LOG:"+timestamp_str+"  "+"chocolate_buy_order_price: " + str(chocolate_buy_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"strawberries_buy_order_price: " + str(strawberries_buy_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"roses_buy_order_price: " + str(roses_buy_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_components_buy_order_price: " + str(gb_components_buy_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_buy_order_price: " + str(gb_buy_order_price))

        print("TRADER_LOG:"+timestamp_str+"  "+"chocolate_sell_order_price: " + str(chocolate_sell_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"strawberries_sell_order_price: " + str(strawberries_sell_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"roses_sell_order_price: " + str(roses_sell_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_components_sell_order_price: " + str(gb_components_sell_order_price))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_sell_order_price: " + str(gb_sell_order_price))

        print("TRADER_LOG:"+timestamp_str+"  "+"chocolate_position: " + str(chocolate_position))
        print("TRADER_LOG:"+timestamp_str+"  "+"strawberries_position: " + str(strawberries_position))
        print("TRADER_LOG:"+timestamp_str+"  "+"roses_position: " + str(roses_position))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_position: " + str(gb_position))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_min_neg_position: " + str(gb_min_neg_position))
        print("TRADER_LOG:"+timestamp_str+"  "+"gb_max_pos_position: " + str(gb_max_pos_position))

        if gb_buy_order_price < gb_components_buy_order_price:
            gb_buy_order_price = gb_buy_order_price
            # gb_buy_quantity = limit_width - gb_position
            gb_buy_quantity = gb_min_neg_position - gb_position
            gb_orders.append(Order("GIFT_BASKET", gb_buy_order_price, gb_buy_quantity))
        else:
            # buy_quantity = limit_width - position
            # orders.append(Order(product, buy_order_price, buy_quantity))
            chocolate_buy_quantity = chocolate_limit - chocolate_position
            chocolate_orders.append(Order("CHOCOLATE", chocolate_buy_order_price, chocolate_buy_quantity))
            strawberries_buy_quantity = strawberries_limit - strawberries_position
            strawberries_orders.append(Order("STRAWBERRIES", strawberries_buy_order_price, strawberries_buy_quantity))
            roses_buy_quantity = roses_limit - roses_position
            roses_orders.append(Order("ROSES", roses_buy_order_price, roses_buy_quantity))

        if gb_sell_order_price > gb_components_sell_order_price:
            gb_sell_order_price = gb_sell_order_price
            # gb_sell_quantity = -limit_width - gb_position
            gb_sell_quantity = -gb_max_pos_position - gb_position
            gb_orders.append(Order("GIFT_BASKET", gb_sell_order_price, gb_sell_quantity))
        else:
            # sell_quantity = -limit_width - position
            # orders.append(Order(product, sell_order_price, sell_quantity))
            chocolate_sell_quantity = -chocolate_limit - chocolate_position
            chocolate_orders.append(Order("CHOCOLATE", chocolate_sell_order_price, chocolate_sell_quantity))
            strawberries_sell_quantity = -strawberries_limit - strawberries_position
            strawberries_orders.append(Order("STRAWBERRIES", strawberries_sell_order_price, strawberries_sell_quantity))
            roses_sell_quantity = -roses_limit - roses_position
            roses_orders.append(Order("ROSES", roses_sell_order_price, roses_sell_quantity))

        result = {}
        result["CHOCOLATE"] = chocolate_orders
        result["STRAWBERRIES"] = strawberries_orders
        result["ROSES"] = roses_orders
        result["GIFT_BASKET"] = gb_orders
        
        # return orders, 0, data
        return result, 0

class Trader:    
    def run(self, state: TradingState):
        result = {}

        if state.traderData:
            traderData = jsonpickle.decode(state.traderData)
        else:
            traderData = {
                "CHOCOLATE": {
                    "worst_buy": None,
                    "best_buy": None,
                    "worst_sell": None,
                    "best_sell": None
                },
                "STRAWBERRIES": {
                },
                "ROSES": {
                },
                "GIFT_BASKET": {
                }
            }

        conversions = 0

        # for product in state.order_depths:
            
        #     print("TRADER_LOG  product:", product, "order_depths:", state.order_depths[product])
            
        #     # if product == "ORCHIDS":
        #     #     trader = OrchidTrader()
        #     #     result[product], orchid_conversions, traderData[product] = trader.run(state, product, traderData[product])
        #     #     conversions += orchid_conversions
        #     # elif product == "AMETHYSTS":
        #     #     trader = AmethystTrader()
        #     #     result[product], amethyst_conversions, traderData[product] = trader.run(state, product, traderData[product])
        #     # elif product == "STARFRUIT":
        #     #     trader = StarfruitTrader()
        #     #     result[product], starfruit_conversions, traderData[product] = trader.run(state, product, traderData[product])

        #     # if product in ["CHOCOLATE", "STRAWBERRIES", "ROSES"]:
        #     #     trader = ItemTrader()
        #     #     result[product], orchid_conversions, traderData[product] = trader.run(state, product, traderData[product])
        #     #     conversions += orchid_conversions
        #     if product == "GIFT_BASKET":
        #         trader = BasketTrader()
        #         result, basket_conversions, traderData = trader.run(state, product, traderData)

        timestamp = state.timestamp
        timestamp_str = str(timestamp)
        
        print("TRADER_LOG  main_loop  timestamp:", timestamp_str)

        trader = BasketTrader()
        result, basket_conversions = trader.run(state)
        
        traderData = jsonpickle.encode(traderData)
        return result, conversions, traderData