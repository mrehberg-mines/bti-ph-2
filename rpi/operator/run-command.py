
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
# this is what sends a command to the pi
import socket
from commonFunctions import setupIPs, parseMessage 
global pi_IP

def send_command(varID, varValue):
    TCP_IP = pi_IP
    TCP_PORT = 5005
    BUFFER_SIZE = 1024
    MESSAGE = f"{varID}:{varValue}"
    byt = MESSAGE.encode()
    while 1:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(byt)
        data = s.recv(BUFFER_SIZE)
        s.close()
        break
    
    ret_varID, ret_varValue = parseMessage(data)
    return ret_varID, ret_varValue


## Dash Variables ####
box_style={'backgroundColor':'#ffffff','border': '1px solid black','borderRadius': '4px', 'maxHeight': '30px', 'maxWidth':'300px', 'overflow': 'auto', 'padding':4}
page_background='#999999'

### DASH Application #######


## DASH Variables ####
box_style={'backgroundColor':'#EBECF0','border': '0px solid grey','borderRadius': '4px', 'maxHeight': '30px', 'maxWidth':'90px', 'overflow': 'auto', 'padding':4}
page_background='#111111'



### DASH Application #######

app = Dash(__name__)


app.layout = html.Div([
    html.Div([
            html.H1(children = 'Rover Control Panel', 
             style = {
            'textAlign': 'center', 
            'font-family' : 'monospace'
            }
            ),
        html.H2(children = 'NASA Break The Ice!', 
             style = {
            'textAlign': 'center', 
            'font-family' : 'monospace'
            }
            ),
    ], style={'padding': 10, 'border':'1px solid white','borderRadius' :'10px', 'backgroundColor': '#808080'}
    ),
    html.Div([
        html.H2(children = 'Hammer Controls', 
             style = {
            'textAlign': 'center', 
            'font-family' : 'monospace'
            }
            ),
        html.Br(),
        html.H3(children = 'Hammer motor power: ', 
            style = {
            'font-family' : 'monospace'
        }),
        dcc.RadioItems(
            id = "hammer_power",
            style= box_style,
            options=['On', 'Off'],
            value='Off'
        ),
        html.Div(id="hammer_power:return"),

        html.Br(),
        html.H3(children = 'Hammer height direction (up): ', 
            style = {
            'font-family' : 'monospace'
        }),
        dcc.RadioItems(
            id = "hammer_height_up",
            style= box_style,
            options=['On', 'Off'],
            value='Off'
        ),
        html.Div(id="hammer_height_up:return"),

        html.Br(),
        html.H3(children = 'Hammer height direction (down): ', 
            style = {
            'font-family' : 'monospace'
        }),
        dcc.RadioItems(
            id = "hammer_height_down",
            style= box_style,
            options=['On', 'Off'],
            value='Off'
        ),
        html.Div(id="hammer_height_down:return"),
        html.Br()
    ], 
    style={'padding': 10, 'border':'1px solid white','borderRadius' :'10px', 'backgroundColor': '#89CFF0'}),
    html.Div([
        html.H2(children = 'Bucket Controls', 
             style = {
            'textAlign': 'center', 
            'font-family' : 'monospace'
            }
            ),

        html.Br(),
        html.H3(children = 'Bucket height direction (up): ', 
            style = {
            'font-family' : 'monospace'
        }),
        dcc.RadioItems(
            id = "bucket_height_up",
            style= box_style,
            options=['On', 'Off'],
            value='Off'
        ),
        html.Div(id="bucket_height_up:return"),

        html.Br(),
        html.H3(children = 'Bucket height direction (down): ', 
            style = {
            'font-family' : 'monospace'
        }),
        dcc.RadioItems(
            id = "bucket_height_down",
            style= box_style,
            options=['On', 'Off'],
            value='Off'
        ),
        html.Div(id="bucket_height_down:return"),

        html.Br(),
        html.H3(children = 'Bucket angle direction (up): ', 
            style = {
            'font-family' : 'monospace'
        }),
        dcc.RadioItems(
            id = "bucket_angle_up",
            style= box_style,
            options=['On', 'Off'],
            value='Off'
        ),
        html.Div(id="bucket_angle_up:return"),

        html.Br(),
        html.H3(children = 'Bucket height direction (down): ', 
            style = {
            'font-family' : 'monospace'
        }),
        dcc.RadioItems(
            id = "bucket_angle_down",
            style= box_style,
            options=['On', 'Off'],
            value='Off'
        ),
        html.Div(id="bucket_angle_down:return"),
        html.Br()
        ], style={'padding': 10, 'border':'1px solid white','borderRadius' :'10px', 'backgroundColor': '#FFCCCB'}
        )
])

@app.callback(
    Output("hammer_power:return", "children"),
    Input("hammer_power", "id"),
    Input("hammer_power", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"


@app.callback(
    Output("hammer_height_power:return", "children"),
    Input("hammer_height_power", "id"),
    Input("hammer_height_power", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("hammer_height_up:return", "children"),
    Input("hammer_height_up", "id"),
    Input("hammer_height_up", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("hammer_height_down:return", "children"),
    Input("hammer_height_down", "id"),
    Input("hammer_height_down", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("bucket_height_power:return", "children"),
    Input("bucket_height_power", "id"),
    Input("bucket_height_power", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("bucket_height_up:return", "children"),
    Input("bucket_height_up", "id"),
    Input("bucket_height_up", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("bucket_height_down:return", "children"),
    Input("bucket_height_down", "id"),
    Input("bucket_height_down", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("bucket_angle_power:return", "children"),
    Input("bucket_angle_power", "id"),
    Input("bucket_angle_power", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("bucket_angle_up:return", "children"),
    Input("bucket_angle_up", "id"),
    Input("bucket_angle_up", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"

@app.callback(
    Output("bucket_angle_down:return", "children"),
    Input("bucket_angle_down", "id"),
    Input("bucket_angle_down", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"




if __name__ == '__main__':
    use_case = 'MattHome'
    pi_IP, laptop_IP = setupIPs(use_case)
    app.run_server(debug=True)