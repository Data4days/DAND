
# OpenStreetMap Data Case Study

By: Adam Friedman

March 2017

### Map Area

Johannesburg, South Africa
http://www.openstreetmap.org/export#map=11/-26.2044/28.0495

Downloaded from: https://mapzen.com/data/metro-extracts/

I chose Johannesburg because it's where I currently live. I'm interested to see how much of it is captured on OpenStreetMap and what can be revealed with SQL.


After creating a sample of the total dataset using sample.py (about 7% of the whole dataset), I used audit.py to find the most common irregularities with the street names and postal codes in the data. The most common problem seemed to be abbreviated street types e.g RD, St, Ext., Ave. There were also streets where the street types were in Afrikaans. All postcodes in the sample conformed to the 4 digit format used in South Africa. I then applied the audit to the entire data set and found instances of postcodes with only 3 digits. Enquiry into the addresses showed that these numbers were missing a zero at the beginning.

To correct the street names, I used the following function from audit.py


```python
def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            if street_type in mapping.keys():
                name = re.sub(street_type_re, mapping[street_type], name)

    return name
```

This function mapped the incorrect street types to their corrected versions . This fixed most of the inconsistencies. To correct the postcode, a leading zero was added.

I was pleasantly surprised to see that Johannesburg's OpenStreetMap data is quite clean, with most street names presented in full and most postcodes in the correct format.

# Data Overview

-----------

This sections contains information about the Johannesburg OpenStreetMap dataset and the SQL queries used to obtain the information

#### File Sizes

    johannesburg.osm   149 MB
    openstreet.db      110 MB
    nodes.csv          56 MB
    nodes_tags.csv     3 MB
    ways.csv           6 MB
    ways_nodes.csv     20 MB 
    ways_tags.csv      8 MB
    

#### Number of nodes

sqlite> SELECT COUNT(\*) FROM nodes;

679 630


#### Number of ways

    sqlite> SELECT COUNT(\*) FROM ways;

    109 370


#### Number of unique users

    sqlite> SELECT COUNT(DISTINCT(e.uid))          
    FROM (SELECT uid FROM nodes UNION ALL SELECT uid FROM ways) e;

    1 100

#### Top 10 contributing users

    sqlite> SELECT e.user, COUNT(\*) as num
    FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
    GROUP BY e.user
    ORDER BY num DESC
    LIMIT 10;

    Ido Marom     65 197
    Firefishy     60 174
    thomasF       42 159
    Adrian Frith  40 980
    NicRoets      30 056
    Tinshack      28 753
    Markus59      26 858
    Pa Deef       25 977
    Gerhardus
    Geldenhuis    18 918
    titanbeos     16 966

#### Number of users appearing only once (having 1 post)

    sqlite> SELECT COUNT(\*) 
    FROM
        (SELECT e.user, COUNT(*) as num
         FROM (SELECT user FROM nodes UNION ALL SELECT user FROM ways) e
         GROUP BY e.user
         HAVING num=1)  u;

    223
     


#### Top 10 appearing amenities

    sqlite> SELECT value, COUNT(*) as num
    FROM nodes_tags
    WHERE key='amenity'
    GROUP BY value
    ORDER BY num DESC
    LIMIT 10;


    restaurant        546
    fuel              485
    fast_food         390
    school            201
    place of worship  182
    parking           178
    atm               175
    bank              155
    cafe              137
    pharmacy          111


#### Most represented fast food chains

    sqlite> SELECT nodes_tags.value, COUNT(*) as num
    FROM nodes_tags 
        JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='fast_food') i
        ON nodes_tags.id=i.id
    WHERE nodes_tags.key='name'
    GROUP BY nodes_tags.value
    ORDER BY num DESC
    LIMIT 10;

    McDonald's     33
    Wimpy          30
    Fishaways      10
    Scooters       10
    Debonairs      9
    Nandos         9
    London Pie     7
    Anat           6


#### Most represented fuel stations

    sqlite> SELECT nodes_tags.value, COUNT(*) as num
    FROM nodes_tags 
        JOIN (SELECT DISTINCT(id) FROM nodes_tags WHERE value='fuel') i
        ON nodes_tags.id=i.id
    WHERE nodes_tags.key='name'
    GROUP BY nodes_tags.value
    ORDER BY num DESC
    LIMIT 5;

    Engen      79
    BP         39
    Total      34
    Caltex     32
    Shell      31



## Conclusion

From the beginning of this exercise I've suspected that the OpenStreetMap data for Johannesburg is very much incomplete due to the size of the .osm file (only 149 MB). After conducting further analysis, I'm still of this opinion. The easiest way to identify this is to look at the top 10 most represented food chains. It's easy to see that the numbers for those chains look too low and there are a few major players missing (e.g. Steers).

Looking at the top users, the top 10 users are responsible for about 42% of the data. The amount of data each of them have uploaded suggests that they are using some kind of automated GPS gathering techniques. With the help of processes like those found in audit.py and data.py, it would certainly be possible for someone to use a GPS processor and upload a significant amount of Johannesburg's information.

The low number of users (1100) is an extremely small percentage of the Johannesburg population. This suggests that people either don't know about OpenStreetMap, don't know how to load information or don't care to load information. A way to improve the amount of quality data is to launch a campaign to educate businesses about the benefits of loading their information on OpenStreetMap as well as a step by step guide on how to load it. There might be some issues where non tech-savvy users upload the information incorrectly, but it should lead to a vastly improved set of data on the city.



```python

```
