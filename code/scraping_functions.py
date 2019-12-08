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
############################# SCRAPING FUNCTIONS ##############################
###############################################################################

#%% Load Required Libraries

#tweepy: Twitter API wrapper
import tweepy

#time: for initiating system delays
import time

#logging: Used to create logs
import logging


#%% Configure logger

logger = logging.getLogger(__name__)


#%% Import Required Functions from Other Modules

import authentication_functions as axf
import processing_functions as wrangle
import db_functions as dbf


#%% API Activation

#Define a function to create an API object
def StartAPI(credJSON = 'credentials.json'):
    #Call the credential reading function
    credentialsTwitter = axf.ReadTwitterCredentials(credJSON)

    #Unpack the credentials
    twitAppKey, twitAppSecret, twitKey, twitSecret = credentialsTwitter
    
    #Authenticate the API Wrapper
    auth = tweepy.OAuthHandler(twitAppKey, twitAppSecret)
    auth.set_access_token(twitKey, twitSecret)
    
    #Create an API object
    api = tweepy.API(auth,
                     wait_on_rate_limit = True,
                     wait_on_rate_limit_notify = False)
    
    try:
        #Verify the API credentials
        api.verify_credentials()
        
    except Exception as e:
        #Add error to log and raise
        logger.error("Error creating API", exc_info=True)
        raise e
    
    #Add success to log
    logger.info("API created")

    #Return the API Object
    return(auth, api)
    
    
#%% 'Scraping' Code
    
#Define a function to get the trends of a given grographic area
def GetTrends(api, locationID):
    '''
    This function obtains the top ten trends of a given location.
    
    Arguments:
        api         : Connection to Twitter API
        locationID  : Yahoo! Where On Earth ID (https://github.com/famibelle/TwitteR/blob/master/WOEID.json)
    '''
    
    try:
         #Get the trends of the WOEID location
         trends = api.trends_place(locationID)
        
    except Exception as e:
        #Add error to log and raise
        logger.error("Error Getting Trend Data from API", exc_info=True)
        raise e
            
    #Extract dictionary from list
    trends = trends[0]
    
    #Add success to log
    logger.info('Obtained Trends Dictionary Object')

    #Return the trends dictionary object
    return(trends)


#Define a class for streaming the tweets 
class StreamListener(tweepy.StreamListener):
    def __init__(self, api, credentialsDB, locationID, addStreamData):
        self.api = api
        self.me = api.me()
        self.credentialsDB = credentialsDB
        self.locationID = locationID
        self.addStreamData = addStreamData
        
    def on_connect(self):
        logger.info('Connected to Twitter Stream')
        
    def on_data(self, data):
        #Extract and process the data received
        dataOutput, dataRelations = wrangle.ProcessTwitterData(data, self.locationID)
        
        #Connect to the database
        cnx, cursor = dbf.Connect2DB(self.credentialsDB)
        
        try:
            #Write to DB
            dbf.WriteStreamData2DB(cnx, cursor, self.addStreamData, dataOutput, dataRelations)
            
        except Exception as e:
            #Close the connection
            dbf.CloseDBConnection(cnx, cursor)
            
            #Raise the error
            raise(e)

        #Close the connection
        dbf.CloseDBConnection(cnx, cursor)
        
    def on_limit(self, status):
        #Sleep for 15 minutes
        time.sleep(15 * 60)
        
        #Keep the stream open
        return(True)

    def on_error(self, status):
        #Write the status to the log
        logger.error(status)
        
        #Close the stream
        return(False)
        

#Define a function to listen for tweets at a given area
def StreamTweets(api, auth, bbox, credentialsDB, locationID, addStreamData):
    '''
    This function listens for tweets that match a given criteria.
    
    Arguments:
        api     : Connection to Twitter API
        auth    : Authentication details for the twitter API
        bbox    : Geographical coordinate bounding box as list of coordinates
                  For example; [minLon, minLat, maxLon, maxLat]
    
    Note that this function is recurrsive and will return a runtime error when
    the recursive depth limit has been reached.
    '''

    try:
        #Instantiate Stream Listener
        streamListener = StreamListener(api, credentialsDB, locationID, addStreamData)
        twitterStream = tweepy.Stream(auth, streamListener)
        
        #Run the stream filtering on location
        twitterStream.filter(locations = bbox)
        
        logger.info('Stream Started')
        
    except Exception as e:
        #If a stream error
        if isinstance(e,tweepy.TweepError):
            #Start streaming again
            StreamTweets(api, auth, bbox, credentialsDB, locationID, addStreamData)
       #If maximum recursion reached
        elif isinstance(e, RuntimeError):
            #Log the error
            logger.error('Maximum Recursion Reached on Attempting to Restart Stream', exc_info = True)
            #Raise the error
            raise e
       #Otherwise
        else:
            #Log the error
            logger.error('Unknown Problem Restarting Stream on Failue', exc_info = True)
            #Raise the error
            raise e
            
    #Return true to maintain the stream
    return(True)