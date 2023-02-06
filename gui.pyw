import PySimpleGUI as sg
layout = [[sg.Text('My one-shot Window, ')],
          [sg.InputText()],
          [sg.Submit(), sg.Cancel()]]
window = sg.Window('Window Title', layout)

event, values = window.read()
window.close()

text_input = values[0]
sg.popup('you entered' , text_input)