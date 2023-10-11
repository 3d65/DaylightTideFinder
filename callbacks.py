from dash import Dash, html
from dash import Input, Output, State
from layout import low_tide_card, locations
from bs4 import BeautifulSoup
import requests
from typing import List, Tuple, Optional
import pandas as pd
from datetime import datetime
from util import TideData
from io import StringIO
from dash.exceptions import PreventUpdate


def get_callbacks(app: Dash) -> None:
    @app.callback(
        [Output('tide-info-div', 'children')],
        [Input('tide-search-btn', 'n_clicks')],
        [State('location-selection', 'value')],
        prevent_inital_call=True
    )
    def get_low_tide_cards(n_clicks, location_links: List) -> List:

        # don't generate until at least one click
        if n_clicks is None:
            raise PreventUpdate

        rows = []
        if location_links:
            for location_link in location_links:
                rows.append(html.H3(locations[location_link]))
                res = requests.get(location_link)
                soup = BeautifulSoup(res.content, 'html.parser')
                tide_days = soup.find_all('div', class_={'tide-day'})
                for day in tide_days:
                    tide_date = day.find('h4').text.split(': ')[-1]  # get date text
                    tide_info, sun_info = pd.read_html(StringIO(str(day.find('div', class_='tide-day__tables'))))
                    valid_low_tides = get_daytime_tide_data(tide_info, sun_info)
                    rows.append(low_tide_card(tide_date, valid_low_tides))

            rows.append(html.Br())  # add spacing at bottom of location
        else:
            rows.append(html.H1('No rows'))
        return [rows]

    def get_daytime_tide_data(tide_info, sun_info) -> List[Optional[TideData]]:
        parse_format = '%I:%M%p'
        low_tides = tide_info[tide_info['Tide'] == 'Low Tide']
        low_tide_times = [tide.split('(')[0] for tide in low_tides.iloc[:, 1]]  # time occurs before '(', ex: 2:34AM(Oct 8)
        low_tide_times = [tide_time.replace('00:', '12:') for tide_time in low_tide_times]  # site sometimes uses 00 AM for 12 AM
        low_tide_times = [datetime.strptime(time.replace(' ', ''), parse_format) for time in low_tide_times]  # remove all spaces before parsing

        sunrise = sun_info[0][0].split(' ')[-1]  # time occurs after space, ex: Sunrise: 7:34AM
        sunset = sun_info[1][0].split(' ')[-1]

        sunrise = datetime.strptime(sunrise, parse_format)
        sunset = datetime.strptime(sunset, parse_format)

        res = []
        for low_tide_time, low_tide_height in zip(low_tide_times, low_tides['Height']):
            if sunrise < low_tide_time < sunset:
                res.append(
                    TideData(
                        tide_time=datetime.strftime(low_tide_time, parse_format),
                        tide_height=low_tide_height
                    )
                )
        return res
