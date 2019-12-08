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
############################# DATABASE FUNCTIONS ##############################
###############################################################################


#%% Requried Libraries

#mySQL Connector: Used to interact with SQL database
import mysql.connector

#re: for regular expressions on strings
import re

#logging: Used to create logs
import logging


#%% Configure logger

logger = logging.getLogger(__name__)


#%% Interaction Functions

#Define a function to connect to the database
def Connect2DB(credentialsDB):

    try:
        #Connect to the DB
        cnx = mysql.connector.connect(host   = credentialsDB[0],
                                      user   = credentialsDB[1],
                                      passwd = credentialsDB[2],
                                      db     = credentialsDB[3])
            
    except Exception as e:
        #Add error to log and raise
        logger.error("Error connecting to the Database", exc_info = True)
        raise e
    
    #Add success to log
    logger.info('Connected to the Database')
        
    #Set the character set for the connection
    cnx.set_charset_collation(charset = 'utf8mb4', collation = 'utf8mb4_bin')
    
    #Create a cursor object
    cursor = cnx.cursor()
    
    #Return the cnx and cursor
    return(cnx, cursor)
   

#Define a function to close the database connection
def CloseDBConnection(cnx, cursor):
    #Close the cursor
    _ = cursor.close()
    
    #Close the connection
    cnx.close()
    
    #Add info to log
    logger.info('Closed the Database Conenction')
    
    #Return Null  
    

#%% Query Generation Functions
    
#Define a function to generate the SQL Insert Statements
def GenerateSQLInsert(request):
    
    if request.lower() == 'trends':
        #Define a mySQL insert statement for trend data
        addTrendData = ("INSERT INTO trends "
                        "(trend_woeid, \
                        trend_woeid_name, \
                        trend_datetime_asof, \
                        trend_datetime_createdat, \
                        trend_rank, \
                        trend_name, \
                        trend_url, \
                        trend_promotedcontent, \
                        trend_query, \
                        trend_tweetvolume) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
  
        #Add success to log
        logger.info('Successfully Generated SQL Insert Statement')
        
        #Return output
        return(addTrendData)
        
    elif request.lower() == 'stream':
              
        #Define mySQL insert statements for streaming data
        addPlaceData = ("INSERT IGNORE INTO places "
                        "(place_id, \
                        place_url, \
                        place_type, \
                        place_name, \
                        place_fullname, \
                        place_countrycode, \
                        place_country, \
                        place_bbox_type, \
                        place_bbox_coordinates, \
                        place_attributes) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                        
        addUserData = ("INSERT IGNORE INTO users "
                       "(user_id, \
                        user_name, \
                        user_screenname, \
                        user_location, \
                        user_url, \
                        user_description, \
                        user_translator, \
                        user_protected, \
                        user_verified, \
                        user_numfollowers, \
                        user_numfriends, \
                        user_numlisted, \
                        user_numfavourites, \
                        user_numstatus, \
                        user_joinedstring, \
                        user_joined, \
                        user_utcoffset, \
                        user_timezone, \
                        user_geoenabled, \
                        user_lang, \
                        user_contributorsenabled, \
                        user_istranslator, \
                        user_profile_bgcolour, \
                        user_profile_bgimageurl, \
                        user_profile_bgtile, \
                        user_profile_linkcolour, \
                        user_profile_sidebordercolour, \
                        user_profile_sidefillcolour, \
                        user_profile_textcolour, \
                        user_profile_bgimage, \
                        user_profile_image, \
                        user_profile_banner, \
                        user_default_profile, \
                        user_default_profileimage, \
                        user_following, \
                        user_followrequestsent, \
                        user_notifications) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        addTweetData = ("REPLACE INTO tweets "
                        "(tweet_id, \
                         tweet_createdstring, \
                         tweet_created, \
                         tweet_content, \
                         tweet_source, \
                         tweet_truncated, \
                         tweet_replyto_id, \
                         tweet_replyto_userid, \
                         tweet_replyto_screenname, \
                         tweet_user_id, \
                         tweet_place_id, \
                         tweet_geo, \
                         tweet_coordinates, \
                         tweet_contributors, \
                         tweet_isquotestatus, \
                         tweet_quotecount, \
                         tweet_replycount, \
                         tweet_retweetcount, \
                         tweet_favouritecount, \
                         tweet_favourited, \
                         tweet_retweeted, \
                         tweet_filterlevel, \
                         tweet_lang, \
                         tweet_mstimestamp, \
                         tweet_streamlocation, \
                         tweet_entities, \
                         tweet_full_json) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        
        addUserMentionData = ("INSERT IGNORE INTO usermentions "
                              "(mentioneduser_id, \
                              mentioneduser_screenname, \
                              mentioneduser_name) "
                              "VALUES (%s, %s, %s)")
                        
        addEntityData = ("INSERT IGNORE INTO entities_used "
                         "(entity_content, \
                          entity_type) "
                         "VALUES (%s, %s)")
                         
        addMediaData = ("INSERT IGNORE INTO media_included "
                         "(media_id, \
                          media_displayurl, \
                          media_url, \
                          media_sourcestatus, \
                          media_type) "
                         "VALUES (%s, %s, %s, %s, %s)")
        
        addTweetEntityRelation = ("INSERT IGNORE INTO tweet_entities "
                                 "(tweet_id, \
                                  entity_content, \
                                  entity_type) "
                                 "VALUES (%s, %s, %s)")
        
        addTweetMentionRelation = ("INSERT IGNORE INTO tweet_usermentions "
                                 "(tweet_id, \
                                  mentioneduser_id) "
                                 "VALUES (%s, %s)")

        addTweetMediaRelation = ("INSERT IGNORE INTO tweet_media "
                                 "(tweet_id, \
                                  media_id) "
                                 "VALUES (%s, %s)")
        
        #Combine into one tuple
        addStreamData = (addPlaceData,
                         addUserData,
                         addTweetData,
                         addUserMentionData,
                         addEntityData,
                         addMediaData,
                         addTweetEntityRelation,
                         addTweetMentionRelation,
                         addTweetMediaRelation)
        
        #Add logger info
        logger.info('Successfully Generated SQL Insert Statements')
        
        #Return output
        return(addStreamData)
        
    else:
        #Add error to log and raise
        logger.error("Incorrect Request Entered", exc_info = True)
        raise AttributeError('Expected "trends" or "stream" but got %s' % request)
  
    
#%% Writing Functions
        
#Define a function to write the trend data to the database
def WriteTrendData2DB(cnx, cursor, addTrendData, trends):
    ''' This function appends an entry to a mySQL database.
    '''
    try:
        #Extract the as of timestamp
        trend_asof = re.sub(r"[a-zA-Z]", " ", trends['as_of'])
        #Remove trailing spaces
        trend_asof = trend_asof.strip()
    
        #Extract the created timestamp
        trend_created = re.sub(r"[a-zA-Z]", " ", trends['created_at'])
        #Remove trailing spaces
        trend_created = trend_created.strip()
        
        #Extract the woeid data
        trend_woeid = trends['locations'][0]['woeid']
        trend_woeid_name = trends['locations'][0]['name']
        
        #For every trend in trends
        for trend in trends['trends']:
            trend_rank = trends['trends'].index(trend) + 1
            trend_name = trend['name']
            trend_url = trend['url']
            trend_promcont = trend['promoted_content']
            trend_query = trend['query']
            trend_tweetvol = trend['tweet_volume']
            
            #Create tuple of data information
            data = (trend_woeid,
                    trend_woeid_name,
                    trend_asof,
                    trend_created,
                    trend_rank,
                    trend_name,
                    trend_url,
                    trend_promcont,
                    trend_query,
                    trend_tweetvol)
            
            # Insert the new observation to the database
            cursor.execute(addTrendData, data)
            
    except Exception as e:
        #Add error to log and raise
        logger.error('Error Parsing /or Executing Trend Data to DB', exc_info = True)
        raise e
                
    try:
        #Commit to the database
        cnx.commit()
        
    except Exception as e:
        #Add error to log and raise
        logger.error('Error Committing Trend Data to the Database', exc_info = True)
        raise e
        
    logger.info('Trend Data Successfully Written to the Database')
        
    #Return Null
    
    
#Define a function to write the stream data to the database
def WriteStreamData2DB(cnx, cursor, addStreamData, dataOutput, dataRelations):
    '''
    This function appends a tweet and its meta-data to a mySQL database.
    '''
    
    #Unpack dataOutput tuple
    dataTweet, dataUser, dataPlace, dataEntities, dataUserMentions, dataMedia = dataOutput
    
    #Unpack sql command tuple
    addPlaceData, addUserData, addTweetData, addUserMentionData, addEntityData, addMediaData, addTweetEntityRelation, addTweetMentionRelation, addTweetMediaRelation = addStreamData
        
    #Unpack dataRelations tuple
    dataTweetMentions, dataTweetEntities, dataTweetMedia = dataRelations
    
    try:
        #Insert any new places
        cursor.execute(addPlaceData, dataPlace)
        
        #Commit to the database
        cnx.commit()
        
        #Insert any new users
        cursor.execute(addUserData, dataUser)
          
        #Commit to the database
        cnx.commit()
        
        #Insert the tweet
        cursor.execute(addTweetData, dataTweet)
        
        #Commit to the database
        cnx.commit()
        
    # !! OLD CODE - CAN EXECUTE ALL AT ONCE !!
    #    #Insert the user mentions
    #    for mention in dataUserMentions:
    #        cursor.execute(addUserMentionData, mention)
    #
    #    #Insert the entities
    #    for entity in dataEntities:
    #        cursor.execute(addEntityData, entity)  
            
        #Insert the user mentions
        cursor.executemany(addUserMentionData, dataUserMentions)
        
        #Commit to the database
        cnx.commit()
        
        #Insert the entities
        cursor.executemany(addEntityData, dataEntities)
             
        #Commit to the database
        cnx.commit()
        
        #Insert the media included
        cursor.executemany(addMediaData, dataMedia)
        
        #Commit to the database
        cnx.commit()
        
        
        #Add the tweet mention relationships
        cursor.executemany(addTweetMentionRelation, dataTweetMentions)
        
        #Commit to the database
        cnx.commit()
        
        #Add the tweet entity relationships
        cursor.executemany(addTweetEntityRelation, dataTweetEntities)
        
        #Commit to the database
        cnx.commit()
        
        #Add the tweet media relationships
        cursor.executemany(addTweetMediaRelation, dataTweetMedia)
        
        #Commit to the database
        cnx.commit()
        
    except Exception as e:
        #Add error to log and raise
        logger.error('Error Writing Stream Data to Database', exc_info = True)
        raise e
        
    logger.info('Stream Data Successfully Written to the Database')
        
    #Return Null
    
    