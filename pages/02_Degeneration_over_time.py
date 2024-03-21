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
start_year = solara.reactive(2002)
end_year = solara.reactive(2020)

# Find the indexes of the chosen years in the list 'years'
start_index = years.index(start_year.value)
end_index = years.index(end_year.value)

burnedAreaVis = {
    'min': 0,
    'max': 1,
    'palette': ['FFFFB2']  
}

burnedArea_norm = burnedArea.map(lambda img: img.divide(ee.Image.constant(366)))

class Map2(geemap.Map):

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

        lc_diff = brazil_lc_images[end_index].subtract(brazil_lc_images[start_index])

        self.setCenter(-55, -10, 4)
        self.addLayer(lc_diff, color_ramp, 'Land Cover Change from 2002 to 2020')
        self.addLayerControl()
        self.addLayer(burnedArea_norm.mean(), burnedAreaVis, f'Burned Area {start_year} to {end_year}')

class Map3(geemap.Map):

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

        lc_diff = brazil_lc_images[end_index].subtract(brazil_lc_images[start_index])

        self.setCenter(-55, -10, 4)
        self.addLayer(lc_diff, color_ramp, 'Land Cover Change from 2002 to 2020')
        self.addLayerControl()

clicks = solara.reactive(0)

def increment():
    clicks.value += 1

@solara.component
def Page():

    mess = "Hide" if clicks.value%2 == 0 else "View"
    solara.Button(label=f"{mess} Wildfires between dates", on_click=increment, color="primary")

    solara.SliderInt("Start year", value=start_year, min=2002, max=2020)
    solara.SliderInt("End year", value=end_year, min=2002, max=2020)

    with solara.Column(style={"min-width": "500px"}):
        if clicks.value%2 == 0:
            Map2.element()
        else:
            Map3.element()
