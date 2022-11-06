# import libraries
import os.path
from urllib.request import urlopen, Request
import pandas as pd
import json

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
  print(url)
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
    print(e)

# Convert dictionary into a pandas dataframe
df1 = pd.DataFrame(dataDict.items(), columns=['id', 'title'])

if os.path.exists("data.csv"):
  df2 = pd.read_csv('data.csv')
  pd1 = pd.concat([df1, df2]).drop_duplicates().reset_index(drop=True)

print(df1)
df1.to_csv('data.csv', index=False)




