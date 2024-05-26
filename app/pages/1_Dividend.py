import pandas as pd
import streamlit as st
import util

util.common_page_config()

THIS_YEAR = util.this_year()

# Upload File
uploaded_file = st.file_uploader("Choose a file",type=['csv'])
if(uploaded_file is not None):
    pd.read_csv(uploaded_file).to_csv('data/stock_dividend.csv',index=False)

"""
# Dividend Dashboard
"""
if util.checkFile('data/stock_dividend.csv'):
    df = util.load_stock_dividend()
    total_dividend = util.get_total_dividend()
    this_year_dividend = util.get_this_year_dividend()
    annual_dividend = df[['year','dividend']].groupby('year',as_index=False).sum()

    col1,col2 = st.columns(2)
    with col1:
        st.metric(label="Total Dividend", value=f'¥{format(total_dividend,',')}', delta=f'¥{format(this_year_dividend,',')} ({THIS_YEAR}-now)')
        st.dataframe(df, hide_index=True)
    with col2:
        st.bar_chart(annual_dividend, x='year',y='dividend',height=550)
else:
    st.write('No Data.')
