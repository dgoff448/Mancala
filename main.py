import PySimpleGUI as sg
import mancalaGame


sg.theme("DarkGrey12")
layout = []
layout.append([sg.VPush()])
layout.append([sg.Text("Mancala", font=('Arial', 25, 'bold'))])
layout.append([sg.Text("Game Mode:", font=('Arial', 15, 'bold'), pad=(0, 0))])
layout.append([sg.Radio("Normal", 'gMode', key='norm', default=True), 
               sg.Radio("Long", 'gMode', key='long'),
               sg.Radio("Random", 'gMode', key='rand')])
layout.append([sg.Button("Play", key='play', size=(10, 1), font=("Arial", 20, "bold"))])
layout.append([sg.Button("Quit", key='quit', size=(10, 1), font=("Arial", 20, "bold"))])
layout.append([sg.VPush()])


layout.append([sg.Text("", font=('Arial', 30, 'bold'), text_color='gold')])
layout.append([sg.Button("New Game", key='-newGame-', visible=False)])

window = sg.Window("Mancala", layout, size=(1000,500), finalize=True, element_padding=(0,20), element_justification='c')


while True:
    event, values = window.read()
    if event == None:
        quit()
    elif event == 'quit':
        quit()
    elif event == 'play':
        if values['norm']:
            mancalaGame.start('norm')
        elif values['long']:
            mancalaGame.start('long')
        elif values['rand']:
            mancalaGame.start('rand')
