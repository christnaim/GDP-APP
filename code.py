subprocess.check_call(['pip', 'install', 'plotly'])
import subprocess
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Welcome to Christ Naim App", page_icon=":rocket:")

page = st.sidebar.selectbox("Select a page", ["Home", "GDP Top 4 European Countries 1960-2020", "GDP World Leaders 2000-2020"])

if page == "Home":
    st.balloons()
    st.title("Welcome To Christ Naim's App! :slightly_smiling_face:")
    st.header("")
    st.header("This app is intended to demonstrate the change in the Gross Domestic Product(GDP) of the top 4 European countries(Germany, France, UK, and Italy) from 1960 to 2020, and then compare these countries rankings against worldwide GDP leaders from 2000-2020")
    st.header("")
    
    st.header("This app is presented to **Dr. Fouad Zablith** at the American University of Beirut (AUB)")
    
    st.subheader("As part of MSBA 325 course: Data Visualization and Communication")
    st.header("")
    st.subheader("Presented on the 24th of September, 2023")

elif page == "GDP Top 4 European Countries 1960-2020":
    gdp_world=pd.read_csv("C:/Users/chris/OneDrive/Desktop/MSBA/Fall/MSBA 325 - Data Visualization & Communication\Homework\HW2\gdp_1960_2020.csv")

    gdp_Ger=gdp_world[gdp_world['country']=="Germany"]
    gdp_Fra=gdp_world[gdp_world['country']=="France"]
    gdp_UK=gdp_world[gdp_world['country']=="United Kingdom"]
    gdp_Ita=gdp_world[gdp_world['country']=="Italy"]

    gdp_Ger_2=gdp_Ger[['year','gdp']]
    gdp_Fra_2=gdp_Fra[['year','gdp']]
    gdp_Uk_2=gdp_UK[['year','gdp']]
    gdp_Ita_2=gdp_Ita[["year","gdp"]]

    gdp_top_eur = pd.merge(gdp_Ger_2, gdp_Fra_2, on='year', how="outer", suffixes=('_ger', '_fra'))
    gdp_top_eur = pd.merge(gdp_top_eur, gdp_Uk_2, on='year', how="outer", suffixes=('_ger', '_uk'))
    gdp_top_eur = pd.merge(gdp_top_eur, gdp_Ita_2, on='year', how='outer', suffixes=('_uk', '_ita'))

    gdp_top_eur.rename(columns={
        'gdp_ger': 'Germany',
        'gdp_fra': 'France',
        'gdp_uk': 'United Kingdom',
        'gdp_ita': 'Italy',
    }, inplace=True)

    st.title("GDP Visualization For Top 4 European Countries")
    st.subheader("Line Chart with Year Slider and Country Selection \U0001F4C8")

    selected_year = st.sidebar.slider("Select a Year", min_value=int(gdp_top_eur['year'].min()), max_value=int(gdp_top_eur['year'].max()), value=int(gdp_top_eur['year'].max()))

    selected_country = st.sidebar.multiselect("Select Countries", gdp_top_eur.columns[1:], default=list(gdp_top_eur.columns[1:]))

    filtered_gdp_top_eur = gdp_top_eur[gdp_top_eur['year'] <= selected_year][['year'] + selected_country]


    st.line_chart(filtered_gdp_top_eur.set_index('year'))

elif page == "GDP World Leaders 2000-2020":
    
    st.title("GDP Visualization For GDP World Leaders From 2000 - 2022 🌍")
    st.header("Bar Chart with Year Slider and Continent Selection \U0001F4CA")
    st.header("Hover Over Bars For Some Valuable Insights💡")

    gdp_world=pd.read_csv("C:/Users/chris/OneDrive/Desktop/MSBA/Fall/MSBA 325 - Data Visualization & Communication\Homework\HW2\gdp_1960_2020.csv")
    
    gdp_2000_2020=gdp_world[gdp_world['country'].isin(["the United States","Canada","China","India","South Korea","Germany","United Kingdom","France","Italy","Russia"])]
    
    gdp_2000_2020=gdp_2000_2020[gdp_2000_2020['year'].between(2000,2020)]
    
    #selected_year = st.sidebar.slider('Select a year', min_value=gdp_2000_2020['year'].min(), max_value=gdp_2000_2020['year'].max(),value=int(gdp_2000_2020['year'].max()))
    selected_year=st.sidebar.number_input("Select a year",min_value=gdp_2000_2020['year'].min(), max_value=gdp_2000_2020['year'].max(),value=int(gdp_2000_2020['year'].max()),step=1)

    filtered_data = gdp_2000_2020[gdp_2000_2020['year'] == selected_year]

    
    dflt_continents=gdp_2000_2020['continent'].unique()

    selected_continents=st.sidebar.multiselect("Select Continents", filtered_data['continent'].unique(),default=dflt_continents)

    filtered_data = filtered_data[filtered_data['continent'].isin(selected_continents)]

    continent_color_mapping={'Europe':'blue','Asia':'red','America':'green'}

    colors=filtered_data['continent'].map(continent_color_mapping)



    hover_template = "<b>Country:</b> %{x}<br><b>GDP:</b> %{y}<br><b>World Rank:</b> %{customdata[0]}<br><b>GDP Percent:</b> %{customdata[1]}"

    fig = go.Figure(data=[go.Bar(x=filtered_data['country'], y=filtered_data['gdp'],marker_color=colors,customdata=list(zip(filtered_data['rank'], filtered_data['gdp_percent'])),hovertemplate=hover_template)])


    fig.update_layout(
    title=f'GDP by Country for the year {selected_year}',
    xaxis=dict(title='Countries'),
    yaxis=dict(title='GDP on Log Scale',type='log'),
    legend=dict(title='Continent Legend',orientation='h',yanchor='bottom',y=1.02,xanchor='right',x=1))

    st.plotly_chart(fig)


    
