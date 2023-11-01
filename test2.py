import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

#possible features:
#error handling
    #if a vintage is already added
    # if a vintage w filters does not exist - DONE
        #for both Submit and Add - DONE
#conditional rendering/disabling/enabling certain buttons
    #only submit appears first
    #once one vintage is added, switch button to add
#clear functionality or reset to default
    #reset button present at all times
#deleting a single vintage from the graphs 
#put graph rendering in functions to reduce redundancy

df = pd.read_csv(
    r"C:\Users\JeAdkins\OneDrive - CreditOne Bank\Documents\Data_Test.csv", dtype="unicode")

#Replace any NaN values in table with a string "None"
#Graph won't render otherwise
dfFixNone = df.replace(np.nan, 'None')
df = dfFixNone

clist = df['Vintage'].unique()
clist1 = df['FirstSecond'].unique()
clist2 = df['Branding']. unique()
clist3 = df['Channel'].unique()
clist4 = df['Source'].unique()
clist5 = df['Association'].unique()
clist6 = df['AnnualFeeGroup'].unique()
clist7 = df['OriginalCreditLineRange'].unique()


# initialize default dataframe to hold ALL csv data
if 'df_default' not in st.session_state:
    st.session_state['df_default'] = df

# initialize blank dataframe to hold First df created from user filters
if 'blank_df' not in st.session_state:
    st.session_state['blank_df'] = pd.DataFrame(columns=[
        "Vintage", "FirstSecond", 'Branding', 'Channel', 'Source',
        'Association', 'AnnualFeeGroup', "OriginalCreditLineRange", "MonthsOnBooks", "NewAccountIndicator",
        "ActiveAccountIndicator", "PreTaxIncome", "EndingReceivable", "CumlNewAccountIndicator", "CumlActiveAccountIndicator",
        "CumlPreTaxIncome", "CumlEndingReceivable", "AverageActives", "AverageReceivable", "CumlROA", "CumlROAAnnualized"])

# initialize dataframe to be added to the main dataframe
if "added_df" not in st.session_state:
    st.session_state['added_df'] = pd.DataFrame(columns=[
        "Vintage", "FirstSecond", 'Branding', 'Channel', 'Source',
        'Association', 'AnnualFeeGroup', "OriginalCreditLineRange", "MonthsOnBooks", "NewAccountIndicator",
        "ActiveAccountIndicator", "PreTaxIncome", "EndingReceivable", "CumlNewAccountIndicator", "CumlActiveAccountIndicator",
        "CumlPreTaxIncome", "CumlEndingReceivable", "AverageActives", "AverageReceivable", "CumlROA", "CumlROAAnnualized"])
    
# initialize default dataframe to hold ALL csv data
if 'df_clear' not in st.session_state:
    st.session_state['df_clear'] = df
    
#initialize boolean for adding a new vintage
#True - the user wants to add another vintage
#False - the user has not yet added another vintage
if "isDfAdded" not in st.session_state:
    st.session_state['isDfAdded'] = False
    
if "isDfSubmitted" not in st.session_state:
    st.session_state['isDfSubmitted'] = False

if "dfState" not in st.session_state:
    st.session_state['dfState'] = "Submit"
    
def submit_callback():
    if submit:
        df_new = df.loc[(df['Vintage'] == selected)
                        & (df['FirstSecond'] == FirstSecond)
                        & (df['Branding'] == Branding)
                        & (df['Channel'] == Channel)
                        & (df['Source'] == Source)
                        & (df['Association'] == Association)
                        & (df['AnnualFeeGroup'] == AnnualFeeGroup)
                        & (df['OriginalCreditLineRange'] == OriginalCreditLineRange)]
        #check if anything matches filters 
        if df_new.empty == True:
            st.warning('The specified vintage does not exist.', icon="⚠️") 
        else:
        # store this new df into df made earlier
            st.session_state['blank_df'] = pd.concat(
            [st.session_state['blank_df'], df_new], axis=0)
            st.session_state['isDfSubmitted'] = True;
            st.session_state['dfState'] = "Add"
    

# def main():
#     if submit:
#         # filter from original df using selected values
#         # create a new filtered df from the entire df
#         df_new = df.loc[(df['Vintage'] == selected)
#                         & (df['FirstSecond'] == FirstSecond)
#                         & (df['Branding'] == Branding)
#                         & (df['Channel'] == Channel)
#                         & (df['Source'] == Source)
#                         & (df['Association'] == Association)
#                         & (df['AnnualFeeGroup'] == AnnualFeeGroup)
#                         & (df['OriginalCreditLineRange'] == OriginalCreditLineRange)]
#         #check if anything matches filters 
#         if df_new.empty == True:
#             st.warning('The specified vintage does not exist.', icon="⚠️") 
#         else:
#         # store this new df into df made earlier
#             st.session_state['blank_df'] = pd.concat(
#             [st.session_state['blank_df'], df_new], axis=0)
#             st.session_state['isDfSubmitted'] = True;
#             st.session_state['dfState'] = "Add"
  

def add_to_main():
    if add:
        df_add = df.loc[(df['Vintage'] == selected)
                        & (df['FirstSecond'] == FirstSecond)
                        & (df['Branding'] == Branding)
                        & (df['Channel'] == Channel)
                        & (df['Source'] == Source)
                        & (df['Association'] == Association)
                        & (df['AnnualFeeGroup'] == AnnualFeeGroup)
                        & (df['OriginalCreditLineRange'] == OriginalCreditLineRange)]
        #ERROR - if the vintage user tries to add doesnt exist, output warning
        if df_add.empty == True:
            st.warning('The specified vintage does not exist.', icon="⚠️") 
        if df_add.merge(st.session_state['blank_df']).shape == df_add.shape == True:
            st.warning('The specified vintage has been added.', icon="⚠️") 
        if df_add.merge(st.session_state['added_df']).shape == df_add.shape == True:
            st.warning('The specified vintage has been added.', icon="⚠️") 
        #IF THE ADDED DF IS EMPTY
        #User has not yet added another dataframe to the initial dataframe, this runs if the Add button is hit for the First time
        if st.session_state['added_df'].empty == True:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['blank_df'], df_add], axis=0)
        #IF THE ADDED DF IS NOT EMPTY
        #User has added a df before, just take the previous df and concat with new one
        elif st.session_state['added_df'].empty == False:
            st.session_state['added_df'] = pd.concat(
                [st.session_state['added_df'], df_add], axis=0)
        st.session_state['isDfAdded'] = True
        
def clear_main():
    if clear:
        if st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
            st.session_state['added_df'] = st.session_state['df_default']
        elif st.session_state['blank_df'].empty == False and st.session_state['isDfAdded'] == False:
            st.session_state['blank_df'] = st.session_state['df_default']
        # st.session_state.vintages_selected = []
    else:
        return
        
            

def return_graphs(graph):
    fig1a = px.line(graph.melt(id_vars="Vintage"), x=graph['MonthsOnBooks'], y=df['ActiveAccountIndicator'], color=graph['Vintage'],
                    markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig1a)
    fig1b = px.line(graph.melt(id_vars="Vintage"), x=graph['MonthsOnBooks'], y=graph['CumlROAAnnualized'], color=graph['Vintage'],
                    markers=True, title='Cumulative ROA Annualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
    fig1b.update_layout(yaxis_ticksuffix=".3%") 
    st.plotly_chart(fig1b)
    fig1c = px.line(graph.melt(id_vars="Vintage"), x=graph['MonthsOnBooks'], y=graph['CumlPreTaxIncome'], color=graph['Vintage'],
                    markers=True, title='Cumulative PreTax Income', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig1c)
    fig1d = px.line(graph.melt(id_vars="Vintage"), x=graph['MonthsOnBooks'], y=graph['EndingReceivable'], color=graph['Vintage'],
                    markers=True, title='Ending Receivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig1d)

st.header("Vintage Comparison")
options = st.multiselect("Select vintages:", clist, key="vintages_selected")
with st.form('my_form'):
    with st.sidebar:
    
        st.header('Filters')
        selected = st.selectbox("Selected Vintages:",
                                options, key="current_vintage")
        FirstSecond = st.selectbox("FirstSecond:", clist1)
        Branding = st.selectbox("Branding", clist2)
        Channel = st.selectbox("Channel", clist3)
        Source = st.selectbox("Source", clist4)
        Association = st.selectbox("Association", clist5)
        AnnualFeeGroup = st.selectbox("AnnualFeeGroup", clist6)
        OriginalCreditLineRange = st.selectbox(
            "OriginalCreditLineRange", clist7)
        submit = st.form_submit_button(label="Submit", on_click=submit_callback)
        add = st.form_submit_button('Add')
        clear = st.form_submit_button('Reset Vintages')
        

if __name__ == "__main__":
    # main()
    submit_callback()
    clear_main()
    add_to_main()   
    
# if __name__ == "__main__" and st.session_state['isDfSubmitted'] == True:
    
#ENTIRE DF AND ALL PLOT LINES ON LOAD, this is default case
if st.session_state['blank_df'].empty == True:
    st.write(df)
    return_graphs(df)
#THE FIRST FILTERED DF WILL DISPLAY, this case happens on first click of "Display Vintage"
elif st.session_state['blank_df'].empty == False and st.session_state['isDfAdded'] == False:
    st.dataframe(st.session_state['blank_df'])
    fig2a = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['ActiveAccountIndicator'],
                    color=st.session_state['blank_df']['Vintage'], markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig2a)
    fig2b = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['CumlROAAnnualized'],
                    color=st.session_state['blank_df']['Vintage'], markers=True, title='Cumulative ROA Annualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
    fig2b.update_layout(yaxis_ticksuffix=".3%")
    st.plotly_chart(fig2b)
    fig2c = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['CumlPreTaxIncome'],
                    color=st.session_state['blank_df']['Vintage'], markers=True, title='Cumulative PreTax Income', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig2c)
    fig2d = px.line(st.session_state['blank_df'].melt(id_vars="Vintage"), x=st.session_state['blank_df']['MonthsOnBooks'], y=st.session_state['blank_df']['EndingReceivable'],
                    color=st.session_state['blank_df']['Vintage'], markers=True, title='Ending Receivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig2d)
#THE ADDED VINTAGES WILL DISPLAY, this case happens after n clicks of "Add a Vintage"
elif st.session_state['added_df'].empty == False and st.session_state['isDfAdded'] == True:
    st.dataframe(st.session_state['added_df'])
    fig3a = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['ActiveAccountIndicator'],
                    color=st.session_state['added_df']['Vintage'], markers=True, title='Active Accounts', labels={'y': 'Active Accounts', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig3a)
    fig3b = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['CumlROAAnnualized'],
                    color=st.session_state['added_df']['Vintage'], markers=True, title='Cumulative ROA Annualized', labels={'y': 'ROAAnnualized', 'x': 'Months on Book', "color": "Vintage"})
    fig3b.update_layout(yaxis_ticksuffix=".3%")
    st.plotly_chart(fig3b)
    fig3c = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['CumlPreTaxIncome'],
                    color=st.session_state['added_df']['Vintage'], markers=True, title='Cumulative PreTax Income', labels={'y': 'PreTaxIncome', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig3c)
    fig3d = px.line(st.session_state['added_df'].melt(id_vars="Vintage"), x=st.session_state['added_df']['MonthsOnBooks'], y=st.session_state['added_df']['EndingReceivable'],
                    color=st.session_state['added_df']['Vintage'], markers=True, title='Ending Receivable', labels={'y': 'EndingReceivable', 'x': 'Months on Book', "color": "Vintage"})
    st.plotly_chart(fig3d)
