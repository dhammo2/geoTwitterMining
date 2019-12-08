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
########################## AUTHENTICATION FUNCTIONS ##########################
###############################################################################

#%% Notes

# 1. Note that the logger will be defined in the main script.


#%% Requried Libraries

#json: Used to store credentials
import json

#logging: Used to create logs
import logging


#%% Configure logger

logger = logging.getLogger(__name__)


#%% Database

#Define a function to read the DB credentials
def ReadDBCredentials(credJSON = 'credentials.json'):
    
    try:
        #Read the credentials file as a dictionary
        with open(credJSON) as creds:    
            credentials = json.load(creds)
        
        #Set the authentication details in credentials.json as variables
        dbHost     = credentials['host']
        dbUsername = credentials['dbUsername']
        dbPassword = credentials['dbPassword']
        db         = credentials['db'] 
        dbTable    = credentials['dbTable']
    
    except Exception as e:
        #Add error to log and raise
        logger.error("Could Not Read Credentials File", exc_info = True)
        raise e
  
    #Add success to log
    logger.info('Successfully Accessed Credentials File')

    #Create DB Credentials Object
    credentialsDB = (dbHost, dbUsername, dbPassword, db, dbTable)   
    
    #Add success to log
    logger.info('Created Twitter Credentials Object')
      
    #Return the credentials as variables
    return(credentialsDB)


#%% Twitter
#Define a function for reading the Twitter API Credentials
def ReadTwitterCredentials(credJSON = 'credentials.json'):
    
    try:
        #Read the credentials file as a dictionary
        with open(credJSON) as creds:    
            credentials = json.load(creds)
        
        #Set the authentication details in credentials.json as variables
        twitAppKey    = credentials['twitter_app_key']
        twitAppSecret = credentials['twitter_app_secret']
        twitKey       = credentials['twitter_key']
        twitSecret    = credentials['twitter_secret'] 
   
    except Exception as e:
        #Add error to log and raise
        logger.error("Could Not Read Credentials File", exc_info = True)
        raise e
        
    #Add success to log
    logger.info('Successfully Accessed Credentials File')

    #Create Twitter Credentials Object
    credentialsTwitter = (twitAppKey, twitAppSecret, twitKey, twitSecret)
    
    #Add success to log
    logger.info('Created Twitter Credentials Object')
    
    #Return the credentials as variables
    return(credentialsTwitter) 
    
    
#%% Flickr
    
#Read credentials file for flickr
def ReadFlickrCredentials(credJSON = 'credentials.json'):
    
    try:
        #Read the credentials file as a dictionary
        with open(credJSON) as creds:    
            credentials = json.load(creds)
        
        #Set the authentication details in credentials.json as variables
        flickrKey    = credentials['flickr_key']
        flickrSecret = credentials['flickr_secret']
   
    except Exception as e:
        #Add error to log and raise
        logger.error("Could Not Read Credentials File", exc_info = True)
        raise e
        
    #Add success to log
    logger.info('Successfully Accessed Credentials File')

    #Return the credentials
    return(flickrKey, flickrSecret)