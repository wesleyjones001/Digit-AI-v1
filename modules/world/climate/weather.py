from common import preprocessing
import datetime
from common import module_testing
import requests

global module_version
module_version = "v1.0.0"


def check_input(data: str, memory: list) -> float:
    score = 0
    data = preprocessing.process(data)
    if "weather" in data:
        score = 2
    if "temperature" in data:
        score += 3
    if "how is the" in data:
        score += 2
    if "what is the" in data:
        score += 1
    if " the temp" in data:
        score += 6
    if " the weather" in data:
        score += 6
    if "the climate" in data:
        score += 1
    return score


def parse_(data, sep):
    suffixes = ["today", "tomorrow", "next", "this", "on "]
    x1 = data[data.index(sep) + len(sep):].lower()
    a1 = x1.split()
    date_to_check = None
    if x1 == "":
        date_to_check = datetime.date.today()
    if "like" in a1:
        a1.remove("like")
    location = ' '.join(a1[0:])
    for index, item in enumerate(a1):
        for index2, item2 in enumerate(suffixes):
            if item == item2:
                location = ' '.join(a1[0:index])
                if index2 == 0:
                    date_to_check = datetime.date.today()
                    break
                if index2 == 1:
                    date_to_check = datetime.date.today() + datetime.timedelta(days=1)
                    break
                if index2 == 2:
                    string = (' '.join(a1[index:]))[len(item2):].strip().lower()
                    day = -1
                    if string == "monday":
                        day = 0
                    elif string == "tuesday":
                        day = 1
                    elif string == "wednesday":
                        day = 2
                    elif string == "thursday":
                        day = 3
                    elif string == "friday":
                        day = 4
                    elif string == "saturday":
                        day = 5
                    elif string == "sunday":
                        day = 6
                    else:
                        return None
                    days = (day - datetime.date.today().weekday() + 7) % 7
                    date_to_check = datetime.date.today() + datetime.timedelta(days=days)
                    if date_to_check == datetime.date.today():
                        date_to_check += datetime.timedelta(days=7)
                if index2 == 3:
                    string = (' '.join(a1[index:]))[len(item2):].strip().lower()
                    day = -1
                    if string == "monday":
                        day = 0
                    elif string == "tuesday":
                        day = 1
                    elif string == "wednesday":
                        day = 2
                    elif string == "thursday":
                        day = 3
                    elif string == "friday":
                        day = 4
                    elif string == "saturday":
                        day = 5
                    elif string == "sunday":
                        day = 6
                    else:
                        return None, None
                    days = (day - datetime.date.today().weekday() + 7) % 7
                    date_to_check = datetime.date.today() + datetime.timedelta(days=days)
    if location == "":
        location = "New York City"
    return location, date_to_check


def get_location(data: str, keyword: str):
    location = None
    date_to_check = None
    if " in " in data:
        location, date_to_check = parse_(data, " in ")
    else:
        if keyword == "temp":
            var = data.split()
            for index, item in enumerate(var):
                if "temp" in item:
                    var[index] = "temp"
            data = ' '.join(var)
            location, date_to_check = parse_(data, keyword)
        if keyword == "weather":
            location, date_to_check = parse_(data, keyword)
    if location is not None:
        return location, date_to_check
    else:
        return None, None


def get_weather(city_name, date_to_check: datetime.date):
    api_key = "de35551fca0c4d3a8b9211105222806"
    mode = 0
    if date_to_check is not None and city_name is not None:
        days_from_now = (date_to_check - datetime.date.today()).days
        url = f"https://api.weatherapi.com/v1/forecast.json?q={city_name}&days={days_from_now+1}&key={api_key}"
        mode = 1
    elif date_to_check is not None and city_name is None:
        days_from_now = (date_to_check - datetime.date.today()).days
        city_name = ""  # fill me in
        mode = 1
        url = f"https://api.weatherapi.com/v1/current.json?q={city_name}&days={days_from_now+1}&key={api_key}"
    elif date_to_check is None and city_name is not None:

        url = f"https://api.weatherapi.com/v1/current.json?q={city_name}&key={api_key}"
    else:
        city_name = ""  # change me
        url = f"https://api.weatherapi.com/v1/current.json?q={city_name}&key={api_key}"
    response = requests.get(url)
    x = response.json()
    new_user_response = None
    if response.status_code != 400:
        if mode == 0:
            new_user_response = f"In {x['location']['name']}, it is currently {round(int(x['current']['temp_f']))} degrees Fahrenheit."
        else:
            forecast_obj = x["forecast"]["forecastday"]
            forecast = None

            for item in forecast_obj:
                if datetime.datetime.strptime(item["date"], "%Y-%m-%d").day == date_to_check.day:
                    forecast = item
                    break

            if forecast is not None:
                max_temp = round(int(forecast["day"]["maxtemp_f"]))
                min_temp = round(int(forecast["day"]["mintemp_f"]))
                new_user_response = f"On {date_to_check.strftime('%B')}, {date_to_check.day}st in {x['location']['name']}, expect a high of {max_temp} and a low of {min_temp}."
            else:
                new_user_response = "Sorry, I don't have that weather information."
        return new_user_response
    else:
        return "I am unable to fetch weather data."


def eval(data: str, memory: list) -> object:
    data = preprocessing.process(data)
    mode = -1
    if "weather" in data:
        mode = 0
    elif "temp" in data:
        mode = 1

    if mode == -1:
        return None
    if mode == 0:
        # Get general weather data
        location, date_to_check = get_location(data, "weather")
        weather = get_weather(location, date_to_check)
        return weather
    elif mode == 1:
        # get temperature data
        location, date_to_check = get_location(data, "temp")
        weather = get_weather(location, date_to_check)
        return weather
        return
    return None


if __name__ == "__main__":
    module_testing.run_module(check_score_func=check_input, eval_module_func=eval)
