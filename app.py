from flask import Flask, render_template, request
import requests
from jinja2 import Template

app = Flask(__name__)


def render_weather_page(city, temperature, pressure, humidity, wind_speed):
    # Load the weather template
    with open('templates/weather.html', 'r') as file:
        template_content = file.read()
    
    # Create a Jinja2 Template object
    template = Template(template_content)
    
    # Render the template with the provided data
    rendered_html = template.render(city=city, temperature=temperature, pressure=pressure,
                                    humidity=humidity, wind_speed=wind_speed)
    
    # Save the rendered HTML content to a static HTML file
    with open(f'static/{city}_weather.html', 'w') as output_file:
        output_file.write(rendered_html)


def fetch_weather_data(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=a35cfae53c781d8331f68e88fbc411e1"
    response = requests.get(url)
    data = response.json()

    temperature = round(data['main']['temp'] - 273.15)
    pressure = data['main']['pressure']
    humidity = data['main']['humidity']
    wind_speed = round(data['wind']['speed'] * 3.6)

    return temperature, pressure, humidity, wind_speed


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['POST'])
def weather():
    city = request.form['city']
    
    # Fetch weather data
    temperature, pressure, humidity, wind_speed = fetch_weather_data(city)
    
    # Render and save weather page
    render_weather_page(city, temperature, pressure, humidity, wind_speed)
    
    # Return a response
    return f"Weather page for {city} generated! Check <a href='/static/{city}_weather.html'>here</a>."


if __name__ == '__main__':
    app.run('0.0.0.0')
