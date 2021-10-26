import datetime
import json
import urllib.request

def url_builder(lat1, lon1):
    user_api = '2975d8fae93d5fb86bc1e9f0349a3500'  
    unit = 'metric'
    return 'http://api.openweathermap.org/data/2.5/weather' + \
           '?units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat1) +  \
           '&lon=' + str(lon1)


def fetch_data(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)
    
def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')

lon1= -6.675298
lat1 = 55.147872
json_data = fetch_data( url_builder(lat1, lon1) )

temperature = str( json_data['main']['temp'] )
timestamp = time_converter( json_data['dt'] )
description = json_data['weather'][0]['description']
location = json_data['name']
sunsetTime = time_converter( json_data['sys']['sunset'])
print("Current weather")
print(timestamp + " : " + temperature + " : " + location + " : " + description + " : " + sunsetTime)