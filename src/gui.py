import PySimpleGUI as sg
from main import *

UPDATE_FREQUENCY_MILLISECONDS = 5 * 1000

layout = [
            [sg.Text("Welcome to TradingStats!")],
            [sg.Text("Account Balance (Margin): "), sg.Text("0", key="-MARGIN_BAL-"), sg.Text("Account Balance (Cash): "), sg.Text("0", key="-CASH_BAL-")],
            [sg.Text("{ Balance graph goes here }")]
          ]

window = sg.Window("TradingStats",
                   layout,
                   no_titlebar=False,
                   grab_anywhere=True,
                   margins=(15, 15))

def update(window):
  print("updated")
  # get_assets()
  window["-MARGIN_BAL-"].update(str(UPDATE_FREQUENCY_MILLISECONDS))

# Create an event loop -- window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
while True:
    event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
        
    update(window)

window.close()