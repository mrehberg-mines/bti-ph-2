# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import datetime

import dash
from dash import dcc
from dash import html
from dash import dash_table
import plotly
from dash.dependencies import Input, Output
# import os
import subprocess
import glob
import pandas as pd
import plotly.express as px
global first, df, n_lanes, save_file, bat_file


config = {'displayModeBar': False}

bat_file='transfer-data-from-rpi.bat'
folder='rpi-data'

def get_data(folder):
    subprocess.call([bat_file])
    files=glob.glob(folder+'\*.csv')       
    df=pd.DataFrame()

    for file in files:
        temp=pd.read_csv(file, delimiter=',')
        df=df.append(temp)
        
    return df




#initializing variables

df=get_data(folder)
df_dict=[]
for col in df.columns:
    df_dict.append({'label':col, 'value':col})
    
checkbox_style={'backgroundColor':'#ffffff','border': '1px solid black','borderRadius': '4px', 'maxHeight': '600px', 'maxWidth':'230px', 'overflow': 'auto', 'padding':4}
graph_background='#c7cad7'
page_background='#dadada'
params=['Variable', 'Units', 'Min', 'Max', 'Color']

app = dash.Dash(__name__)
app.layout = html.Div(children=[
    html.Div([
        html.Div(style={'width': '230px', 'height': '156px', 'overflow': 'hidden'},children=[
            html.Img(src='https://clipground.com/images/mines-logo-4.jpg')]),

        html.Br(),
        html.Br(),
        'Update Interval (s)',
        html.Br(),
        dcc.Input(id='my-input', value=15, type='number', style=checkbox_style, debounce=True),
        html.Br(),
        'Graphable Variables',
        html.Br(),
        dcc.RadioItems(id='variables-radio', labelStyle={'display': 'block'}, style=checkbox_style),
    ],
    style={'padding': 10, 'flex': 1, 'border':'1px solid black','borderRadius' :'10px', 'backgroundColor':graph_background}
    ),
    html.Div([
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, # in milliseconds
            n_intervals=0
        ),
        dcc.Slider(
            id='time-slider',
            min=df.index.min(),
            max=df.index.max(),
            value=df.index.min(),
            step=5),
        dash_table.DataTable(id='table-editing-simple',
            columns=(
                [{'id': 'Lane', 'name': 'Lane'}] +
                [{'id': 'Axis', 'name': 'Axis'}] +
                [{'id': p, 'name': p} for p in params]
            ),
            data=[
                dict(Lane=i, Axis=i, **{param: '' for param in params})
                for i in range(1, 11)
        ],
        editable=True,
        )
    ],style={'padding': 30, 'flex': 1})
],style={'display': 'flex', 'flex-direction': 'row','backgroundColor':page_background, 'padding':10, 'position':'fixed', 'top':'0px', 'bottom':'0px','left':'0px','right':'0px'})

@app.callback(
    Output(component_id='interval-component', component_property='interval'),
    Input(component_id='my-input', component_property='value'))

def update_output_div(n):
    return max(6,n)*1000



@app.callback(Output('live-update-graph', 'figure'),
              Output('time-slider', 'max'),
              Output('variables-radio', 'options'),
              Input('interval-component', 'n_intervals'),
              Input('xaxis-type', 'value'),
              Input('time-slider', 'value'),
              Input('table-editing-simple', 'data'),
              Input('table-editing-simple', 'columns'))
    
def update_graph_live(n, xaxis_type, time, data_rows, columns):
    table_vars=pd.DataFrame(data_rows, columns=[c['name'] for c in columns])
    table_vars=table_vars.fillna('')
    table_vars=table_vars[table_vars['Variable'].str.len()>=3]
    table_vars=table_vars.reset_index(drop=True)
    df=get_data(folder)
    # Create the graph with subplots
    filtered_df=df[df.index>=time]
    #filtered_df=filtered_df[cols]
    if xaxis_type=='Shared':
        x_type=True
    else:
        x_type=False    
    graph_height=700
    graph_width=1300
    table_vars['Lane']=table_vars['Lane'].apply(str)
    unique_lanes=table_vars['Lane'].unique()
    #print(table_vars['Lane'])
    spacing=0.02
    fig = plotly.subplots.make_subplots(rows=max(1,len(unique_lanes)), cols=1, shared_xaxes=x_type, horizontal_spacing = spacing, vertical_spacing=spacing)
    fig['layout']['margin'] = {'l': 10, 'r': 10, 'b':10, 't': 10}
    fig['layout']['legend'] = {'x': -.2, 'y': 1, 'xanchor': 'left'}
    
    #create axis dictionary
    x_ax_dict={1:('xaxis','x'), 2:('xaxis2','x2'), 3:('xaxis3','x3'), 4:('xaxis4', 'x4'), 5:('xaxis5','x5')}
    y_ax_dict={1:('yaxis','y'), 2:('yaxis2', 'y2'), 3:('yaxis3','y3'), 4:('yaxis4','y4'), 5:('yaxis5','y5')}
   
    for i in range(len(table_vars)):
        try:
            col=table_vars['Variable'][i].lower()
            xaxis=int(table_vars['Lane'][i])
            yaxis=table_vars['Axis'][i]
            if yaxis=='': yaxis=1
            else: yaxis=int(yaxis)
            #generate y axis if it doesnt exist
            if yaxis>len(unique_lanes):
                #calculate domain
                num_lanes=len(unique_lanes)
                num_spacings=max(num_lanes-1,1)
                height=(1-num_spacings*spacing)/num_lanes
                dom_min=1-(xaxis-1)*height-max(0,xaxis-1)*spacing
                dom_max=dom_min-height
                y_str='yaxis'+str(yaxis)
                anchor_x=x_ax_dict[xaxis][1]
                over_y=y_ax_dict[xaxis][1]
                fig['layout'][y_str]=dict(anchor=anchor_x , domain=[dom_max, dom_min], overlaying=over_y, side='right')
            
            #set axis range
            if len(table_vars['Min'][i])>0:
                min_y=float(table_vars['Min'][i])
            else:
                min_y=min(filtered_df[col])*0.99
                
            if len(table_vars['Max'][i])>0:
                max_y=float(table_vars['Max'][i])
            else:
                max_y=max(filtered_df[col])*1.01
            y_axis_range=y_ax_dict[yaxis][0]
            ax_title=table_vars['Units'][i]
            fig['layout'][y_axis_range].update(range=[min_y, max_y], title=ax_title)
            ax_color=table_vars['Color'][i]
            if len(ax_color)<2:
                ax_color=px.colors.qualitative.Plotly[i]
            fig['layout'][y_axis_range].update(color=ax_color)
            
            fig.append_trace({'x': filtered_df['time'],'y': filtered_df[col],'name': col,'mode': 'lines','type': 'scatter', 'line':dict(color=ax_color), 'legendgroup':int(table_vars['Lane'][i]), },\
                              row=xaxis, col=1)
                
            
            y_axis_var=table_vars['Axis'][i]
            if y_axis_var=='': y_axis_var=1
            else: y_axis_var=int(y_axis_var)
            fig['data'][i].update(yaxis= y_ax_dict[y_axis_var][1])    

        except: continue
    for x in fig['layout']:
        if 'yaxis' in x:
            fig['layout'][x].update(showgrid=False, showline=True, linewidth=1, linecolor='black', mirror=True, title_font_size=18, title_font_family='Arial', tickfont_size=14, tickfont_family='Arial')
        if 'xaxis' in x:
              fig['layout'][x].update(showgrid=False, showspikes=True, spikethickness=2, spikedash="dot", spikecolor="#999999",spikemode="across", showline=True, linewidth=1, linecolor='black', mirror=True)


    fig.update_layout(height=graph_height, width=graph_width, legend_tracegroupgap = (graph_height+60)/(1+len(unique_lanes)))
    fig.update_layout(paper_bgcolor=page_background, font_color='#000000')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(hovermode="x", hoverdistance=100, spikedistance=1000)
    
    # variable return
    
    return fig, df.index.max(), [{'label': i, 'value': i} for i in df.columns]

if __name__ == '__main__':
    app.run_server(debug=False)
    #app.run_server(debug=True)

