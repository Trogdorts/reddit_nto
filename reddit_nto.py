# import libraries
import os.path
from urllib.request import urlopen, Request
import pandas as pd
import json
import logging
import sys

# Save the log file in the local directory
LOG_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "reddit_nto.log")
DATA_FILE = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data.csv")

logging.basicConfig(filename=LOG_FILE,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

logging.info("Running Reddit NotTheOnion Script")
logger = logging.getLogger('reddit_nto')



# How far to look back, join to the url
top_options = ['hour', 'day', 'month', 'week', 'year', 'all']
named_options = ['hot', 'new', 'rising']

# How many results to request
num_results =  1000

urls = []
dataDict = {}


# Brute force way of building out URLS
for option in top_options:
  url = "https://www.reddit.com/r/nottheonion/top/.json?t={}?limit={}".format(option, num_results)
  urls.append(url)
for option in named_options:
  url = "https://www.reddit.com/r/nottheonion/{}/.json?limit={}".format(option, num_results)
  urls.append(url)


# Process each URL
for url in urls:
  logger.debug(f"Fetching {url}")
  try:
    # Provide a user-agent because reddit doesnt like programs spamming it
    response = urlopen(Request(url, headers={'User-Agent': 'Mozilla'}))

    # storing the JSON response from url in data
    data_json = json.loads(response.read())

    # format each json object for better reading
    json_formatted_str = json.dumps(data_json, indent=2)

    # extract the title and post id for each post
    for post in data_json['data']['children']:
      id = post['data']['name'].split("_")[1].upper()
      title = post['data']['title']
      if id not in dataDict.keys():
        dataDict[id] = title
  except Exception as e:
    logger.error(f"Failed processing {url} with error: {e}")

# Convert dictionary into a pandas dataframe
df1 = pd.DataFrame(dataDict.items(), columns=['id', 'title'])

if os.path.exists(DATA_FILE):
  logger.info("Merging new titles into the existing titles.")
  df2 = pd.read_csv(DATA_FILE)
  pd1 = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)
else:
  logger.info("First run, creating the csv file.")
pd1.to_csv(DATA_FILE, index=False)
logger.info("Exiting.")
sys.exit()



