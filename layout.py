from dash import html, dcc
from typing import List
from util import TideData

locations = {
    'https://www.tide-forecast.com/locations/Half-Moon-Bay-California/tides/latest': 'Half Moon Bay, California',
    'https://www.tide-forecast.com/locations/Huntington-Beach/tides/latest': 'Huntington Beach, California',
    'https://www.tide-forecast.com/locations/Providence-Rhode-Island/tides/latest': 'Providence, Rhode Island',
    'https://www.tide-forecast.com/locations/Wrightsville-Beach-North-Carolina/tides/latest': 'Wrightsville Beach, North Carolina'
}


def low_tide_card(date: str, tide_data: List[TideData]) -> html.Div:
    div = html.Div([
        html.B(f'{date}:', style={'float': 'left', 'width': '280px'}),
    ])
    if tide_data:
        div.children.append(
            html.Div(', '.join([f' Low Tide: {tide.tide_time}, {tide.tide_height}' for tide in tide_data]))
        )
        return div
    else:
        div.children.append(
            html.Div('There will be no daylight low tides on this day.')
        )
    return div


def serve_layout() -> html.Div:
    return html.Div([
        html.H1('Daylight Tide Finder'),
        dcc.Dropdown(
            options=locations,
            multi=True,
            value=[k for k in locations.keys()],
            id='location-selection'
        ),
        html.Button('Find My Tides', id='tide-search-btn'),
        html.Hr(style={'margin': '50px'}),
        dcc.Loading(html.Div(id='tide-info-div'))
    ], style={'margin': '100px'})
