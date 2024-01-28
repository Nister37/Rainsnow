import requests
import os
import datetime

import control_files as cf

from winotify import Notification
from winotify import audio

from time import sleep

first_time_launch = True
notified = False
tickrate = 30
LATITUDE = 51
LONGITUDE = 39
API_KEY = "zrb4rC9Bg1u67o9uFX6UZm06sRcOdCRL"

def receive_data(j_data):
    print(j_data)
    try:
        j_data["Message"] == "The allowed number of requests has been exceeded."
        message = "The allowed number of requests has been exceeded."
        weather_type, fall_type, phrase, url = "", "", "", ""
    except:
        data = j_data["Summary"]["Phrase"]
        weather_type = ""

        if "No" in data:
            weather_type = "Nothing"
        elif "starting" in data:
            weather_type = "Coming"
        elif "at least" in data:
            weather_type = "Currently"

        data = int(j_data["Summary"]["TypeId"])

        fall_type = ""
        if data == 1:
            fall_type = "rain"
        elif data == 2:
            fall_type = "snow"
        else:
            fall_type = ""

        if weather_type == "Currently":
            fall_type += "ing"

        phrase = j_data["Summary"]["Phrase"]
        url = j_data["Link"]
        message = "Success."

    return message, weather_type, fall_type, phrase, url


def send_notification(header_part_1: str, header_part_2: str, content: str, radar_url: str):
    toast = Notification(
        title=header_part_1 + header_part_2,
        msg=content,
        app_id="Snowrain",
        icon=os.path.abspath('Rainsnow//icons//mainIcon1.ico')
    )

    toast.set_audio(audio.Mail, loop=False)
    toast.duration = 'long'
    if radar_url != "":
        toast.add_actions(
            label="See it on the radar!",
            launch=radar_url
        )
    toast.show()

def send_request(latitude: float, longitude: float, api_key: str):
    response = requests.get(
        f'http://dataservice.accuweather.com/forecasts/v1/minute.json?q={latitude},{longitude}&apikey={api_key}')
    print(response)
    return response

def control_notifications():
    global first_time_launch, last_notification_time
    if first_time_launch:
        cf.read_time()

        first_time_launch = False
        last_notification_time = datetime.datetime.now()-datetime.timedelta(minutes=50)

    if last_notification_time+datetime.timedelta(seconds=10) < datetime.datetime.now():
        last_notification_time = datetime.datetime.now()
        cf.save_time(last_notification_time)

        server_response = send_request(LATITUDE,LONGITUDE,API_KEY)
        message, weather_type, fall_type, phrase, url = receive_data(server_response.json())

        if message == "Success.":
            send_notification(weather_type, fall_type, phrase, url)
        elif message == "The allowed number of requests has been exceeded.":
            send_notification("Oh no!", "",
                              "You have used all of the requests per day. This means you will not be notified about "
                              "upcoming weather changes until the next day appears!", "")
            return 0
    else:
        pass

"""arg1: float, arg2: float, arg3: str"""
def main():
    cf.save_time(datetime.datetime.now())
    print(cf.read_time())
    while True:
        control_notifications()
        sleep(3)


if __name__ == '__main__':
    main()
