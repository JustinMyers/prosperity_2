from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List

class Trader:    
    def run(self, state: TradingState):
        
        # class TradingState(object):
        # def __init__(self,
        #             traderData: str,
        #             timestamp: Time,
        #             listings: Dict[Symbol, Listing],
        #             order_depths: Dict[Symbol, OrderDepth],
        #             own_trades: Dict[Symbol, List[Trade]],
        #             market_trades: Dict[Symbol, List[Trade]],
        #             position: Dict[Product, Position],
        #             observations: Observation):
        #     self.traderData = traderData
        #     self.timestamp = timestamp
        #     self.listings = listings
        #     self.order_depths = order_depths
        #     self.own_trades = own_trades
        #     self.market_trades = market_trades
        #     self.position = position
        #     self.observations = observations
        
        timestamp = state.timestamp
        timestamp_str = str(timestamp)
        
        print("TRADER_LOG:"+timestamp_str+"  "+"traderData: " + str(state.traderData))
        print("TRADER_LOG:"+timestamp_str+"  "+"listings: " + str(state.listings))
        for pname in ["AMETHYSTS", "STARFRUIT", "ORCHIDS"]:
            # print("TRADER_LOG:"+timestamp_str+"  "+"order_depths: " + pname +": " + str(state.order_depths[pname]))
            print("TRADER_LOG:"+timestamp_str+"  "+"order_depths: " + pname +": " + "buy_orders:" +": " + str(state.order_depths[pname].buy_orders))
            print("TRADER_LOG:"+timestamp_str+"  "+"order_depths: " + pname +": " + "sell_orders:" +": " + str(state.order_depths[pname].sell_orders))
        print("TRADER_LOG:"+timestamp_str+"  "+"own_trades: " + str(state.own_trades))
        print("TRADER_LOG:"+timestamp_str+"  "+"market_trades: " + str(state.market_trades))
        print("TRADER_LOG:"+timestamp_str+"  "+"position: " + str(state.position))
        print("TRADER_LOG:"+timestamp_str+"  "+"Observations: " + str(state.observations))
        

        ####################
        
        result = {}
        for product in state.order_depths:
            
            
                
                
            if product == "ORCHIDS":
                
                # TRADER_LOG:5900  Observations: (plainValueObservations: {},
                # conversionObservations: {"ORCHIDS": {"py/object": "datamodel.ConversionObservation",
                    # "bidPrice": 1101.0,
                    # "askPrice": 1102.5,
                    # "transportFees": 0.9,
                    # "exportTariff": 9.5,
                    # "importTariff": -5.0,
                    # "sunlight": 2084.1125, 
                    # "humidity": 71.27687}})

                if product in state.observations.plainValueObservations:
                    plainValueObservations = state.observations.plainValueObservations[product]
                else:
                    plainValueObservations = ""
                print("TRADER_LOG:"+timestamp_str+"  "+"plainValueObservations: " + str(plainValueObservations))
                
                if product in state.observations.conversionObservations:
                    conversionObservations = state.observations.conversionObservations[product]
                else:
                    conversionObservations = ""
                print("TRADER_LOG:"+timestamp_str+"  "+"conversionObservations: " + str(conversionObservations))
                
                bidPrice = conversionObservations.bidPrice
                askPrice = conversionObservations.askPrice
                transportFees = conversionObservations.transportFees
                exportTariff = conversionObservations.exportTariff
                importTariff = conversionObservations.importTariff
                sunlight = conversionObservations.sunlight
                humidity = conversionObservations.humidity
                
                def sunlight_production(sunlight_value):
                    sunlight_70 = (10000 / 24 * 7)  # 2916.666666666667
                    minutes_10 = (10000 / 24 / 6)  # 69.44444444444444
                    sunlight_production = 1.0
                    if (sunlight_value < sunlight_70):
                        sunlight_deficit_pct = (sunlight_70 - sunlight_value) / minutes_10
                        sunlight_penalty_pct = sunlight_deficit_pct * 4
                        sunlight_production -= sunlight_penalty_pct / 100
                    return sunlight_production

                def humidity_production(humidity_value):
                    humidity_production = 1.0
                    if (humidity_value > 80):
                        bad_humidity_pct = humidity_value - 80.0
                        humidity_penalty_pct = bad_humidity_pct / 5 * 2
                        humidity_production -= humidity_penalty_pct / 100
                    elif (humidity_value < 60):
                        bad_humidity_pct = 60 - humidity_value
                        humidity_penalty_pct = bad_humidity_pct / 5 * 2
                        humidity_production -= humidity_penalty_pct / 100
                    return humidity_production

                production_penalty = sunlight_production(sunlight) * humidity_production(humidity)
                
                listings = state.listings
                buy_orders = state.order_depths[product].buy_orders
                sell_orders = state.order_depths[product].sell_orders
                own_trades = state.own_trades
                market_trades = state.market_trades
                position = state.position
                
                if timestamp == 0:
                    print(";".join(["ORCHIDS_INFO", "timestamp", "bidPrice", "askPrice", "transportFees", "exportTariff", "importTariff", "sunlight", "humidity", "production_penalty", "buy_orders", "sell_orders"]))
                print(";".join(str(element) for element in ["ORCHIDS_INFO", timestamp, bidPrice, askPrice, transportFees, exportTariff, importTariff, sunlight, humidity, production_penalty, buy_orders, sell_orders]))
            
            
                
            
            
            
            
            
            
            
            
            if product in state.position:
                position = state.position[product]
            else:
                position = 0

            order_depth: OrderDepth = state.order_depths[product]
            
            # limit_width = 20
            limit_width = {"AMETHYSTS": 20, "STARFRUIT": 20, "ORCHIDS": 100}

            orders: List[Order] = []
            
            if product == "AMETHYSTS":

                sell_quantity = -limit_width[product] - position
                orders.append(Order(product, 10002, sell_quantity))
                buy_quantity = limit_width[product] - position
                orders.append(Order(product, 9998, buy_quantity))

            else:
            
                buy_orders = order_depth.buy_orders
                buy_order_prices = sorted(buy_orders.keys())
                buy_order_price = buy_order_prices[0]
                buy_order_price += 1
                
                sell_orders = order_depth.sell_orders
                sell_order_prices = sorted(sell_orders.keys(), reverse=True)
                sell_order_price = sell_order_prices[0]
                sell_order_price -= 1

                sell_quantity = -limit_width[product] - position
                orders.append(Order(product, sell_order_price, sell_quantity))

                buy_quantity = limit_width[product] - position
                orders.append(Order(product, buy_order_price, buy_quantity))

            result[product] = orders
            
            print("RESULT: product: " + product + "orders: " + str(orders) )
            print("RESULT: product: ", product, "orders: ", str(orders), orders )
        
        
        print("RESULT: ", str(result), result)

        traderData = "SAMPLE"         
        conversions = 0
        return result, conversions, traderData