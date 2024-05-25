import pandas as pd
import streamlit as st
from datetime import datetime

THIS_YEAR = datetime.now().year
st.set_page_config(
    page_title='Stock Dashboard',
    layout='wide',
    page_icon='assets/logo.png'
)


st.write('Welcomes!!')