import requests
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd


#Get Lat and Lon from ISS API
iss_data = requests.get("https://api.wheretheiss.at/v1/satellites/25544")

response = iss_data.json()

print("latitue:", response["latitude"])
print("longitude:", response["longitude"])

df = pd.DataFrame.from_dict(response, orient="index")



#Get a Map

fig = px.scatter_mapbox(df, lat=df.loc["latitude"], lon=df.loc["longitude"], color_discrete_sequence=["red"], zoom=2, height=500)

fig.update_layout(
    mapbox_style="open-street-map",
    mapbox_layers=[
        {
            "below": 'traces',
            "sourcetype": "raster",
            "sourceattribution": "United States Geological Survey",
            "source": [
                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
            ]
        }
      ])
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
# fig.show()


#set up webpage
app = dash.Dash(__name__)

app.layout = html.Div([html.H1("Where is the ISS?"),
                    html.Div(dcc.Graph(figure=fig))
])

app.run_server(debug=True)
