from dash import Dash, dcc, html
from dash.dependencies import Output, Input, State
# https://www.tiingo.com/
#https://github.com/ranaroussi/yfinance
import yfinance as yf
from datetime import datetime

app = Dash(__name__)
server = app.server

app.layout = html.Div([
            html.H1('Stock Ticker Dashboard'),
            html.Div((html.H3('Enter a stock symbol:', style={'paddingRight': '30px'}),
                      dcc.Input(
                          id='my_stock_picker',
                          value='TSLA',
                          multiple=True,
                          style={'fontSize': 24, 'width': 75}
                      )), style={'display': 'inline-block', 'verticalAlign': 'top'}),
            html.Div([html.H3('Select a start and end date:'),
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
                                children='Submit',
                                style={'fontSize': 24,'marginLeft':'30px'})
            ]),
            dcc.Graph(id='my_graph',
                        figure={'data':[
                            {'x': [1,2], 'y':[3,1]}
                        ], 'layout':{'title':'Default title'}}
                )
            ])

@app.callback(Output('my_graph', 'figure'),
               Input('submit-button', 'n_clicks'),
               State('my_stock_picker','value'),
               State('my_date_picker','start_date'),
               State('my_date_picker', 'end_date'))

def update_graph(n_clicks,stock_ticker, start_date, end_date):

    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')
    data = yf.download(stock_ticker, start, end)
    fig = {
        'data': [{'x': data.index, 'y': data['Close']}],
        'layout':{'title': stock_ticker}
    }
    return fig

if __name__ == '__main__':
 app.run(debug=False, port=8051)