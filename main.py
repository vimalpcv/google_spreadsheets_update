import requests, os
from datetime import datetime


# Nutritionix API   : https://www.nutritionix.com/business/api
# Nutritionix Home  : https://developer.nutritionix.com/admin
# Nutritionix API documentation : https://docs.google.com/document/d/1_q-K-ObMTZvO0qUEAxROrN3bwMujwAN25sLHwJzliK0/preview

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
headers = {
    "x-app-id": os.environ.get("APP_ID", 'd7ffe3c6'),
    "x-app-key": os.environ.get("APP_KEY", '02b9e0a8646a4b9eeecc33d989a7a55b')
}
exercise_text = input("Tell me which exercises you did: ")

gender = 'male'
weight_kg = 85
height_cm = 183
age = 28

params = {
    'query':exercise_text, 
    'gender':gender,
    'weight_kg':weight_kg,
    'height_cm':height_cm,
    'age':age
}

response = requests.post(exercise_endpoint, json=params, headers=headers)
result = response.json()
data_set = []
date = datetime.strftime(datetime.now(), '%d/%m/%Y')
time = datetime.strftime(datetime.now(), '%H:%M:%S')
for data in result['exercises']:
    data = {
        'date': date,
        'time': time,
        'exercise': data['name'].title(),
        'duration': data['duration_min'],
        'calories': data['nf_calories']
    }

    # create project in sheety => https://dashboard.sheety.co/
    # spreadsheet link => https://docs.google.com/spreadsheets/d/1yTnmeic3np05O2wuK3BoKgtHMDOKQrmxyy8ScbCJ9zE/edit#gid=0

    sheet_endpoint = 'https://api.sheety.co/e827b7bd165502344cd84c0db5bf0e8a/myWorkouts/workouts'
    sheet_headers = {'Authorization': f'Bearer {os.environ.get("SHEETY_TOKEN", "my_secret_token")}'}
    update_request = requests.post(url=sheet_endpoint, headers=sheet_headers, json={'workout': data})
    update_response = update_request.json()
    print(update_response)
    print('Sheet updated')
