# importing the covid19 data

url      = 'https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json'
response = requests.get(url, 'covid19.json')
df       = pd.DataFrame.from_records(pd.read_json('covid19.json').records.tolist())

#importing the geojson data

geojson_url = 'https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson'
response    = requests.get(geojson_url)
geojson     = response.json()


# cleaning the covid19 data 

df = df.dropna()                # deleting na and negative values
df = df[df['cases']>=0]
df = df[df['deaths']>=0]

df = df.astype({'cases': int})  # transforming cases to cases per 100.000
df = df.astype({'deaths': int})
df = df.astype({'popData2020': float})
df['cases'] = df['cases']/df['popData2020']*100000

df['Date'] = pd.to_datetime(df[['year','month','day']])        # making the date as index for easier plotting
df.index   = pd.DatetimeIndex(df['Date'])


df.drop(columns=['dateRep', 'Date', 'day', 'month', 'year', 'countryterritoryCode',
                 'continentExp', 'popData2020'], inplace=True) # deleting extra columns
df.rename(columns={'cases': 'Cases','deaths': 'Deaths',
                   'countriesAndTerritories': 'Country'}, inplace=True)

df_map = df                     # a copy for the map

# start of the dashboarding

st.set_page_config(layout='wide')
st.title('COVID19 DASHBOARDS')

# a radio button widget for choosing the country

country = st.radio(
     'Choose a country:',
      ('Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
       'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece',
       'Hungary', 'Iceland', 'Ireland', 'Italy', 'Latvia',
       'Liechtenstein', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands',
       'Norway', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
       'Spain', 'Sweden'), horizontal=True)  
df = df[df['Country']==country]             # filtering the DataFrame by the country

# inserting two side-by-side dashboards

col1, col2 = st.columns(2)
with col1:
    st.header('Cases per 100.000')           # Cases dashboard
    st.line_chart(df['Cases'])
with col2:
    st.header('Deaths')                      # Deaths dashboard
    st.line_chart(df['Deaths'])

# inserting the map dashboard

st.header('Covid19 map')
col1, col2 = st.columns(2)
with col2:                                   # col2 to select the date and cases/deaths parameter      
    date      = st.date_input('Choose a date:', datetime.date(2020, 1, 1))
    parameter = st.radio('',('Cases', 'Deaths'))

df_map.index = df_map.index.astype('str')  
df_map = df_map[df_map.index==str(date)]     # selecting the chosen date

# configuring the map
map_fig = folium.Map(location=[58,18], zoom_start=3)
folium.Choropleth(
    geo_data=geojson,
    data=df_map,
    columns=['geoId', parameter],
    key_on='feature.properties.ISO2',        # this is the key, on which geojson and df_map are connected
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=parameter).add_to(map_fig)

with col1:
    st_folium(map_fig, height=500, width=700)