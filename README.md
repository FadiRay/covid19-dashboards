# covid19-dashboards

`covid19.py` creates three dashborads to show the possible insights from the [this dataset](https://opendata.ecdc.europa.eu/covid19/nationalcasedeath_eueea_daily_ei/json/), which includes covid19 daily cases and deaths.


The dashboard framework used here is `streamlit` in combination with `folium` to create an interactive map. The dataset is connected to the map using this [geojson file](https://raw.githubusercontent.com/leakyMirror/map-of-europe/master/GeoJSON/europe.geojson), on the key **properties.ISO2**.


`covid19.py` is automatically tested by any push or pull request using GitHub actions, which let **pytest** and **flake8** to run `covid19_dashboards.py` on the latest **ubuntu** version after installing all the requirments.


`covid19_dashboards.py` checks the connection to the dataset and geojson file and checks, that only one element is selected in the dashboards.
In Addition, `covid19_dashboards.py` let the user select only vailed dates.
