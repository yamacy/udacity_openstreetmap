# Udacity OpenStreetMap Data Case Study
## Map Area

Istanbul, Turkey

This data is of my hometown. In this project we will investigate Istanbul Metro Extracts data from MapZen. You can download it from:

- https://mapzen.com/data/metro-extracts/metro/istanbul_turkey/ or
- https://www.openstreetmap.org/export#map=9/41.2017/28.9648 

## Data Auditing

Before submitting data to the database, i  first need to investigate data if there is any problem in it. So i did it, in the <a href="https://github.com/yamacyilmaz-koczer/udacity_openstreetmap/blob/master/Udacity_OpenStreetMap_DataAuditing.html">data auditing</a> file.


## Problems Encountered In The Map
In the data auditing process i saw there were errors in street names seen in the following:
- Incorrect k values for the tag elements ("Lima Emlak 2", "Sisli", "payment:\u0130stanbulkart", "yap\u0131", "\u03c0\u03b5\u03c1\u03b9\u03bf\u03c7\u03b7", "fixme", and "FIXME")
- Overabbreviated street names (“14 sk.”, "Mete sok")
- Incorrect street names("Eminönü")
- Incorrect city names ("", "", "", etc.)

## Incorrect k values for the tag elements


'''
streetname_mappings = { 
    "Sokak": ["Sk.","sk.", "Sk", "sk", "Sok", "sok", "Sok.", "sok."],
    "Caddesi": ["Cadessi", " cadessi", "Cad.", "cad.", "Cd.", "cd.", "Cad", "cad", "Cd", "cd"],
    "Mahallesi": ["Mah.", "mah.", "Mh.", "mh.", "Mah", "mah", "Mh", "mh"],
    "Bulvar\u0131": ["Bulv.", "bulv.", "Bulv", "bulv"],
    "Apartman\u0131": ["Apt.", "apt.", "Apt", "apt"]
}

def update_streetname(street_name, mappings):
    for prop in mappings:
        for val in mappings[prop]:
            parts = street_name.split(" ")
            
            for part in parts:
                if part == val:
                    street_name = street_name.replace(val, prop)
                    break
                    
    return street_name
'''

## Data Overview and Additional Ideas
### File Sizes

```
İstanbul_turkey.osm ..... 242 MB
İstanbul_turkey.db ........ 130 MB
nodes.csv ............... 2,36 MB
nodes_tags.csv ......... 27,8 MB
ways.csv ............... 11,1 MB
ways_tags.csv ........... 35,6 MB
ways_nodes.cv .......... 10,6 MB 
```

### Number Of Nodes

```
sqlite> select count(*) from nodes;

1165055
```

### Number Of Ways

```
sqlite> select count(*) from ways;

192639
```

### Number of unique users

```
sqlite> select count(distinct(a.uid))
from (select uid from nodes union all select uid from ways) a;

2333
```
### Top 10 contributing users

```
sqlite> select a.user, count(*) as counter
from (select user from nodes union all select user from ways) a
group by a.user
order by counter desc
limit 10;

Nesim,99994
bigalxyz123,86289
Cicerone,63380
Ckurdoglu,49328
katpatuka,49093
JeLuF,48538
EC95,38399
canTurgay,36459
Sakthi20,27504
turankaya74,25341
```

### Number of users appearing only once (having 1 post)

```
sqlite> select count(*) 
from (select a.user, count(*) as counter
     from (select user from nodes union all select user from ways) a
     group by a.user
     having counter = 1) u;

640
```

### Top 10 appearing amenities

```
sqlite> select value, count(*) as counter
from nodes_tags
where key='amenity'
group by value
order by counter desc
limit 10;

pharmacy,2440
restaurant,853
cafe,736
bank,493
fuel,319
fast_food,291
parking,263
atm,257
place_of_worship,220
school,172
```

## 3 Top 10 cuisines

```
sqlite> select nodes_tags.value, count(*) as counter
from nodes_tags 
    join (select distinct(id) from nodes_tags where value='restaurant') i
    on nodes_tags.id=i.id 
where nodes_tags.key='cuisine' 
group by nodes_tags.value 
order by counter desc 
limit 10;

turkish,95
kebab,27
regional,26
pizza,12
seafood,10
fish,8
international,7
italian,6
local,6
burger,5
```

## Additional Ideas
### Number of pharmacies, and parking areas
It is very interesting for a city to become famous with its pharmacies, isn't it? The number of pharmacies is top 1 in the list, it is true or is there a problem? Should we think that Turkish people isn't healthy? Maybe. Or Turkish people loves taking drugs? The right answer isn't important for now, the important thing is that the number of pharmacies is relatively very high.

Let's say that most of hospitals are far from the map area or hospitals are really very big and much more pharmacies are needed. But still pharmacies are in the map area, but hospitals are not, it is supposed to be closer to each other. 

On the other hand in Turkey, drugs are sold only in pharmacies, not in supermarkets or malls. Because of this, pharmacies may have a high rate but still, its position in the list is very significant.

It seems there is a problem.

Also, parking areas are very less. Compared to restaurants, cafes, and fast food areas, parking areas are very poor. Anyone living in Istanbul already knows this.

### Dominant Turkish Cuisine
In the Top 10 Cuisines list, Turkish title has a very high rate. But we need to know more about the scope of this title, because i don't see "doner" despite its popularity, Turkish title may include doner or the second title "kebap" may include or mean doner. So we need to make it clear. This is important because doner or kebap are both like fast food. And this may point health problems to us like obesity, or heart attacks. In the above, i tried to pay attention to the number of pharmacies. But i assume that Turkish title doesn't include doner and kebap title include doner.

I think this list shows us Turkish people has a strong taste, so they are very selective and conservative about foods.  

# Conclusion
This project as a beginning in python was really cool. And investigating my hometown was also good. This data shows us some improvements about data are necessary. Data that is unclear will not be effective, we see that in the top 10 cuisines list. On the other hand in the amenities list pharmacies indicates a question to be answered. In the last few years Turkish goverments tries to decrease taking drugs especially antibiotics. The next question is much more important. If this is the pointer of consuming drugs so much, then why?


