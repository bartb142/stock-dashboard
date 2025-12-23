import pandas as pd
import streamlit as st
import util

THIS_YEAR = util.this_year()

# Upload File
uploaded_file = st.file_uploader("Choose a file (Full data)",type=['csv'])
if(uploaded_file is not None):
    try:
        pd.read_csv(uploaded_file,encoding='shift_jis').to_csv('data/stock_dividend.csv',index=False, encoding='UTF8')
    except UnicodeDecodeError:
        pd.read_csv(uploaded_file,encoding='UTF8').to_csv('data/stock_dividend.csv',index=False, encoding='UTF8')
    uploaded_file = None
    st.rerun()

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
        
        """
        ### Dividend Received By Stock
        """
        year_filter = st.multiselect(
            label='Year filter:',
            options=df['year'].unique(),
            default=df['year'].max()
        )
        dividend_by_code_df = df.query('year == @year_filter').groupby(by=['銘柄コード','銘柄','month'])['dividend'].sum().sort_values(ascending=False)
        st.dataframe(dividend_by_code_df,
                    column_config={'銘柄コード': st.column_config.NumberColumn(format='%d'),})
    with col2:
        st.bar_chart(annual_dividend, x='year',y='dividend',height=550)
    
    """
    ### Monthly Dividend
    """
    md_filter = st.multiselect(
            label='Year:',
            options=df['year'].unique(),
            default=df['year'].max()
    )
    monthly_dividend = df[['year','month','dividend']].query('year == @md_filter').groupby('month',as_index=False).sum()
    st.bar_chart(monthly_dividend, x='month',y='dividend')
    """
    ### Dividend Records
    """
    st.dataframe(df, hide_index=True,
                    column_config={
                        '入金日': st.column_config.DateColumn(
                            format='YYYY-MM-DD'
                        ),
                        '銘柄コード': st.column_config.NumberColumn(
                            format='%d'
                        ),
                        'year': st.column_config.NumberColumn(
                            format='%d'
                        )
                    }
        )

else:
    st.write('No Data.')
