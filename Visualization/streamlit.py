#!/usr/bin/env python3
"""
The purpose of streamlit.py is to create and demonstrate a new library(https://www.streamlit.io/) that helps to build data apps quickly.

:: Functions ::
    def load_data(path)
        - path: The path to the dataframe

Author(s): Dan Blevins
"""

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

#Read, clean, and cache data
@st.cache(allow_output_mutation=True)
def load_data(path):
    data = pd.read_csv(path, encoding="ISO-8859-1")
    data = data.loc[data['Country'].isin(['United Kingdom', 'France', 'Italy'])]
    data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
    data['InvoiceYearMonth'] = data['InvoiceDate'].map(lambda date: 100*date.year + date.month)
    data['int_InvoiceYearMonth'] = data['InvoiceYearMonth']
    data['InvoiceYearMonth'] = pd.to_datetime(data['InvoiceYearMonth'], format='%Y%m')
    data['Revenue'] = data['UnitPrice'] * data['Quantity']
    return data
data = load_data('./data/OnlineRetail.csv')

#Create Title and sidebar
st.title('Marketing KPIs for European Consumers')
chart = st.sidebar.selectbox(
    "How would you like to view the data?",
    ('Line Charts','Bar Charts')
    )
country = st.sidebar.radio(
    "Filter by Country",
    ('All',)+ tuple(data['Country'].unique())
    )

#Visualize data
if country == 'All':
    st.title('Europe')
    rev = data.groupby(['InvoiceYearMonth'])['Revenue'].sum().reset_index()
    rev['MonthlyGrowth'] = rev['Revenue'].pct_change().fillna(0)
    rev_monthly_active = data.groupby('InvoiceYearMonth')['CustomerID'].nunique().reset_index()

    if chart == 'Line Charts':
        fig = px.line(rev, x="InvoiceYearMonth", y="Revenue", title='Total Monthly Revenue')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(rev, x="InvoiceYearMonth", y="MonthlyGrowth", title='Total Monthly Growth Rate')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(rev_monthly_active, x="InvoiceYearMonth", y="CustomerID", title='Total Monthly Active Users')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(rev, x="InvoiceYearMonth", y="Revenue", title='Total Monthly Revenue')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(rev, x="InvoiceYearMonth", y="MonthlyGrowth", title='Total Monthly Growth Rate')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(rev_monthly_active, x="InvoiceYearMonth", y="CustomerID", title='Total Monthly Active Users')
        st.plotly_chart(fig, use_container_width=True)
else:
    st.title(country)
    sub = data[data['Country'] == country]
    rev = sub.groupby(['InvoiceYearMonth'])['Revenue'].sum().reset_index()
    rev['MonthlyGrowth'] = rev['Revenue'].pct_change().fillna(0)
    rev_monthly_active = sub.groupby('InvoiceYearMonth')['CustomerID'].nunique().reset_index()

    if chart == 'Line Charts':
        fig = px.line(rev, x="InvoiceYearMonth", y="Revenue", title='Total Monthly Revenue')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(rev, x="InvoiceYearMonth", y="MonthlyGrowth", title='Total Monthly Growth Rate')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.line(rev_monthly_active, x="InvoiceYearMonth", y="CustomerID", title='Total Monthly Active Users')
        st.plotly_chart(fig, use_container_width=True)
    else:
        fig = px.bar(rev, x="InvoiceYearMonth", y="Revenue", title='Total Monthly Revenue')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(rev, x="InvoiceYearMonth", y="MonthlyGrowth", title='Total Monthly Growth Rate')
        st.plotly_chart(fig, use_container_width=True)
        fig = px.bar(rev_monthly_active, x="InvoiceYearMonth", y="CustomerID", title='Total Monthly Active Users')
        st.plotly_chart(fig, use_container_width=True)