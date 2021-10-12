
import time
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
from main import *

UPDATE_FREQUENCY_MILLISECONDS = 2 * 1000
time_data = []
price_data = []


################
#    UTILS     #
################
# Generate a formatted order string from an order object
def generateOrderStr(order):
  _time = str(order['time'])[:10]
  _fmtd_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(_time)))
  _pair = "{}/USD".format(order['symbol'].split('-')[0])
  _side = order['side'].upper()
  _amount = order['orderQty']
  _price = order['price']
  _result = "{}: {} - New order for {} @ {} USD - {}".format(_fmtd_time, _pair, _amount, _price, _side)
  return _result


def drawFigure(canvas, figure, loc=(0, 0)):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


##################
#   PROCESSING   #
##################

# Initialize orders array and latest numSeq
def initOrders():

  global orders
  global latest_seqNum

  orders = []
  latest_seqNum = 0

  _order_history = get_orderHistory()
  if _order_history['code'] == 0: # check for error in response
    for i in range(10):
      order = _order_history['data'][i]
      order_str = generateOrderStr(order)

      if order['seqNum'] > latest_seqNum:
        latest_seqNum = order['seqNum']

      # print(_result)
      orders.append(order_str)


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


# init graph - 72 hr time period
def initGraph(window):

  canvas_elem = window['-GRAPH-']
  canvas = canvas_elem.TKCanvas

  # get the balance data - separate x time and y balance values
  print("balance: $", get_balance())
  price_data.append(get_balance())
  time_data.append(get_timestamp())
  

  # draw the initial plot in the window
  fig = Figure()
  ax = fig.add_subplot(111)
  ax.set_xlabel("Time (x)")
  ax.set_ylabel("Balance (y)")
  ax.grid()
  fig_agg = drawFigure(canvas, fig)

  ax.cla()                    # clear the subplot
  ax.grid()                   # draw the grid
  ax.plot(time_data, price_data, color='purple')
  fig_agg.draw()


    # for res in response['data']['collaterals']:
    #   cur_account_bal = (if balance is positive add together) - (all contract upnl)



def updateGraph(window):
  canvas_elem = window['-GRAPH-']
  canvas = canvas_elem.TKCanvas

  # get the balance data - separate x time and y balance values
  print("balance: $", get_balance())
  price_data.append(get_balance())
  time_data.append(get_timestamp())
  print('Graph updated')



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
            # [sg.Text(text=ordersStr, size=(70, 13), justification='left', key='-ORDERS-')],
            [sg.Text("Current trading balance: $"), sg.Text("0", key='-BALANCE-')],
            [sg.Multiline(default_text=ordersStr, size=(70, 13), autoscroll=True, enter_submits=False, key='-ORDERS-', do_not_clear=True, no_scrollbar=True)],
            [sg.HorizontalSeparator('')],
            [sg.Canvas(size=(400, 400), key='-GRAPH-')],
            [sg.Text(_last_updated_str, key='-UPDATED-')]
          ]

  window = sg.Window("TradingStats",
                   layout,
                   no_titlebar=False,
                   grab_anywhere=True,
                   margins=(10, 10))

  initGraph(window)

  print("Window initialization completed")
  return window


##################
#    Runtime     #
##################

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

  window.close()


if __name__ == '__main__':
  main()
