#on off to get available targets for station latency. This request takes so long that 
#for testing purposes, it is easier to first create the file and then read it with get_station_data.py
import os, json, urllib
from pprint import pprint

#request json from url and turn it into python obj
def request(url):
    json_response=urllib.urlopen(url)
    return json.loads(json_response.read())
    
z_chans=['HHZ','ELZ','SHZ','HNZ','BHZ','EHZ','ENZ','MNZ','MHZ','EH1','HN1','VM1','BM1']
chan_str=""
for chan in z_chans:
    chan_str+="%schan=%s"%("&", chan)

url="http://service.iris.edu/mustang/targets/1/query?metric=data_latency&output=json&net=UW%s"%chan_str

json_response=urllib.urlopen(url)
j= json.loads(json_response.read())
with open('./mustang_station_latencies.json', 'w') as outfile:
    json.dump(j, outfile)

#now try to read it

with open('mustang_station_latencies.json') as data_file:
     stations=json.load(data_file)
pprint(stations)
 
