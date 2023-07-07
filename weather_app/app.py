from flask import Flask, render_template, request
import requests
import gtts
import playsound
from multiprocessing import Process
import base64


app = Flask(__name__)

def play_fun(temp, max_temp, min_temp, city_name):
    text = f"The current temperature in {city_name} is {temp} degrees, maximum temperature is {max_temp} degrees, and minimum is {min_temp} degrees."
    sound = gtts.gTTS(text, lang="en")
    sound.save("forecast.mp3")
    playsound.playsound("forecast.mp3")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city_name = request.form['name']
        # print(city_name)
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&APPID=579d31302c9ef3c1ec0a685880940718'
        response = requests.get(url.format(city_name)).json()
        temp = response['main']['temp']
        weather = response['weather'][0]['description']
        min_temp = response['main']['temp_min']
        max_temp = response['main']['temp_max']
        icon = response['weather'][0]['icon']
        p1 = Process(target=play_fun, args=(temp, max_temp, min_temp, city_name))
        p1.start()
        return render_template('index.html', temp=temp, weather=weather, min_temp=min_temp, max_temp=max_temp, icon=icon, city_name=city_name)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)