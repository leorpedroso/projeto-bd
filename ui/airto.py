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

normalize = {
    'health':"vida", 
    'health_regen':"regeneração de vida", 
    'resource':"recurso", 
    'resource_regen': "resource_regen", 
    'armor': "armadura",
    'magic_resist': "resistencia magica",
    'attack_damage': "dano de ataque",
    'mov_speed': "velocidade de movimento", 
    'range': "alcance",
    'store_price_be': "custo em essencias azuis",
    'store_price_rp': "custo em essencias laranjas",
    'class':"classes",
    'position': "posições",
    'range_type': "tipos de alcance",
    'adaptive_type': "tipos de dano",
    'region': "regiões"
}

def generate_trivia():
    numeric_att = ['health', 'health_regen', 'resource', 'resource_regen', 'armor', 'magic_resist',
                    'attack_damage', 'mov_speed', 'range', 'store_price_be', 'store_price_rp']

    non_numeric = ['crit_damage', 'release_date']

    atts = es.get_attributes()
   
    attribute, value = random.choice(list(atts.items())) #chooses a random attribute
    
    if attribute in numeric_att:
        # chooses between lowest or highest
        choice = random.randint(0, 1)

        name = es.get_champ_from_att(attribute, value[choice]) #get the corresponding champion with that attribute:value

        attribute_normalized = normalize[attribute]

        if choice:
            l = 'maior'
        else:
            l = 'menor'

        # print(f'O campeão com {l} {attribute_normalized} é {name}: {value[choice]}')
        trivia = f'O campeão com {l} {attribute_normalized} é {name}: {value[choice]}'

    elif attribute not in non_numeric:
        attribute_normalized = normalize[attribute]
        # print(f'Existem {len(value)} {attribute_normalized} no jogo: {", ".join(value)}')
        trivia = f'Existem {len(value)} {attribute_normalized} no jogo: {", ".join(value)}'

    else:
        # print(f'League of Legends foi lançado oficialmente em 27 de outubro de 2009' )
        trivia = f'League of Legends foi lançado oficialmente em 27 de outubro de 2009'

    return trivia

def generate_tip(infos):
    while True:
        attribute, value = random.choice(list(infos.items())) #chooses a random tip, a pair attribute : value to show the user
        if attribute == 'name':
            pass
        elif attribute == 'last_changed':
            pass
        else:
            break
    # value = infos['abilities']

    if type(value) == list:                 #sometimes a value will be a list
        y = random.randint(0, len(value)-1) #in which case, we choose a random position of the list to show as a tip
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
            [sg.Button('Vai!', font=("Spiegel", 15)), sg.Button("Trivia!", font=("Spiegel", 15))],
            [sg.Multiline('', size=(70, 20), key='-DICA-', font=("Spiegel", 15))]]

    # Create the window
    window = sg.Window('Quem é Esse Campeão?', layout, finalize=True)
    window['input'].bind("<Return>", "_Enter")


    # Event loop to process events and get input from the user
    while True:
        event, guesses = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Trivia!':
            trivia = generate_trivia()
            sg.popup(f"{trivia}", title="Trivia", font=("Spiegel",20))
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