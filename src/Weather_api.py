import requests
from datetime import datetime

from config import weather_api_id


class Weather:

    # String -> String
    @staticmethod
    def reformat_time(time):
        ts = int(time)-3600
        return datetime.utcfromtimestamp(ts).strftime('%H:%M')

    # This func works with weather api, returns some today weather and an id of a picture of a weather.
    @staticmethod
    def get():
        api_url = 'https://api.openweathermap.org/data/2.5/weather'

        # params = {
        #     'q': 'Saint Petersburg',
        #     'appid': weather_api_id,
        #     'lang': 'ru',
        #     'units': 'metric'
        # }
        params = {
            'lat': 60,
            'lon': -30,
            'lang': 'ru',
            'units': 'metric',
            'appid': weather_api_id
        }

        res = requests.get(api_url, params=params)
        res = res.json()
        # print(res)
        text = f"Температура за окном +{res['main']['temp']}. " \
               f"Ощущается как {str(res['main']['feels_like'])}.\n {res['weather'][0]['description']}." \
               f" Солнце зайдет в {Weather.reformat_time(res['sys']['sunset'])} "
        icon_path = '../icons/{}@2x.png'.format(res['weather'][0]['icon'])
        return [text, icon_path]


if __name__ == '__main__':
    weather, picture_name = Weather.get()
    print(weather, picture_name)
