from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import jsonpickle

class BasketTrader:
    def run(self, state: TradingState, product: str, data: dict):
        order_depth: OrderDepth = state.order_depths["GIFT_BASKET"]

        gift_basket_buy_orders = order_depth.buy_orders
        gift_basket_buy_order_prices = sorted(gift_basket_buy_orders.keys())
        gift_basket_lowest_buy_order_price = gift_basket_buy_order_prices[0]
        gift_basket_highest_buy_order_price = gift_basket_buy_order_prices[-1]
        
        gift_basket_sell_orders = order_depth.sell_orders
        gift_basket_sell_order_prices = sorted(gift_basket_sell_orders.keys())
        gift_basket_lowest_sell_order_price = gift_basket_sell_order_prices[0]
        gift_basket_highest_sell_order_price = gift_basket_sell_order_prices[-1]

        gift_basket_mid_price = int((gift_basket_highest_buy_order_price + gift_basket_lowest_sell_order_price) / 2)

        print(f"Gift Basket Mid Price: {gift_basket_mid_price}, ")

        sum_of_basket_products = chocolate_mid_price * 4 + strawberries_mid_price * 6 + roses_mid_price
        data["GIFT_BASKET"]["prev_sums_of_basket_products"].append(sum_of_basket_products)
        
        basket_ratio = sum_of_basket_products / gift_basket_mid_price

        data["GIFT_BASKET"]["prev_basket_ratios"].append(basket_ratio)

        print(f"Sum of Basket Products: {sum_of_basket_products}, ")

        orders = {
            "CHOCOLATE": [],
            "STRAWBERRIES": [],
            "ROSES": [],
            "GIFT_BASKET": []
        }

        gift_basket_limit_width = 60

        negative_price_modifier = -1
        positive_price_modifier = 6
        avg_history_length = 20

        gift_basket_position = state.position["GIFT_BASKET"] if "GIFT_BASKET" in state.position else 0
        recent_avg_sums_of_basket_products = sum(data["GIFT_BASKET"]["prev_sums_of_basket_products"][-avg_history_length:]) / len(data["GIFT_BASKET"]["prev_sums_of_basket_products"][-avg_history_length:])
        median_basket_ratio = sorted(data["GIFT_BASKET"]["prev_basket_ratios"])[int(len(data["GIFT_BASKET"]["prev_basket_ratios"]) / 2)]
        low_basket_ratio = sorted(data["GIFT_BASKET"]["prev_basket_ratios"])[int(len(data["GIFT_BASKET"]["prev_basket_ratios"]) / 3)]
        high_basket_ratio = sorted(data["GIFT_BASKET"]["prev_basket_ratios"])[int(len(data["GIFT_BASKET"]["prev_basket_ratios"]) / 3 * 2)]

        if basket_ratio < low_basket_ratio:
            orders["GIFT_BASKET"].append(Order("GIFT_BASKET", gift_basket_lowest_sell_order_price + negative_price_modifier, -gift_basket_limit_width - gift_basket_position))
        elif basket_ratio > high_basket_ratio:
            orders["GIFT_BASKET"].append(Order("GIFT_BASKET", gift_basket_highest_buy_order_price - negative_price_modifier, gift_basket_limit_width - gift_basket_position))

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

        orders.append(Order(product, mid_price - 1, -limit_width))
        conversions = -position

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
        
        basket_trader = BasketTrader()
        basket_result, basket_conversions, traderData["BASKET"] = basket_trader.run(state, "BASKET", traderData["BASKET"])
        result["CHOCOLATE"] = basket_result["CHOCOLATE"]
        result["STRAWBERRIES"] = basket_result["STRAWBERRIES"]
        result["ROSES"] = basket_result["ROSES"]
        result["GIFT_BASKET"] = basket_result["GIFT_BASKET"]

        traderData = jsonpickle.encode(traderData)
        return result, conversions, traderData