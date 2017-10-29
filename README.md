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
- Overabbreviated street names (“sk.”, "cd.", "mh.", etc.)
- Incorrect street names("Eminönü")
- Incorrect and missing city names ("Istambul", "İstanbuş", "Üsküdar", etc.)

## Overabbreviated street names
At the auditing the data stage, I realized that a lot of street names were not standard and overabbreviated. So, i use the following method to standardize them:
```
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
```

## Incorrect and missing city names
For the addr:city k values, there are more problems than one. Some values are not city names, instead they are county names like Esenler. Some are street names, some are city names. So I decided to change values into ones that last word is city name.

```
correction_mappings = {
    " ": ["/", ",", "\\", "-", "(AVR)", "Europe", "Türkiye"],
    "İstanbul": ["istanbul", "Istanbul", "İSTANBUL", "iSTANBUL", "İstanbbul", "Istambul", "ISTANBUL", "(İstanbul)", "İstanbuş"],
    "Şişli": ["Sisli", "Şişi"],
    "Kocaeli": ["KOCAELİ"],
    "Bayrampaşa": ["BAYRAMPAŞA"],
    "Pendik": ["pendik"],
    "Beylikdüzü": ["beylikdüzü"],
    "Sultanbeyli": ["sultanbeyli"],
    "Şekerpınar Köyü Çayırova": ["Şekerpinar Köyü"]
}

city_mappings = {
    "İstanbul": ["Heybeliada","Sancaktepe","Bayrampaşa","Eyüp","Kağıthane","Beşiktaş","Başakşehir","Maltepe","Zeytinburnu","Kartal","Topkapı","Beyoğlu","Üsküdar","Bakırköy","Kavacık","Büyükada","Sarıyer","Ataşehir","Esenyurt","Kadıköy","Avcılar","Rumeli","Beylikdüzü","Sultanahmet","Pendik","Şile","Tuzla","Kilyat","Kumburgaz","Sultanbeyli","Taksim","Çekmeköy", "Şişli", "Balat", "Yenibosna"],
    "Kocaeli": ["Gebze", "Çayırova", "Dilovası", "Darıca"]
}
    
def update_cityname(city_name, mappings):
    tempValue = city_name
    
    for correction in correction_mappings:
        for mapping in correction_mappings[correction]:
            tempValue = tempValue.replace(mapping, correction);

    parts = tempValue.split(" ")
    city = ""

    for part in parts:
        if (part.strip() != ""):
            if (city != ""):
                city = city + " "

            city = city + part.strip()

    parts = city.split(" ")
    
    if parts[len(parts) - 1] not in ["İstanbul", "Kocaeli"]:
        mapping = ""

        for city_mapping in city_mappings:
            if parts[len(parts) - 1] in city_mappings[city_mapping]:
                mapping = city_mapping

        if mapping != "" :
            parts[len(parts) - 1] = parts[len(parts) - 1] + " " + mapping
        else:
            if parts[len(parts) - 1] == "İstanbu":
                parts[len(parts) - 1] = "İstanbul"
            else:
                parts[len(parts) - 1] = parts[len(parts) - 1] + " İstanbul"

    city_name = " ".join(parts)
    return city_name
```

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
## Incorrect k values for the tag elements
I saw that there are few k values for the tag element like 'Lima Emlak 2' and 'Design Office'  that include spaces and wierd values like u'yap\u0131'. k values for the tag elements has speacial importance and must be standart as much as possible. So, I think there must be some restrictions on these values, for example 'no space' or 'no non-standart characters', because highly non-standart values may prevent us from interpreting data correctly.


# Conclusion
This project as a beginning in python was really cool. And investigating my hometown was also good. This data shows us some improvements about data are necessary. Data that is unclear will not be effective, we see that in the top 10 cuisines list. On the other hand in the amenities list pharmacies indicates a question to be answered. In the last few years Turkish goverments tries to decrease taking drugs especially antibiotics. The next question is much more important. If this is the pointer of consuming drugs so much, then why?


