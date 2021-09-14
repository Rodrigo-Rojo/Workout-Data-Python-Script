import requests
import datetime as dt
import os

API_KEY = os.getenv("API_KEY")
API_ID = os.getenv("API_ID")
API_URL = "https://trackapi.nutritionix.com"
SHEETY_API = os.getenv("SHEETY_API")
exercise_endpoint = "/v2/natural/exercise"
sheety_url = "https://api.sheety.co/413dff96600cab6a40f9796d103e1da2/myWorkouts/workouts"
today = dt.datetime.today()
today_strftime = today.strftime("%d/%m/%Y")
time = today.strftime("%H:%M:%S")

header = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json",
    "x-remote-user-id": "0"
}

user_input = input("Tell me which exercises you did: ")

params = {
     "query": user_input,
     "gender": "male",
     "weight_kg": 72.5,
     "height_cm": 167.64,
     "age": 30
}
sent = False
while not sent:
    try:
        res = requests.post(url=f"{API_URL}{exercise_endpoint}", json=params, headers=header)
        res.raise_for_status()
        data = res.json()
        exercise = data["exercises"][0]["name"].title()
        duration = data["exercises"][0]["duration_min"]
        calories = data["exercises"][0]["nf_calories"]
    except:
        pass
    else:
        sent = True

sheety_params = {
    "workout": {
        "date": today_strftime,
        "time": time,
        "exercise": exercise,
        "duration": duration,
        "calories": calories
    }
}

sheety_header = {
    "Authorization": SHEETY_API
}
sheet_sent = False
while not sheet_sent:
    try:
        res = requests.post(url=sheety_url, json=sheety_params, headers=sheety_header)
        res.raise_for_status()
        data = res.text
        print(data)
    except:
        pass
    else:
        sheet_sent = True

