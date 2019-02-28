"""
Format data points to geojson for visualization
"""

import cPickle as pickle
import pandas as pd
import json, codecs
from datetime import datetime

# TODO: use argparse to specify cols to be downloaded
# import argparse

# Load data
FILE = '../Data_Step1_8'
df = pickle.load(open(FILE,'rb')) # Pandas dataframe
OUTPUT = 'dataPoints.js'

tmp = df.SalePrice.max()
print tmp
raw_input()

class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)

# Convert pandas dataframe to geojson format
def df_to_geojson(df, properties=list(df), lat='lat', lon='lng'):
    geojson = {'type':'FeatureCollection', 'features':[]}
    for _, row in df.iterrows():
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}
        feature['geometry']['coordinates'] = [row[lon],row[lat]]
        for prop in properties:
            feature['properties'][prop] = row[prop]
        geojson['features'].append(feature)
    return geojson

# Specify cols to dump
cols = [u'DataId', u'SaleType', u'PropertyType', u'ListPrice', u'SalePrice',
        u'State', u'County', u'City', u'Address', u'UnitNumber', u'PostalCode',
        ]
geojson = df_to_geojson(df, properties=cols)

with open(OUTPUT, 'wb') as output_file:
    output_file.write('var dataset = ')
    json.dump(geojson, output_file, indent=2, cls=SetEncoder)
print 'Data dumped'

# Columns available:
# [u'Id', u'DataSourceId', u'DataId', u'MLSNumber', u'ModificationDateTime',
# u'StatusChangeDateTime', u'Status', u'StatusEnum', u'SaleType', u'SaleTypeEnum',
# u'PropertyType', u'PropertyTypeEnum', u'ListPrice', u'SalePrice', u'OnMarketDateTime',
# u'ListingAgentFullName', u'ListingOfficeName', u'ListingAgentLicenseNumber', u'SellingAgentFullName', u'SellingOfficeName',
# u'SellingAgentLicenseNumber', u'DOM', u'CDOM', u'State', u'County',
# u'City', u'Address', u'UnitNumber', u'PostalCode', u'Area',
# u'CrossStreets', u'Description', u'YearBuilt', u'LotSqFt', u'StructureSqFt',
# u'Bedrooms', u'BathsFull', u'BathsHalf', u'APN', u'HeatingYN',
# u'Heating', u'CoolingYN', u'Cooling', u'FireplaceYN', u'Fireplace',
# u'LaundryYN', u'Laundry', u'AppliancesYN', u'Appliances', u'Utilities',
# u'Rooms', u'Floor', u'EatingArea', u'InteriorFeatures', u'ExteriorFeatures',
# u'LotFeatures', u'DirectionFaces', u'ViewYN', u'View', u'ConstructionType',
# u'ConstructionStatus', u'Style', u'AttachedStructure', u'CommonWalls', u'ParkingYN',
# u'Parking', u'GarageSpaces', u'ParkingSpaces', u'GarageAttached', u'FenceYN',
# u'Fence', u'PatioYN', u'Patio', u'PoolYN', u'Pool',
# u'WaterSource', u'Sewer', u'Foundation', u'Roof', u'DoorFeatures',
# u'WindowFeatures', u'Communications', u'SecurityFeatures', u'NumberUnits', u'StoriesTotal',
# u'Stories', u'HOAExistYN', u'HOAFee', u'HOAAmenities', u'CommunityFeatures',
# u'SeniorYN', u'Restrictions', u'ElementarySchool', u'ElementarySchoolDistrict', u'MiddleOrJuniorSchool',
# u'MiddleOrJuniorSchoolDistrict', u'HighSchool', u'HighSchoolDistrict', u'dataSourceName', u'dataSourceDescription',
# 'Location', 'lat', 'lng']
