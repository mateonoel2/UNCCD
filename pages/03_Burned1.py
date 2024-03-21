import ee
import geemap
import solara
import geopandas
import os
from geemap import geojson_to_ee, ee_to_geojson

ee.Authenticate()
ee.Initialize (project='eee-mateonoel2')
brazil_shapefile = geemap.shp_to_ee('/Users/mateonoel/Desktop/UNCCD/content/Brazil.shp')

years = range(2002, 2021)  # 2002 to 2020
lc_images = []

for year in years:
    lc_image = ee.Image(f"MODIS/006/MCD12Q1/{year}_01_01").select('LC_Type1')
    lc_images.append(lc_image)
    
brazil_lc_images = [lc.clip(brazil_shapefile) for lc in lc_images]

# Define the dataset and filter by date for all years
dataset = ee.ImageCollection('MODIS/061/MCD64A1').filter(ee.Filter.date('2002-01-01', '2021-12-31'))

# Select the 'BurnDate' band and clip to Brazil
burnedArea = dataset.select('BurnDate').map(lambda img: img.clip(brazil_shapefile))

# Select start and end years
start_year, end_year = 2002, 2020

# Find the indexes of the chosen years in the list 'years'
start_index = years.index(start_year)
end_index = years.index(end_year)

class Map(geemap.Map):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()
        self.add("layer_manager")
        self.add("inspector")

    def add_ee_data(self):
        color_ramp = {
            'min': -17,
            'max': 17,
            'palette': ['00ff00', 'ffffff', 'ff0000']
        }

        burnedAreaVis = {
            'min': 0,
            'max': 1,
            'palette': ['FFFFB2']  # light yellow in hex
        }

        # Compute the difference between land cover maps
        lc_diff = brazil_lc_images[end_index].subtract(brazil_lc_images[start_index])

        # Normalize to 0-1 range
        burnedArea_norm = burnedArea.map(lambda img: img.divide(ee.Image.constant(366))) # 366 is the maximum possible value of 'BurnDate'

        self.setCenter(-55, -10, 4)
        self.addLayer(lc_diff, color_ramp, f'Land Cover Change from {start_year} to {end_year}')
        self.addLayer(burnedArea_norm.mean(), burnedAreaVis, 'Burned Area 2002-2021')
        self.addLayerControl()


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element()
    