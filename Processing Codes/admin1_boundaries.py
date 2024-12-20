import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt
import math
import json

wd_file = 'Datasets\Humdata\egy_admbnda_adm1_capmas_20170421\egy_admbnda_adm1_capmas_20170421.shp'

gdf = gpd.read_file(wd_file,
                    encoding='UTF-8')

f, axes = plt.subplots(1, figsize=(12, 12))
axes = gdf.plot(ax=axes)
plt.show()

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


f, axes = plt.subplots(1, figsize=(12, 12))
axes = gdf['squares'].plot(ax=axes)
plt.show()

data_list = []
for index, row in gdf.iterrows():
  data_list.append({'ADM1': row['ADM1_AR'],
    'ADM1': row['ADM1_AR'], 
    'lat_range':[row['squares'].bounds[1], row['squares'].bounds[3]],
    'long_range':[row['squares'].bounds[0], row['squares'].bounds[2]]})

with open('all_admin1_boundaries.json', 'w', encoding='utf-8') as outfile:
   json.dump(data_list, outfile, ensure_ascii=False)

#to read it in, use:
# with open("file_name.json") as f:
#     data = json.load(f)
   
