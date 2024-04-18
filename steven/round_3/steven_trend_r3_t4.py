from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle
from itertools import pairwise

def get_product_trend(tracking_list, mid_price):
    trend_size = 9
    tracking_list = tracking_list[-(trend_size -1):] + [mid_price]
    price_history = tracking_list
    # pct_change_limit = 0.01  # one percent per timestamp
    # pct_change_limit = 0.005  # half of one percent per timestamp
    # pct_change_limit = 0.001  # tenth of one percent per timestamp
    # pct_change_limit = 0.0001  # one hundreth of one percent per timestamp
    # pct_change_limit = 0.00005  # five thousandths of one percent per timestamp
    pct_change_limit = 0.00003  # three thousandths of one percent per timestamp
    if (len(price_history) >= trend_size):
        # https://stackoverflow.com/questions/5314241/difference-between-consecutive-elements-in-list
        price_differences = [y - x for x, y in pairwise(price_history)]
        # positive_count = len([num for num in price_differences if num >= 1])
        # negative_count = len([num for num in price_differences if num <= -1])
        # highest_price = sorted(price_history)[-1]
        lowest_price = sorted(price_history)[0]
        price_history_pct_diffs = [(x / lowest_price) for x in price_differences]
        average_diff = (sum(price_history_pct_diffs) / (trend_size -1))
        # percent_diff = average_diff / lowest_price
        trend_status = "FLAT"
        if (average_diff > pct_change_limit):
            trend_status = "UP"
        elif (average_diff < -pct_change_limit):
            trend_status = "DOWN"
        
        print ("trend_status, price_history, price_differences:  ", trend_status, price_history, price_differences)
        print ("trend_status, price_history_pct_diffs, average_diff:  ", trend_status, price_history_pct_diffs, average_diff)
        
    else:
        trend_status = "FLAT"
        print ("trend_status, NOT ENOUGH HISTORY:  ", trend_status)
        
    return tracking_list, trend_status

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

        data["GIFT_BASKET"]["tracking"], gb_trend = get_product_trend(data["GIFT_BASKET"]["tracking"], gift_basket_mid_price)
        data["CHOCOLATE"]["tracking"], chocolate_trend = get_product_trend(data["CHOCOLATE"]["tracking"], chocolate_mid_price)
        data["STRAWBERRIES"]["tracking"], strawberries_trend = get_product_trend(data["STRAWBERRIES"]["tracking"], strawberries_mid_price)
        data["ROSES"]["tracking"], roses_trend = get_product_trend(data["ROSES"]["tracking"], roses_mid_price)
        
        print("TRACKING_LOG", "GIFT_BASKET", gb_trend, data["GIFT_BASKET"]["tracking"])
        print("TRACKING_LOG", "CHOCOLATE", chocolate_trend, data["CHOCOLATE"]["tracking"])
        print("TRACKING_LOG", "STRAWBERRIES", strawberries_trend, data["STRAWBERRIES"]["tracking"])
        print("TRACKING_LOG", "ROSES", roses_trend, data["ROSES"]["tracking"])
        
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

        # data["tracking"] += [mid_price]  # AMETHYSTS mid price not useful
        # print("TRACKING_LOG", product, data["tracking"])
        
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

        highest_buy_order_price = buy_order_prices[-1]
        lowest_sell_order_price = sell_order_prices[0]
        mid_price = int((highest_buy_order_price + lowest_sell_order_price) / 2)
        data["tracking"], product_trend = get_product_trend(data["tracking"], mid_price)
        print("TRACKING_LOG", product, product_trend, data["tracking"])
        
        if (product_trend != "UP"):
            sell_quantity = -limit_width - position
            orders.append(Order(product, sell_order_price, sell_quantity))

        if (product_trend != "DOWN"):
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
        data["tracking"], product_trend = get_product_trend(data["tracking"], mid_price)
        print("TRACKING_LOG", product, product_trend, data["tracking"])

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
                    # "tracking": []  # AMETHYSTS mid price not useful
                },
                "STARFRUIT": {
                    "tracking": []
                },
                "ORCHIDS": {
                    "convert": False,
                    "tracking": []
                },
                "BASKET": {
                    "CHOCOLATE": {
                        "prev_weights": [],
                        "prev_prices": [],
                        "tracking": []
                    },
                    "STRAWBERRIES": {
                        "prev_weights": [],
                        "prev_prices": [],
                        "tracking": []
                    },
                    "ROSES": {
                        "prev_weights": [],
                        "prev_prices": [],
                        "tracking": []
                    },
                    "GIFT_BASKET": {
                        "prev_prices": [],
                        "prev_sums_of_basket_products": [],
                        "prev_basket_ratios": [],
                        "tracking": []
                    },
                }
            }

        conversions = 0

        for product in state.order_depths:
            if product == "ORCHIDS":
                trader = OrchidTrader()
                result[product], orchid_conversions, traderData[product] = trader.run(state, product, traderData[product])
                conversions += orchid_conversions
            elif product == "AMETHYSTS":
                trader = AmethystTrader()
                result[product], amethyst_conversions, traderData[product] = trader.run(state, product, traderData[product])
            elif product == "STARFRUIT":
                trader = StarfruitTrader()
                result[product], starfruit_conversions, traderData[product] = trader.run(state, product, traderData[product])
        
        basket_trader = BasketTrader()
        basket_result, basket_conversions, traderData["BASKET"] = basket_trader.run(state, "BASKET", traderData["BASKET"])
        result["CHOCOLATE"] = basket_result["CHOCOLATE"]
        result["STRAWBERRIES"] = basket_result["STRAWBERRIES"]
        result["ROSES"] = basket_result["ROSES"]
        result["GIFT_BASKET"] = basket_result["GIFT_BASKET"]

        traderData = jsonpickle.encode(traderData)
        
        return result, conversions, traderData