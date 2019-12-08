# geoTwitterMining


## Description

This code utilises the twitter API to obtain information on a given geographical region. The code has two main functionalities: obtaining the top 50 trends in a given region (single run), and listening on the twitter API to obtain tweets as they are posted (continuous run).

The code also links with the Flickr API to identify the geographic bounding boxes (longitude and latitude pairs) of a given WOEID.

## Requirements

- Python 3
- MySQL Database
- Twitter API Key (Apply here: https://developer.twitter.com/en/apply-for-access)
- Flickr API Key (Apply here: https://www.flickr.com/services/apps/create/apply)

## Setup

1. Download all files in the `code` sub-directory of this repository.
2. Run the `geoTwitterMining.sql` file to create the appropriate database.
3. Edit the `credentials.json` file, replacing the empty quotes with your authentication details.
4. Open the command prompt and move to the relevant directory.
5. Enter the following command

```python
python start-mining.py --locationID #1 -- request #2 --credJSON #3
```
where:
\#1 is the WOEID for the region of interest.
\#2 is a choice of `trends` to obtain the current top 50 trends for the specified locationID or `stream` to listen on the API and save tweets as they become available.
\#3 is the filepath/name of the credentials JSON file.

For example, to listen for tweets from London UK you would call the following:
```python
python start-mining.py --locationID 44418 -- request stream --credJSON credentials.json
```

## Citing This Package
Please accredit this package by citing the following in your references. 

```
@phdthesis{hammocks_2019, title={Horizon Scanning Through Computer-Automated Information Prioritisation}, author={Hammocks, Daniel}, year={2019}}
```
