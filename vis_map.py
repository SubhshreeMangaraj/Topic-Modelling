import dash
import dash_core_components
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import random
from datetime import datetime
from dash.dependencies import Input, Output
from app import app

import glob
import os

import time

##Data Pre-processing

list_of_files = glob.glob('data/events/*') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
data = pd.read_csv(latest_file)
event_list = data.Group.unique()
el = event_list.tolist()
print(el)
fdata = data[data.Group == el[0]]
rgb = pd.DataFrame()
reload_count = 0

#-------------Lat Long-----------------------
# data[['Lat','Lon']] = data.Coordinates.str.split(",",expand=True)
# data['Lat'] = data['Lat'].str.strip('[')
# data['Lon'] = data['Lat'].str.strip(']')
# print(data)

#----------------Color-----------------------

color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(len(event_list))])
             for i in range(len(event_list))]
rgb['Color'] = color
rgb['Group'] = el

#----------------------------------------------

mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layoutmap = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    # legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    showlegend = False,
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-55.3781, lat=3.4360),
        zoom=2,
    )
)

def layout():

    list_of_files = glob.glob('data/events/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    print(latest_file)
    data = pd.read_csv(latest_file)
    event_list = data.Group.unique()
    el = event_list.tolist()
    print(el)
    fdata = data[data.Group == el[0]]
    rgb = pd.DataFrame()
    reload_count = 0

    return html.Div([
    dcc.Tabs([
        dcc.Tab(
            label='5 Minutes Window', children=[
            html.H1(children='Event Visualization'),

            html.Label('Select the events to be '),
            dcc.Dropdown(
                id='opt-dropdown',
                options=[{'label': opt, 'value': opt} for opt in el],
                value=[el[0]],
                multi=True
            ),
            html.Button(dcc.Link('Refresh', href='/vis_map')),
            dcc.Graph(id='map-disp',),
            html.Button(dcc.Link('Click for topic visualization for 5 Min window',  href='/page-1', className='b1')),
        ]),
        dcc.Tab(
            label='10 Minutes Window', children=[
            html.H1(children='Event Visualization'),

            html.Label('Select the events to be '),
            dcc.Dropdown(
                id='opt-dropdown1',
                options=[{'label': opt, 'value': opt} for opt in el],
                value=[el[0]],
                multi=True
            ),
            html.Button(dcc.Link('Refresh', href='/vis_map')),
            dcc.Graph(id='map-disp1',),
            html.Button(dcc.Link('Click for topic visualization for 10 Min window"', href='/page-2', className='b1')),
        ]),
        dcc.Tab(
            label='1 Hour Window', children=[
            html.H1(children='Event Visualization'),

            html.Label('Select the events to be '),
            dcc.Dropdown(
                id='opt-dropdown2',
                options=[{'label': opt, 'value': opt} for opt in el],
                value=[el[0]],
                multi=True
            ),
            html.Button(dcc.Link('Refresh', href='/vis_map')),
            dcc.Graph(id='map-disp2',),
            html.Button(dcc.Link('Click for topic visualization for 1 Hour window',     href='/page-3', className='b1')),
        ])
    ]),
    dcc.Interval(
            id='interval-component',
            interval=10*1000, # in milliseconds
            n_intervals=0
        ),
    dbc.Toast(
            "This toast is placed in the top right "+str(reload_count),
            id="positioned-toast",
            header="Positioned toast",
            is_open=False,
            dismissable=True,
            icon="danger",
            # top: 66 positions the toast below the navbar
            style={"position": "fixed", "top": 66, "right": 10, "width": 350},
        )]
)

@app.callback(
    Output('opt-dropdown', 'disabled'),
    [Input('opt-dropdown', 'value')]
    # [dash.dependencies.State('ref', 'n_clicks')]
)
def disable_dropdown_one(val1):

    if len(val1) > 4:
        return True
    else:
        return False

@app.callback(
    Output('opt-dropdown1', 'disabled'),
    [Input('opt-dropdown1', 'value')]
)
def disable_dropdown_one(val1):

    if len(val1) > 4:
        return True
    else:
        return False

@app.callback(
    Output('opt-dropdown2', 'disabled'),
    [Input('opt-dropdown2', 'value')]
)
def disable_dropdown_one(val1):

    if len(val1) > 4:
        return True
    else:
        return False


@app.callback(
   Output('map-disp', 'figure'),
   [Input('opt-dropdown', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []


    fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layoutmap,
    }

@app.callback(
   Output('map-disp1', 'figure'),
   [Input('opt-dropdown1', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layoutmap,
    }

@app.callback(
   Output('map-disp2', 'figure'),
   [Input('opt-dropdown2', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layoutmap,
    }


@app.callback(
   Output('map-disp3', 'figure'),
   [Input('opt-dropdown3', 'value')])
def updatefigure(selectedevent):
    traces1 = []
    col = []

    fdata1 = data[data['Group'].isin(selectedevent)]
    # year_data = data[data['Year'] == selectedyear]
    # print(year_data)

    for l in range(len(fdata1)):
        for k in range(len(rgb)):
            if rgb.iloc[k,1] == fdata1.iloc[l,5]:
                col.append(rgb.iloc[k,0])

    for i in range(len(fdata1)):
        traces1.append(
           go.Scattermapbox(
               lat=[fdata1.iloc[i,6]],
               lon=[fdata1.iloc[i,7]],
               mode='markers',
               marker=go.scattermapbox.Marker(
                   size=14,
                   color= col[i]
               ),
               text=[fdata1.iloc[i,5]]

       ))
    # print(fdata1)
    return {
           'data': traces1,
           'layout': layoutmap,
    }


@app.callback(Output('positioned-toast', 'is_open'),
              [Input('interval-component', 'n_intervals')])
def update_metrics(n):
    # print('opening toast',n )
    global reload_count
    reload_count +=1
    return True
