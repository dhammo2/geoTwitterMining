CREATE DATABASE IF NOT EXISTS `twitter_geo_stream`;
USE `twitter_geo_stream`;
COMMIT;

/* TABLE CREATION FOR LOCATION TRENDS */

########## CREATE TREND TABLES ##########
CREATE TABLE trends (
	trend_id INT NOT NULL AUTO_INCREMENT,
    trend_woeid INT,
	trend_woeid_name VARCHAR(128),
    trend_datetime_asof DATETIME,
	trend_datetime_createdat DATETIME,
    trend_rank TINYINT,
    trend_name VARCHAR(128),
    trend_url VARCHAR(1024),
    trend_promotedcontent VARCHAR(512),
    trend_query VARCHAR(128),
    trend_tweetvolume INT,
	PRIMARY KEY (trend_id)
);


/* TABLE CREATION FOR TWITTER STREAMING */

########## CREATE PLACES TABLE ##########
CREATE TABLE places (
	place_id VARCHAR(128) NOT NULL,
    place_url VARCHAR(1024),
    place_type VARCHAR(64),
    place_name VARCHAR(128),
    place_fullname VARCHAR(128),
    place_countrycode VARCHAR(4),
    place_country VARCHAR(128),
    place_bbox_type VARCHAR(64),
    place_bbox_coordinates VARCHAR(256),
    place_attributes VARCHAR(512),
    PRIMARY KEY (place_id)
);

########## CREATE USERS TABLE ##########
CREATE TABLE users (
	user_id BIGINT NOT NULL,
    user_name VARCHAR(128),
    user_screenname VARCHAR(128),
    user_location VARCHAR(256),
    user_url VARCHAR(1024),
    user_description MEDIUMTEXT,
    user_translator VARCHAR(64),
    user_protected BOOLEAN,
    user_verified BOOLEAN,
    user_numfollowers BIGINT,
    user_numfriends INT,
    user_numlisted INT,
    user_numfavourites INT,
    user_numstatus INT,
    user_joinedstring VARCHAR(128),
    user_joined DATETIME,
    user_utcoffset VARCHAR(8),
    user_timezone VARCHAR(128),
    user_geoenabled BOOLEAN,
    user_lang VARCHAR(64),
    user_contributorsenabled BOOLEAN,
    user_istranslator BOOLEAN,
    user_profile_bgcolour VARCHAR(6),
    user_profile_bgimageurl VARCHAR(1024),
    user_profile_bgtile BOOLEAN,
    user_profile_linkcolour VARCHAR(6),
    user_profile_sidebordercolour VARCHAR(6),
    user_profile_sidefillcolour VARCHAR(6),
    user_profile_textcolour VARCHAR(6),
    user_profile_bgimage BOOLEAN,
    user_profile_image VARCHAR(1024),
    user_profile_banner VARCHAR(1024),
    user_default_profile BOOLEAN,
    user_default_profileimage BOOLEAN,
    user_following VARCHAR(64),
    user_followrequestsent VARCHAR(64),
    user_notifications VARCHAR(64),
    PRIMARY KEY (user_id)
);


CREATE TABLE tweets (
	tweet_id BIGINT NOT NULL,
	tweet_createdstring VARCHAR(128),
	tweet_created DATETIME,
	tweet_content VARCHAR(312),
	tweet_source VARCHAR(256),
	tweet_truncated BOOLEAN,
	tweet_replyto_id BIGINT,
	tweet_replyto_userid BIGINT,
	tweet_replyto_screenname VARCHAR(128),
	tweet_user_id BIGINT NOT NULL,
	tweet_place_id VARCHAR(128),
	tweet_geo VARCHAR(64),
	tweet_coordinates VARCHAR(128),
	tweet_contributors VARCHAR(64),
	tweet_isquotestatus BOOLEAN,
	tweet_quotecount INT,
	tweet_replycount INT,
	tweet_retweetcount INT,
	tweet_favouritecount INT,
	tweet_favourited BOOLEAN,
	tweet_retweeted BOOLEAN,
	tweet_filterlevel VARCHAR(128),
	tweet_lang VARCHAR(64),
	tweet_mstimestamp BIGINT,
	tweet_streamlocation INT,
	tweet_entities MEDIUMTEXT,
    tweet_full_json MEDIUMTEXT,
	PRIMARY KEY (tweet_id),
    FOREIGN KEY (tweet_user_id)
        REFERENCES users (user_id),
	FOREIGN KEY (tweet_place_id)
        REFERENCES places (place_id)
);

CREATE TABLE usermentions (
	mentioneduser_id BIGINT NOT NULL,
    mentioneduser_screenname VARCHAR(128),
    mentioneduser_name VARCHAR(128),
	PRIMARY KEY (mentioneduser_id)
);
    
CREATE TABLE entities_used (
	entity_content VARCHAR(128) NOT NULL,
    entity_type VARCHAR(10) NOT NULL,
    PRIMARY KEY (entity_content, entity_type)
);

CREATE TABLE media_included (
	media_id BIGINT,
    media_displayurl VARCHAR(1024),
    media_url VARCHAR(1024),
    media_sourcestatus BIGINT,
    media_type VARCHAR(64),
    PRIMARY KEY (media_id)
);

########## CREATE RELATIONSHIP TABLES ##########
CREATE TABLE tweet_entities (
	tweet_id BIGINT NOT NULL,
    entity_content VARCHAR(128) NOT NULL,
    entity_type VARCHAR(10) NOT NULL,
    PRIMARY KEY (tweet_id, entity_content, entity_type),
    FOREIGN KEY (tweet_id)
		REFERENCES tweets (tweet_id),
	FOREIGN KEY (entity_content, entity_type)
		REFERENCES entities_used (entity_content, entity_type)    
);

CREATE TABLE tweet_usermentions (
	tweet_id BIGINT NOT NULL,
    mentioneduser_id BIGINT NOT NULL,
    PRIMARY KEY (tweet_id, mentioneduser_id),
    FOREIGN KEY (tweet_id)
		REFERENCES tweets (tweet_id),
	FOREIGN KEY (mentioneduser_id)
		REFERENCES usermentions (mentioneduser_id)
);

CREATE TABLE tweet_media (
	tweet_id BIGINT NOT NULL,
    media_id BIGINT NOT NULL,
    PRIMARY KEY (tweet_id, media_id),
    FOREIGN KEY (tweet_id)
		REFERENCES tweets (tweet_id),
	FOREIGN KEY (media_id)
		REFERENCES media_included (media_id)
);

COMMIT;