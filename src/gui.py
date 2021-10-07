import PySimpleGUI as sg

layout = [[sg.Text("Welcome to TradingStats!")], [sg.Button("OK")]]

window = sg.Window('TradingStats', layout, no_titlebar=True)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()