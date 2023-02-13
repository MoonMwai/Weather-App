from django.shortcuts import render
import requests
from .models import City
from .form import CityForm
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()

def index(request):
    API_KEY=os.getenv("API_KEY")
    cities = City.objects.all().order_by('-created_at') #return all the cities in the database
    city = "Nairobi"
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
   
    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        if form.is_valid():
            city = form.cleaned_data['name']
            existing_city = City.objects.filter(name=city).first()
            if not existing_city:
                form.save()

    form = CityForm()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url).json() #request the API data and convert the JSON to Python data types

        weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }

        weather_data.append(weather) #add the data for the current city into our list
    return render(request, 'weather/index.html', {'weather_data' : weather_data, 'weather' : weather, 'form' : form}) #returns the index.html template


def weather_details(request, city_name):
    if request.method == 'POST':
        city_name = request.POST['city']

    API_KEY=os.getenv("API_KEY")
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&units=metric&appid={API_KEY}'
    three_hour_url = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={API_KEY}'
    url_5day = f'http://api.openweathermap.org/data/2.5/forecast?q={city_name}&units=metric&appid={API_KEY}'

    city_weather = requests.get(url).json()
    three_hour_weather = requests.get(three_hour_url).json()
    five_day_weather = requests.get(url_5day).json()
    city = city_name

    weather_data = []
    weather = {
            'city' : city,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
    weather_data.append(weather)
    three_hour_data = []
    for i in three_hour_weather['list']:
        dt = datetime.strptime(i['dt_txt'], "%Y-%m-%d %H:%M:%S")
        formatted_dt = dt.strftime("%I:%M %p")        
        three_hours = {
            'time': formatted_dt,
            'temperature': i['main']['temp'],
            'description': i['weather'][0]['description'],
            'icon': i['weather'][0]['icon']
        }
        three_hour_data.append(three_hours)

    

    five_day_weather_data = []
    for day in five_day_weather['list']:
        if "09:00:00" in day['dt_txt']:
            dt = datetime.strptime(day['dt_txt'], "%Y-%m-%d %H:%M:%S")
            formatted_dt = dt.strftime("%A, %B %d")
            weather5 = {
                'date_time': formatted_dt,
                'temperature': day['main']['temp'],
                'description': day['weather'][0]['description'],
                'icon': day['weather'][0]['icon']
            }
            five_day_weather_data.append(weather5)
       
    return render(request, 'weather/weather.html', {
        'city_name': city_name,
        'weather_data': weather_data,
        'three_hour_data': three_hour_data,
        'five_day_weather_data': five_day_weather_data,
        'city': city_name,
    })
