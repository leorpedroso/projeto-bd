from types import NoneType
import PySimpleGUI as sg
import random
import sys, os
sys.path.append(os.path.join(sys.path[0], '../scraper/'))
sys.path.append(os.path.join(sys.path[0], '../persistence/'))

import sender
import main
import urllib3
urllib3.disable_warnings()

list_tips = [] #keep track of every tip given so far

def generate_tip(infos):
    while True:
        attribute, value = random.choice(list(infos.items())) #choses a random tip, a pair attribute : value to show the user
        if attribute == 'name':
            pass
        elif attribute == 'last_changed':
            pass
        else:
            break
    # value = infos['abilities']

    if type(value) == list:                 #sometimes a value will be a list
        y = random.randint(0, len(value)-1)   #in which case, we chose a random position of the list to show as a tip
        chosen_value = value[y]
    else:
        chosen_value = value

    if type(chosen_value) == dict:
        chosen_value = chosen_value['name'] + ": " + chosen_value['description']

    if type(chosen_value) == NoneType:
        chosen_value = "None"


    chosen_tip = attribute + ": " + chosen_value

    return chosen_tip, attribute

def menu(champion, infos):
    points = 300 #user points, decreases by 10 each try

    sg.theme('DarkTeal10')

    # Define the layout of the window
    layout = [[sg.Text('Adivinhe o campeão:', font=("Spiegel", 20))],
            [sg.Input(do_not_clear=False, key='input',font=("Spiegel", 15))],
            [sg.Button('Vai!', font=("Spiegel", 15))],
            [sg.Multiline('', size=(70, 20), key='-DICA-', font=("Spiegel", 15))]]

    # Create the window
    window = sg.Window('Quem é Esse Campeão?', layout, finalize=True)
    window['input'].bind("<Return>", "_Enter")


    # Event loop to process events and get input from the user
    while True:
        event, guesses = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Vai!' or event == "input" + "_Enter":
            tentativa = main.normalize_champ_name(guesses['input']).lower() #normalizes user input
            if tentativa == champion.lower(): 
                sg.popup('Acertou!\nSua pontuação é:\n', points, title="Acertou!", font=("Spiegel",20))
                break
            else:
                points = points - 10
                if points <= 0:
                    points = 0
                while True: # only generates tips that werent given before
                    chosen_tip, attribute = generate_tip(infos)
                    if attribute in list_tips:
                        pass
                    else: 
                        list_tips.append(attribute)
                        break
                window['-DICA-'].update(f'{chosen_tip}\n{guesses["-DICA-"]}', font=("Spiegel", 15))

    # Close the window
    window.close()

if __name__ == '__main__':

    es = sender.Elastic()
    es.connect()

    champions = es.get_champ_indexes() #gets a list of all champions
    # print(champions)

    x = random.randint(0, len(champions)) #choses a random index
    champion = champions[x] # champion the user will have to guess
    # print("Champion:", champion)

    # champion = 'Anivia'

    infos = es.get_champ_info(champion.lower()) #gets a dictionary containing all info about a champion
    # print(infos)

    # print("Champion:", champion)
    # print(infos)
    # print(attribute, ":", value)
    # print("Type:", type(value))
    # print("CHOSEN TIP:", chosen_tip)
    
    menu(champion, infos)

# colocar uma opcao da versao do jogo