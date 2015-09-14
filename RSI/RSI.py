import talib
import numpy as np

# Initialize Global Variables
def initialize(context):

    context.stock = sid(8554)

 # Define RSI Constants
    context.rsi_LOW = 30
    context.rsi_HIGH = 75
    context.rsi_timeperiod = 30
    context.rsi_recommendation_weight = 1
    context.rsi_is_tracing = True

# Will be called on every trade event for the securities you specify.
def handle_data(context, data):
    
     #Get a trailing window of data
     prices_df = history(context.rsi_timeperiod + 1, '1d', 'price', False)
     prices = prices_df.dropna(axis=1)
     rsi_data = prices.apply(talib.RSI, timeperiod=context.rsi_timeperiod).iloc[-1]
            
     print context.stock.symbol + " willer recommendation: " + str(determine_rsi_recommendation(context, data, context.stock, rsi_data))


"""
Determine if the RSI recommends a buy or a sell.

Requires Globals: context.LOW_W, context.HIGH_W, context.rsi_recommendation_weight
Requires: context, data, stock, rsi_data
Returns: 1 for a buy and -1 for a sell, 0 for neutral
"""
def determine_rsi_recommendation(context, data, stock, rsi_data):    
    if stock in data:
        try:
            stock_rsi = rsi_data[stock]

             # first 14 days, the william value will be numpy.nan
            if not np.isnan(stock_rsi):

                if stock_rsi > context.rsi_HIGH:
                    if context.rsi_is_tracing:
                        log.info(stock.symbol + " recommend sell with value of: " + str(stock_rsi))
                    return -context.rsi_recommendation_weight
                elif stock_rsi < context.rsi_LOW:
                    if context.rsi_is_tracing:
                        log.info(stock.symbol + " recommend buy with value of: " + str(stock_rsi))
                    return context.rsi_recommendation_weight
                else:
                    if context.rsi_is_tracing:
                        log.info(stock.symbol + " recommend neutral with value of: " + str(stock_rsi))
                    return 0

            else:
                if context.rsi_is_tracing:
                        log.info(stock.symbol + " rsi is nan")
                return 0
        except Exception as excep:
            log.error(excep)
            return -context.rsi_recommendation_weight
    else: # stock is not in data, may no longer be trading, recommend a sell
        if context.rsi_is_tracing:
            log.info(stock.symbol + " not in data")
        return -context.rsi_recommendation_weight 
