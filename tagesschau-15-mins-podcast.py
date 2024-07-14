import requests
import os
import datetime
import xml.etree.ElementTree as ET
from urllib.request import urlretrieve
import re
import glob

current_time = datetime.datetime.now()
print("Current time:", current_time)

media_path = "/root/media/tagesschau"

rss = "https://www.tagesschau.de/multimedia/podcast/15-minuten/index~podcast.xml"
response = requests.get(rss)
data = response.text

root = ET.fromstring(data)

for item in root.findall('channel/item'):
    item_title = item.find('title').text
    item_title = item_title.replace(" / ", "_").replace(" - ", "_").replace(" ", "-")
    item_title = re.sub(r'[<>:"/\\|?*]', '', item_title)
    item_enclosure_url = item.find('enclosure').get('url')
    # print(item_enclosure_url)
    
    filename = os.path.basename(item_enclosure_url)
    
    item_pub_date = item.find('pubDate').text
    # print(item_pub_date)
    item_pub_date_datetime = datetime.datetime.strptime(item_pub_date, "%a, %d %b %Y %H:%M:%S %z")
    item_pub_date_mysql_format = item_pub_date_datetime.strftime("%Y-%m-%d")
    
    new_title = item_pub_date_mysql_format+"_"+item_title+".mp3"
    
    file_path = os.path.join(media_path, new_title)
    if not os.path.exists(file_path):
        print("Downloading:",item_enclosure_url,"as",file_path)
        urlretrieve(item_enclosure_url, file_path)

    else:
        break
    
# Get all files in media_path folder
files = glob.glob(os.path.join(media_path, "*.mp3"))

# Sort files by date in their title
files.sort(key=lambda x: os.path.basename(x).split("_")[0], reverse=True)

# Check if there are more than 5 files
if len(files) > 5:
    # Delete the oldest files until there are only 5 left
    for file in files[5:]:
        print("Removing file:",file)
        os.remove(file)
