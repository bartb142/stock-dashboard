import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path

THIS_YEAR = datetime.now().year
st.set_page_config(
    page_title='Stock Dashboard',
    layout='wide',
    page_icon='random'
)

def checkFile(path):
    file_path = Path(path)
    return file_path.exists()

# Upload File
uploaded_file = st.file_uploader("Choose a file",type=['csv'])
if(uploaded_file is not None):
    pd.read_csv(uploaded_file).to_csv('data/stock_dividend.csv',index=False)

"""
# Dividend Dashboard
"""
if checkFile('data/stock_dividend.csv'):
    df = pd.read_csv('data/stock_dividend.csv', parse_dates=['入金日'])
    df['year'] = df['入金日'].dt.year
    df['dividend'] = df['受取金額[円/現地通貨]'].str.replace(',','').astype(int)
    total_dividend = df['dividend'].sum()
    this_year_dividend = df[df['year'] == THIS_YEAR]['dividend'].sum()
    annual_dividend = df[['year','dividend']].groupby('year',as_index=False).sum()

    col1,col2 = st.columns(2)
    with col1:
        st.metric(label="Total Dividend", value=f'¥{format(total_dividend,',')}', delta=f'¥{format(this_year_dividend,',')} ({THIS_YEAR}-now)')
        st.dataframe(df, hide_index=True)
    with col2:
        st.bar_chart(annual_dividend, x='year',y='dividend',height=550)
else:
    st.write('No Data.')
