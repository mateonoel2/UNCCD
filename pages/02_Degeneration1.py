import ee
import geemap
import solara
import geopandas
import os
from geemap import geojson_to_ee, ee_to_geojson

ee.Authenticate()
ee.Initialize (project='eee-mateonoel2')
brazil_shapefile = geemap.shp_to_ee('/Users/mateonoel/Desktop/UNCCD/content/Brazil.shp')

class Map(geemap.Map):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_ee_data()
        self.add("layer_manager")
        self.add("inspector")

    def add_ee_data(self):
        years = range(2002, 2021)  # 2002 to 2020
        lc_images = []

        for year in years:
            lc_image = ee.Image(f"MODIS/006/MCD12Q1/{year}_01_01").select('LC_Type1')
            lc_images.append(lc_image)
            
        brazil_lc_images = [lc.clip(brazil_shapefile) for lc in lc_images]
        # Define a color ramp from red to white to green
        color_ramp = {
            'min': -17,
            'max': 17,
            'palette': ['00ff00', 'ffffff', 'ff0000']
        }

        start_year=2002
        end_year=2020

        start_index = years.index(start_year)
        end_index = years.index(end_year)

        lc_diff = brazil_lc_images[end_index].subtract(brazil_lc_images[start_index])

        # Create a map to visualize the change
        self = geemap.Map(center=[-10, -55], zoom=4)
        self.addLayer(lc_diff, color_ramp, 'Land Cover Change from 2002 to 2021')
        self.addLayerControl()


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element()