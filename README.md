# Colorado Geography Dashboard
- Data on county crime, county census demographics, and school district education demographics

## Code
- This project was rushed. The code is messy and has no comments. Enjoy!

#### Layout and data: [app.py](app.py) (run this file)
#### Visualization: [plotting.py](plotting.py) (generate Folium map dynamically)
#### Styling: [custom.css](assets/custom.css)
#### [geo_df.py](geo_df.py) (wrapper class for interacting with `geopandas`)
#### [script.js](assets/script.js) (custom DOM manipulations that can't be done in Dash)

### Notes

- If building your own project with similar functionality, you may run into issues when pip installing `pyproj` and `geopandas`, into a virtual environment. For me, I solved this by installing: `brew install gdal` and `brew install proj` on my machine.
