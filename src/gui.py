import PySimpleGUI as sg
import time
from main import *

UPDATE_FREQUENCY_MILLISECONDS = 3 * 1000



def initOrders():

  global orders
  global latest_seqNum

  orders = []
  latest_seqNum = 0

  _order_history = get_orderHistory()
  if _order_history['code'] == 0: # check for error in response
    for i in range(10):
      order = _order_history['data'][i]
      _time = str(order['time'])[:10]
      _fmtd_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(_time)))
      _pair = "{}/USD".format(order['symbol'].split('-')[0])
      _side = order['side']
      _amount = order['orderQty']
      _price = order['price']
      _result = "{}: {} - New order for {} @ {} USD - {}".format(_fmtd_time, _pair, _amount, _price, _side)

      if order['seqNum'] > latest_seqNum:
        latest_seqNum = order['seqNum']

      # print(_result)
      orders.append(_result)


# determine if new order has been published, if so add it to orders array
def newOrderFound():

  global latest_seqNum

  _order_history = get_orderHistory()
  if _order_history['code'] == 0: # check for error in response
    for order in _order_history['data']:
      if order['seqNum'] > latest_seqNum:
        print("New order found:\n", order)
        orders.append(order)
        latest_seqNum = order['seqNum']
        return True
  return False



# update window with new content
def updateWindow(window):
  _order_history = get_orderHistory()
  ordersStr = '\n'.join(orders)
  last_updated = time.localtime()
  _last_updated_str = "Last updated: {}".format(time.strftime("%H:%M:%S", last_updated))

  if _order_history['code'] == 0: # check if data can be used
    window['-ORDERS-'].update(ordersStr)
    window['-UPDATED-'].update(_last_updated_str)
    print("Window updated")



# Create a window
def initWindow():

  global last_updated

  initOrders()
  ordersStr = '\n'.join(orders)
  last_updated = time.localtime()
  _last_updated_str = "Last updated: {}".format(time.strftime("%H:%M:%S", last_updated))

  layout = [
            [sg.Text("Welcome to TradingStats!")],
            [sg.Multiline(default_text=ordersStr, size=(70, 13), autoscroll=True, enter_submits=False, key='-ORDERS-', do_not_clear=True)],
            [sg.HorizontalSeparator()],
            [sg.Text("{ Balance graph goes here }")],
            [sg.Text(_last_updated_str, key='-UPDATED-')]
          ]

  window = sg.Window("TradingStats",
                   layout,
                   no_titlebar=False,
                   grab_anywhere=True,
                   margins=(10, 10))

  print("Window initialization completed")
  return window


def main():

  window = initWindow()

  # Create an event loop
  while True:
    event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)

    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    
    if newOrderFound():
      updateWindow(window)

    # window.close()


if __name__ == '__main__':
  main()
