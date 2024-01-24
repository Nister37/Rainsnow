import webbrowser
import sys
import subprocess

import PySimpleGUI as sg

from time import sleep

sg.theme('Reddit')  # Add a touch of color
font = ("Verdana", 12)
# All the stuff inside your window.
message_text = ""
message_color = 'red'

col_layout_center = [[sg.Text('\nLog In')],
                     [sg.Text(message_text, text_color=message_color, key='-MESSAGE-')]]
col_layout_right = [[sg.Text('Username or e-mail address'), sg.InputText(key='-USERNAME-')],
                    [sg.Text('Password'), sg.InputText(key='-PASSWORD-', password_char='*')]]

layout = [[sg.Text('In order to use this function you need to register your account on: ')],
          [sg.Text('https://developer.accuweather.com/user/register', enable_events=True, key='-LINK-',
                   text_color='blue')],
          [sg.Column(col_layout_center, element_justification='center', expand_x=True)],
          [sg.Column(col_layout_right, element_justification='right', expand_x=True)],
          [sg.Column([[sg.Button('Log In', key='-SEND_DATA-', enable_events=True)]], element_justification='center',
                     expand_x=True)]]

# Create the Window
window = sg.Window('Rainsnow register', layout, icon='icons/mainIcon1.ico', font=font)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    message_text = ""

    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == "-LINK-":
        webbrowser.open('https://developer.accuweather.com/user/register')
    elif event == "-SEND_DATA-":
        data_correct = True
        username_email = values['-USERNAME-']
        user_password = values['-PASSWORD-']

        if len(username_email) == 0:
            message_text += "Please enter your username or email. "
            data_correct = False

        if len(user_password) == 0:
            message_text += "Please enter your password. "
            data_correct = False

        if data_correct:
            message_color = 'black'
            window['-MESSAGE-'].update("Trying to log in... Be patient.")
            window.refresh()
            message_color = 'red'
            sleep(0.5)
            received_data = subprocess.check_output([sys.executable, "headless_browser.py", f"{username_email}",
                                                     f"{user_password}"])
            data = received_data[:-2].decode('utf-8')

            if data == "Could not log in! The account might not exist or the network is unstable.":
                message_text = data
            else:
                subprocess.Popen(['python', 'main_window.py'])
                sys.exit(0)
            print(data)

        window['-MESSAGE-'].update(message_text)

window.close()
