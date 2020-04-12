import json
import folium
import pandas as pd
import matplotlib.pyplot as plt

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
w = 0 
for s in states:
    with open(s + '.txt', encoding = "UTF-8") as f:
        data = json.load(f)

    for x in data["elements"]:
        if x["type"] == "node" and "tags" in x.keys():
            if "cuisine" not in x["tags"].keys():
                cuisine = "none"
            else:
                cuisine = x["tags"]["cuisine"]
                
            if "name" not in x["tags"].keys():
                name = "none"
            else:
                name = x["tags"]["name"]
                
            if "lat" not in x.keys() or "lon" not in x.keys():
                point = [0.,0.]
            else:
                point = [float(x["lat"]), float(x["lon"])]
            
            arr.append([name,cuisine,point,s])
        if x["type"] == "way":
            w += 1
            
        # #print(x)
        # if "cuisine" not in x["tags"].keys():
        #     cuisine = "none"
        # else:
        #     cuisine = x["tags"]["cuisine"]
        # if x["geometry"]["type"] == "Polygon":
        #     point = x["geometry"]["coordinates"][0][0]
        #     #print(point)
        # else:
        #     point = x["geometry"]["coordinates"]
        # if "name" not in x["properties"].keys():
        #     name = "none"
        # else:
        #     name = x["properties"]["name"]
        # arr.append([name,cuisine,point,s])
        # #print(len(x["geometry"]["coordinates"]))
        
# for x in data["elements"]:
#     print(x)
    
# for x in data["osm3s"]:
#     print(x)
    
# for x in data["generator"]:
#     print(x)

df = pd.DataFrame(arr, columns=["name","cuisine","loc", "state"])
# df2 = pd.DataFrame(df["loc"].to_list())
# df["lat"] = df2[0]
# df["lon"] = df2[1]

df["cuisine_new"] = df["cuisine"]
for y in df.index:
    c = df.loc[y,"cuisine"].lower()
    if "mexican" in c or "taco" in c:
        new = "mexican"
    elif "bbq" in c or "barbeque" in c or "barbecue" in c:
        new = "bbq"
    elif "breakfast" in c or "pancake" in c:
        new = "breakfast"
    elif "vietnamese" in c:
        new = "vietnamese"
    elif "tex-mex" in c:
        new = "tex-mex"
    elif "italian" in c:
        new = "italian"
    elif "steak" in c:
        new = "steak"
    elif "asian" in c:
        new = "asian"
    elif "american" in c:
        new = "american"
    elif "mediterranean" in c:
        new = "mediterranean"
    elif "japanese" in c:
        new = "japanese"
    elif "burger" in c:
        new = "burger"
    elif "seafood" in c:
        new = "seafood"
    elif "indian" in c:
        new = "indian"
    elif "sandwich" in c:
        new = "sandwich"
    elif "french" in c:
        new = "french"
    elif "thai" in c:
        new = "thai"
    elif "korean" in c:
        new = "korean"
    elif "pizza" in c:
        new = "pizza"
    elif "donut" in c:
        new = "donut"
    elif "nepalese" in c:
        new = "nepalese"
    elif "sushi" in c:
        new = "sushi"
    elif "chinese" in c:
        new = "chinese"
    elif "fast_food" in c:
        new = "fast_food"
    elif "cajun" in c:
        new = "cajun"
    elif "taiwanese" in c:
        new = "taiwanese"
    elif "wings" in c or "chicken" in c:
        new = "chinese"
    elif "greek" in c:
        new = "greek"
    elif "hawaiian" in c:
        new = "hawaiian"
    elif "persian" in c:
        new = "persian"
    elif "turkish" in c:
        new = "turkish"
    elif "regional" in c:
        new = "regional"
    elif "peruvian" in c:
        new = "peruvian"
    elif "german" in c:
        new = "german"
    elif "persian" in c:
        new = "persian"
    elif "catfish" in c:
        new = "catfish"
    elif "brazilian" in c:
        new = "brazilian"
    elif "ramen" in c:
        new = "ramen"
    elif "none" in c:
        new = "none"
    else:
        new = "other"
    df.loc[y,"cuisine_new"] = new


filt = (df['cuisine_new'] != "other") & (df['cuisine_new'] != "none")
df_filt = df.loc[filt,:]


count = df_filt.groupby(["cuisine_new"])["cuisine_new"].count()
#plt.bar(x = count.index, height = count)
#plt.show()

df.to_csv("restaurants_all_us.csv")

# RESTAURANTS WITH "BUBBA" IN THE TITLE
# WITH BAR AND GRILL 
# MOST POPULAR PHRASE IN TITLE
# MOST COMMON RESTAURANT
# FAVORITE ETHNIC FOOD
# FAVORITE EUROPEAN
# FAVORITE ASIAN
    