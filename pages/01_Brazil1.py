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
        landcover = ee.Image('MODIS/006/MCD12Q1/2004_01_01').select('LC_Type1')

        igbpLandCoverVis = {
            'min': 1.0,
            'max': 17.0,
            'palette': [
                '05450a',
                '086a10',
                '54a708',
                '78d203',
                '009900',
                'c6b044',
                'dcd159',
                'dade48',
                'fbff13',
                'b6ff05',
                '27ff87',
                'c24f44',
                'a5a5a5',
                'ff6d4c',
                '69fff8',
                'f9ffa4',
                '1c0dff',
            ],
        }

        brazil_lc = landcover.clip(brazil_shapefile)
        self.setCenter(-55, -10, 4)
        self.addLayer(brazil_lc, igbpLandCoverVis, 'MODIS Land Cover')
        

@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element() 