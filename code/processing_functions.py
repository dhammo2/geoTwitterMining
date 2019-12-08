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
########################## DATA PROCESSING FUNCTIONS ##########################
###############################################################################

#%% Required Libraries

#json: Used to read JSON files
import json

#datetime: for extracting datetimes from strings
from datetime import datetime

#logging: Used to create logs
import logging


#%% Configure logger

logger = logging.getLogger(__name__)


#%% Functions

#Define a function for processing raw twitter data
def ProcessTwitterData(data, locationID):
    
    try:
        #Read data as JSON
        dataJSON = json.loads(data)
    except Exception as e:
        #Write error to log
        logger.error('Could Not Read JSON Data File')
        #Raise the error
        raise e
    
    try:
        #Convert to string for storage
        tweet_full_json = str(dataJSON)
        
        #Extract tweet data
        tweet_streamlocation = locationID
        tweet_createdstring  = dataJSON['created_at']
        tweet_created        = datetime.strptime(tweet_createdstring, '%a %b %d %H:%M:%S %z %Y')
        tweet_id             = dataJSON['id']
        tweet_content        = dataJSON['text']
        tweet_source         = dataJSON['source']
        tweet_truncated      = 1 if dataJSON['truncated'] == True else 0
        
        tweet_replyto_id     = dataJSON['in_reply_to_status_id']       
        tweet_replyto_userid = dataJSON['in_reply_to_user_id']
        tweet_replyto_screenname    = dataJSON['in_reply_to_screen_name']
        
        ## Foreign Keys ##
        tweet_user_id        = dataJSON['user']['id']
        tweet_place_id       = dataJSON['place']['id']
        ## ~~~~~~~~~~~~~ ##
        
        try:
            tweet_geo        = str(dataJSON['geo']['coordinates'])
        except:
            tweet_geo        = ''
    
        try:
            tweet_coordinates    = str(dataJSON['coordinates']['coordinates'])
        except:
            tweet_coordinates = ''
        
        tweet_contributors   = dataJSON['contributors']
        tweet_isquotestatus  = 1 if dataJSON['is_quote_status'] == True else 0
        tweet_quotecount     = dataJSON['quote_count']
        tweet_replycount     = dataJSON['reply_count']
        tweet_retweetcount   = dataJSON['retweet_count']
        tweet_favouritecount = dataJSON['favorite_count']
        
        tweet_favourited     = 1 if dataJSON['favorited'] == True else 0
        tweet_retweeted      = 1 if dataJSON['retweeted'] == True else 0
        tweet_filterlevel    = dataJSON['filter_level']
        tweet_lang           = dataJSON['lang']
        tweet_mstimestamp    = dataJSON['timestamp_ms']
        tweet_entities       = str(dataJSON['entities'])
        
        #Create Tweet Data Object
        dataTweet = (tweet_id,
                     tweet_createdstring,
                     tweet_created,
                     tweet_content,
                     tweet_source,
                     tweet_truncated,
                     tweet_replyto_id,
                     tweet_replyto_userid,
                     tweet_replyto_screenname,
                     tweet_user_id,
                     tweet_place_id,
                     tweet_geo,
                     tweet_coordinates,
                     tweet_contributors,
                     tweet_isquotestatus,
                     tweet_quotecount,
                     tweet_replycount,
                     tweet_retweetcount,
                     tweet_favouritecount,
                     tweet_favourited,
                     tweet_retweeted,
                     tweet_filterlevel,
                     tweet_lang,
                     tweet_mstimestamp,
                     tweet_streamlocation,
                     tweet_entities,
                     tweet_full_json)
        
        
        ## Many-to-Many relations
        
        #Extract entities used
        entities_hashtags           = [(x['text'], 'hashtag') for x in dataJSON['entities']['hashtags']]
        entities_urls               = [(x['expanded_url'], 'url') for x in dataJSON['entities']['urls']]
        entities_symbols            = [(x['text'], 'symbol') for x in dataJSON['entities']['symbols']]
        
        #Create entity object
        dataEntities = entities_hashtags + entities_urls + entities_symbols
        
        
        #Extract mentioned users
        usermentions_screennames    = [x['screen_name'] for x in dataJSON['entities']['user_mentions']]
        usermentions_names          = [x['name'] for x in dataJSON['entities']['user_mentions']]
        usermentions_ids            = [x['id'] for x in dataJSON['entities']['user_mentions']]
        
        #create mentioned users object
        dataUserMentions = list(zip(usermentions_ids,
                                    usermentions_screennames,
                                    usermentions_names))
        
        #Extract included media
        if 'extended_entities' in dataJSON:
            media_id            = [x['id'] for x in dataJSON['extended_entities']['media']]
            media_displayurl    = [x['expanded_url'] for x in dataJSON['extended_entities']['media']]
            media_url           = [x['media_url'] for x in dataJSON['extended_entities']['media']]
            try:
                media_sourcestatus  = [x['source_status_id'] for x in dataJSON['extended_entities']['media']]
            except:
                media_sourcestatus  = ['' for x in dataJSON['extended_entities']['media']]  
            media_type           = [x['type'] for x in dataJSON['extended_entities']['media']]
            
            #Create included media object
            dataMedia = list(zip(media_id,
                                 media_displayurl,
                                 media_url,
                                 media_sourcestatus,
                                 media_type))
        
        else:
            #Create blank media object
            dataMedia = []
            
        
        #Extract place data (if exists)
        
        place_id                = dataJSON['place']['id']
        place_url               = dataJSON['place']['url']
        place_type              = dataJSON['place']['place_type']
        place_name              = dataJSON['place']['name']
        place_fullname          = dataJSON['place']['full_name']
        place_countrycode       = dataJSON['place']['country_code']
        place_country           = dataJSON['place']['country']
        place_bbox_type         = dataJSON['place']['bounding_box']['type']
        place_bbox_coordinates  = str(dataJSON['place']['bounding_box']['coordinates'])
        place_attributes        = str(dataJSON['place']['attributes'])
        
        #Create place data object
        dataPlace = (place_id,
                     place_url,
                     place_type,
                     place_name,
                     place_fullname,
                     place_countrycode,
                     place_country,
                     place_bbox_type,
                     place_bbox_coordinates,
                     place_attributes)
        
        #Extract User Data
        user_id                         = dataJSON['user']['id']       
        user_name                       = dataJSON['user']['name']
        user_screenname                 = dataJSON['user']['screen_name']
        user_location                   = dataJSON['user']['location']
        user_url                        = dataJSON['user']['url']
        user_description                = dataJSON['user']['description']
        user_translator                 = dataJSON['user']['translator_type']
        user_protected                  = 1 if dataJSON['user']['protected'] == True else 0
        user_verified                   = 1 if dataJSON['user']['verified'] == True else 0
        user_numfollowers               = dataJSON['user']['followers_count']
        user_numfriends                 = dataJSON['user']['friends_count']
        user_numlisted                  = dataJSON['user']['listed_count']
        user_numfavourites              = dataJSON['user']['favourites_count']
        user_numstatus                  = dataJSON['user']['statuses_count']
        user_joinedstring               = dataJSON['user']['created_at']
        user_joined                     = datetime.strptime(user_joinedstring, '%a %b %d %H:%M:%S %z %Y')
        user_utcoffset                  = dataJSON['user']['utc_offset']
        user_timezone                   = dataJSON['user']['time_zone']
        user_geoenabled                 = 1 if dataJSON['user']['geo_enabled'] == True else 0
        user_lang                       = dataJSON['user']['lang']
        user_contributorsenabled        = 1 if dataJSON['user']['contributors_enabled'] == True else 0
        user_istranslator               = 1 if dataJSON['user']['is_translator'] == True else 0
        user_profile_bgcolour           = dataJSON['user']['profile_background_color']
        user_profile_bgimageurl         = dataJSON['user']['profile_background_image_url']
        user_profile_bgtile             = 1 if dataJSON['user']['profile_background_tile'] == True else 0
        user_profile_linkcolour         = dataJSON['user']['profile_link_color']
        user_profile_sidebordercolour   = dataJSON['user']['profile_sidebar_border_color']
        user_profile_sidefillcolour     = dataJSON['user']['profile_sidebar_fill_color']
        user_profile_textcolour         = dataJSON['user']['profile_text_color']
        user_profile_bgimage            = 1 if dataJSON['user']['profile_use_background_image'] == True else 0
        user_profile_image              = dataJSON['user']['profile_image_url']
        try:
            user_profile_banner             = dataJSON['user']['profile_banner_url']
        except:
            user_profile_banner             = ''          
        user_default_profile            = 1 if dataJSON['user']['default_profile'] == True else 0
        user_default_profileimage       = 1 if dataJSON['user']['default_profile_image'] == True else 0
        user_following                  = dataJSON['user']['following']
        user_followrequestsent          = dataJSON['user']['follow_request_sent']
        user_notifications              = dataJSON['user']['notifications']
        
        #Place into User Object
        dataUser = (user_id,
                    user_name,
                    user_screenname,
                    user_location,
                    user_url,
                    user_description,
                    user_translator,
                    user_protected,
                    user_verified,
                    user_numfollowers,
                    user_numfriends,
                    user_numlisted,
                    user_numfavourites,
                    user_numstatus,
                    user_joinedstring,
                    user_joined,
                    user_utcoffset,
                    user_timezone,
                    user_geoenabled,
                    user_lang,
                    user_contributorsenabled,
                	user_istranslator,
                	user_profile_bgcolour,
                	user_profile_bgimageurl,
                	user_profile_bgtile,
                	user_profile_linkcolour,
                	user_profile_sidebordercolour,
                	user_profile_sidefillcolour,
                	user_profile_textcolour,
                	user_profile_bgimage,
                	user_profile_image,
                	user_profile_banner,
                	user_default_profile,
                	user_default_profileimage,
                	user_following,
                	user_followrequestsent,
                	user_notifications)
        
        #Compile data objects into tuple
        dataOutput = (dataTweet, dataUser, dataPlace, dataEntities, dataUserMentions, dataMedia)
        
        #Create relationship entries
        dataTweetMentions = [(tweet_id, x[0]) for x in dataUserMentions]
        dataTweetEntities = [(tweet_id, x[0], x[1]) for x in dataEntities]
        dataTweetMedia = [(tweet_id, x[0]) for x in dataMedia]
        
        #Compile relationships into tuple
        dataRelations = (dataTweetMentions,
                         dataTweetEntities,
                         dataTweetMedia)
    
    except Exception as e:
        #Add error to log
        logger.error('Could Not Process Tweet Data')
        #Raise error
        raise e
        
    logger.info('Tweet Data Objects Successfully Created')
    
    #Return data objects
    return(dataOutput, dataRelations)
    