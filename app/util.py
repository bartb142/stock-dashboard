from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd



def this_year():
    return datetime.now().year

def last_year():
    return this_year() - 1 

def checkFile(path):
    file_path = Path(path)
    return file_path.exists()

def common_page_config():
    st.set_page_config(
        page_title='Stock Dashboard',
        layout='wide',
        page_icon='assets/logo.png'
    )

#Data Related

# Dividend Dashboard
def load_stock_dividend():
    df = pd.read_csv('data/stock_dividend.csv', parse_dates=['入金日'])
    df['year'] = df['入金日'].dt.year
    df['dividend'] = df['受取金額[円/現地通貨]'].str.replace(',','').astype(int)
    return df

def get_total_dividend():
    df = load_stock_dividend()
    return df['dividend'].sum()

def get_this_year_dividend():
    df = load_stock_dividend()
    return df[df['year'] == this_year()]['dividend'].sum()