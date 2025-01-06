import pandas as pd
import streamlit as st
import util



"""
# Investment Records
"""

THIS_YEAR = util.this_year()
LAST_YEAR = util.last_year()
INVESTMENT_RECORDS = util.INVESTMENT_RECORDS

df = util.load_investment_record()
annual_investment = util.load_annual_investment()
this_year_investment = util.load_this_year_investment()
last_year_investment = util.last_year_investment()
total_acc_investment = util.total_acc_investment()
with st.expander('Add new record'):
    with st.form("new_invest_form"):
        in_date = st.date_input('Date')
        in_amount = st.number_input('Invest Amount (¥):',value=200000,format='%g',step=10000)
        in_year = in_date.year
        submitted = st.form_submit_button("Submit")
        if submitted:
            in_record = f'\n{in_date},{in_amount},{in_year}'
            with open(INVESTMENT_RECORDS, 'at') as f:
                f.write(in_record)
            st.rerun()
            st.write(in_record)
            st.write('submitted!')
col1,col2 = st.columns(2)
with col1:
    sec1,sec2= st.columns(2)
    sec1.metric(label=f'This Year ({THIS_YEAR})', value=f'¥{format(this_year_investment,',')}')
    sec2.metric(label=f'Last Year ({LAST_YEAR})', value=f'¥{format(last_year_investment,',')}')

    year_filter = st.multiselect(
        label='Year filter:',
        options=df['Year'].unique(),
        default=df['year'].max()
    )
    df_filtered = df.query('Year == @year_filter')[['Date','Amount']].sort_values(by='Date',ascending=False)
    st.dataframe(df_filtered,
                 hide_index=True,
                 column_config={
                    'Date': st.column_config.DateColumn(
                        format='YYYY-MM-DD'
                    ),
                    'Amount': st.column_config.NumberColumn(
                        'Amount(¥)',
                    )
                }
    )
with col2:
    st.metric(label=f'Total Investment', value=f'¥{format(total_acc_investment,',')}')
    st.bar_chart(annual_investment, x='Year',y='Amount',height=550)