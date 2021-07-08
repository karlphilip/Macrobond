import plotly.express as px
import win32com.client
import pandas as pd
c = win32com.client.Dispatch("Macrobond.Connection")
d = c.Database

#Getting the region key
s = d.FetchOneSeries("owidvacci_ar_pfvph")
key = s.Metadata.GetFirstValue("RegionKey") #Getting the region key of a series

regionkey = d.FetchOneEntity(key) 
regionkeydesc = regionkey.Metadata.GetFirstValue("Description") #Getting the full name of the concept

regionkeydesc

#Searching for all series with the region key/concept 
query = d.CreateSearchQuery()
query.SetEntityTypeFilter("TimeSeries")
query.AddAttributeValueFilter("RegionKey", key)
result = d.Search(query).Entities

#Getting the last value and the region of the series via the metadata
val = pd.DataFrame(columns=['value'])
region = pd.DataFrame(columns=['region'])

for s in result:
    region= region.append({'region': s.Metadata.GetFirstValue("Region")}, ignore_index=True)
    val= val.append({'value': s.Metadata.GetFirstValue("LastValue")}, ignore_index=True)

#Translating the region code to ISO 3 and accessing the full name of the country
li=region.values.tolist()

iso = pd.DataFrame(columns=['iso'])
country = pd.DataFrame(columns=['country'])

entities = d.FetchEntities(li)

for e in entities:
    iso= iso.append({'iso': e.Metadata.GetFirstValue("IsoCountryCode3")}, ignore_index=True)
    country= country.append({'country': e.Metadata.GetFirstValue("Description")}, ignore_index=True)

#Merging the ISO3, Country name, Region and Values into one 
df = pd.merge(iso, country, left_index=True, right_index=True)
df=pd.merge(df, region, left_index=True, right_index=True)
df=pd.merge(df, val, left_index=True, right_index=True)
df['iso'] = df['iso'].str.upper()

import plotly.graph_objects as go

fig = go.Figure(data=go.Choropleth(
    locations = df['iso'],
    z = df['value'],
    text = df['country'],
    colorscale = 'viridis',
    autocolorscale=False,
    reversescale=True,
    marker_line_color='darkgray',
    marker_line_width=0.5,
    colorbar_title = '',
))

# Adding a dynamic title and sourcing
fig.update_layout(
    title_text=regionkeydesc,
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
    annotations = [dict(
        x=0.55,
        y=0.00001,
        xref='paper',
        yref='paper',
        text='Source: <a href="https://www.macrobond.com/">Macrobond</a>',
        showarrow = False
    )]
)
