from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    url = f"https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=a35cfae53c781d8331f68e88fbc411e1"
    response = requests.get(url)
    data = response.json()

    temperature = round(data['main']['temp'] - 273.15)
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = round(data['wind']['speed'] * 3.6)

    return render_template('weather.html', city=city, temperature=temperature, pressure=pressure, humidity=humidity,
                           wind_speed=wind_speed)


if __name__ == '__main__':
    app.run('0.0.0.0')
