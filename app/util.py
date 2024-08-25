from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd

STOCK_DIVIDEND = 'data/stock_dividend.csv'
INVESTMENT_RECORDS = 'data/investment_records.csv'
ACCOUNT_DETAILS = 'data/account_details.csv'


def this_year():
    return datetime.now().year

def last_year():
    return this_year() - 1 

def checkFile(path):
    file_path = Path(path)
    return file_path.exists()


#Data Related

# Dividend Dashboard
def load_stock_dividend():
    df = pd.read_csv(STOCK_DIVIDEND, parse_dates=['入金日'])
    df['year'] = df['入金日'].dt.year
    df['dividend'] = df['受取金額[円/現地通貨]'].str.replace(',','').astype(int)
    return df

def get_total_dividend():
    df = load_stock_dividend()
    return df['dividend'].sum()

def get_this_year_dividend():
    df = load_stock_dividend()
    return df[df['year'] == this_year()]['dividend'].sum()

# Investment Records
def load_investment_record():
    return pd.read_csv(INVESTMENT_RECORDS,parse_dates=['Date'])

def load_annual_investment():
    df = load_investment_record()
    return df[['Year','Amount']].groupby('Year',as_index=False).sum()
def load_this_year_investment():
    df = load_investment_record()
    return df[df['Year'] == this_year()]['Amount'].sum()
def last_year_investment():
    df = load_investment_record()
    return df[df['Year'] == last_year()]['Amount'].sum()
def total_acc_investment():
    df = load_investment_record()
    return df['Amount'].sum()