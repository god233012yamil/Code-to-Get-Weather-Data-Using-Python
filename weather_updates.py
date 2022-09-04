# OpenWeather API link : https://openweathermap.org/api
# OpenWeather API Documents link: https://openweathermap.org/api/one-call-3
# OpenWeather API keys link: https://home.openweathermap.org/api_keys

# The OpenWeather API response is a json object that looks like:
"""
{
'coord': {'lon': -80.1937, 'lat': 25.7743},
'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04d'}],
'base': 'stations',
'main': {'temp': 304.54, 'feels_like': 311.49, 'temp_min': 303.15, 'temp_max': 305.94, 'pressure': 1018, 'humidity': 69},
'visibility': 10000,
'wind': {'speed': 3.09, 'deg': 70},
'clouds': {'all': 75},
'dt': 1662216363,
'sys': {'type': 2, 'id': 2009435, 'country': 'US', 'sunrise': 1662202923, 'sunset': 1662248318},
'timezone': -14400,
'id': 4164138,
'name': 'Miami',
'cod': 200
}
"""

"""
How to make an API call API call?
https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={lat}&lon={lon}&dt={time}&appid={API key}
"""

# Import required modules.
import requests
from bs4 import BeautifulSoup
from prettytable import PrettyTable
from config import OPENWEATHER_API_KEY


def get_weather_data_using_openweather_api(city: str) -> None:
    """
    Convenience function to get current weather data for a city.
    :param city: City to get for.
    :return: None
    """
    # Define the API endpoint URL.
    endpoint_url = "http://api.openweathermap.org/data/2.5/weather?appid={0}&q={1}".format(OPENWEATHER_API_KEY, city)
    print(endpoint_url)
    try:
        # Sends a GET request.
        response = requests.get(url=endpoint_url)
        # Returns True if status_code is less than 400.
        if response.ok:
            # Get the json-encoded content of a response, if any.
            response_json = response.json()
            # Get the value of the "main" key.
            main = response_json["main"]
            # Get the value of "temp" key.
            temperature_kelvin = main["temp"]
            # Get the value of "pressure" key.
            pressure = main["pressure"]
            # Get the value of "humidity" key.
            humidity = main["humidity"]
            # Get the value of "weather" key.
            weather = response_json["weather"]
            # Get the value of weather "description" key.
            description = weather[0]["description"]
            # Get the value of "coord" key.
            coordinates = response_json["coord"]
            # Get the value of coordinates "lon" key.
            longitude = coordinates["lon"]
            # Get the value of coordinates "lat" key.
            latitude = coordinates["lat"]
            # Show the current weather data available for passed city.
            print("Temperature = {0} kelvin = {6:.2f} celsius\n"
                  "Atmospheric pressure (hPa) = {1}\n"
                  "Humidity (%) = {2}\n"
                  "Weather description = {3}\n"
                  "Longitude = {4}\n"
                  "Latitude = {5}".format(temperature_kelvin,
                                          pressure,
                                          humidity,
                                          description,
                                          longitude,
                                          latitude,
                                          temperature_kelvin - 273.15))
        else:
            print("Weather data for city: {0} wasn't found".format(city))
    except requests.exceptions.ConnectionError as e:
        print("A connection error took place: \n{0}".format(e))
    except requests.exceptions.HTTPError as e:
        print("An HTTP error occurred.: \n{0}".format(e))
    except requests.exceptions.Timeout as e:
        print("The request timed out.: \n{0}".format(e))
    except requests.exceptions.JSONDecodeError as e:
        print("The response body does not contain valid json.: \n{0}".format(e))


def get_weather_data_using_google(city: str) -> None:
    # Replace any space character with a plus sign (+) character.
    city_parsed = city.replace(" ", "+")
    # Google parameters.
    q = "{0} weather".format(city_parsed)
    oq = "{0} weather".format(city_parsed)
    sourceid = "chrome"
    ie = "UTF-8"
    # Define the end url.
    base_url = "https://www.google.com/search?q={0}&oq={1}&sourceid={2}&ie={3}".format(q, oq, sourceid, ie)
    # Define the request get method header.
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Content-Language': 'en-US,en;q=0.5'
    }
    try:
        # Sends a GET request.
        response = requests.get(
            url=base_url,
            headers=headers
        )
        # Returns True if status_code is less than 400.
        if response.ok:
            # Parse the response using BeautifulSoup.
            response_soup = BeautifulSoup(response.text, 'html.parser')
            # Extract the location.
            location = response_soup.find(name="div", attrs={"id": "wob_loc"}).text
            # Extract the day hour.
            time = response_soup.find(name="div", attrs={"id": "wob_dts"}).text
            # Extract the weather now.
            weather_now = response_soup.find(name="span", attrs={"id": "wob_dc"}).text
            # Extract the temperature now.
            temperature = response_soup.find(name="span", attrs={"id": "wob_tm"}).text
            # Extract the Precipitations.
            precipitations = response_soup.find(name="span", attrs={"id": "wob_pp"}).text
            # Extract the humidity.
            humidity = response_soup.find(name="span", attrs={"id": "wob_hm"}).text
            # Extract the wind.
            wind = response_soup.find(name="span", attrs={"id": "wob_ws"}).text
            # Show Today weather data.
            print("Location: {0}\n"
                  "Time: {1}\n"
                  "Weather now: {2}\n"
                  "Temperature now: {3}\n"
                  "Precipitations: {4}\n"
                  "Humidity: {5}\n"
                  "Wind: {6}".format(location,
                                     time,
                                     weather_now,
                                     temperature,
                                     precipitations,
                                     humidity, wind))
            # Crete a Table to show the weather data.
            table = PrettyTable(["Day", "Weather", "Max Temp(C)", "Min Temp(C)"])
            # Get weather data for week ahead.
            days = response_soup.find("div", attrs={"id": "wob_dp"})
            for day in days.findAll("div", attrs={"class": "wob_df"}):
                # extract the name of the day
                day_name = day.findAll("div")[0].attrs['aria-label']
                # get weather status for that day
                weather = day.find("img").attrs["alt"]
                temp = day.findAll("span", {"class": "wob_t"})
                # Maximum temperature in Celsius, use temp[1].text
                # if you want fahrenheit
                max_temp = temp[0].text
                # Minimum temperature in Celsius, use temp[3].text
                # if you want fahrenheit
                max_temp = temp[2].text
                # Add a row to the table.
                table.add_row([day_name, weather, max_temp, max_temp])
            # Print a table with weather data for week ahead.
            print(table)
        else:
            print("Weather data for city: {0} wasn't found".format(city))
    except requests.exceptions.ConnectionError as e:
        print("A connection error took place: \n{0}".format(e))
    except requests.exceptions.HTTPError as e:
        print("An HTTP error occurred.: \n{0}".format(e))
    except requests.exceptions.Timeout as e:
        print("The request timed out.: \n{0}".format(e))
    except IndexError as e:
        print("List index out of range.: \n{0}".format(e))
    except AttributeError as e:
        print("Attribute Error.: \n{0}".format(e))


if __name__ == '__main__':
    get_weather_data_using_google("Coral Gables, Florida, USA")
