import requests

def weather():
    """returns the weather"""
    url = "https://wttr.in/?format=j1"
    weather = requests.get(url).json()
    return weather
