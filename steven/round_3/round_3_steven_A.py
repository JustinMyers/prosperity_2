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

class ItemTrader:
    def run(self, state: TradingState, product: str, data: dict, limit_width_dict: dict):
        order_depth: OrderDepth = state.order_depths[product]

        orders: List[Order] = []

        position = state.position[product] if product in state.position else 0

        # limit_width = 20
        limit_width = limit_width_dict[product]

        orders: List[Order] = []

        buy_orders = order_depth.buy_orders
        buy_order_prices = sorted(buy_orders.keys())
        buy_order_price = buy_order_prices[0]
        buy_order_price += 1
        
        sell_orders = order_depth.sell_orders
        sell_order_prices = sorted(sell_orders.keys(), reverse=True)
        sell_order_price = sell_order_prices[0]
        sell_order_price -= 1

        sell_quantity = -limit_width - position
        orders.append(Order(product, sell_order_price, sell_quantity))

        buy_quantity = limit_width - position
        orders.append(Order(product, buy_order_price, buy_quantity))

        return orders, 0, data

class BasketTrader:
    def run(self, state: TradingState, product: str, data: dict, limit_width_dict: dict):
        order_depth: OrderDepth = state.order_depths[product]

        orders: List[Order] = []

        position = state.position[product] if product in state.position else 0

        # limit_width = 20
        limit_width = limit_width_dict[product]

        orders: List[Order] = []

        buy_orders = order_depth.buy_orders
        buy_order_prices = sorted(buy_orders.keys())
        buy_order_price = buy_order_prices[0]
        buy_order_price += 1
        
        sell_orders = order_depth.sell_orders
        sell_order_prices = sorted(sell_orders.keys(), reverse=True)
        sell_order_price = sell_order_prices[0]
        sell_order_price -= 1

        sell_quantity = -limit_width - position
        orders.append(Order(product, sell_order_price, sell_quantity))

        buy_quantity = limit_width - position
        orders.append(Order(product, buy_order_price, buy_quantity))

        return orders, 0, data

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

        limit_width_dict = {"CHOCOLATE": 250, "STRAWBERRIES": 350, "ROSES": 60, "GIFT_BASKET": 60}

        for product in state.order_depths:
            
            print("TRADER_LOG  product:", product, "order_depths:", state.order_depths[product])
            
            # if product == "ORCHIDS":
            #     trader = OrchidTrader()
            #     result[product], orchid_conversions, traderData[product] = trader.run(state, product, traderData[product])
            #     conversions += orchid_conversions
            # elif product == "AMETHYSTS":
            #     trader = AmethystTrader()
            #     result[product], amethyst_conversions, traderData[product] = trader.run(state, product, traderData[product])
            # elif product == "STARFRUIT":
            #     trader = StarfruitTrader()
            #     result[product], starfruit_conversions, traderData[product] = trader.run(state, product, traderData[product])
            if product in ["CHOCOLATE", "STRAWBERRIES", "ROSES"]:
                trader = ItemTrader()
                result[product], orchid_conversions, traderData[product] = trader.run(state, product, traderData[product], limit_width_dict)
                conversions += orchid_conversions
            elif product == "GIFT_BASKET":
                trader = BasketTrader()
                result[product], amethyst_conversions, traderData[product] = trader.run(state, product, traderData[product], limit_width_dict)


        traderData = jsonpickle.encode(traderData)
        return result, conversions, traderData