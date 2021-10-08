import PySimpleGUI as sg
from main import *

UPDATE_FREQUENCY_MILLISECONDS = 20 * 1000

layout = [
            [sg.Text("Welcome to TradingStats!")],
            [sg.Text("Account Balance (Margin): "), sg.Text("Account Balance (Cash): ")],
            [sg.Text("{ Balance graph goes here }")]
          ]

window = sg.Window("TradingStats",
                   layout,
                   no_titlebar=True,
                   grab_anywhere=True,
                   margins=(15, 15))

def update():
  print("updated")
  get_cashBal()

# Create an event loop -- window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
while True:
    event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    
    update()

window.close()