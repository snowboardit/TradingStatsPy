# Imports
from datetime import datetime
import core.list_open_order as loo
import core.get_curr_order_hist as coh
import core.get_futures_positions as fp
import kucoin_futures as kf

"""
New exchange API - KuCoin - https://docs.kucoin.com/#get-account-info
"""





"""
----------------------------------------------------
"""


# Setup
# CONFIG_PATH = 'C:/Users/maxla/Dev/TradingStats/config.json' ## MAX-PC
# CONFIG_PATH = 'C:/Users/Max/Dev/TradingStats/config.json' ## MAX-LT
# CONFIG_PATH = 'Z:\Dev\TradingStats\config.json' ## WORK-PC
CONFIG_PATH = '../config.json'
LOGFILE_PATH = '../log.txt'

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
def get_balance():

  positions = get_positions()
  # print(positions)

  collateral_balance = 0
  contracts_balance = 0

  if positions['code'] == 0:
    collateral = positions['data']['collaterals']
    for asset in collateral:
      bal = float(asset['balance'])
      ref_price = float(asset['referencePrice'])
      if float(asset['referencePrice']) > 0:
        collateral_balance += (bal * ref_price)
    # print("collateral_balance\n", collateral_balance)

    contracts = positions['data']['contracts']
    for contract in contracts:
      unreal_pnl = float(contract['unrealizedPnl'])
      contracts_balance += unreal_pnl
    # print("contracts_balance\n",contracts_balance)

  return collateral_balance + contracts_balance


def get_timestamp():
  return datetime.now()



#############
#  Logging  #
#############
def initLog():
  try:
    f = open(LOGFILE_PATH, 'a')
    print('Logfile opened successfully')
    f.write('TradingStats - Max L. 2021 - Started at {}\n'.format(datetime.now()))
    f.close()
  except Exception as e:
    print('Error opening log: ', e)


def writeToLog(content):
  try:
    f = open(LOGFILE_PATH, 'a')
    f.write(content + '\n')
    f.close()
  except Exception as e:
    print('Error writing to log: ', e)
