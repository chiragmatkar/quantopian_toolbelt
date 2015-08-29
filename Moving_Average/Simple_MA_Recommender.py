
# Initialize Global Variables
def initialize(context):

    context.stock = symbol('SPY')

    # Define MA Constants
    context.fma_days = 50
    context.sma_days = 200
    context.ma_recommendation_weight = 1
    context.ma_is_tracing = False

# Will be called on every trade event for the securities you specify.
def handle_data(context, data):
    print context.stock.symbol + " moving average recommendation: " + str(determine_ma_recommendation(context, data, context.stock))

"""
Determine if the moving average recommends a buy or a sell for a given stock.

Requires Globals: context.fma_days, context.sma_days, context.ma_recommendation_weight
Requires: context, data, and stock
Returns: positive for a buy and negative for a sell, 0 for neutral
"""
def determine_ma_recommendation(context, data, stock):
    if stock in data:
        # calculate fast moving average
        fast_moving_average = data[stock].mavg(context.fma_days)

        # calculate slow moving average
        slow_moving_average = data[stock].mavg(context.sma_days)

        if (fast_moving_average > slow_moving_average):
            if context.ma_is_tracing:
                log.info(stock.symbol + " recommend a buy with fast: " + str(fast_moving_average) + " slow: " + str(slow_moving_average))
            return  context.ma_recommendation_weight
        elif (fast_moving_average < slow_moving_average):
            if context.ma_is_tracing:
                log.info(stock.symbol + " recommend a sell with fast: " + str(fast_moving_average) + " slow: " + str(slow_moving_average))
            return -context.ma_recommendation_weight
        else:
            if context.ma_is_tracing:
                log.info(stock.symbol + " recommend neutral with fast: " + str(fast_moving_average) + " slow: " + str(slow_moving_average))
            return 0
    else: # stock may no longer be selling, recommend sell
        if context.ma_is_tracing:
            log.info(stock.symbol + " not in data")
        return  -context.ma_recommendation_weight
