# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.
from dash import Dash, html, dcc, Input, Output, callback, dash_table, State,ctx
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
        html.Div(className="sidebar-contents", children=[
            html.Label(children='Selected Vintages:'),
            dcc.Dropdown(id="selected-vintages", options=[], value=[]),
            html.Label(children='First Second'),
            dcc.Dropdown(id='first-second', options=clist1, ),
            html.Label(children='Branding'),
            dcc.Dropdown(id='branding', options=clist2),
            html.Label(children='Channel'),
            dcc.Dropdown(id='channel',options=clist3),
            html.Label(children='Source'),
            dcc.Dropdown(id='source',options=clist4),
            html.Label(children='Association'),
            dcc.Dropdown(id='association',options=clist5),
            html.Label(children='Annual Fee Group'),
            dcc.Dropdown(id='annualfeegrp',options=clist6),
            html.Label(children='Original Credit Line Range'),
            dcc.Dropdown(id='ogcredrange',options=clist7),
            html.Button('Submit', id='submit-btn', n_clicks=0),
            html.Button('Add Vintage', id='add-btn', n_clicks=0, disabled=True),
            html.Button('Reset Vintages', id='reset-btn', n_clicks=0),
        ]),
    ]),    

    
    html.Div(className = "vintage", children=[html.H1(children='Vintage Comparison'),
        html.Div(id="filters"),
        dcc.Dropdown(
            id='vintages',
            options=[{'label':i, 'value':i} for i in clist],
            multi=True,
            value=None,
            className='main-dd'
        ),
    
        ##*CONDITIONAL RENDERING: graph values are based off Submit and Add buttons !! need to make a switch statement of some sort ??
        html.Div(id='df-table', children={}),   
     
    ]),
])

###     CALLBACK FUNCTIONS     #


#*cb for grabbing the values from Vintage Multiselect to use as options for Selected Vintages dropdown
@app.callback(
    Output(component_id='selected-vintages', component_property='options'),
    Input(component_id='vintages', component_property='value'),
    prevent_initial_call=True
)
def setSelectedVintages(vintages):
     return vintages
 
 
#* function to grab filtered values and make new dataframe
@app.callback(
    Output('df-table', 'children'),
    Output('add-btn', 'disabled'),
    Input('submit-btn', 'n_clicks'),
    Input('selected-vintages', 'value'),
    Input('first-second', 'value'),
    Input('branding', 'value'),
    Input('channel', 'value'),
    Input('source', 'value'),
    Input('association', 'value'),
    Input('annualfeegrp', 'value'),
    Input('ogcredrange', 'value'),
    # State('ogcredrange', 'value')
    # prevent_initial_call=True
  
)
def submit_df_on_click(clicks, v, fs, b, c, s, a, afg, oclr):
    if 'submit-btn' == ctx.triggered_id:
        submit_df = df.loc[(df['Vintage'] == v)
                        & (df['FirstSecond'] == fs)
                        & (df['Branding'] == b)
                        & (df['Channel'] == c)
                        & (df['Source'] == s)
                        & (df['Association'] == a)
                        & (df['AnnualFeeGroup'] == afg)
                        & (df['OriginalCreditLineRange'] == oclr)]
    
        fig1 = px.line(submit_df.melt(id_vars="Vintage"), x=submit_df['MonthsOnBooks'], y=submit_df['ActiveAccountIndicator'], color=submit_df['Vintage'],
                    markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
        fig2 = px.line(submit_df.melt(id_vars="Vintage"), x=submit_df['MonthsOnBooks'], y=submit_df['CumlROAAnnualized'], color=submit_df['Vintage'],
                    markers=True, title='Cumulative ROA Annualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
        fig2.update_layout(yaxis_ticksuffix=".3%") 
        fig3 = px.line(submit_df.melt(id_vars="Vintage"), x=submit_df['MonthsOnBooks'], y=submit_df['CumlPreTaxIncome'], color=submit_df['Vintage'],
                    markers=True, title='Cumulative PreTax Income', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
        fig4 = px.line(submit_df.melt(id_vars="Vintage"), x=submit_df['MonthsOnBooks'], y=submit_df['EndingReceivable'], color=submit_df['Vintage'],
                    markers=True, title='Ending Receivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
        return html.Div([
            dash_table.DataTable(
            data=submit_df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in submit_df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'}) ,
            
            dcc.Graph(id='fig1', figure=fig1 ),
            dcc.Graph(id='fig2', figure=fig2),
            dcc.Graph(id='fig3', figure=fig3),
            dcc.Graph(id='fig4', figure=fig4)
        ]), False
    else:
        
        fig1 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['ActiveAccountIndicator'], color=df['Vintage'],
                    markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
        fig2 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['CumlROAAnnualized'], color=df['Vintage'],
                    markers=True, title='Cumulative ROA Annualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
        fig2.update_layout(yaxis_ticksuffix=".3%") 
        fig3 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['CumlPreTaxIncome'], color=df['Vintage'],
                    markers=True, title='Cumulative PreTax Income', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
        fig4 = px.line(df.melt(id_vars="Vintage"), x=df['MonthsOnBooks'], y=df['EndingReceivable'], color=df['Vintage'],
                    markers=True, title='Ending Receivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
        
        return html.Div([
            dash_table.DataTable(
            data=df.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df.columns],
            page_size=10,
            style_table={'overflowX': 'auto'}) ,
            
            dcc.Graph(id='fig1', figure=fig1 ),
            dcc.Graph(id='fig2', figure=fig2),
            dcc.Graph(id='fig3', figure=fig3),
            dcc.Graph(id='fig4', figure=fig4)
        ]), True
    

#* cb for add button, grab filters and make new df, concat with existing df        
# @app.callback(Output('df-table', 'children'), 
#             Input('add-btn', 'n_clicks'),
#             Input('df-table', 'children'),
#             Input('selected-vintages', 'value'),
#             Input('first-second', 'value'),
#             Input('branding', 'value'),
#             Input('channel', 'value'),
#             Input('source', 'value'),
#             Input('association', 'value'),
#             Input('annualfeegrp', 'value'),
#             Input('ogcredrange', 'value'), 
#             prevent_initial_call=True)
# def add_df_on_click(clicks, table, v, fs, b, c, s, a, afg, oclr):
#     if 'add-btn' == ctx.triggered_id:
#         new_df = df.loc[(df['Vintage'] == v)
#                         & (df['FirstSecond'] == fs)
#                         & (df['Branding'] == b)
#                         & (df['Channel'] == c)
#                         & (df['Source'] == s)
#                         & (df['Association'] == a)
#                         & (df['AnnualFeeGroup'] == afg)
#                         & (df['OriginalCreditLineRange'] == oclr)]
#     # add_df = pd.concat(table, new_df)
#     return html.Div(table)


if __name__ == '__main__':
    app.run(debug=True)