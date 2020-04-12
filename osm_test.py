import json
import folium

with open('restaurantes_dallas.geojson', encoding = "UTF-8") as f:
    data = json.load(f)
    
for x in data["features"]:
    if "cuisine" in x["properties"].keys():
        print(x["properties"]["cuisine"])

m = folium.Map()

# def sf(y):
#     {
#     if "cuisine" in y["properties"].keys():
#         if y['properties']['cuisine'] == "chinese" :
#             'fillColor': '#0000ff'
#         elif y['properties']['cuisine'] == "pizza":
#             'fillColor': '#ff0000'
#         else:
#             'fillColor': '#ffffff'
#     else:
#         'fillColor': '#ffffff'
#         }
        
        
colors = {"chinese" : {'color': '#ffffff'}}

sss = lambda x : {'color': '#0000ff' , 'icon' : 'circle'
                  if "cuisine" not in x["properties"].keys() 
                      or x["properties"]["cuisine"] not in colors
                  else colors[x["properties"]["cuisine"]]}
    # if "cuisine" in x["properties"].keys():
    #     if x['properties']['cuisine'] == "chinese" :
    #         {'fillColor': '#0000ff'}
    #     elif x['properties']['cuisine'] == "pizza":
    #         {'fillColor': '#ff0000'}
    #     else:
    #         {'fillColor': '#ffffff'}
    # else:
    #     {'fillColor': '#ffffff'}
folium.GeoJson(data, style_function = sss).add_to(m)


m.save("restaurants.html")

    
# fin  = open('restaurantes_dallas.geojson', encoding = "UTF-8")

# input =""
# for line in fin:
#     input += line

# fin.close()
