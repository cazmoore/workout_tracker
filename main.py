import config
import requests
from datetime import datetime

now = datetime.now()

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_url = "https://api.sheety.co/edd4f12c447d43ee70ed0c3f3cf09b20/myWorkouts/workouts"

exercise_params = {
    "query": "Ran 3 miles",
    "gender": "female",
    "weight_kg": 72.5,
    "height_cm": 167,
    "age": 42
}

headers = {
    "x-app-id": config.APP_ID,
    "x-app-key": config.APP_KEY,
    "x-remote-user-id": "0"
}

response = requests.post(nutritionix_endpoint, exercise_params, headers=headers)
result = response.json()

today_date = now.strftime("%d/%m/%y")
today_time = now.strftime("%H:%M:%S")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": today_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    bearer_headers = {
        "Authorization": f"Bearer {config.BEARER_HEADER}"
    }

    sheet_response = requests.post(sheety_url, json=sheet_inputs, headers=bearer_headers)

    print(sheet_response.text)