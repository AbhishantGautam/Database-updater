import time
import psycopg2
from psycopg2.extras import RealDictCursor
import json
import requests


url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q":"30.7333,76.7794"}

headers = {
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com",
    'x-rapidapi-key': "not_to_disclosed"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

current_weather = (response.text)

f = json.loads(current_weather)

datetime = f['current']['last_updated'].split(" ")[0]
temp = f['current']['temp_c']
feelslike = f['current']['feelslike_c']
humidity = f['current']['humidity']
precip = f['current']['precip_mm']
windspeed = f['current']['wind_kph']
winddir = f['current']['wind_degree']
sealevelpressure = f['current']['pressure_mb']
visibility = f['current']['vis_km']

dict_1 ={
    'temp' : temp,
    'feelslike' : feelslike,
    'humidity' : humidity,
    'precip' : precip,
    'windspeed' : windspeed,
    'winddir' : winddir,
    'sealevelpressure' : sealevelpressure,
    'visibility' : visibility
}
# dict_1 ={'temp' : temp,'feelslike' : feelslike,'humidity' : humidity,'precip' : precip,'windspeed' : windspeed,'winddir' : winddir,'sealevelpressure' : sealevelpressure,'visibility' : visibility}
# feed = json(dict_1)
 #API request

URL = 'https://abhi-weather-api.herokuapp.com/'
resp = requests.post(URL, json=dict_1)
# print(dict(resp.text)[0][8])

pred_temperature = json.loads(resp.text)
predicted_temperature = pred_temperature['data']['pred_temp']

# Connecting to postgres database using psycopg2
while True:
    try:
        conn = psycopg2.connect(host='ec2-54-158-247-97.compute-1.amazonaws.com', database='dad725bctfvgr', user='vuxxchsiudjzcq', password='not_to_be_disclosed', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('database connection was successful')
        break
    except Exception as error:
        print('Connection to database failed')
        print('Error',error)
        time.sleep(20)
cursor.execute(""" INSERT INTO mytable(datetime,temp,feelslike,humidity,precip,windspeed,winddir,sealevelpressure,visibility,pred_temp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); """,(datetime,temp,feelslike,humidity,precip,windspeed,winddir,sealevelpressure,visibility,predicted_temperature))
conn.commit()
