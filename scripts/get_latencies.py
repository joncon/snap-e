'''
This script will iterate through the channels found in /www/assets/snap-e/pnsn_station_latencies.json
And make a json requst for each in as tight window to get the most current and least amount of metrics
IRIS updates the data_latency metric every four hours on what appearst to be the fours(00,04,04,12,16,20)
To be safe cron will wait till 15 after.
This script takes no arguements.
'''
import os,json, urllib
from pprint import pprint
import datetime

latency_file="/www/assets/snap-e/pnsn_station_latencies.json"
base_url ="http://service.iris.edu/mustang/measurements/1/query?metric=data_latency&output=json"
#request json from url and turn it into python obj
def request(url):
    json_response=urllib.urlopen(url)
    return json.loads(json_response.read())

#return date string for query in form
#of YYYY-MM-DDTHH:MM:ss
def construct_date_string(dateobj):
  return dateobj.strftime("%Y-%m-%dT%H:%M:%S")
    


###################GET EXISTING STRUCTURE FROM FILE#######################
with open(latency_file) as data_file:
    try:
        json_obj=json.load(data_file)
    except ValueError:
        print "file has no json man..."
        exit(1)

#now iterate through the targets from mustang, get lat, lon for each from stas_aqms
count =0
stop= datetime.datetime.utcnow()
start = stop - datetime.timedelta(hours=9) #this is probably more than enough 5 would suffice. 
stop_string=construct_date_string(stop)
start_string=construct_date_string(start)
for key in json_obj:
    url ="%s&sta=%s&chan=%s&timewindow=%s,%s"%(base_url,key,json_obj[key]['chan'], start_string, stop_string)
    response=request(url)
    dl = response['measurements']['data_latency']
    if(len(dl)> 0):
        json_obj[key]['latency'] = dl[0]['value']
# # #write the whole thing back to file:
with open(latency_file, 'w') as outfile:
    json.dump(json_obj, outfile)

