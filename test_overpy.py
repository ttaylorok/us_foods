import overpy
api = overpy.Overpass()
r = api.query("""
[out:json][timeout:25];
// gather results
(
  // query part for: “bar”
  area[name="Oklahoma"];
  nwr["amenity"="restaurant"](area);
);
// print results
out body;
>;
out skel qt;
""")


for x in r.nodes:
    print(x)