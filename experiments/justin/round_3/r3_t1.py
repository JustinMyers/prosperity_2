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

        order_depth: OrderDepth = state.order_depths["CHOCOLATE"]

        chocolate_buy_orders = order_depth.buy_orders
        chocolate_buy_order_prices = sorted(chocolate_buy_orders.keys())
        chocolate_lowest_buy_order_price = chocolate_buy_order_prices[0]
        chocolate_highest_buy_order_price = chocolate_buy_order_prices[-1]

        chocolate_sell_orders = order_depth.sell_orders
        chocolate_sell_order_prices = sorted(chocolate_sell_orders.keys())
        chocolate_lowest_sell_order_price = chocolate_sell_order_prices[0]
        chocolate_highest_sell_order_price = chocolate_sell_order_prices[-1]

        chocolate_mid_price = int((chocolate_highest_buy_order_price + chocolate_lowest_sell_order_price) / 2)

        order_depth: OrderDepth = state.order_depths["STRAWBERRIES"]

        strawberries_buy_orders = order_depth.buy_orders
        strawberries_buy_order_prices = sorted(strawberries_buy_orders.keys())
        strawberries_lowest_buy_order_price = strawberries_buy_order_prices[0]
        strawberries_highest_buy_order_price = strawberries_buy_order_prices[-1]

        strawberries_sell_orders = order_depth.sell_orders
        strawberries_sell_order_prices = sorted(strawberries_sell_orders.keys())
        strawberries_lowest_sell_order_price = strawberries_sell_order_prices[0]
        strawberries_highest_sell_order_price = strawberries_sell_order_prices[-1]

        strawberries_mid_price = int((strawberries_highest_buy_order_price + strawberries_lowest_sell_order_price) / 2)

        order_depth: OrderDepth = state.order_depths["ROSES"]

        roses_buy_orders = order_depth.buy_orders
        roses_buy_order_prices = sorted(roses_buy_orders.keys())
        roses_lowest_buy_order_price = roses_buy_order_prices[0]
        roses_highest_buy_order_price = roses_buy_order_prices[-1]

        roses_sell_orders = order_depth.sell_orders
        roses_sell_order_prices = sorted(roses_sell_orders.keys())
        roses_lowest_sell_order_price = roses_sell_order_prices[0]
        roses_highest_sell_order_price = roses_sell_order_prices[-1]

        roses_mid_price = int((roses_highest_buy_order_price + roses_lowest_sell_order_price) / 2)

        print(f"Gift Basket Mid Price: {gift_basket_mid_price}, ")
        print(f"Chocolate Mid Price: {chocolate_mid_price}, ")
        print(f"Strawberries Mid Price: {strawberries_mid_price}, ")
        print(f"Roses Mid Price: {roses_mid_price}, ")

        sum_of_basket_products = chocolate_mid_price * 4 + strawberries_mid_price * 6 + roses_mid_price
        data["GIFT_BASKET"]["prev_sums_of_basket_products"].append(sum_of_basket_products)
        
        basket_ratio = sum_of_basket_products / gift_basket_mid_price

        data["GIFT_BASKET"]["prev_basket_ratios"].append(basket_ratio)

        print(f"Sum of Basket Products: {sum_of_basket_products}, ")

        chocolate_weight = chocolate_mid_price * 4 / sum_of_basket_products
        strawberries_weight = strawberries_mid_price * 6 / sum_of_basket_products
        roses_weight = roses_mid_price / sum_of_basket_products

        print(f"Chocolate Weight: {chocolate_weight}, Strawberries Weight: {strawberries_weight}, Roses Weight: {roses_weight}")

        data["CHOCOLATE"]["prev_weights"].append(chocolate_weight)
        data["STRAWBERRIES"]["prev_weights"].append(strawberries_weight)
        data["ROSES"]["prev_weights"].append(roses_weight)

        data["CHOCOLATE"]["prev_prices"].append(chocolate_mid_price)
        data["STRAWBERRIES"]["prev_prices"].append(strawberries_mid_price)
        data["ROSES"]["prev_prices"].append(roses_mid_price)

        orders = {
            "CHOCOLATE": [],
            "STRAWBERRIES": [],
            "ROSES": [],
            "GIFT_BASKET": []
        }

        negative_price_modifier = -1
        positive_price_modifier = 6
        price_modifier = positive_price_modifier
        avg_history_length = 20

        gift_basket_position = state.position["GIFT_BASKET"] if "GIFT_BASKET" in state.position else 0
        gift_basket_limit_width = 60
        recent_avg_sums_of_basket_products = sum(data["GIFT_BASKET"]["prev_sums_of_basket_products"][-avg_history_length:]) / len(data["GIFT_BASKET"]["prev_sums_of_basket_products"][-avg_history_length:])
        # get the value in the middle of the basket ratios
        median_basket_ratio = sorted(data["GIFT_BASKET"]["prev_basket_ratios"])[int(len(data["GIFT_BASKET"]["prev_basket_ratios"]) / 2)]
        low_basket_ratio = sorted(data["GIFT_BASKET"]["prev_basket_ratios"])[int(len(data["GIFT_BASKET"]["prev_basket_ratios"]) / 3)]
        high_basket_ratio = sorted(data["GIFT_BASKET"]["prev_basket_ratios"])[int(len(data["GIFT_BASKET"]["prev_basket_ratios"]) / 3 * 2)]
        if basket_ratio < low_basket_ratio:
            orders["GIFT_BASKET"].append(Order("GIFT_BASKET", gift_basket_lowest_sell_order_price + negative_price_modifier, -gift_basket_limit_width - gift_basket_position))
        elif basket_ratio > high_basket_ratio:
            orders["GIFT_BASKET"].append(Order("GIFT_BASKET", gift_basket_highest_buy_order_price - negative_price_modifier, gift_basket_limit_width - gift_basket_position))
        # orders["GIFT_BASKET"].append(Order("GIFT_BASKET", gift_basket_lowest_sell_order_price + negative_price_modifier, -gift_basket_limit_width - gift_basket_position))
        # orders["GIFT_BASKET"].append(Order("GIFT_BASKET", gift_basket_highest_buy_order_price - negative_price_modifier, gift_basket_limit_width - gift_basket_position))

        chocolate_position = state.position["CHOCOLATE"] if "CHOCOLATE" in state.position else 0
        chocolate_limit_width = 250
        # chocolate_avg_weight = sum(data["CHOCOLATE"]["prev_weights"]) / len(data["CHOCOLATE"]["prev_weights"])
        # chocolate_recent_avg_weight = sum(data["CHOCOLATE"]["prev_weights"][-5:]) / len(data["CHOCOLATE"]["prev_weights"][-5:])
        # chocolate_recent_avg_price = sum(data["CHOCOLATE"]["prev_prices"][-avg_history_length:]) / len(data["CHOCOLATE"]["prev_prices"][-avg_history_length:])
        # if chocolate_mid_price < chocolate_recent_avg_price:
        #     orders["CHOCOLATE"].append(Order("CHOCOLATE", chocolate_mid_price + price_modifier, -chocolate_limit_width - chocolate_position))
        # else:
        #     orders["CHOCOLATE"].append(Order("CHOCOLATE", chocolate_mid_price - price_modifier, chocolate_limit_width - chocolate_position))
        # orders["CHOCOLATE"].append(Order("CHOCOLATE", chocolate_highest_sell_order_price + negative_price_modifier, -chocolate_limit_width - chocolate_position))
        # orders["CHOCOLATE"].append(Order("CHOCOLATE", chocolate_lowest_buy_order_price - negative_price_modifier, chocolate_limit_width - chocolate_position))

        strawberries_position = state.position["STRAWBERRIES"] if "STRAWBERRIES" in state.position else 0
        strawberries_limit_width = 350
        # strawberries_avg_weight = sum(data["STRAWBERRIES"]["prev_weights"]) / len(data["STRAWBERRIES"]["prev_weights"])
        # strawberries_recent_avg_weight = sum(data["STRAWBERRIES"]["prev_weights"][-5:]) / len(data["STRAWBERRIES"]["prev_weights"][-5:])
        # strawberries_recent_avg_price = sum(data["STRAWBERRIES"]["prev_prices"][-avg_history_length:]) / len(data["STRAWBERRIES"]["prev_prices"][-avg_history_length:])
        # if strawberries_mid_price < strawberries_recent_avg_price:
        #     orders["STRAWBERRIES"].append(Order("STRAWBERRIES", strawberries_mid_price + price_modifier, -strawberries_limit_width - strawberries_position))
        # else:
        #     orders["STRAWBERRIES"].append(Order("STRAWBERRIES", strawberries_mid_price - price_modifier, strawberries_limit_width - strawberries_position))
        # orders["STRAWBERRIES"].append(Order("STRAWBERRIES", strawberries_highest_sell_order_price + negative_price_modifier, -strawberries_limit_width - strawberries_position))
        # orders["STRAWBERRIES"].append(Order("STRAWBERRIES", strawberries_lowest_buy_order_price - negative_price_modifier, strawberries_limit_width - strawberries_position))

        roses_position = state.position["ROSES"] if "ROSES" in state.position else 0
        roses_limit_width = 60
        # roses_avg_weight = sum(data["ROSES"]["prev_weights"]) / len(data["ROSES"]["prev_weights"])
        # roses_recent_avg_weight = sum(data["ROSES"]["prev_weights"][-5:]) / len(data["ROSES"]["prev_weights"][-5:])
        # roses_recent_avg_price = sum(data["ROSES"]["prev_prices"][-avg_history_length:]) / len(data["ROSES"]["prev_prices"][-avg_history_length:])
        # if roses_mid_price < roses_recent_avg_price:
        #     orders["ROSES"].append(Order("ROSES", roses_mid_price + price_modifier, -roses_limit_width - roses_position))
        # else:
        #     orders["ROSES"].append(Order("ROSES", roses_mid_price - price_modifier, roses_limit_width - roses_position))
        # orders["ROSES"].append(Order("ROSES", roses_highest_sell_order_price + negative_price_modifier, -roses_limit_width - roses_position))
        # orders["ROSES"].append(Order("ROSES", roses_lowest_buy_order_price - negative_price_modifier, roses_limit_width - roses_position))

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