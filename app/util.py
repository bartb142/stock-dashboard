from pathlib import Path
from datetime import datetime
import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

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
    df['month'] = df['入金日'].dt.month
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

# Google Sheet related
# Authenticate with Google Sheets
def authenticate_gspread():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("data/sapient-tangent-382305-5ecc2d4bce4e.json", scopes=scope)
    return gspread.authorize(creds)

# Load data from Google Sheets
def load_sheet_data(sheet_url, sheet_name):
    client = authenticate_gspread()
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    data = sheet.get_all_records()
    return pd.DataFrame(data)

def load_specific_range(sheet_url, sheet_name, range_string):
    client = authenticate_gspread()
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    data = sheet.get(range_string)
    return pd.DataFrame.from_dict(data)

# Update a specific cell in Google Sheets
def update_cell(sheet_url, sheet_name, cell, value):
    """
    Update a specific cell in a Google Sheet.

    Args:
        sheet_url (str): URL of the Google Sheet
        sheet_name (str): Name of the worksheet/tab
        cell (str): Cell reference (e.g., "B2")
        value (str/int/float): Value to set in the cell
    """
    client = authenticate_gspread()
    sheet = client.open_by_url(sheet_url).worksheet(sheet_name)
    sheet.update_acell(cell, value)
