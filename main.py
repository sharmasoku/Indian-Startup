import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('startup_clean.csv')
st.set_page_config(layout='wide',page_title='StartUp Analysis')

# data cleaning
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year



def load_investor_info(investor):
    # showing investors name
    st.header(investor)
    # showing investors recently funds
    last_5df = df[df['investors'].str.contains(investor)][['date', 'startup', 'vertical', 'city', 'investment type', 'amount']].head()
    st.subheader('Most Recent Investments')
    st.dataframe(last_5df)
    # highest Investment
    col1,col2 = st.columns(2)
    with col1:
        high_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investment')
        st.dataframe(high_series)
    with col2:
        fig, ax = plt.subplots()
        ax.bar(high_series.index,high_series.values)

        st.pyplot(fig)

    col3,col4 = st.columns(2)
    with col3:
        # investment sector
        field_df = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        fig1, ax1 = plt.subplots()
        ax1.pie(field_df,labels = field_df.index,autopct = "%0.01f%%")

        st.subheader('Investment Sectors')
        st.pyplot(fig1)

    with col4:
        # most investment city area
        city_df = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(ascending=False)
        fig2, ax2 = plt.subplots()
        ax2.pie(city_df, labels=city_df.index, autopct="%0.01f%%")

        st.subheader('City')
        st.pyplot(fig2)

    #year to year investment
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    y2y_df = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    fig3, ax3 = plt.subplots()
    ax3.plot(y2y_df.index,y2y_df.values )

    st.subheader('Y2Y Investment')
    st.pyplot(fig3)

def load_overall_analysis():
    # total funded amount
    total_amount =round(df['amount'].sum())
    # max funded amount
    max_amount = df.groupby('startup')['amount'].max().sort_values(ascending =False).head(1).values[0]
    # avg funded amount
    avg_amount =round(df.groupby('startup')['amount'].sum().mean())
    # total funded startups
    num_startups = df['startup'].nunique()

    col11,col12,col13,col14 = st.columns(4)
    with col11:
        st.metric('Total',str(round(df['amount'].sum()))+" Cr")
    with col12:
        st.metric('Max',str(max_amount)+" Cr")
    with col13:
        st.metric('Avg',str(avg_amount)+" Cr")
    with col14:
        st.metric('Funded Startups',num_startups)

    st.header('MoM graph')
    selected_option = st.selectbox('Select Type', ['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')

    fig5, ax5 = plt.subplots()
    ax5.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig5)


#main
st.sidebar.title('Start-up Funding Analysis')
choice = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])
if choice=='Overall Analysis':
    st.title('Overall Analysis')
    load_overall_analysis()





elif choice=='Startup':
    st.title('Startup Analysis')
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Search')
else:
    st.title('Investor Analysis')
    selected_investor = st.sidebar.selectbox('Select Investor', sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Search')
    if btn2:
        load_investor_info(selected_investor)




