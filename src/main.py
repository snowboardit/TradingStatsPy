# Imports
import core.query_prv_balance as qb
import core.query_pub_assets as qpa
import core.query_prv_open_orders as qoo

## Setup
CONFIG_PATH = 'config.json'

# fetch all open orders - cash and margin
# @click.option("--symbol", type=str, default=None)
# @click.option("--account", type=click.Choice(['cash', 'margin']), default="cash", help="account category")
# @click.option("--config", type=str, default="config.json", help="path to the config file")
# @click.option("--verbose/--no-verbose", default=False)
def get_openCashOrders():
  return qoo.run(None, 'cash', CONFIG_PATH, True)

def get_openMarginOrders():
  return qoo.run(None, 'margin', CONFIG_PATH, True)

# fetch margin and cash account balance for all assets
# @click.option("--asset", type=str, default=None,
#               help='optional, if none, return all assets with non-empty balance. You can specify an asset (e.g. "BTC")')
# @click.option("--account", type=click.Choice(['cash', 'margin']), default="cash", help="cash (default) or margin")
# @click.option("--show-all/--no-show-all", default=False, help="show all balances, including empty balances")
# @click.option("--config", type=str, default="config.json", help="path to the config file")
# @click.option("--verbose/--no-verbose", default=False)
def get_marginBal():
  return qb.run(None, 'margin', True, CONFIG_PATH, True)

def get_cashBal():
  return qb.run(None, 'cash', True, CONFIG_PATH, True)

# fetch something public
# @click.option("--config", type=str, default="config.json")
def get_assets():
  return qpa.run(CONFIG_PATH)