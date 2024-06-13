import pandas as pd
import streamlit as st
import util

util.common_page_config()

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

col1,col2,col3,col4 = st.columns(4)
with col1:
    if(total_dividend and this_year_dividend):
        st.metric(label="Total Dividend", value=f'¥{format(total_dividend,',')}', delta=f'¥{format(this_year_dividend,',')} ({THIS_YEAR}-now)')

"""
# Stock Portfolio
"""
if util.checkFile('data/stock_records.csv'):
    df = pd.read_csv('data/stock_records.csv')
    df['Total Stock Acquired'] = df['acquired_price'] * df['shares']
    df = st.data_editor(df,
                        hide_index=True,
                        num_rows='dynamic',
                        column_config={
                            'stock_code': st.column_config.NumberColumn('Stock Code',format='%d')
                        },
                        disabled=['Total Stock Acquired'])
    df.to_csv('data/stock_records.csv',index=False)