import datetime
import json
import urllib.request

def url_builder(lat, lon):
    user_api = '2975d8fae93d5fb86bc1e9f0349a3500'  
    unit = 'metric'
    return 'http://api.openweathermap.org/data/2.5/weather' + \
           '?units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat) +  \
           '&lon=' + str(lon)

def url_builder(lat2, lon2):
    user_api = '2975d8fae93d5fb86bc1e9f0349a3500'  
    unit = 'metric'
    return 'http://api.openweathermap.org/data/2.5/weather' + \
           '?units=' + unit + \
           '&APPID=' + user_api + \
           '&lat=' + str(lat2) +  \
           '&lon=' + str(lon2)


def fetch_data(full_api_url):
    url = urllib.request.urlopen(full_api_url)
    output = url.read().decode('utf-8')
    return json.loads(output)
    
def time_converter(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d %b %I:%M %p')

lon = input("Please enter your first longitudinal coordinate: ")
lat = input("Please enter your first latitudinal coordinate: ")
json_data = fetch_data( url_builder(lat, lon) )



temperature = str( json_data['main']['temp'] )
location = json_data['name']
print("Location 1")
location1 = str(location + " : " + temperature + "'C")
print(location1)


lon2 = 26.8206
lat2 = 30.8025
json_data2 = fetch_data (url_builder(lat2, lon2))
temperature2 = str( json_data2['main']['temp'])
location_2 = json_data2['name']

location2 = str(location_2 + " : " + temperature2 + "'C")
print("Location 2: ")
print(location2)

if json_data['main']['temp'] > json_data2['main']['temp']:
    print(location + " is hotter than " + location_2)
else:
    print(location_2 + " is hotter than " + location)

