
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

app = Dash(__name__)
app.layout = html.Div(
    children =[
        html.Br(),
        html.H4('excavator:motor_speed: '),
        dcc.Input(
            id="excavator:motor_speed", type="number",
            debounce=True, placeholder=0, min=0, max=100,
            style= box_style,
        ),
        html.Div(id="excavator:motor_speed:return"),
        
        html.Br(),
        'excavator:motor_power: ',
        dcc.RadioItems(
            id = "excavator:motor_power",
            style= box_style,
            options=['True', 'False'],
            value='False'
        ),
        html.Div(id="excavator:motor_power:return"),
    ],
    style={'padding': 10, 'border':'1px solid black','borderRadius' :'10px', 'backgroundColor':page_background}
)

@app.callback(
    Output("excavator:motor_speed:return", "children"),
    Input("excavator:motor_speed", "id"),
    Input("excavator:motor_speed", "value"),
)
def send_var(varID, varValue):
    ret_varID, ret_varValue = send_command(varID, varValue)
    return f"{ret_varID}:{ret_varValue}"


@app.callback(
    Output("excavator:motor_power:return", "children"),
    Input("excavator:motor_power", "id"),
    Input("excavator:motor_power", "value"),
)
def send_var(varID, varValue):
    varReturn = send_command(varID, varValue)
    return f"{varReturn}"




if __name__ == '__main__':
    use_case = 'MattHome'
    pi_IP, laptop_IP = setupIPs(use_case)
    app.run_server(debug=True)