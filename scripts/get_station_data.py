'''
1) get availabe channels with data_latentcies from mustang
2) then get lat/lon from aqms_query
3 )and write to file in the following structure:

{sta1: {
    lat: float,
    lon :float
    latency: int (-1 = undefined)
    chan: string
   },
   sta2{...
   } 
}
'''
import os,json, urllib
from pprint import pprint
#if running in test mode, write a json file using create_mustang_target_file.py first
#The target query to iris can take minutes to complete so use json file for testing. 
test=False
#this is where the file will be served from 
latency_file="/www/assets/snap-e/pnsn_station_latencies.json"
#request json from url and turn it into python obj
def request(url):
    json_response=urllib.urlopen(url)
    return json.loads(json_response.read())
    


##############GET AQMS STATIONS####################
url="https://assets.pnsn.org/aqms_query/stations?key=%s"%os.environ['AQMS_API_KEY']
temp_stations_aqms= request(url)
stas_aqms={}

#lets get make this a keyed hash for O(1) lookup
for station in temp_stations_aqms:
    sta=station['sta']
    if sta not in stas_aqms:
        stas_aqms[sta]=station

################GET MUSTANG TARGETS#########################
#use file when testing since the mustang call takes ~ 3 minutes
if test:
    with open('mustang_station_latencies.json') as data_file:
         targets=json.load(data_file)

else:
    z_chans=['HHZ','ELZ','SHZ','HNZ','BHZ','EHZ','ENZ','MNZ','MHZ','EH1','HN1','VM1','BM1']
    chan_str=""
    for chan in z_chans:
        chan_str+="%schan=%s"%("&", chan)

    url="http://service.iris.edu/mustang/targets/1/query?metric=data_latency&output=json&net=UW%s"%chan_str
    targets= request(url)

###################GET EXISTING STRUCTURE FROM FILE#######################
with open(latency_file) as data_file:
    try:
        json_file=json.load(data_file)
    except ValueError:
        print "file has no json man..."


#Now build out new structure with lat/lon from aqms, sta name, and chan from mustang and latency from file
stas_final={}
#now iterate through the targets from mustang, get lat, lon for each from stas_aqms
count =0
for target in targets['targets']:
    sta=target['sta']
    #if station exists in stations table and we have not already created a key for this stations
    if sta in stas_aqms and sta not in stas_final:
        count +=1
        aqms=stas_aqms[sta]
        stas_final[sta]={}
        if sta in json_file:
            latency=json_file[sta]['latency']
        else:
            latency=-1
        stas_final[sta]['latency'] = latency
        stas_final[sta]["chan"]=target['chan']
        stas_final[sta]['lat'] = stas_aqms[sta]['lat']
        stas_final[sta]['lon'] = stas_aqms[sta]['lon']
# pprint(stas_final)
#write the whole thing back to file:
with open(latency_file, 'w') as outfile:
    json.dump(stas_final, outfile)
    
