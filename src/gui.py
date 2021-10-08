import PySimpleGUI as sg
import main

UPDATE_FREQUENCY_MILLISECONDS = 20 * 1000

layout = [
            [sg.Text("Welcome to TradingStats!")],
            [sg.Text("Account Balance (Margin): "), [], sg.Text("Account Balance (Cash): ", [])],
            [sg.Text("{ Balance graph goes here }")],
            [sg.Button("OK")]
          ]

window = sg.Window("TradingStats",
                   layout,
                   text_justification='c',
                   no_titlebar=True,
                   grab_anywhere=True,
                   margins=(15, 15)
                  )

def update():
  print("updated")
  main.get_cashBal()
  pass

# Create an event loop
while True:
    event, values = window.read(timeout=UPDATE_FREQUENCY_MILLISECONDS)
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    update()

window.close()