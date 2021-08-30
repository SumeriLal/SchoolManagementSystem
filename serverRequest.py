import requests
from datetime import datetime
import json
baseUrl = "https://bhl-ams.herokuapp.com"

# device login
login_url = f"{baseUrl}/auth/local"
response = requests.post(login_url, json={'identifier':'dev01@gmail.com', 'password':'dev01bhl'})

# device

postUrl = f"{baseUrl}/attendances"



time_now  = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')

authorization = f"Bearer {response.json()['jwt']}"
json = {"date_time": time_now, "student": "1"}
headers = {"Authorization": authorization} 
post_res = requests.post(postUrl, json=json,headers=headers )

print(post_res.text)   
