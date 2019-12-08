## Twitter Geo-location Scraper

## Created as part of the following research:
## Horizon Scanning Through Computer-Automated Information Prioritisation

## Daniel Hammocks - 2019-11-18
## GH: dhammo2

## This code utilises the twitter API to obtain information on a given
## geographical zone. The code has two main functionalities for obtaining the
## top 50 trends in a given region (single run) or for listening on the twitter
## API for obtaining tweets as they are posted (continuous run).

###############################################################################
############################### WOEID FUNCTIONS ###############################
###############################################################################

#%% Load Required Libraries

#requests: for sending http requests
import requests

#re: for regular expressions on strings
import re

#json: Used to read JSON files
import json

#logging: Used to create logs
import logging


#%% Configure logger

logger = logging.getLogger(__name__)


#%% Import Required Functions from Other Modules

import authentication_functions as axf


#%% Functions

# Function to obtain a list of available WOEIDs used on Twitter
def IdentifyWOEIDLocations(api):
    try:
        #Identify Available regions
        woeidList = api.trends_available()  
        
    except Exception as e:
        #Add error to log and raise
        logger.error("Error Getting WOEID Data from API", exc_info=True)
        raise e
    
    try:
        #Write to JSON file
        with open('woeidList.json', 'w') as outfile:
            json.dump(woeidList, outfile)
        
    except Exception as e:
        #Add error to log and raise
        logger.error("Error Writing Data to JSON File", exc_info=True)
        raise e
        
    #Add success to log
    logger.info('Successfully Written WOEID Data to File')
        
    #Return JSON file
    return(woeidList)
    
    
# Function to convert a WOEID location to a bounding box of coordinates  
def BBoxofWOEID(locationID, credJSON = 'credentials.json'):
    
    #Extract Credentials
    flickrKey, _ = axf.ReadFlickrCredentials(credJSON)
    
    #Base URL
    urlBase = 'https://www.flickr.com/services/rest/?method=flickr.places.getInfo'
     
    #Create the URL
    urlQuery = urlBase + '&api_key=' + str(flickrKey) + '&format=json&woe_id=' + str(locationID)

    try:
        #Query the flickr API
        response = requests.get(urlQuery).text
        
    except Exception as e:
        #Log the error
        logger.error('No Response From the FLICKR API')
        
        #Raise the error
        raise e
    
    try:
        ## Parse the response
        #Remove last bracket
        responseParsed = response[:-1]
        #Remove everything before first brace
        responseParsed = re.sub('^[^{]+', '', responseParsed)
        
        #Load as JSON
        responseJSON = json.loads(responseParsed)
        
        #Extract Coordinate Data
        shape = responseJSON['place']['shapedata']['polylines']['polyline'][0]['_content']
    
        #Process coordinates
        coordinates = shape.split(' ')
        coordinates = [x.split(',') for x in coordinates]
        
        #Find the bbox values
        minLat = min([float(x) for x, y in coordinates])
        minLon = min([float(y) for x, y in coordinates])
        maxLat = max([float(x) for x, y in coordinates])
        maxLon = max([float(y) for x, y in coordinates])
        
        #Create bbox object
        bbox = [minLon, minLat, maxLon, maxLat]
        
    except Exception as e:
        #Log the error
        logger.error('Error Parsing the Response from the Flickr API')
        
        #Raise the error
        raise e
        
    logger.info('Successfuly Identified the Bounding Box of the WOEID')
    
    #Return bbox
    return(bbox)
        