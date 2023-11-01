# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc, Input, Output, callback, dash_table
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__)

df = pd.read_csv(
    r"U:\repo\dashtest\Data_Test.csv", dtype="unicode")

dfFix =df.replace(np.nan, 'None')
df = dfFix

#lists for selects and dropdowns
clist = df['Vintage'].unique()
clist1 = df['FirstSecond'].unique()
clist2 = df['Branding']. unique()
clist3 = df['Channel'].unique()
clist4 = df['Source'].unique()
clist5 = df['Association'].unique()
clist6 = df['AnnualFeeGroup'].unique()
clist7 = df['OriginalCreditLineRange'].unique()

###     figures and graphs     ###
fig1 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['ActiveAccountIndicator'], color=df['Vintage'],
                    markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
fig2 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['CumlROAAnnualized'], color=df['Vintage'],
                    markers=True, title='Cumulative ROA Annualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
fig2.update_layout(yaxis_ticksuffix=".3%") 
fig3 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['CumlPreTaxIncome'], color=df['Vintage'],
                    markers=True, title='Cumulative PreTax Income', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
fig4 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['EndingReceivable'], color=df['Vintage'],
                    markers=True, title='Ending Receivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})

###     making table from default dataframe     ###
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])
    
###      MAIN APP      ###
app.layout = html.Div(className = 'wrapper', children=[
    
html.Div(className = "sidebar", children=[
    html.Label(children='Selected Vintages:'),
    dcc.Dropdown(id="selected-vintages", options=[], value=[]),
    html.Label(children='First Second'),
    dcc.Dropdown(options=clist1, id='first-second'),
    html.Label(children='Branding'),
    dcc.Dropdown(options=clist2),
    html.Label(children='Channel'),
    dcc.Dropdown(options=clist3),
    html.Label(children='Source'),
    dcc.Dropdown(options=clist4),
    html.Label(children='Association'),
    dcc.Dropdown(options=clist5),
    html.Label(children='Annual Fee Group'),
    dcc.Dropdown(options=clist6),
    html.Label(children='Original Credit Line Range'),
    dcc.Dropdown(options=clist7),
    html.Button('Submit', id='submit-btn', n_clicks=0)
    ]),    

    
    html.Div(className = "vintage", children=[html.H1(children='Vintage Comparison'),
    html.Div( id="filters"),
    
    dcc.Dropdown(
            id='vintages',
            options=[{'label':i, 'value':i} for i in clist],
            multi=True,
            value=None
        ),
    
    dash_table.DataTable(
    data=df.to_dict('records'),
    columns=[{'id': c, 'name': c} for c in df.columns],
    page_size=10,
     style_table={'overflowX': 'auto'},
),
    
    dcc.Graph(id='fig1', figure=fig1),
    dcc.Graph(id='fig2', figure=fig2),
    dcc.Graph(id='fig3', figure=fig3),
    dcc.Graph(id='fig4', figure=fig4),
    
    ]),
])

###     CALLBACK FUNCTIONS     #

@app.callback(
    Output(component_id='selected-vintages', component_property='options'),
    # Output(component_id='selected-vintages',component_property='value'),
    Input(component_id='vintages', component_property='value'),
    prevent_initial_call=True
)
def setSelectedVintages(vintages):
     return vintages

@app.callback(
    Output('filters', 'children'),
    Input('submit-btn', 'n_clicks'),
    Input('first-second', 'value')
)
def return1and2(clicks, selected):
    return clicks, selected

if __name__ == '__main__':
    app.run(debug=True)
