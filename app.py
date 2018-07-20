'''
main python script
'''

# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# initialize dash app
app = dash.Dash()

# read from csv
df = pd.read_csv('./data/noah.csv')
x = [pd.to_datetime(date, format='%m/%d') for date in df['transaction_date']]
y = df['amount']

# generates a table (reusable component)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


# defines front-end layout
app.layout = html.Div(children=[
    html.H1(children='Bank Parser Dashboard'),

    html.Div(children='''
        For DANY by hackNY :)
    '''),

    # graph
    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': x, 'y': y, 'type': 'bar', 'name': 'Transactions'}
            ],
            'layout': {
                'title': 'Transactions'
            }
        }
    ),

    # table
    generate_table(df)
])

# starts app from command line, run Flask server
if __name__ == '__main__':
    app.run_server(debug=True)
