#importing libraries
import pandas as pd
import pymongo
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
from PIL import Image

#setting up page configuration
st.set_page_config(page_title = "Airnbn Data Visualization",
                   layout = "wide",
                   initial_sidebar_state = "expanded",
                   menu_items={'About': """# The dashboard app is created !
                                        Data has been gathered from mongodb atlas"""}
)

#setting up title
st.title("Airbnb Analysis", anchor=None)
st.divider()

#Creating option menu in side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore","Conclusion"], 
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon= "menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#517fc9"},
                                   "nav-link-selected": {"background-color": "#517fc9"}}
                          )
    


#reading the cleaned dataframe
df = pd.read_csv(r'C:\Users\Muthusamy\Documents\PROJECTS-2023\4.Airbnb_Project\airbnb_data.csv')
#home page
if selected == "Home":
    col1,col2 = st.columns(2,gap= 'large')
    with col1:
        col1.markdown("##### :red[Domain] ")
        st.write("Travel Industry, Property Management and Tourism.")
        col1.markdown("##### :red[Technologies used]")
        st.write(" Python, Pandas, Plotly, Streamlit, MongoDB, PowerBI or Tableau.")
        col1.markdown("##### :red[Overview] ")
        st.write(" To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations. Create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends.")
        
    with col2:
        col2.image(Image.open(r"C:\Users\Muthusamy\Pictures\Wallpapers\download (3).jpeg"), width=300)

# OVERVIEW PAGE
if selected == "Overview":
    tab1,tab2 = st.tabs(["$\small 📝 DATA $", "$\small🚀 TOP-INSIGHTS $"])
    with tab1:
        st.write("## :blue[Data Frame]")
        st.write(df)

    with tab2:
         # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
        price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
        
        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
        
        # CREATING COLUMNS
        col1,col2 = st.columns(2,gap='medium')
        with col1:
            
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='Listings',
                         y='Property_type',
                         orientation='h',
                         color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 
        
            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='Listings',
                         y='Host_name',
                         orientation='h',
                         color='Host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig,use_container_width=True)
        
        with col2:
            
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='Room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                        )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig,use_container_width=True)
            
            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                               )
            st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")
    
    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country',sorted(df.Country.unique()),sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type',sorted(df.Property_type.unique()),sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type',sorted(df.Room_type.unique()),sorted(df.Room_type.unique()))
    price = st.slider('Select Price',df.Price.min(),df.Price.max(),(df.Price.min(),df.Price.max()))
    
    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'
    
    # HEADING 1
    st.markdown("## Price Analysis")
    
    # CREATING COLUMNS
    col1,col2 = st.columns(2,gap='medium')
    
    with col1:
        
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('Room_type',as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
        # HEADING 2
        st.markdown("## Availability Analysis")
        
        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    with col2:
        
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       color_continuous_scale='agsunset'
                            )
        col2.plotly_chart(fig,use_container_width=True)
        
        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")
        
        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country',as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Availability_365', 
                                       hover_data=['Availability_365'],
                                       locationmode='country names',
                                       size='Availability_365',
                                       title= 'Avg Availability in each Country',
                                       color_continuous_scale='agsunset'
                            )
        st.plotly_chart(fig,use_container_width=True)

# Conclusion PAGE
if selected == "Conclusion":
    st.write("As my observation from the analysis ...")

    st.subheader(":violet[Types of the Rooms]")
    st.write("  * Apartments are in more number compare than the other room types.")
    st.write("  * Most of the rooms are mostely located in USA, followed by CANADA and BRAZIL.")   
    
    st.subheader(":red[Price Wise]")
    st.write("  * Average price of the rooms are depend on your numbers.")
    st.write("  * Average price of the rooms are high in BRAZil, followed by CHINA and TURKEY.")

    st.subheader(":green[Availability]")
    st.write("  * The availability of the Entier home/Apt are nearly equal with Shared Rooms.")
    st.write("  * PORTUGAL  and TURKEY have the highest availability of rooms.")

        