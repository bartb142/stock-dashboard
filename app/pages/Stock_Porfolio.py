import pandas as pd
import streamlit as st
import util
import plotly.express as px


THIS_YEAR = util.this_year()

"""
# Metrics
"""
total_dividend = False
this_year_dividend = False
if util.checkFile('data/stock_dividend.csv'):
    df = util.load_stock_dividend()
    total_dividend = util.get_total_dividend()
    this_year_dividend = util.get_this_year_dividend()

col1,col2 = st.columns(2)
with col1:
    if(total_dividend and this_year_dividend):
        st.metric(label="Total Dividend", value=f'¥{format(total_dividend,',')}', delta=f'¥{format(this_year_dividend,',')} ({THIS_YEAR}-now)')

"""
# Account details
"""
def get_account_metrics():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Wyd6NrRmjeuByDffQOC_OCwD9GsYIYe6bUn07Tjkgm4"
    SHEET_NAME = "streamlit_metrics"
    df = util.load_sheet_data(SHEET_URL, SHEET_NAME)
    df.to_csv('data/account_metrics.csv',index=False)

if util.checkFile('data/account_metrics.csv'):
    metrics_df = pd.read_csv('data/account_metrics.csv')
    MAX_COLUMNS = 4
    columns = st.columns(MAX_COLUMNS) # create 4 columns
    for idx, label in enumerate(metrics_df.columns):
        col = columns[idx % MAX_COLUMNS]
        col.metric(label=label, value=str(metrics_df[label][0]))


"""
# Stock Portfolio
"""
def get_stock_records():
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1Wyd6NrRmjeuByDffQOC_OCwD9GsYIYe6bUn07Tjkgm4"
    SHEET_NAME = "Bart"
    df = util.load_sheet_data(SHEET_URL, SHEET_NAME)
    df = df[0:12] # get the range to 12th row
    df.to_csv('data/stock_records.csv',index=False)

if util.checkFile('data/stock_records.csv'):
    df = pd.read_csv('data/stock_records.csv')

    # Data for Stock Holding share pie chart
    df_stock = df[['stock name','total stock acquired']].copy()
    df_stock['total stock acquired'] = df_stock['total stock acquired'].str.replace('¥','')
    df_stock['total stock acquired'] = df_stock['total stock acquired'].str.replace(',','')
    df_stock['total stock acquired'] = df_stock['total stock acquired'].astype(int)
    df_stock = df_stock.groupby(by='stock name', as_index=False).sum()
    fig = px.pie(df_stock, names='stock name', values='total stock acquired', title="Stock Holdings Share")
    st.dataframe(df,
                 hide_index=True,
                 column_config={
                    'stock_code': st.column_config.NumberColumn('Stock Code',format='%d'),
                    'Dividend%': st.column_config.NumberColumn('Dividend %',format='%.2f％'),
                        })
    st.plotly_chart(fig)

with st.sidebar:
    if st.button("Update"):
        get_stock_records()
        get_account_metrics()
        st.rerun()
        st.toast('Table is updated!', icon="✅")