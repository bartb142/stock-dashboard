import pandas as pd
import streamlit as st
import util


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
    df['Dividend%'] = (df['dividend_per_share'] / df['acquired_price'] * 100).round(2)
    df['Annual Dividend'] = df['dividend_per_share'] * df['shares']
    df.loc[df['account'] != "NISA", 'Annual Dividend'] = df.loc[df['account'] != "NISA", 'Annual Dividend'] * 0.8
    
    total_annual_dividend = int(df['Annual Dividend'].sum())

    st.metric(label="Annual Dividend", value=f'¥{format(total_annual_dividend,',')}')
    df = st.data_editor(df,
                        hide_index=True,
                        num_rows='dynamic',
                        column_config={
                            'stock_code': st.column_config.NumberColumn('Stock Code',format='%d'),
                            'Dividend%': st.column_config.NumberColumn('Dividend %',format='%.2f％'),
                        },
                        disabled=['Total Stock Acquired'])
    if st.button("Update"):
        df.to_csv('data/stock_records.csv',index=False)
        st.success('Table is updated!', icon="✅")