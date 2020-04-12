import requests
import json

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

states = ["Alabama"]

overpass_url = "http://overpass-api.de/api/interpreter"

for s in states:
    print(s)
    overpass_query = """
    [out:json][timeout:60];
    (
      area[name="%s"];
      nwr["amenity"="restaurant"](area);
    );
    out body;
    >;
    out skel qt;
    """ % (s)
    response = requests.get(overpass_url, 
                            params={'data': overpass_query})
    data = response.json()
    
    with open(s+'.txt', 'w') as outfile:
        json.dump(data, outfile)