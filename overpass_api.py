import overpy
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# states = ["Alabama",
# "Alaska",
# "Arizona",
# "Arkansas",
# "California",
# states=["Colorado",
# "Connecticut",
# "Delaware",
# "Florida",
# states=["Georgia",
# "Hawaii",
# "Idaho",
# "Illinois",
# "Indiana",
# "Iowa",
# "Kansas",
# "Kentucky",
# "Louisiana",
# "Maine",
# "Maryland",
# "Massachusetts",
# "Michigan",
# "Minnesota",
# states=["Mississippi",
# "Missouri",
# "Montana",
# states=["Nebraska",
# "Nevada",
# "New Hampshire",
# "New Jersey",
# "New Mexico",
# "New York",
# "North Carolina",
# states=["North Dakota",
# "Ohio",
# states=["Oklahoma",
# "Oregon",
# "Pennsylvania",
# "Rhode Island",
# "South Carolina",
# "South Dakota",
# "Tennessee",
# "Texas",
# "Utah",
# "Vermont",
# "Virginia",
# "Washington",
# states=["West Virginia",
# "Wisconsin",
"Wyoming"]

arr = []
for s in states:
    print(s)
    api = overpy.Overpass()
    r = api.query("""
    [out:json][timeout:200];
    (
      area[name="%s"];
      nwr["amenity"="restaurant"](area);
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
        # if x != {}:
        #     print(x)
        #print(x)
        if "name" in x:
            name = x["name"]
        else:
            name = "none"
        if "cuisine" in x:
            cuisine = x["cuisine"]
        else:
            cuisine = "none"
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
        for m in n.nodes:
            lt += m.lat
            ln += m.lon
        lat = lt/len(n.nodes)
        lon = ln/len(n.nodes)
            
        #print([name, cuisine, lat, lon])
        arr.append([name, cuisine, lat, lon, s])
    
df = pd.DataFrame(arr)
df.to_csv("all_restaurants_usa_overpass_fast_food_v1.csv")
