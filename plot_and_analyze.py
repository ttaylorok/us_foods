import pandas as pd
import matplotlib.pyplot as plt
import mpld3
import seaborn as sns
from sklearn.cluster import KMeans

pd.set_option('display.max_columns', 500)
pd.set_option('display.max_rows', 500)
pd.set_option('display.width', 1000)

data = pd.read_csv("all_restaurants_compiled_full.csv")



## total number of restaurants

num_rest = data.groupby(["state"])["cuisine_new"].count()

## number of types of restaurants

g = data.groupby(["state","cuisine_new"])["cuisine_new"].count()
g.sort_index(inplace = True)

gu = g.unstack()

## by cuisine region

filt2 = (data["cuisine_group"] != "other") & (data["cuisine_group"] != "none") & (data["cuisine_group"] != "America, Northern")
data_filt = data.loc[filt2,:]
g2 = data_filt.groupby(["state","cuisine_group"])["cuisine_group"].count()
gs = data_filt.groupby("state")["state"].count()
g3 = g2 / gs

gu2 = g3.unstack()

#colors = ["#00e803","#00be00","#009400","#01eeff","#00aeba","#ff01ee","#ce00c1","#a4009c","#80007c","#560054","#ffe601","#ff8373","#ff2e17","#b40f00","#8e0b00","#5a0600","#ff6f01"]
#plt.figure(figsize=(6,10))

# gu2.plot(kind='barh', stacked=True, figsize=(12,15))#, color = colors)
# plt.gca().invert_yaxis()
# plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
# plt.subplots_adjust(right=0.79)
# plt.savefig("cuisine_by_group")

# plt.show()

# #### MPLD3 TEST

# fig, ax = plt.subplots()

# for c in gu2.columns:
#     print(c)
#     ax.barh(gu2.index.to_list(), gu2[c].fillna(0).to_list(), label = c)
# plt.show()

# mpld3.save_html(fig,"test2.html")

import plotly.graph_objects as go

cols = []
# reorganize data for stacked bar chart
for c in gu2.columns:
    cols.append(go.Bar(name = c,
                       y=gu2.index.to_list(),
                       x=gu2[c].fillna(0).to_list(),
                       orientation='h'))
# create plot
fig = go.Figure(data=cols)
fig.update_layout(barmode='stack', height = 1000)
fig.write_html("restaurants_by_country_region.html")


## subplots by cuisine group

filt3 = (data["cuisine_group"] != "other") & (data["cuisine_group"] != "none") & (data["cuisine_group"] != "America, Northern")
data_filt2 = data.loc[filt3,:]
data_c = data_filt2.set_index(keys=["cuisine_group"])
data_c.sort_index(inplace=True)
groups = data_c.index.value_counts().sort_index()



#fig, ax = plt.subplot(num_groups,1)
fig, ax = plt.subplots(1, 1, figsize=(15,22))
plt.subplots_adjust(top=0.96, bottom=0.08)
plt.grid(b=True, which='both', axis='x', zorder=0)
for n,i in enumerate(groups.index):
    temp = data_c.loc[i,:]
    temp2 = temp.groupby("cuisine_new")["cuisine_new"].count()
    #temp3 = temp2.unstack()
    plt.barh(y=temp2.index, width=temp2, label = i, zorder=3)
    plt.xscale("log")
plt.legend()
plt.gca().invert_yaxis()
plt.title("Cuisines by Country and Region", fontweight="heavy", fontsize=12)
#plt.grid(b=True, which='both', axis='x', zorder=0)
#plt.show()
fig.savefig("cuisines_by_group")

### number of chain restaurants

data_full = pd.read_csv("all_restaurants_compiled_full_with_empty_cuisine.csv")
data_ff = pd.read_csv("all_restaurants_usa_overpass_fast_food_v1.csv")
data_ff.columns = ["id","name","cuisine","lat","lon","state"]
d2 = data_full.append(data_ff)

d2.to_csv("combined_restaurant_and_ff.csv")


d2 = d2[d2["name"] != "none"]
rs = d2.groupby("name")["name"].count().sort_values()
rsc = rs > 3

rm = pd.merge(d2, rsc, left_on="name", right_index=True)
rm.rename(columns={"name_y" : "is_chain"}, inplace=True) 

rg = rm.groupby(["state","is_chain"])["is_chain"].count()
rgu = rg.unstack()
#rgu.columns = rgu.columns.droplevel()
rgu["percent_chain"] = rgu[1]/(rgu[1] + rgu[0]) * 100


### most popular chain restaurant

counts = pd.DataFrame(d2.groupby(['state','name'])['name'].count())
counts.rename(columns = {"name" : "count"}, inplace = True)
counts.reset_index()
trans = counts.groupby(['state'])['count'].transform(max)
idx = trans == counts['count']
chains = counts[idx]


# clustering

filt3 = (data["cuisine_new"] != "other") & (data["cuisine_new"] != "none") 
data_filt3 = data.loc[filt3,:]
st = data_filt3.groupby("state")["state"].count()
#stb = st > 300

mg = pd.merge(data_filt3,st,left_on = "state", right_index = True)
mg.rename(columns = {"state_y" : "n_restaurants"}, inplace = True)
mg = mg[mg["n_restaurants"] > 300]

mg3 = mg.groupby(["state","cuisine_new"])["cuisine_new"].count()
mg_by_st = mg3 / st * 100
mg3u = mg_by_st.unstack()
mg4 = mg3u.dropna(axis = 'columns')
#data_filt3["st_filt"] = st

#sns.set(style="ticks")
#sns.pairplot(mg4)

kmeans = KMeans(n_clusters=4, random_state=0).fit(mg4)
mg4['class'] = kmeans.labels_
#sns.pairplot(mg4, hue="labels", size = 3)
#sns.set(font_scale = 1.6)
#sns.set(font_scale = 1.2)
sns.pairplot(mg4[["mexican","burger","pizza","bbq","italian","chinese","america","seafood","class"]], hue="class", size = 3)

centers = kmeans.cluster_centers_

fig, ax = plt.subplots(1,1, figsize = (8,5))
plt.subplots_adjust(bottom=0.16,top=0.9)
plt.grid(b=True, which='both', axis='x', zorder=0)
for a,line in enumerate(centers):
    plt.plot(mg4.columns[:19],line,linewidth = 3, label = "Class: " + str(a))
plt.xticks(rotation = 45, fontsize = 12)
plt.yticks(fontsize = 12)
plt.xlabel("Cuisine")
plt.ylabel("Class Center")
plt.title("Clustering Centers",  weight = "heavy")
plt.legend(fontsize = 12)
plt.show()

c_temp = pd.DataFrame(chains).reset_index()
m1 = pd.merge(rgu, c_temp, on = "state", how='left')
m2 = pd.merge(m1, mg4["class"], left_on = "state", right_index = True, how = 'left')

m2.to_csv("food_stats_output.csv")

# cuisine in rural vs metropolitan areas
# create map of cuisine areas and plot number of restaurants as numbers
# bar chart of cuisine types and countries (two levels)
# show distribution of cuisine types by state
# show distribution of american food by state (burger, hotdog, pizza, seafood,)
# mexican/ latin?
# asian
# european
# african
# latin
# variety
# clustering result (base clusters on continents)
# pizza, burger, etc...
# southern
# seafood
# vegetarian/vegan
# look at new england, classify areas



