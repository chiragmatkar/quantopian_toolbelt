import numpy as np
import math
import operator

# Initialize Global Variables
def initialize(context):

    context.stock = symbol('SPY')

    # Define WILLER Constants
    # Set up Williams %R by ta lib
    context.willer = ta.WILLR(timeperiod=30)
    context.LOW_W = -85
    context.HIGH_W = -15
    context.willer_recommendation_weight = 1
    context.willer_is_tracing = False

# Will be called on every trade event for the securities you specify.
def handle_data(context, data):
    print context.stock.symbol + " moving average recommendation: " + str(determine_willer_recommendation(context, data, context.stock))

"""
Determine if the Willer %R recommends a buy or a sell.

Requires Globals: context.LOW_W, context.HIGH_W, context.willer_recommendation_weight
Requires: context, data, stock
Returns: 1 for a buy and -1 for a sell, 0 for neutral
"""
def determine_willer_recommendation(context, data, stock):
    if stock in data:
        try:
            try:
                willer_data = context.willer(data)
            except Exception as excep:
                log.error(excep)
                return -context.willer_recommendation_weight

            stock_willer = willer_data[stock]

             # first 14 days, the william value will be numpy.nan
            if not np.isnan(stock_willer):

                if stock_willer > context.HIGH_W:
                    if context.willer_is_tracing:
                        log.info(stock.symbol + " recommend sell with value of: " + str(stock_willer))
                    return -context.willer_recommendation_weight
                elif stock_willer < context.LOW_W:
                    if context.willer_is_tracing:
                        log.info(stock.symbol + " recommend buy with value of: " + str(stock_willer))
                    return context.willer_recommendation_weight
                else:
                    if context.willer_is_tracing:
                        log.info(stock.symbol + " recommend neutral with value of: " + str(stock_willer))
                    return 0
            else:
                if context.willer_is_tracing:
                        log.info(stock.symbol + " willer is nan")
                return 0
        except Exception as excep:
            log.error(excep)
            return -context.willer_recommendation_weight
    else: # stock is not in data, may no longer be trading, recommend a sell
        if context.willer_is_tracing:
            log.info(stock.symbol + " not in data")
        return -context.willer_recommendation_weight