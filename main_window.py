import webbrowser
import sys
import subprocess
import os

import PySimpleGUI as sg

def inform_about_coords(coords: str):
    decoded_result = coords
    result_string = ""
    for char in decoded_result:
        if char.isalpha() or char == ',' or char == ' ':
            result_string += char

    result_array = result_string.split(',')
    if result_array[0] != "Success":
        sg.popup_ok(f"We could not find any results with given data!")
    else:
        for index in range(len(result_array)):
            if result_array[index] == "":
                result_array[index] = 'None'

        sg.popup_ok(f"City: {result_array[1]}\nVoivodeship: {result_array[2]}\nCountry:{result_array[3]}")

def get_check_input_data():
    global event, values, is_city_visible
    if is_city_visible:
        city = values['-CITY-INPUT-']
        county = values['-COUNTY-INPUT-']
        if county != "":
            status = detect_incorrect_chars("city",[city, county])
        else:
            status = detect_incorrect_chars("city",[city])

        return status, city, county

    else:
        latitude = values['-LATITUDE-INPUT-']
        longitude = values['-LONGITUDE-INPUT-']
        status = detect_incorrect_chars("coordinates",[latitude, longitude])

        return status, latitude, longitude

def detect_incorrect_chars(input_type: str, data_to_check: []):
    message_text = ""
    window['-MESSAGE1-'].update(message_text)
    window['-MESSAGE2-'].update(message_text)

    def return_false(info: str, message_index: int):
        message_text = info
        window[f'-MESSAGE{message_index}-'].update(message_text)
        return False

    for value in data_to_check:
        if value == "":
            return_false('Missing the data. Please fill the input field/fields.')
        else:
            for char in value:
                if input_type == "city":
                    if char.isdigit():
                        return return_false('Incorrect data. Please avoid using numbers in the input field.',1)
                    elif not char.isalpha():
                        return return_false('Incorrect data. Please avoid using special characters in the input field.',1)
                elif input_type == "coordinates":
                    if char == ',':
                        value = value.repalce(char, '.')

                    if char.isalpha():
                        return return_false('Incorrect data. Please avoid using letters in the input field.',2)
                    elif not char.isalnum() and char != '.':
                        return return_false('Incorrect data. Please avoid using special characters in the input field.',2)

    return True

from time import sleep

sg.theme('Reddit')  # Add a touch of color
font = ("Verdana", 12)
# All the stuff inside your window.
message_text = ""
message_color = 'red'
is_city_visible = True
is_coord_visible = False

col_data_left = [[sg.Text('Select by:')],
                  [sg.Radio("City name", "method", key='-CITY-',enable_events=True, default=True)],
                  [sg.Radio("Coordinates", "method", key='-COORD-', enable_events=True,)]]

col_data_right_city = [[sg.Text('City '), sg.InputText(key='-CITY-INPUT-')],
                       [sg.Text('County (optional) '), sg.InputText(key='-COUNTY-INPUT-')],
                       [sg.Text(message_text,text_color=message_color, key='-MESSAGE1-')]]

col_data_right_coord = [[sg.Text('Latitude '), sg.InputText(key='-LATITUDE-INPUT-')],
                        [sg.Text('Longitude '), sg.InputText(key='-LONGITUDE-INPUT-')],
                        [sg.Text(message_text,text_color=message_color, key='-MESSAGE2-')]]

layout = [[sg.Column([[sg.Text('\n Welcome!')]], element_justification='center', expand_x=True)],
          [sg.Column(col_data_left, vertical_alignment='c', element_justification='left', expand_x=True),
           sg.Column(col_data_right_city, vertical_alignment='c', element_justification='right', expand_x=True, visible=True, key='-CITY-COLUMN-'),
           sg.Column(col_data_right_coord, vertical_alignment='c', element_justification='right', expand_x=True, visible=False, key='-COORD-COLUMN-')],
          [sg.Column([[sg.Button('Set', key='-SET-', enable_events=True),
                       sg.Button('Find', key='-FIND-', enable_events=True),
                       #sg.Button('Notify now!', key='-NOTIFY-', enable_events=True),
                       sg.Button('Log out', key='-LOG-OUT-', enable_events=True)]], element_justification='center', expand_x=True)]]

# Create the Window
window = sg.Window('Rainsnow register', layout, icon='icons/mainIcon1.ico', font=font)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    message_text = ""

    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    elif event == "-CITY-":

        if is_coord_visible:
            message_text = ''
            window['-MESSAGE1-'].update(message_text)
            window['-CITY-COLUMN-'].update(visible=True)
            window['-COORD-COLUMN-'].update(visible=False)
            is_city_visible = True
            is_coord_visible = False

    elif event == "-COORD-":

        if is_city_visible:
            message_text = ''
            window['-MESSAGE2-'].update(message_text)
            window['-CITY-COLUMN-'].update(visible=False)
            window['-COORD-COLUMN-'].update(visible=True)
            is_city_visible = False
            is_coord_visible = True

    elif event == "-SET-":
        if is_city_visible:
            approved, city, county = get_check_input_data()
            if approved:
                completed_process = subprocess.run(
                    [sys.executable, "check_coords.py", "--set-city", f"{city}", f"{county}"],
                    capture_output=True,
                    text=True  # This specifies that the output should be in text (string) mode
                )

        else:
            approved, latitude, longitude = get_check_input_data()
            if approved:
                completed_process = subprocess.run(
                    [sys.executable, "check_coords.py", "--set-coords", f"{latitude}", f"{longitude}"],
                    capture_output=True,
                    text=True  # This specifies that the output should be in text (string) mode
                )

    elif event == "-FIND-":
        if is_city_visible:
            approved, city, county = get_check_input_data()
            if approved:
                completed_process = subprocess.run(
                    [sys.executable, "check_coords.py", "--check-city", f"{city}", f"{county}"],
                        capture_output=True,
                        text=True  # This specifies that the output should be in text (string) mode
                )
                result_str = completed_process.stdout.strip()
                inform_about_coords(result_str)

        else:
            approved, latitude, longitude = get_check_input_data()
            if approved:
                completed_process = subprocess.run(
                    [sys.executable, "check_coords.py", "--check-coords", f"{latitude}", f"{longitude}"],
                    capture_output=True,
                    text=True  # This specifies that the output should be in text (string) mode
                )
                result_str = completed_process.stdout.strip()
                inform_about_coords(result_str)

    elif event == "-LOG-OUT-":
        confirm = sg.popup_yes_no("Are you sure you want to log out?")
        if confirm == "Yes":
            pass
            #HEADLESS BROWSER TO LOG OUt
            #DELETE ACCOUNT DATA
            subprocess.Popen(['python', 'register_log_in.py'])
            sys.exit(0)


window.close()
