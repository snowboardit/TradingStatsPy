
import time
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib.figure import Figure
from main import *

UPDATE_FREQUENCY_MILLISECONDS = 5 * 1000
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



def updateBalance(window):
  _balance = str(get_balance())
  window['-BALANCE-'].update(_balance)



def updateTimestamp(window):
  last_updated = time.localtime()
  _last_updated_str = "Last updated: {}".format(time.strftime("%H:%M:%S", last_updated))
  window['-UPDATED-'].update(_last_updated_str)



# init graph
def initGraph(window):

  canvas_elem = window['-GRAPH-']
  canvas = canvas_elem.TKCanvas

  # get the balance data - separate x time and y balance values
  _balance = get_balance()
  _timestamp = get_timestamp() 
  price_data.append(_balance)
  time_data.append(_timestamp)
  
  # draw the initial plot in the window
  fig = Figure()
  fig_agg = drawFigure(canvas, fig)
  ax = fig.add_subplot(111)
  ax.set_xlabel("Time")
  ax.set_ylabel("Balance")
  ax.grid()
  ax.plot(time_data, price_data, color='purple')
  fig_agg.draw()

  updateTimestamp(window)                        # update timestamp
  updateBalance(window)                          # update balance

  return ax, fig_agg



def updateGraph(window, ax, fig_agg):

  # get the balance data - separate x time and y balance values
  print("Updated balance: $", get_balance())
  _balance = get_balance()
  _timestamp = get_timestamp() 
  price_data.append(_balance)
  time_data.append(_timestamp)
  
  ax.cla()                                       # clear the subplot
  ax.grid()                                      # draw a grid
  ax.plot(time_data, price_data, color='purple') # re-plot with new data
  fig_agg.draw()                                 # re-draw/render the canvas

  updateTimestamp(window)                        # update timestamp
  updateBalance(window)                          # update balance



# update window with new content
def updateWindow(window):
  _order_history = get_orderHistory()
  ordersStr = '\n'.join(orders)

  if _order_history['code'] == 0: # check if data can be used
    window['-ORDERS-'].update(ordersStr)
    updateTimestamp(window)
    updateBalance(window)
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
                   margins=(10, 10),
                   finalize=True,
                   font='Times')

  print("Window initialization completed")
  return window




##################
#    Runtime     #
##################
def main():

  window = initWindow() # Initialize Window 
  ax, fig_agg = initGraph(window) # Initialize and draw graph inside of window

  # Create an event loop
  while True:
    event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)

    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
      break
    
    # Update the graph every iteration
    updateGraph(window, ax, fig_agg)

    # Only if there is a new order found do we update the order book
    if newOrderFound():
      updateWindow(window)


  window.close()



if __name__ == '__main__':
  main()
