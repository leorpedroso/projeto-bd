import PySimpleGUI as sg

Champions = ["Aatrox", "Ahri", "Akali", "Vayne", "Ezreal", "Sivir"]

# Define the layout of the window
layout = [[sg.Text('Guess the champion:'), sg.InputText()],
          [sg.Button('OK'), sg.Button('Cancel')]]

# Create the window
window = sg.Window('My Window', layout)

# Event loop to process events and get input from the user
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):  # if user closes window or clicks cancel
        break
    if event == 'OK':
        # Print the user's input
        if values[0] in Champions:
            print("Acertou!")
        else:
            print("Momento Junior")
        # print(f'Hello {values[0]}!')

# Close the window
window.close()
