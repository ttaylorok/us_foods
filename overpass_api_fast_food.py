import overpy
import numpy as np
import pandas as pd
import time

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

states = ["Alabama",
"Alaska",
"Arizona",
"Arkansas",
"California",
"Colorado",
"Connecticut",
"Delaware",
"Florida",
"Georgia",
"Hawaii",
"Idaho",
"Illinois",
"Indiana",
"Iowa",
"Kansas",
"Kentucky",
"Louisiana",
"Maine",
"Maryland",
"Massachusetts",
"Michigan",
"Minnesota",
"Mississippi",
"Missouri",
"Montana",
"Nebraska",
"Nevada",
"New Hampshire",
"New Jersey",
"New Mexico",
"New York",
"North Carolina",
"North Dakota",
"Ohio",
"Oklahoma",
"Oregon",
"Pennsylvania",
"Rhode Island",
"South Carolina",
"South Dakota",
"Tennessee",
"Texas",
"Utah",
"Vermont",
"Virginia",
"Washington",
"West Virginia",
"Wisconsin",
"Wyoming"]

arr = []
for s in states:
    print(s)
    time.sleep(60)
    api = overpy.Overpass()
    r = api.query("""
    [out:json][timeout:200];
    (
      area[name="%s"];
      nwr["amenity"="fast_food"](area);
    );
    out body;
    >;
    out skel qt;
    """ % (s))
    
    # for n in np.arange(0,len(r.nodes)):
    #     #x = n.tags
    #     print(r.nodes[n].tags)
    
          
    for n in r.nodes:
        x = n.tags
        name, cuisine = "none", "none"
        if "name" in x:
            name = x["name"]
        if "cuisine" in x:
            cuisine = x["cuisine"]
        lat = n.lat
        lon = n.lon
        #print([name, cuisine, lat, lon])
        arr.append([name, cuisine, lat, lon, s])
       
    
    for n in r.ways:
        x = n.tags
        # if x != {}:
        #     print(x)
        if "name" in x:
            name = x["name"]
        else:
            name = "none"
        if "cuisine" in x:
            cuisine = x["cuisine"]
        else:
            cuisine = "none"
        
        lt = 0
        ln = 0
        nodes = n.get_nodes(resolve_missing=True)
        for m in nodes:
            lt += m.lat
            ln += m.lon
        lat = lt/len(n.nodes)
        lon = ln/len(n.nodes)
            
        #print([name, cuisine, lat, lon])
        arr.append([name, cuisine, lat, lon, s])
    
df = pd.DataFrame(arr)
df.to_csv("all_restaurants_usa_overpass_fast_food_v1.csv")
