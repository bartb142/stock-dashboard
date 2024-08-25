import pandas as pd
import streamlit as st
import util

st.set_page_config(
        page_title='Stock Dashboard',
        layout='wide',
        page_icon='assets/logo.png'
    )

# Page setup 
page1 = st.Page(
    page='pages/Stock_Porfolio.py',
    title='Stock Porfolio',
    icon=':material/account_balance:',
    default=True,
)

page2 = st.Page(
    page='pages/Investment_Records.py',
    title='Investment_Records',
    icon=':material/contract:',
)

page3 = st.Page(
    page='pages/Dividend.py',
    title='Dividend',
    icon=':material/payments:',
)

# Nav setup
pg = st.navigation(pages=[page1,page2,page3])
pg .run()