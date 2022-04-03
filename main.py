"""
1. День, с минимальной разницей "ощущаемой" и фактической температуры ночью (с указанием разницы в градусах Цельсия)
2. Максимальную продолжительностью светового дня (считать, как разницу между временем заката и рассвета) за ближайшие 5 дней
(включая текущий), с указанием даты.
"""

import requests
from re import search
from datetime import datetime


class Request:
    """
    Request class. Accepts params as input, that includes
    path, latitude, longitude and API key.
    Returns json response from openweather.
    """

    def __init__(self, path, lat, lon, key):
        self.url = f"https://api.openweathermap.org/data/2.5/{path}?lat={lat}&lon={lon}&appid={key}&units=metric"

    def get_json(self):
        response = requests.get(self.url)
        return response.json()


class Temperature:
    """
    Accepts json-like data as input.
    :_get_night_temp_difference: class method returns intervals with difference between "feels" and actual temperature at night
    :get_min_night_temp: returns the day with minimal temperature difference.
    """

    def __init__(self, data):
        self.data = data

    def show_min_night_temp(self, data=None):
        if data is None:
            data = self._get_night_temp_difference()
        min_temp = min(data.values())
        date = min(data, key=data.get)
        return f"{date:.10s} число, с минимальной разницей {min_temp:.2f} °C \"ощущаемой\" и фактической температуры ночью"

    def _get_night_temp_difference(self) -> dict:
        night_intervals = {}
        for index in self.data["list"]:
            if search('00:00:00', index["dt_txt"]) or search('03:00:00', index["dt_txt"]):  # processing only night time
                actual_temp = index["main"]["temp"]
                feel_temp = index["main"]["feels_like"]
                txt_time = index["dt_txt"]
                temp_diff = abs(actual_temp - feel_temp)
                night_intervals[txt_time] = temp_diff
        return dict(night_intervals)


class DaylightTime:
    """
    Accepts json-like data as input.
    :_get_sun_time_days: class method returns daylight hours for 5 days (including current day)
    :get_daylight: representation of daylight hours for 5 days
    """

    def __init__(self, data):
        self.data = data

    def show_daylight(self):
        daylight = self._get_sun_time_days()
        for key, val in daylight.items():
            print("День " + key + " имеет продолжительность " + val + " светового дня")

    def _get_sun_time_days(self) -> dict:
        daylight = {}
        for counter, index in enumerate(self.data["daily"], 1):
            sunset = index["sunset"]
            sunrise = index["sunrise"]
            date = datetime.utcfromtimestamp(sunrise).strftime(f"%Y-%m-%d")
            sun_length = (sunset - sunrise)
            sun_length = datetime.utcfromtimestamp(sun_length).strftime(f"%H:%M:%S")
            daylight[date] = sun_length
            if counter == 5: break  # for 5 days
        return dict(daylight)


if __name__ == "__main__":
    # params
    # city = "Saint Petersburg,RU"
    path = "forecast"
    lat, lon = 59.8944, 30.2642
    key = "9eb2769f106028251c21cc4db140aca3"

    # min night temperature difference request
    req = Request(path=path, lat=lat, lon=lon, key=key).get_json()
    min_night_temp = Temperature(req).show_min_night_temp()
    print(min_night_temp)

    # daylight request
    path = "onecall"
    req1 = Request(path=path, lat=lat, lon=lon, key=key).get_json()
    DaylightTime(req1).show_daylight()
