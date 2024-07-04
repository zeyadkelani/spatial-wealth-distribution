import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import math
import json
#import shapely
#from shapely.geometry import box

wd_file = '/Users/nourabdelbaki/Desktop/Personal/Work/Spatial/spatial-wealth-distribution/Humdata/egy_admbnda_adm3_capmas_20170421/egy_admbnda_adm3_capmas_20170421.shp'

gdf = gpd.read_file(wd_file,
                    encoding='UTF-8')

f, axes = plt.subplots(1, figsize=(12, 12))
axes = gdf.plot(ax=axes)
plt.show()

### Two methods ###

# Testing, directly from shapely:
# https://shapely.readthedocs.io/en/stable/manual.html#polygons
# x = gdf.iloc[0, -1] # The polygon for the first entry
# bbox = box(*x.bounds) # W/ polygon bounds; make a box, not necess square
# Looking at 1st entry's: 
# (31.52563203300008, 31.076032703000067, 31.545053627000073, 31.08957390300003) 

# Another method
#### makes an exact square ####
def to_square(polygon):
    '''
    This function takes a polygon and returns a square that has the same centroid
    and the same diagonal as the polygon.
    Input: 
        polygon: a shapely Polygon object
    Returns:
        a shapely object that is a square
    '''
    # unpacking the polygon's bounds
    minx, miny, maxx, maxy = polygon.bounds
    
    # getting the centroid
    centroid = [(maxx+minx)/2, (maxy+miny)/2]
    # getting the diagonal
    diagonal = math.sqrt((maxx-minx)**2+(maxy-miny)**2)
    
    # creating the square
    return Point(centroid).buffer(diagonal/math.sqrt(2.)/2., cap_style=3)

gdf['squares'] = gdf['geometry'].map(to_square)

# look at 1st entry's under second method:
# (31.526972029478774, 31.074432502478746, 31.543713630521378, 31.09117410352135)
# double checked it is a square:

# if (gdf.iloc[0,-1].bounds[2] - gdf.iloc[0,-1].bounds[0]) == \
# (gdf.iloc[0,-1].bounds[3] - gdf.iloc[0,-1].bounds[1]):
#     print("Yes! Square")

f, axes = plt.subplots(1, figsize=(12, 12))
axes = gdf['squares'].plot(ax=axes)
plt.show()

#### For transforming to lat and long:

# It seems that our data is already in WGS84 EPSG:4326 geographic coordinates (lat/lng) 
# same as used by Google maps.

# Sort of confirmed through this map:
# https://epsg.io/map#srs=4326&x=0.000000&y=0.000000&z=1&layer=streets 
# Entering, long: 31.543713630521378 , lat: 31.09117410352135 (1st entry)
# Should give you Al-Gazeera, which on this map, you cannot see, but
# you can confirm its Admin 2, which is: Dikirnis

data_list = []
for index, row in gdf.iterrows():
  data_list.append({'ADM3': row['ADM3_AR'], 'ADM2': row['ADM2_AR'],
    'ADM1': row['ADM1_AR'], 
    'lat_range':[row['squares'].bounds[1], row['squares'].bounds[3]],
    'long_range':[row['squares'].bounds[0], row['squares'].bounds[2]]})

with open('all_admin3_boundaries.json', 'w', encoding='utf-8') as outfile:
   json.dump(data_list, outfile, ensure_ascii=False)

#to read it in, use:
# with open("output.json") as f:
#     data = json.load(f)