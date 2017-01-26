## Assignment 14
## TeamAA - Araza, Arias
## January 26, 2017

## Traffic situation in Manila, Philippines 

#Import necessary modules
from twython import Twython
import json
import datetime
from osgeo import ogr, osr
import os

#Codes to access twitter API
APP_KEY = 'f1RY7hpQ9Ivtyrv8G8vzkSrbK'
APP_SECRET = 'uQzDJBIAfvZe3LSDoNdx6WmzuMuW7ce7mkHZwaQoiqNH01X1U1'
OAUTH_TOKEN = '824468412940353537-xjvIR6GxvnfjL6W3v36escd43UzWbYH'
OAUTH_TOKEN_SECRET = '0WZb3jXjHZOGgTRzTqfx4ogjUd0A9zftye938wQSAA0uf'
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#Setting filter
geocode = ('14.618661,121.002758,100km')
search_results = twitter.search(q='#traffic', count=50, geocode=geocode)

#Test the search result briefly
for results in search_results['statuses']:
    print results

#Parsing out and creates a csv which can be imported in QGIS
data = search_results["statuses"]
output_file = 'result.csv'
mycoords=[]
colnames= '%s, %s, %s'%('Username','Latitude','Longitude')
target = open(output_file, 'w')
target.write(colnames)
target.write('\n')

for tweet in data:
    x = 0
    y = 0    
    username =  tweet['user']['screen_name']
    followers_count =  tweet['user']['followers_count']
    tweettext = tweet['text']
    if tweet['place'] != None:
        full_place_name = tweet['place']['full_name']
        place_type =  tweet['place']['place_type']    
    print username
    print followers_count
    print tweettext
    coordinates = tweet['coordinates'] 
    if not coordinates is None:
       tweet_lon = coordinates['coordinates'][0]
       tweet_lat = coordinates['coordinates'][1]
       coords= (tweet_lon,tweet_lat)
       mycoords.append(coords) #appending every coordinates to a list
       x = str(tweet_lon)
       y = str(tweet_lat)
    theString = '%s, %s, %s'%(username,x,y) #information to be written
    target = open(output_file, 'a')
    target.write(theString) 
    target.write('\n')
    target.close()
    

#Create shapefile
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName   
fn = "points.shp"
layername = "anewlayer"
ds = drv.CreateDataSource(fn)
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
layerDefinition = layer.GetLayerDefn()
for i in mycoords:
    point = ogr.Geometry(ogr.wkbPoint)
    point.SetPoint(0,i[0],i[1]) #feeding coordinates information   
    feature = ogr.Feature(layerDefinition)
    feature.SetGeometry(point)
    layer.CreateFeature(feature) 
ds.Destroy()
       
    