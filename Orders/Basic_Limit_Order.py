
# Initialize Global Variables
def initialize(context):

    context.stocks = symbols('SPY', 'AAPL')

    # Define LimitOrder Constants

    context.limit_order_is_tracing = False
    # Buy when price is x% of current price
    context.limit_perc = .98
    # transaction fees to account for when adjusting cash
    context.trade_fees = 1.00

# Will be called on every trade event for the securities you specify.
def handle_data(context, data):
    cash = context.portfolio.cash

    for stock in context.stocks:
        if cash > data[stock].price:
            cash = place_limit_order(data, context, stock, 1, context.limit_perc, cash)
            print cash


"""
Places a limit order and returns reamining cash to you.

Requires Globals: context.trade_fees
Requires: data, context, stock, num_shares, limit_perc, available_cash
Returns: Remaining cash after trade
"""
"""
Places a limit order and returns reamining cash to you.

Requires Globals: context.trade_fees, context.limit_order_is_tracing
Requires: data, context, stock, num_shares, limit_perc, available_cash
Returns: Remaining cash after trade
"""
def place_limit_order(data, context, stock, num_shares, limit_perc, available_cash):
    if stock in data:
        limit_price = data[stock].price * limit_perc
        order(stock, num_shares, style=LimitOrder(limit_price))
        if context.limit_order_is_tracing:
            log.info(stock.symbol + " - Placing Limit Order for " + str(num_shares) +" shares -- current price: " + str(data[stock].price) + " buy price: " + str(limit_price))
        return available_cash + -((num_shares * data[stock].price) + context.trade_fees)

