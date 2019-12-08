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
################################# MAIN SCRIPT #################################
###############################################################################

#%% Notes

# 1. Run the following to obtain a list of WOEID locations that can be used to
#    to extract trends for a given area.
#    >> woeidList = IdentifyWOEIDLocations(api)

# 2. OpenSSL, although not used explicity, is included to aid in catching any
#    any related errors.


#%% Required Libraries

#logging: Used to create logs
import logging

#pyOpenSSL: Python wrapper for the OpenSSL library
import OpenSSL

#argparse: For specifying arguments on CLI
import argparse

#os: For interacting with the host operating system
import os

#sys: For interacting with the interpreter
import sys


#%% Import Required Functions from Other Modules

import authentication_functions as axf
import db_functions as dbf
import woeid_functions as geo
import scraping_functions as scrape


#%% Main Function
# Define the main function that brings together the whole script
            
def StartMining(locationID, request, credJSON = 'credentials.json'):
   
    #Read the DB credentials
    credentialsDB = axf.ReadDBCredentials(credJSON)

    #Create an API object
    auth, api = scrape.StartAPI(credJSON = 'credentials.json')  
        
    if request.lower() == 'trends':
        #Extract the location trends
        trends = scrape.GetTrends(api, locationID)
        
        #Generate SQL statement
        addTrendData = dbf.GenerateSQLInsert(request)
        
        #Establish a connection to the DB
        cnx, cursor = dbf.Connect2DB(credentialsDB)
        
        #Write the data to the database
        dbf.WriteTrendData2DB(cnx, cursor, addTrendData, trends)
        
        #Close the cursor and connection
        dbf.CloseDBConnection(cnx, cursor)
        
    elif request.lower() == 'stream':
        #Get bbox from locationID
        bbox = geo.BBoxofWOEID(locationID, credJSON = 'credentials.json')
        
        #Generate SQL statements
        addStreamData = dbf.GenerateSQLInsert(request)
        
        #Start streaming
        scrape.StreamTweets(api, auth, bbox, credentialsDB, locationID, addStreamData)
        
    else:
        #Add error to log and raise
        logger.error("Incorrect Request Entered", exc_info = True)
        raise AttributeError('Expected "trends" or "stream" but got %s' % request)       
    
    #Return Null
               
    
#%% Run the Main Function
                
#If in CL environment
if __name__ == '__main__':
    #Configure the logging file
    logging.basicConfig(filename = 'logfile.log', level = logging.DEBUG)
    logger = logging.getLogger()

    #Create ArgumentParser object
    parser = argparse.ArgumentParser()

    #Add arguments
    parser.add_argument('--locationID',
                        type = int,
                        help = 'a WOEID supplied as an integer')
    parser.add_argument('--request',
                        type = str,
                        help = 'option of obtaining "trends" or "stream"ing\
                                from a given WOEID')
    parser.add_argument('--credJSON',
                        type = str,
                        help = 'filepath to JSON credentials file')
    
    #Parse arguments
    args = parser.parse_args()

    #Run the main function
    try:
        StartMining(**vars(args))
        
    #Add an exception for the user to end the script
    except KeyboardInterrupt:
        #Add information to the log
        logger.info('Streaming Ended by User')
        
        #Close the script
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
    