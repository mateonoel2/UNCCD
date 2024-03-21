import ee
import geemap
import solara
import geopandas
import os
from geemap import geojson_to_ee, ee_to_geojson

ee.Authenticate()
ee.Initialize (project='eee-mateonoel2')
brazil_shapefile = geemap.shp_to_ee('/Users/mateonoel/Desktop/UNCCD/content/Brazil.shp')

col = ee.ImageCollection('MODIS/006/MCD12Q1').select('LC_Type1')
fc = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017').filter(
    'country_na == "Brazil"'
)
col_clip = col.map(lambda img: img.clipToCollection(fc))
DOY = col_clip.filterDate('2002-01-01', '2021-01-01')
distinctDOY = col.filterDate('2002-01-01', '2021-01-01')
num_images = distinctDOY.size().getInfo()
layer_names = ['MODIS ' + str(year) for year in range(2002, 2021)]

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
        self.add_basemap('HYBRID')
        self.centerObject(brazil_shapefile)
        self.ts_inspector(left_ts=DOY, left_names=layer_names, left_vis=igbpLandCoverVis, left_index=0,
                        right_ts=DOY, right_names=layer_names, right_vis=igbpLandCoverVis, right_index=-1,
                        width='130px', date_format='YYYY', add_close_button=False)
        self.remove_legend
        self.add_legend(title="MODIS Land Cover", builtin_legend='MODIS/006/MCD12Q1')
        self.addLayerControl


@solara.component
def Page():
    with solara.Column(style={"min-width": "500px"}):
        Map.element() 