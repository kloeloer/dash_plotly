import dash
from dash import dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import socket
import requests
import psutil as ps
import datetime
import dash_bootstrap_components as dbc

############# IMPORT DATA by sending GET request################

def gauge_graph(value,title):
    fig_indicator = go.Figure(
                    go.Indicator(
                                    mode = "gauge+number",
                                    #value = display_cpu()['cpu_perc'],
                                    value = value,
                                    domain = {'x': [0, 1], 'y': [0, 1]},
                                    title = {'text': title},
                                    gauge = {'axis':{'range':[0,100]}}
                                    )
                    )
    return fig_indicator

########################################## dbc.Card configuratiin ##########################################
card_cpu_usage_ws1 = dbc.Card(
                dbc.CardBody([
                            #dbc.Row(html.H1(display_cpu()['host_nm']),style={'textAlign':'center','backgroundColor':'black','color':'white','fontSize':'20px'}),
                            dbc.Row(html.H1(socket.gethostname()),style={'textAlign':'center','backgroundColor':'black','color':'white','fontSize':'20px'}),
                            dbc.Row([
                                    dbc.Col(html.Div([
                                                    html.H4('Number of CPU'),
                                                    html.H1(id='num-cpu-id')
                                                    ],style={'textAlign':'center','backgroundColor':'blue','color':'white','marginTop':'8px'}),width=4),
                                    dbc.Col(html.Div([
                                                    html.H4('Maximum CPU Speed (GHz)'),
                                                    html.H1(id='speed-cpu-id')
                                                    ],style={'textAlign':'center','backgroundColor':'blue','color':'white','marginTop':'8px'}),width=4),
                                    dbc.Col(html.Div([
                                                    html.H4('Total Memory(GB)'),
                                                    html.H1(id='tot-mem-id')
                                                    ],style={'textAlign':'center','backgroundColor':'blue','color':'white','marginTop':'8px'}),width=4)
                                    ]),
                            dbc.Row([
                                    html.Div([
                                            dbc.Row([
                                                    dbc.Col(dcc.Graph(id='live-update-graph'),width=6),
                                                    dbc.Col(dcc.Graph(id='live-plot'),width=6)
                                                    ]),
                                            dbc.Row([
                                                    dbc.Col(dcc.Graph(id='live-update-graph-mem'),width=6),
                                                    dbc.Col(dcc.Graph(id='live-plot-mem'),width=6)
                                                    ]),
                                            dbc.Row([
                                                    dbc.Col(dcc.Graph(id='live-update-graph-pid'),width=6),
                                                    dbc.Col(dcc.Graph(id='live-plot-pid'),width=6)
                                                    ])
                                            ])
                                    ])
                            
                            ])
                )


###########################################################################################
data1=[]
data2=[]
data3=[]
data4=[]

data_mem1=[]
data_mem2=[]

data_pid1=[]
data_pid2=[]

#################################### Main web Layout ######################################

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
app.layout = html.Div([
            dcc.Interval(
                                    id='interval-component',
                                    interval=0.5*1000, # in milliseconds
                                    n_intervals=0
                                    ),
            dbc.Row(html.Div(html.H1('Operating System Resource Realtime Dashboard')),style={'textAlign':'center','marginBottom':'8px','backgroundColor':'yellow'}),
            dbc.Row([
                dbc.Col(card_cpu_usage_ws1,width=12),
                #dbc.Col(card_cpu_usage_ws2,width=6)
                ])
            
    ])


@app.callback([Output('live-update-graph', 'figure'),
               Output('live-plot', 'figure'),
               Output('live-update-graph-mem', 'figure'),
               Output('live-plot-mem', 'figure'),
               Output('tot-mem-id','children'),
               Output('num-cpu-id','children'),
               Output('speed-cpu-id','children'),
               Output('live-update-graph-pid', 'figure'),
               Output('live-plot-pid', 'figure')],
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):

    xxx = ps.cpu_percent()
    yyy = ps.virtual_memory()[2]
    ttt = datetime.datetime.now()
    pid = len(ps.pids())
    total_ram = ps.virtual_memory()[0]/1024/1024/1024
    cpu_speed = ps.cpu_freq()[2]/1024
    cpu_num = ps.cpu_count()

    
    fig1 = gauge_graph(xxx,'CPU Usage(%)')

    
 

    data1.append(ttt)
    data2.append(xxx)
    data = [go.Scatter(x=data1[-150:],y=data2[-150:],mode='lines')]
    layout = go.Layout(yaxis={'range':[0,105]})
    fig2 = go.Figure(data,layout)
    
    #-----------------
    fig3 = gauge_graph(yyy,'RAM Usage (%)')
    
    data_mem1.append(yyy)
    data = [go.Scatter(x=data1[-150:],y=data_mem1[-150:],mode='lines')]
    layout = go.Layout(yaxis={'range':[0,105]})
    fig4 = go.Figure(data,layout)

    #-----------------
    fig5 = gauge_graph(pid,'Number of Process')
    fig5.update_traces(gauge = {'axis':{'range':[0,500]}})
    
    data_pid1.append(pid)
    data = [go.Scatter(x=data1[-150:],y=data_pid1[-150:],mode='lines')]
    layout = go.Layout(yaxis={'range':[0,500]})
    fig6 = go.Figure(data,layout)
    
    return fig1,fig2,fig3,fig4,round(total_ram,2),cpu_num,round(cpu_speed,3),fig5,fig6




if __name__ == '__main__':
    app.run_server(debug=False,port='8090',host='192.168.100.9')
