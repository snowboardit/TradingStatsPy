# Imports
import core.list_open_order as loo
import core.get_curr_order_hist as coh
import core.get_futures_positions as fp

# Setup
CONFIG_PATH = 'C:/Users/maxla/Dev/TradingStats/config.json'
BOT_NAME = 'ascendex'

# fetch all open orders
# @click.option("--config", type=str, default=None, help="path to the config file")
# @click.option("--botname", type=click.Choice(["ascendex", "ascendex-sandbox"]), default="ascendex-sandbox", help="specify the bot to use")
# @click.option("--symbol", type=str, default=None, help="symbol: BTC-PERP")
# @click.option('--verbose/--no-verbose', default=False)
def get_openOrders():
  return loo.run(CONFIG_PATH, BOT_NAME, None, False)

# fetch order history
def get_orderHistory():
  return coh.run(CONFIG_PATH, BOT_NAME, None, None, False, False)

# fetch account information
# @click.option("--config", type=str, default=None, help="path to the config file")
# @click.option("--botname", type=str, default="ascendex", help="specify the bot to use")
# @click.option('--verbose/--no-verbose', default=False)
def get_positions():
  return fp.run(CONFIG_PATH, BOT_NAME, False)

# extract balance from positions and collateral
def get_balance(positions):
  collateral_balance = 0
  contracts_balance = 0

  if positions['code'] == 0:
    collateral = positions['data']['collaterals']
    for asset in collateral:
      if asset['referencePrice'] > 0:
        collateral_balance += (asset['balance'] * asset['referencePrice'])

    contacts = positions['data']['contracts']
    for contract in contacts:
      contracts_balance += (contract['unrealizedPnl'] * contract['markPrice'])

  return collateral_balance + contracts_balance