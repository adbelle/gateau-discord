import random, json, pyowm, os, datetime, sqlite3
from urllib.request import urlopen
from urllib.error import URLError
from urllib.parse import quote

def random_response_line():
    random_response = str(random.choice(list(open('response.txt')))[:-1])
    return random_response


def read_weather(text, key, wu_type):
    owm = pyowm.OWM(str(key))
    wu_target = str(text)
    wu_key = key

    wu_auto_url = urlopen(str("http://autocomplete.wunderground.com/aq?query=" + quote(wu_target)))
    json_data = wu_auto_url.read().decode('utf-8', 'replace')
    data = json.loads(json_data)

    f = open('autocomplete', "w")
    f.write(json_data)
    f.close()

    with open('autocomplete') as search_file:
        data = json.load(search_file)

    wu_guess = data['RESULTS'][0]['l']

    target_url = "http://api.wunderground.com/api/" + str(wu_key + "/alerts/astronomy/conditions/forecast" + quote(wu_guess) + ".json")

    wu_response = urlopen(target_url)

    json_data = wu_response.read().decode('utf-8', 'replace')
    data = json.loads(json_data)

    f = open('observerdata', "w")
    f.write(json_data)
    f.close()

    with open('observerdata') as data_file:
        data = json.load(data_file)

    data_alerts = data['alerts']

    alerts_list = []
    for z in data_alerts:
        alerts_list.append(z['description'])

    alerts_txt = ', '.join(alerts_list)

    if wu_type == 'forecast':
        weather_out = ''.join("```\n" + data['forecast']['txt_forecast']['forecastday'][0]['title'] + ": " + data['forecast']['txt_forecast']['forecastday'][0]['fcttext']
                            + "\n" + data['forecast']['txt_forecast']['forecastday'][1]['title'] + ": " + data['forecast']['txt_forecast']['forecastday'][1]['fcttext']
                            + "\n" + data['forecast']['txt_forecast']['forecastday'][2]['title'] + ": " + data['forecast']['txt_forecast']['forecastday'][2]['fcttext']
                            + "\n" + data['forecast']['txt_forecast']['forecastday'][3]['title'] + ": " + data['forecast']['txt_forecast']['forecastday'][3]['fcttext']
                            + "\n" + data['forecast']['txt_forecast']['forecastday'][4]['title'] + ": " + data['forecast']['txt_forecast']['forecastday'][4]['fcttext'] + "```")
    if wu_type == 'conditions':
        if len(data['current_observation']['observation_location']['full']) < 6:
            station_name = data['current_observation']['display_location']['full']
        else:
            station_name = data['current_observation']['observation_location']['full']
        weather_out = ''.join("```\nCurrent conditions for " + station_name
                         + " (" + data['current_observation']['station_id'] + ", " + data['current_observation']['observation_time']
                         + ")\nTemperature: " + data['current_observation']['temperature_string'] + ", feels like " + data['current_observation']['feelslike_string']
                         + "\nHumidity: " + data['current_observation']['relative_humidity']
                         + "\nSkies: " + data['current_observation']['weather'] + " with " + data['current_observation']['visibility_mi'] + " mi (" + data['current_observation']['visibility_km'] + " km) of visibility\n"
                         + "Wind: " + data['current_observation']['wind_dir'] + " at " + str(data['current_observation']['wind_mph']) + " mph (" + str(data['current_observation']['wind_kph']) + " kph)"
                         + "\nAtmospheric pressure: " + str(data['current_observation']['pressure_mb']) + " mb")
        if str(alerts_txt) != "":
            weather_out = ''.join(weather_out + "\nThis observer is subject to the following alerts: " + alerts_txt + "```")
        else:
            weather_out = ''.join(weather_out + "```")
    try:
        os.remove('autocomplete')
        os.remove('observerdata')
    except OSError:
        pass
    return weather_out


def make_timestamp():
    gattimestamp = time.strftime("%Y-%m-%d %H:%M UTC", time.gmtime())
    return gattimestamp


def read_single_definition(deftitle):
    conn = sqlite3.connect('gateau.db')
    c = conn.cursor()
    t = (deftitle,)
    c.execute('SELECT * FROM definitions WHERE title=?', t)
    data = c.fetchall()
    if str(data) == "[]":
        def_out = str("I don't have a definition for " + deftitle + ".")
    else:
        for row in data:
            def_out = "Definition for " + row[0] + ":```\n" + row[1] + "```"
    conn.close()
    return def_out
