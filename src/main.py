# Imports
import core.query_prv_balance as qb
import core.query_pub_assets as qpa

# @click.option("--asset", type=str, default=None,
#               help='optional, if none, return all assets with non-empty balance. You can specify an asset (e.g. "BTC")')
# @click.option("--account", type=click.Choice(['cash', 'margin']), default="cash", help="cash (default) or margin")
# @click.option("--show-all/--no-show-all", default=False, help="show all balances, including empty balances")
# @click.option("--config", type=str, default="config.json", help="path to the config file")
# @click.option("--verbose/--no-verbose", default=False)

## Setup
CONFIG_PATH = 'config.json'

# fetch margin account balance for all assets & print to console
def get_marginBal():
  return qb.run(None, 'margin', True, CONFIG_PATH, True)

# fetch cash account balance for all assets & print to console
def get_cashBal():
  return qb.run(None, 'cash', True, CONFIG_PATH, True)

# fetch something public
def get_assets():
  return qpa.run(CONFIG_PATH)