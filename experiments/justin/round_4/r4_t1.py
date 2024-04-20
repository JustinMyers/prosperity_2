from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle

class CoconutTrader:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths["COCONUT"]
        coconut_buy_orders = order_depth.buy_orders
        coconut_buy_order_prices = sorted(coconut_buy_orders.keys())
        coconut_lowest_buy_order_price = coconut_buy_order_prices[0]
        coconut_highest_buy_order_price = coconut_buy_order_prices[-1]
        coconut_sell_orders = order_depth.sell_orders
        coconut_sell_order_prices = sorted(coconut_sell_orders.keys())
        coconut_lowest_sell_order_price = coconut_sell_order_prices[0]
        coconut_highest_sell_order_price = coconut_sell_order_prices[-1]
        coconut_mid_price = int((coconut_highest_buy_order_price + coconut_lowest_sell_order_price) / 2)

        data["prev_coconut_prices"].append(coconut_mid_price)

        order_depth: OrderDepth = state.order_depths["COCONUT_COUPON"]
        coconut_coupon_buy_orders = order_depth.buy_orders
        coconut_coupon_buy_order_prices = sorted(coconut_coupon_buy_orders.keys())
        coconut_coupon_lowest_buy_order_price = coconut_coupon_buy_order_prices[0]
        coconut_coupon_highest_buy_order_price = coconut_coupon_buy_order_prices[-1]
        coconut_coupon_sell_orders = order_depth.sell_orders
        coconut_coupon_sell_order_prices = sorted(coconut_coupon_sell_orders.keys())
        coconut_coupon_lowest_sell_order_price = coconut_coupon_sell_order_prices[0]
        coconut_coupon_highest_sell_order_price = coconut_coupon_sell_order_prices[-1]
        coconut_coupon_mid_price = int((coconut_coupon_highest_buy_order_price + coconut_coupon_lowest_sell_order_price) / 2)

        data["prev_coconut_coupon_prices"].append(coconut_coupon_mid_price)

        coconut_limit_width = 300
        coconut_coupon_limit_width = 600

        orders = {
            "COCONUT": [],
            "COCONUT_COUPON": []
        }

        coconut_position = state.position["COCONUT"] if "COCONUT" in state.position else 0
        coconut_coupon_position = state.position["COCONUT_COUPON"] if "COCONUT_COUPON" in state.position else 0

        certain_coconut_price = 10000
        coconut_excess_price = coconut_mid_price - certain_coconut_price

        coconut_spread = 0
        coupon_spread = 0

        if coconut_excess_price * 100 > coconut_coupon_mid_price:
            orders["COCONUT_COUPON"].append(Order("COCONUT_COUPON", coconut_coupon_mid_price - coupon_spread, coconut_coupon_limit_width - coconut_coupon_position))
        else:
            orders["COCONUT_COUPON"].append(Order("COCONUT_COUPON", coconut_coupon_mid_price + coupon_spread, -coconut_coupon_limit_width - coconut_coupon_position))

        coupon_lookback_period = 70
        coupon_lookback_width = 5
        lb_max = coupon_lookback_period + coupon_lookback_width
        lb_min = coupon_lookback_period - coupon_lookback_width

        if len(data["prev_coconut_coupon_prices"]) > lb_max:
            if coconut_coupon_mid_price < (sum(data["prev_coconut_coupon_prices"][-lb_max:-lb_min]) / (coupon_lookback_width * 2)):
                orders["COCONUT"].append(Order("COCONUT", coconut_mid_price + coconut_spread, -coconut_limit_width - coconut_position))
            else:
                orders["COCONUT"].append(Order("COCONUT", coconut_mid_price - coconut_spread, coconut_limit_width - coconut_position))

        return orders, 0, data

class BasketTrader:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths["GIFT_BASKET"]
        gift_basket_buy_orders = order_depth.buy_orders
        gift_basket_buy_order_prices = sorted(gift_basket_buy_orders.keys())
        gift_basket_highest_buy_order_price = gift_basket_buy_order_prices[-1]
        gift_basket_sell_orders = order_depth.sell_orders
        gift_basket_sell_order_prices = sorted(gift_basket_sell_orders.keys())
        gift_basket_lowest_sell_order_price = gift_basket_sell_order_prices[0]
        gift_basket_mid_price = int((gift_basket_highest_buy_order_price + gift_basket_lowest_sell_order_price) / 2)

        order_depth: OrderDepth = state.order_depths["CHOCOLATE"]
        chocolate_buy_orders = order_depth.buy_orders
        chocolate_buy_order_prices = sorted(chocolate_buy_orders.keys())
        chocolate_highest_buy_order_price = chocolate_buy_order_prices[-1]
        chocolate_sell_orders = order_depth.sell_orders
        chocolate_sell_order_prices = sorted(chocolate_sell_orders.keys())
        chocolate_lowest_sell_order_price = chocolate_sell_order_prices[0]
        chocolate_mid_price = int((chocolate_highest_buy_order_price + chocolate_lowest_sell_order_price) / 2)

        order_depth: OrderDepth = state.order_depths["STRAWBERRIES"]
        strawberries_buy_orders = order_depth.buy_orders
        strawberries_buy_order_prices = sorted(strawberries_buy_orders.keys())
        strawberries_highest_buy_order_price = strawberries_buy_order_prices[-1]
        strawberries_sell_orders = order_depth.sell_orders
        strawberries_sell_order_prices = sorted(strawberries_sell_orders.keys())
        strawberries_lowest_sell_order_price = strawberries_sell_order_prices[0]
        strawberries_mid_price = int((strawberries_highest_buy_order_price + strawberries_lowest_sell_order_price) / 2)

        order_depth: OrderDepth = state.order_depths["ROSES"]
        roses_buy_orders = order_depth.buy_orders
        roses_buy_order_prices = sorted(roses_buy_orders.keys())
        roses_highest_buy_order_price = roses_buy_order_prices[-1]
        roses_sell_orders = order_depth.sell_orders
        roses_sell_order_prices = sorted(roses_sell_orders.keys())
        roses_lowest_sell_order_price = roses_sell_order_prices[0]
        roses_mid_price = int((roses_highest_buy_order_price + roses_lowest_sell_order_price) / 2)

        sum_of_basket_products = chocolate_mid_price * 4 + strawberries_mid_price * 6 + roses_mid_price        
        data["GIFT_BASKET"]["prev_sums_of_basket_products"].append(sum_of_basket_products)

        orders = {
            "CHOCOLATE": [],
            "STRAWBERRIES": [],
            "ROSES": [],
            "GIFT_BASKET": []
        }

        gift_basket_limit_width = 60

        price_modifier = 5

        gift_basket_position = state.position["GIFT_BASKET"] if "GIFT_BASKET" in state.position else 0

        magical_ratio = 1.005861

        avg_of_last_three_basket_ratios = sum(data["GIFT_BASKET"]["prev_sums_of_basket_products"][-3:]) / 3

        magical_basket_price_target = int(avg_of_last_three_basket_ratios * magical_ratio)

        if len(data["GIFT_BASKET"]["prev_sums_of_basket_products"]) > 3:
            orders["GIFT_BASKET"].append(Order("GIFT_BASKET", magical_basket_price_target + price_modifier, -gift_basket_limit_width - gift_basket_position))
            orders["GIFT_BASKET"].append(Order("GIFT_BASKET", magical_basket_price_target - price_modifier, gift_basket_limit_width - gift_basket_position))

        return orders, 0, data

class AmethystTrader:
    def run(self, state: TradingState, product: str, data: dict):
        orders: List[Order] = []

        position = state.position[product] if product in state.position else 0

        limit_width = 20

        orders: List[Order] = []

        sell_quantity = -limit_width - position
        orders.append(Order(product, 10002, sell_quantity))
        buy_quantity = limit_width - position
        orders.append(Order(product, 9998, buy_quantity))

        return orders, 0, data

class StarfruitTrader:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths[product]

        orders: List[Order] = []

        position = state.position[product] if product in state.position else 0

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

        sell_quantity = -limit_width - position
        orders.append(Order(product, sell_order_price, sell_quantity))

        buy_quantity = limit_width - position
        orders.append(Order(product, buy_order_price, buy_quantity))

        return orders, 0, data

class OrchidTrader:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths[product]
        
        orders: List[Order] = []

        position = state.position[product] if product in state.position else 0

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

        mid_price = int((highest_buy_order_price + lowest_sell_order_price) / 2)

        limit_width = 100

        print(f"Position: {position}, Cost of Import: {cost_of_import}, Cost of Export: {cost_of_export}")
        print(f"Lowest Sell: {lowest_sell_order_price}, Highest Buy: {highest_buy_order_price}")

        conversions = -position

        if cost_of_import < mid_price - 1:
            orders.append(Order(product, mid_price - 1, -limit_width))
        elif cost_of_export > mid_price + 1:
            orders.append(Order(product, mid_price + 1, limit_width))

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
                    "convert": False
                },
                "BASKET": {
                    "CHOCOLATE": {
                        "prev_weights": [],
                        "prev_prices": []
                    },
                    "STRAWBERRIES": {
                        "prev_weights": [],
                        "prev_prices": []
                    },
                    "ROSES": {
                        "prev_weights": [],
                        "prev_prices": []
                    },
                    "GIFT_BASKET": {
                        "prev_prices": [],
                        "prev_sums_of_basket_products": [],
                        "prev_basket_ratios": []
                    },
                },
                "COCONUT": {
                    "prev_coconut_prices": [],
                    "prev_coconut_coupon_prices": []
                }
            }

        conversions = 0

        # for product in state.order_depths:
        #     if product == "ORCHIDS":
        #         trader = OrchidTrader()
        #         result[product], orchid_conversions, traderData[product] = trader.run(state, product, traderData[product])
        #         conversions += orchid_conversions
        #     elif product == "AMETHYSTS":
        #         trader = AmethystTrader()
        #         result[product], amethyst_conversions, traderData[product] = trader.run(state, product, traderData[product])
        #     elif product == "STARFRUIT":
        #         trader = StarfruitTrader()
        #         result[product], starfruit_conversions, traderData[product] = trader.run(state, product, traderData[product])
        
        # basket_trader = BasketTrader()
        # basket_result, basket_conversions, traderData["BASKET"] = basket_trader.run(state, "BASKET", traderData["BASKET"])
        # result["CHOCOLATE"] = basket_result["CHOCOLATE"]
        # result["STRAWBERRIES"] = basket_result["STRAWBERRIES"]
        # result["ROSES"] = basket_result["ROSES"]
        # result["GIFT_BASKET"] = basket_result["GIFT_BASKET"]

        coconut_trader = CoconutTrader()
        coconut_result, coconut_conversions, traderData["COCONUT"] = coconut_trader.run(state, "COCONUT", traderData["COCONUT"])
        result["COCONUT"] = coconut_result["COCONUT"]
        result["COCONUT_COUPON"] = coconut_result["COCONUT_COUPON"]

        traderData = jsonpickle.encode(traderData)
        return result, conversions, traderData