<p align="center">
  <img src="https://github.com/bear102/osml/blob/main/img/osml.png" alt="OSML Logo">
</p>

<p align="center">
  <a href="https://github.com/bear102/tennis"><img src="https://img.shields.io/badge/GitHub-bear102-%2312100E.svg?style=flat&logo=github" alt="GitHub"></a>
  <img src="https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9-blue" alt="Python">
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License"></a>
</p>

<p align="center">
  Open Street Map data mining project. 
</p>






# Overview

Open Street Map Locator (OSML) was designed to find the coordinates of where a picture or video was taken by analyzing the surroundings. For example, if there are a CVS, McDonald's, and Walmart in close proximity, OSML can narrow down the possible locations to just a few.


# Installation and Setup


1. Make sure you have python >=3.7 installed

2. Download the files in this repository

3. Pip install these 3 libraries in cmd prompt
```
pip install requests
pip install xmltodict
pip install folium
```



# Usage

Example Scenario:

Ok lets say someone were to post this photo on social media. We can easily make out a mcdonalds, starbucks, and popeyes close together.

<img src="https://github.com/bear102/osml/blob/main/img/Screenshot%202023-07-09%20173920.png" alt="Mcdonalds, Wendys, and Starbucks"></img>

<br>

***

<br>


Step 1. **Get approximate distance** 

These 3 stores are no more than .2 kilometers apart from eachother
<br>
***
<br>

Step 2. **Initial guess**

  We need two coordinates of a rectangle that   we want the program to search in. If you already have a general idea of where the location is you can use that. If you   do not you can use the entire world or an entire country.
  
  I Know my location is somewhere in Texas
  I need the South-West corner and the North-East corner's lat and lon
  
  SW: 26.292681, -106.582503
  
  NE: 36.508981, -93.003398
  
<br>

***

<br>

Step 3. **Finding descriptors** 

For this step, go to `openstreetmap.org`

in the search bar, type in *popeyes*. Find any popeyes and click on it. This will bring up a table of information labled `Tags`

<img src="https://github.com/bear102/osml/blob/main/img/Screenshot%202023-07-09%20174925.png" alt="Descriptors of Popeyes"></img>

Choose a few tags that may be relevant to popeyes, some strong ones include:
1. brand
2. brand:wikidata
3. name
(if you are trying to locate based on other features like a water tower or a bridge, choose the tags relevant to that feature)

The left column will be your `key` and the right column will be your `value`

repeat this step for the three locations (mcd, popeyes, starbucks)

    here are my descriptors:
    McDonalds - brand:wikidata = Q38076
    Starbucks - brand:wikidata = Q37158
    Popeyes - brand:wikidata = Q1330910

<br>

***

<br>

Step 4. **Run main.py** Run the python script and follow the instructions ?imageHere

<br>

Step 5. **interpret output** If you see green and results found, that means it found potential locations. 

You can open map.html by double clicking the file and view the locations on a map

**If you see no results found**, that may mean these locations mcdonalds, popeyes, and starbucks, are missing on openstreetmap.


Step 6. **Reading Map** The results are saved to a file named confirmed.json. the files named coords<#>.txt are the coordinates found for individual locations (Mcd, popeyes, starbucks)

Open map.html

The area highlighted in green is the area that the code searched in.

Now look through all the points to see if the mcdonalds, wendys, and starbucks are positioned correctly

Tips:
1. look at the roads or how the buildings are aligned

2. if you find a potential location, click the pin icon in your upper left corner, drop a pin on the location, and click on the pin. This will show the coordinates and you can put that into google maps street view.

3. to mark already visited locations, use a pin
   

?imageHere




# License

MIT
