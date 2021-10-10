import PySimpleGUI as sg
import time
from main import *

UPDATE_FREQUENCY_MILLISECONDS = 3 * 1000

first_run = True
orders = []
latest_order_time = 0

layout = [
            [sg.Text("Welcome to TradingStats!")],
            [sg.Multiline(default_text="No new orders...", size=(100, 50), autoscroll=True, enter_submits=False, key='-ORDERS-', do_not_clear=True)],
            [sg.HorizontalSeparator()],
            [sg.Text("{ Balance graph goes here }")]
          ]

window = sg.Window("TradingStats",
                   layout,
                   no_titlebar=False,
                   grab_anywhere=True,
                   margins=(15, 15))



def loadOrders():
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

      print(_result)
      orders.append(_result)



def updateFirst(window):
  loadOrders()
  window['-ORDERS-'].update("\n".join(orders))

  print("first updated")



def update(window):
  _order_history = get_orderHistory()
  if _order_history['code'] == 0: # check if data can be used
    pass

  print("updated")




# Create an event loop
while True:
    event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)

    updateFirst(window)
    first_run = False


    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
        
    update(window)

window.close()

if __name__ == '__main__':
  updateFirst(window)