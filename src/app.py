from dash import Dash, dcc, html
from dash.dependencies import Output, Input, State
import yfinance as yf
from datetime import datetime
import pandas as pd
import dash_auth

USERNAME_PASSWORD_PAIRS = [['623', '63']]
app = Dash(__name__)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)

server = app.server

nsdq = {"TTF": "TTF=F","WTI":"WTI","HH": "HH=F","Brent Oil": "BZ=F"}

#Sorting the stocks alphabatically
myKeys = list(nsdq.keys())
myKeys.sort()
nsdq = {i: nsdq[i] for i in myKeys}

#pulling the stock data of chosen stocks and combining them in one dataframe
def download_stocks(tickers):
    df_comb=pd.DataFrame()
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period="10y")
            df["ticker"]=ticker
            df_comb=pd.concat([df,df_comb], axis=0)

        except:
            pass
    return df_comb

app.layout = html.Div([
            html.H1('Динамика ценовых индикаторов'),
            html.Div([html.H3('Выбор тикеров:', style={'paddingRight':'30px'}),
            dcc.Dropdown(
                id='my_ticker_picker',
                options=[{'label': key, 'value': value} for key, value in
                              nsdq.items()],
                value=['Urals'],
                multi=True
            )
            ], style={'display':'inline-block', 'verticalAlign':'top','width':'40%'}),
            html.Div([html.H3('Выберете даты:'),
                      dcc.DatePickerRange(id='my_date_picker',
                                          min_date_allowed='2015-1-1',
                                          max_date_allowed =datetime.today(),
                                          start_date='2020-1-1',
                                          end_date=datetime.today()
                                          )
                      ], style={'display':'inline-block'}),
            html.Div([
                    html.Button(id='submit-button',
                                n_clicks=0,
                                children='Show',
                                style={'fontSize': 24,'marginLeft':'30px'})
            ], style ={'display':'inline-block'}),
            dcc.Graph(id='my_graph',
                        figure={'data':[
                            {'x': [1,2], 'y':[3,1]}
                        ]
                    }
                )
            ])

@app.callback(Output('my_graph', 'figure'),
               [Input('submit-button', 'n_clicks')],
               [State('my_ticker_picker','value'),
               State('my_date_picker','start_date'),
               State('my_date_picker', 'end_date')])

def update_graph(n_clicks,stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')
    traces =[]
    for tic in stock_ticker:
        data = yf.download(tic, start, end)
        traces.append({'x': data.index, 'y': data['Close'],'name':tic})
    fig = {
        'data': traces,
        'layout':{'title': ', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
 app.run(debug=True, port=8071)