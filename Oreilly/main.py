from datetime import datetime

import logging
from kivy.app import App
from kivy.factory import Factory
from kivy.network.urlrequest import UrlRequest
from kivy.properties import ObjectProperty, ListProperty, StringProperty, NumericProperty, Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton
from kivy.storage.jsonstore import JsonStore
import json

from kivy.uix.modalview import ModalView

from Oreilly.gesture_box import GestureBox


class WeatherRoot(BoxLayout):
    carousel = ObjectProperty()
    add_location_form = ObjectProperty()
    current_weather = ObjectProperty()
    locations = ObjectProperty()
    forecast = ObjectProperty()

    def __init__(self, **kwargs):
        super(WeatherRoot, self).__init__(**kwargs)
        self.logger = logging.getLogger('WeatherApp.WeatherRoot')
        self.owm = OpenWeatherMap(self)
        self.store = JsonStore('weather_store.json')
        if self.store.exists('locations'):
            locations = self.store.get('locations')
            self.locations.locations_list.adapter.data.extend(locations['locations'])
            current_location = locations["current_location"]
            self.show_current_weather(current_location)
        else:
            Clock.schedule_once(lambda dt: self.show_add_location_form())

    def show_current_weather(self, location):
        if location not in self.locations.locations_list.adapter.data:
            self.locations.locations_list.adapter.data.append(location)
            # self.locations.locations_list._trigger_reset_populate()
            self.store.put('locations', locations=list(self.locations.locations_list.adapter.data),
                           current_location=location)

        self.current_weather.location = location
        self.forecast.location = location
        self.current_weather.update_weather()
        self.forecast.update_weather()

        self.carousel.load_slide(self.current_weather)
        if self.add_location_form is not None:
            self.add_location_form.dismiss()
        # self.owm.search_current_weather_by_location(self.current_weather.location)
        # self.add_widget(self.current_weather)
        # self.carousel.load_slide(self.current_weather)

    def show_add_location_form(self):
        # self.clear_widgets()
        # self.add_widget(self.add_location_form)
        self.add_location_form = AddLocationForm()
        # if self.add_location_form.cancel_button is None:
        #     self.add_location_form.cancel_button = CancelButton()
        #     self.add_location_form.add_widget(self.add_location_form.cancel_button)
        self.add_location_form.open()

    # def show_locations(self):
    #     self.clear_widgets()
    #     self.add_widget(self.locations)

    # def show_forecast(self, location=None):
    #     self.logger.debug('Start method show_forecast()...')
    #     self.clear_widgets()
    #
    #     if self.forecast is None:
    #         self.forecast = Factory.Forecast()
    #
    #     if location is not None:
    #         self.forecast.location = location
    #
    #     self.forecast.update_weather()
    #     self.add_widget(self.forecast)
    #     self.logger.debug('End method show_forecast().')


class AddLocationForm(ModalView):
    search_input = ObjectProperty()
    search_results = ObjectProperty()
    cancel_button = ObjectProperty()

    def __init__(self, **kwargs):
        super(AddLocationForm, self).__init__(**kwargs)
        self.owm = OpenWeatherMap(self)

    def search_location(self):
        print('Searching {keyword}...'.format(keyword=self.search_input.text))
        self.owm.search_current_weather_by_keyword(self.search_input.text)


# class CancelButton(Button):
#     pass


class LocationButton(ListItemButton):
    location = ListProperty()


class CurrentWeather(BoxLayout):
    location = ListProperty(('New York', 'US'))
    conditions = StringProperty()
    conditions_image = StringProperty()
    temp = NumericProperty()
    temp_min = NumericProperty()
    temp_max = NumericProperty()

    def __init__(self, **kwargs):
        super(CurrentWeather, self).__init__(**kwargs)
        self.logger = logging.getLogger('WeatherApp.WeatherRoot.CurrentWeather')

    def update_weather(self):
        self.logger.info('Start method update_weather...')
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault("General", "temp_type", "metric").lower()
        weather_template = "http://api.openweathermap.org/data/2.5/weather?q={},{}&units={}" + '&APPID=37f496ef5b722f579d2d5fc5afabc932'
        weather_url = weather_template.format(self.location[0], self.location[1], temp_type)
        request = UrlRequest(weather_url, self.weather_retrieved)
        self.logger.info('End method update_weather.')

    def weather_retrieved(self, request, data):
        self.logger.info('Start method weather_retrieved...')
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.conditions = data['weather'][0]['description']
        self.conditions_image = "http://openweathermap.org/img/w/{}.png".format(
            data['weather'][0]['icon'])
        self.temp = data['main']['temp']
        self.temp_min = data['main']['temp_min']
        self.temp_max = data['main']['temp_max']
        self.logger.info('End method weather_retrieved.')

class Forecast(BoxLayout):
    location = ListProperty(['New York', 'US'])
    forecast_container = ObjectProperty()

    def __init__(self, **kwargs):
        super(Forecast, self).__init__(**kwargs)
        self.logger = logging.getLogger('WeatherApp.WeatherRoot.Forecast')

    def update_weather(self):
        self.logger.debug('Start method update_weather()...')
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault('General', 'temp_type', 'metric').lower()
        weather_template = 'http://api.openweathermap.org/data/2.5/forecast/' + 'daily?q={},{}&units={}&cnt=7' + '&APPID=37f496ef5b722f579d2d5fc5afabc932'
        weather_url = weather_template.format(self.location[0], self.location[1], temp_type)
        request = UrlRequest(weather_url, self.weather_retrieved)
        self.logger.debug('End method update_weather().')

    def weather_retrieved(self, request, data):
        self.logger.debug('Start method weather_retrieved()...')
        data = json.loads(data.decode()) if not isinstance(data, dict) else data
        self.logger.debug('Forecast data: {}'.format(data))
        self.forecast_container.clear_widgets()
        for day in data['list']:
            label = Factory.ForecastLabel()
            label.date = datetime.fromtimestamp(day['dt']).strftime('%a %b %d')
            label.conditions = day['weather'][0]['description']
            label.conditions_image = 'http://openweathermap.org/img/w/{}.png'.format(day['weather'][0]['icon'])
            label.temp_min = day['temp']['min']
            label.temp_max = day['temp']['max']
            self.forecast_container.add_widget(label)
        self.logger.debug('End method weather_retrieved().')


class WeatherApp(App):
    def __init__(self, **kwargs):
        super(WeatherApp, self).__init__(**kwargs)
        logger = logging.getLogger('WeatherApp')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %I:%M:%S %p')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

    def build_config(self, config):
        config.setdefaults('General', {'temp_type': "Metric"})

    def build_settings(self, settings):
        settings.add_json_panel("Weather Settings", self.config, data="""
[
{"type": "options",
"title": "Temperature System",
"desc": "The type of temperature system, either Metric or Imperial",
"section": "General",
"key": "temp_type",
"options": ["Metric", "Imperial"]
}
]"""
                                )

    def on_config_change(self, config, section, key, value):
        if config is self.config and key == 'temp_type':
            try:
                self.root.current_weather.update_weather()
                self.root.forecast.update_weather()
            except AttributeError:
                pass


class LabApp(App):
    pass


class LabNoKvApp(App):
    # def print_it(self, instance, value):
    #     print('User clicked on', value)

    def build(self):
        # widget = Label(text='Hello [ref=world][color=0000ff]World[/color][/ref]', markup=True)
        # widget.bind(on_ref_press=self.print_it)
        # return widget
        l = Label(text='Very big big line', text_size=(200, None))
        return l


class OpenWeatherMap(object):
    def __init__(self, invoker):
        # self.city_list = None
        # with open(r'city.list.json', mode='r', encoding='utf-8') as f:
        #     self.city_list = json.load(f)
        self.api_url = 'http://api.openweathermap.org/data/2.5/'
        self.api_key = '&APPID=37f496ef5b722f579d2d5fc5afabc932'
        self.units_format = '&units=metric'  # For temperature in Celsius
        self.units_format_config = '&units={}'
        self.invoker = invoker

    def search_current_weather_by_keyword(self, keyword):
        search_template = self.api_url + 'find?q={keyword}' + self.api_key + self.units_format
        search_url = search_template.format(keyword=keyword)
        print('search url: {url}'.format(url=search_url))
        request = UrlRequest(search_url, self.found_location)

    def found_location(self, request, data):
        print(data)
        print(type(data))
        # search_results = [
        # 'City: {city}, Country: {country}, Weather: {weather}'.format(city=d['name'], country=d['sys']['country'],
        #                                                               weather=','.join(
        #                                                                   w['main'] for w in d['weather'])) for d in
        # data['list']]
        cities = [(d['name'], d['sys']['country']) for d in data['list']]
        if str(self.invoker.__class__) == "<class '__main__.AddLocationForm'>":
            self.invoker.search_results.item_strings = cities
            # self.invoker.search_results.adapter.data.clear()
            # self.invoker.search_results.adapter.data.extend(search_results)
            # self.invoker.search_results._trigger_reset_populate()
        else:
            raise ValueError("The invoker is supposed to be <class '__main__.AddLocationForm'>")

    def search_current_weather_by_location(self, location):
        config = WeatherApp.get_running_app().config
        temp_type = config.getdefault('General', 'temp_type', 'metric').lower()
        search_template = self.api_url + 'weather?q={},{}' + self.api_key + self.units_format_config
        # search_url = search_template.format(*location)
        search_url = search_template.format(location[0], location[1], temp_type)
        print('search url: {url}'.format(url=search_url))
        request = UrlRequest(search_url, self.weather_retrieved)

    def weather_retrieved(self, request, data):
        print(data)
        print(type(data))
        if str(self.invoker.__class__) == "<class '__main__.WeatherRoot'>":
            self.invoker.current_weather.conditions = ', '.join([weather['description'] for weather in data['weather']])
            self.invoker.current_weather.conditions_image = "http://openweathermap.org/img/w/{}.png".format(
                data['weather'][0]['icon'])
            self.invoker.current_weather.temp = data['main']['temp']
            self.invoker.current_weather.temp_min = data['main']['temp_min']
            self.invoker.current_weather.temp_max = data['main']['temp_max']
        else:
            raise ValueError("The invoker is supposed to be <class '__main__.WeatherRoot'>")


def locations_args_converter(index, data_item):
    city, country = data_item
    return {'location': (city, country)}


if __name__ == '__main__':
    WeatherApp().run()
    # LabNoKvApp().run()
