import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import numpy as np
# Load CSV data
@st.cache_data
def load_data():
    glassdoor_data = pd.read_json("c:\\Users\\ACER\\Documents\\Office_projects\\streamlit_app\\glassdoor_data.json")
    return glassdoor_data

st.set_page_config(layout="wide")
# Main content
st.title("List of Companies")

# Load data
glassdoor_data = load_data()  
glassdoor_df = pd.DataFrame(glassdoor_data)
#Filter rows is has Null Values
filtered_df = glassdoor_df[~glassdoor_df.isnull().any(axis=1)]

st.set_option('deprecation.showPyplotGlobalUse', False)
# Sidebar
st.sidebar.title("Filter Options")
search_query = st.sidebar.text_input('Search by Name')

# Filter DataFrame based on search query
if search_query:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(search_query, case=False)]
else:
    filtered_df = filtered_df

# Define the range of founding years
option_1= list(range(1882, 2025))
founding_years_range = st.sidebar.selectbox("Select Year Range", list(range(1882, 2022)), index=len(option_1)-12)
if isinstance(founding_years_range, int):
    if founding_years_range != 2024:
        options = list(range(founding_years_range + 10, 2024))
        leng = len(options)
        founding_year_end_range = st.sidebar.selectbox("Select End Year", options, index=min(leng, len(options)-1))



if isinstance(founding_years_range, int):
    if isinstance(founding_year_end_range, int):
        filtered_df = filtered_df[(filtered_df['Founded_year'] >= founding_years_range)&(filtered_df['Founded_year'] <= founding_year_end_range)]
    else:
        filtered_df = filtered_df[filtered_df['Founded_year'] == founding_years_range]


unique_types = glassdoor_df['Type'].unique()
unique_types = ['All'] + list(unique_types)
company_category='All'
company_type = st.sidebar.selectbox('Select Business type', unique_types)
if company_type != 'All':
    filtered_df = glassdoor_df[glassdoor_df['Type'] == company_type]
    unique_business_types = filtered_df['Business_type'].unique() 
    unique_business_types = ['All'] + list(unique_business_types)
    company_category = st.sidebar.selectbox("Category", unique_business_types)
    if company_category != 'All':
        filtered_df = filtered_df[filtered_df['Business_type'] == company_category]
    


# st.sidebar.subheader("Company Ratings")
company_rating = st.sidebar.selectbox("Ratings", ['All', '4', '3', '2'])

# st.sidebar.subheader("Company Size")
unique_size = glassdoor_df['Size'].unique()

company_size = st.sidebar.select_slider("Company Size",unique_size)

# st.sidebar.subheader("Company Revenue")
company_revenue = st.sidebar.selectbox("Company Revenue", ['All', 'Over 10 Billion', '1 - 10 Billion', '100 Million - 1 Billion', '50 - 100 Million', '5 - 25 Million','5 Million Below'])



if company_type != 'All':
    filtered_df = filtered_df[filtered_df['Type'].str.contains(f'{company_type}', case=False)].reset_index(drop=True)



if company_rating != 'All':
    company_rating=int(company_rating)
    if company_rating == 4:
        filtered_df = filtered_df[filtered_df['Rating'] >= company_rating]
        filtered_df = filtered_df.sort_values(by='Rating', ascending=False)
    elif company_rating == 3:
        filtered_df = filtered_df[(filtered_df['Rating'] >= company_rating)&(filtered_df['Rating'] <company_rating+1)]
        filtered_df = filtered_df.sort_values(by='Rating', ascending=False)
    elif company_rating == 2:
        filtered_df = filtered_df[filtered_df['Rating'] < company_rating+1]
        filtered_df = filtered_df.sort_values(by='Rating', ascending=False)
    filtered_df = filtered_df.sort_values(by='Rating', ascending=False).reset_index(drop=True)
    
   
if company_size != 'All':
    if company_size == 10000:
        filtered_df = filtered_df[filtered_df['Size'] >=company_size]
    elif company_size in [5000,1000,500,200,50]:
        filtered_df = filtered_df[filtered_df['Size'] <=company_size]
    filtered_df = filtered_df.sort_values(by='Size', ascending=False).reset_index(drop=True)



if company_category != 'All': # category like internet,cafe,business
    filtered_df = filtered_df[filtered_df['Business_type'].str.contains(company_category, case=False)].reset_index(drop=True)
   

if company_revenue != 'All':
    if company_revenue == 'Over 10 Billion':
        filtered_df = filtered_df[filtered_df['Revenue'] >=10_000_000_000]
    elif company_revenue == '1 - 10 Billion':
        filtered_df = filtered_df[(filtered_df['Revenue'] >= 1_000_000_000) & (filtered_df['Revenue'] < 10_000_000_000)]
    elif company_revenue == '100 Million - 1 Billion':
        filtered_df = filtered_df[(filtered_df['Revenue'] >100_000_000) & (filtered_df['Revenue'] < 1_000_000_000)]
    elif company_revenue == '50 - 100 Million':
        filtered_df = filtered_df[(filtered_df['Revenue'] > 25_000_000) & (filtered_df['Revenue'] <= 100_000_000)]
    elif company_revenue == '5 - 25 Million':
        filtered_df = filtered_df[(filtered_df['Revenue'] > 5_000_000) & (filtered_df['Revenue'] <= 25_000_000)]
    elif company_revenue == '5 Million Below':
        filtered_df = filtered_df[filtered_df['Revenue'] <= 5_000_000]
    filtered_df = filtered_df.sort_values(by='Revenue', ascending=False).reset_index(drop=True)

filtered_df_length=len(filtered_df)
if filtered_df_length>0:
    st.write(filtered_df)

    st.title("Sunburst Filter")

    sunburst_df=filtered_df

    sunburst_df_length = len(sunburst_df)
    chunk_size = 100
    start_idx = 0
    end_idx=100

    if sunburst_df_length != 0:
            sunburst_df = sunburst_df.iloc[start_idx:end_idx]
            
            fig = px.sunburst(sunburst_df, path=['Type', 'Business_type', 'Name'], 
                                values='Revenue', hover_data=['Rating'],
                                color_continuous_scale='RdBu_r',
                                width=800, height=800,
                                template='seaborn',
                                labels={'Revenue': 'Company Revenue'})
                                
            fig.update_layout(font=dict(size=15))
                            
            placeholder = st.empty()
            placeholder.plotly_chart(fig, use_container_width=True)
            start_idx += 100
            end_idx += 100
            
    else:
        st.warning("No companies to display")


    min_max_selct=st.selectbox("Sort By Minimum or Maximum Revenue", ["Min",'Max'])
    search="idxmin"

    if min_max_selct=="Min":
        search="idxmin"
    elif min_max_selct=="Max":
        search="idxmax"
    st.title(f"Graph For Revenue of companies with min revenue({founding_years_range}-{founding_year_end_range})")


    max_revenue_indices = filtered_df.groupby('Founded_year')['Revenue'].agg(search)
    highest_revenue_df = filtered_df.loc[max_revenue_indices]
    plt.figure(figsize=(10, 6))
    sns.barplot(data=highest_revenue_df, x='Founded_year', y='Revenue', hue='Name')
    plt.xlabel('Year')
    plt.ylabel('Revenue')
    plt.title('Revenue Over Years')
    plt.xticks(rotation=45)
    plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')
    st.pyplot()

    st.title("Graph For Rating for above revenue companies")


    plt.figure(figsize=(10, 6))
    sns.barplot(data=highest_revenue_df, x='Founded_year', y='Rating', hue='Name')
    plt.xlabel('Year')
    plt.ylabel('Rating')
    plt.title('Revenue Over Years')
    plt.xticks(rotation=45)
    plt.legend(title='Company', bbox_to_anchor=(1.05, 1), loc='upper left')

    st.pyplot()
    glassdoor_df = glassdoor_df[(glassdoor_df['Revenue'].notnull())&(glassdoor_df['Founded_year']>1800)]
    
    private_sorted_df = glassdoor_df[glassdoor_df['Type']=='Private'].sort_values(by='Revenue',ascending=True).head(5)
    public_sorted_df = glassdoor_df[glassdoor_df['Type']=='Public'].sort_values(by='Revenue',ascending=True).head(5)
    nonprofit_sorted_df = glassdoor_df[glassdoor_df['Type']=='Nonprofit'].sort_values(by='Revenue',ascending=True).head(5)

    bottom_5_private_df = glassdoor_df[glassdoor_df['Type']=='Private'].sort_values(by='Revenue',ascending=True).tail(5)
    bottom_5_public_df = glassdoor_df[glassdoor_df['Type']=='Public'].sort_values(by='Revenue',ascending=True).tail(5)
    bottom_5_nonprofit_df = glassdoor_df[glassdoor_df['Type']=='Nonprofit'].sort_values(by='Revenue',ascending=True).tail(5)

    revenue_stats_df = pd.concat([private_sorted_df, public_sorted_df, nonprofit_sorted_df, bottom_5_private_df, bottom_5_public_df, bottom_5_nonprofit_df], ignore_index=True)
    st.write(revenue_stats_df)

    plt.figure(figsize=(10, 8))
    sns.lineplot(data=revenue_stats_df, x='Founded_year', y='Revenue', hue='Type', style='Type', markers=True, dashes=False)
    sns.scatterplot(data=revenue_stats_df, x='Founded_year', y='Revenue', hue='Name')

    plt.xlabel('Founded Year')
    plt.ylabel('Revenue')
    plt.title('Revenue vs Founded Year')
    plt.xticks(rotation=45)
    plt.legend(title='Business Type', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    st.pyplot()



else:
    st.warning("No Companies to display")


        