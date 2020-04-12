# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 09:11:04 2020

@author: comp
"""
import shapefile
import pandas as pd
import folium

sf = shapefile.Reader("tl_2017_us_state/tl_2017_us_state.shp")
w = shapefile.Writer('tl_2017_us_state_modified')

data = pd.read_csv("all_restaurants_compiled_full.csv")

filt2 = data["cuisine_new"] == "other"
data.loc[filt2,"cuisine"]

## total number of restaurants

num_rest = data.groupby(["state"])["cuisine_new"].count()

## number of types of restaurants

g = data.groupby(["state","cuisine_new"])["cuisine_new"].count()



gu = g.unstack()

gs = pd.read_csv("food_stats_output.csv", index_col = "state").filter(["name","percent_chain","labels"])
gs.fillna(-1, inplace = True)

w.field('State', 'C')
for col in gs.columns:
    if col == "name":
        w.field(col,'C')
    elif col == "percent_chain":
        w.field(col,'N',decimal=2)
    else:
        w.field(col,'N')
    
    
fields = w.fields
num_fields = len(fields)

for shaperec in sf.iterShapeRecords():
    state = shaperec.record[6]
    is_found = False
    for x in gs.index:
        if x == state:
            #print(*tuple([state]+gs.loc[state,:].fillna(0).to_list()))
            w.record(*tuple([state]+gs.loc[state,:].fillna(0).to_list()))
            w.shape(shaperec.shape)
            is_found = True
            #break
    # if is_found == False:
    #     print(state)
    #     w.record(*tuple([state]+([0]*num_fields)))
    #     w.shape(shaperec.shape)
            
    
    
    



