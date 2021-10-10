# Imports
import core.list_open_order as loo
import core.get_curr_order_hist as coh

# Setup
CONFIG_PATH = 'C:/Users/maxla/Dev/TradingStats/config.json'

# fetch all open orders
# @click.option("--config", type=str, default=None, help="path to the config file")
# @click.option("--botname", type=click.Choice(["ascendex", "ascendex-sandbox"]), default="ascendex-sandbox", help="specify the bot to use")
# @click.option("--symbol", type=str, default=None, help="symbol: BTC-PERP")
# @click.option('--verbose/--no-verbose', default=False)
def get_openOrders():
  return loo.run(CONFIG_PATH, "ascendex", None, True)

# fetch order history
def get_orderHistory():
  return coh.run(CONFIG_PATH, "ascendex", None, None, False, True)