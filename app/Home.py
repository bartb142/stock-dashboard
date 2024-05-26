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