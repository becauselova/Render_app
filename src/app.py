from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_auth

USERNAME_PASSWORD_PAIRS = [['username', 'pass'],['jj', 'bsb']]

app = Dash(__name__)

auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server

app.layout = html.Div([
        dcc.RangeSlider(
            id='range-slider',
            min=-5,
            max=20,
            marks={i:str(i) for i in range(-5,20)},
            value=[-3,4]
        ),
        html.H1(id='product')
], style={'width':'50%'})

@app.callback(Output('product', 'children'), Input('range-slider', 'value'))
def update_value(value_list):
    return value_list[0]*value_list[1]

if __name__=='__main__':
    app.run(debug=False, port =8071)