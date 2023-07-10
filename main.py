import requests
import xmltodict
import json
import math
import folium
from folium import plugins
import time
import threading

print('''
\x1b[2J \x1b[1;36m
  
  .oooooo.    .oooooo..o ooo        ooooo ooooo        
 d8P'  `Y8b  d8P'    `Y8 `88.       .888' `888'        
888      888 Y88bo.       888b     d'888   888         
888      888  `"Y8888o.   8 Y88. .P  888   888         
888      888      `"Y88b  8  `888'   888   888         
`88b    d88' oo     .d8P  8    Y     888   888       o 
 `Y8bood8P'  8""88888P'  o8o        o888o o888ooooood8 \x1b[1;32m      


              /------------------------\\
              ¡                        ¡
                  github.com/bear102   
              !                        !
              \\------------------------/\x1b[0m 
''')


print("""\x1b[1;94m 
      Welcome to Open Street Map Locator (OSML).\x1b[0m
""")

distance_threshold = float(input("""\x1b[1;95m
      Enter Distance threshold (kilometers): \x1b[38;5;122;4m"""))

SouthWest = input("""\x1b[0m\x1b[1;95m
      Enter South West corner coordinates (Lat, lon): \x1b[38;5;122;4m""")

NorthEast = input("""\x1b[0m\x1b[1;95m
      Enter North East corner coordinates (Lat, lon): \x1b[38;5;122;4m""")


searchLatLon = SouthWest + ","+ NorthEast

descriptors = []

print("""\x1b[0m\x1b[1;34m
          
        Please input your descriptors. 
        Key Example: brand, brand:wikidata, amenity, name

        Value Example: Wallmart, Q153417, pharmacy, CVS
          """)

while True:
 
    key = input("""\x1b[0m\x1b[1;95m
      Enter a key (Enter 0 to finish): \x1b[38;5;122;4m""")
    try:
      if int(key) == 0:
          break
    except:
        pass
    value = input("""\x1b[0m\x1b[1;95m
      Enter a value (Enter 0 to finish): \x1b[38;5;122;4m""")
    
    try:
      if int(value) == 0:
          break
    except:
        pass
    
    apd = f'["{key}"="{value}"]'

    descriptors.append(apd)

print('\x1b[0m')


frames = ['-', '\\', '|', '/']

animation_speed = 0.2
loading_done = False
# Function to perform the loading animation
def animate_loading():
    while not loading_done:
        for frame in frames:
            print(f'\r\t\t\033[1;34mLoading {frame}\t\t\t\033[0m', end='', flush=True)
            time.sleep(animation_speed)
            print('\r\t\t\033[1;30m', end='', flush=True)
            print('\t', end='', flush=True)
    print('\x1b[0m')



def calculate_distance(point1, point2):
    lat1, lon1 = point1
    lat2, lon2 = point2
    radius = 6371  
    lat_diff = math.radians(float(lat2) - float(lat1))
    lon_diff = math.radians(float(lon2) - float(lon1))
    a = math.sin(lat_diff / 2) ** 2 + math.cos(math.radians(float(lat1))) * math.cos(math.radians(float(lat2))) * math.sin(lon_diff / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance




def find_points_within_distance(coord_list, distance_threshold):
    result = []
    counter = 0

    sublist1 = coord_list[0]
    sublist2 = coord_list[1]
    for point1 in sublist1:
        for point2 in sublist2:
            combination = [point1, point2]
            
            # Calculate distances between each pair of points in the combination
            distances = [calculate_distance(combination[i], combination[j]) for i in range(len(combination)) for j in range(i+1, len(combination))]

            # Check if all distances are within the threshold
            if all(distance <= distance_threshold for distance in distances) and sorted(combination) not in result:
                counter += 1
                result.append(sorted(combination))

    return result, counter


def find_combinations(coord_list, distance_threshold):
    res, counter = find_points_within_distance([coord_list[0], coord_list[1]], distance_threshold)
    completeList = []
    for i in range (len(coord_list)-2):
        resA = [item[0] for item in res]
        resB = [item[1] for item in res]
        res1, counter = find_points_within_distance([resA, coord_list[i + 2]], distance_threshold=distance_threshold)

        for b in res1:
            if b[0] in resA:
                ind = resA.index(b[0])
                completeList.append([b[0],b[1],resB[ind]])
            if b[1] in resA:
                ind = resA.index(b[1])
                completeList.append([b[0],b[1],resB[ind]])

    if len(coord_list) ==2:
        completeList = res
        
    return completeList, counter




def main():
    overpass_url = "https://overpass-api.de/api/interpreter"


    allCoords = []
    for i in range(len(descriptors)):
        #minimum latitude, minimum longitude, maximum latitude, maximum longitude (or South-West-North-East) 
        query = f"""
        (
        node{descriptors[i]}({searchLatLon});
        way{descriptors[i]}({searchLatLon});
        relation{descriptors[i]}({searchLatLon});

        <;
        );
        out center;
        """

        payload = {"data": query}
        response = requests.post(overpass_url, data=payload)

        if response.status_code == 200:
            xml_data = response.text

            # Convert XML to JSON
            json_data = json.dumps(xmltodict.parse(xml_data))
            json_data = json.loads(json_data)

            coordsN = []
            if 'node' in json_data['osm']:
                if len(json_data['osm']['node']) != 4:
                    for node in json_data['osm']['node']:
                        coordsN.append([node['@lat'], node['@lon']])
                else:
                    coordsN.append([json_data['osm']['node']['@lat'],json_data['osm']['node']['@lon']])

            coordsW = []
            if 'way' in json_data['osm']:
                if len(json_data['osm']['way']) != 4:
                    for way in json_data['osm']['way']:
                        cen = way['center']
                        coordsW.append([cen['@lat'],cen['@lon']])
                else:
                    coordsW.append([json_data['osm']['way']['center']['@lat'],json_data['osm']['way']['center']['@lon']])

            coordsR = []
            if 'relation' in json_data['osm']:
                if len(json_data['osm']['relation']) != 4:
                    for relation in json_data['osm']['relation']:
                        cen = relation['center']
                        coordsR.append([cen['@lat'],cen['@lon']])
                else:
                    coordsR.append([json_data['osm']['relation']['center']['@lat'],json_data['osm']['relation']['center']['@lon']])

            coordsList = []
            for b in coordsN:
                coordsList.append(b)
            for b in coordsW:
                coordsList.append(b)
            for b in coordsR:
                coordsList.append(b)

            with open(f'coords{i}.txt', 'w')as f:
                f.write(str(coordsList))


            allCoords.append(coordsList)


        else:
            print("Try again later, Request failed with status code:", response.status_code)
            print(response)



    result, counter = find_combinations(allCoords, distance_threshold)

    global loading_done
    loading_done = True
    time.sleep(.5)
    if counter == 0:
        print(f"""
    \x1b[0m\x1b[38;5;196m\x1b[1m
    ********************************************
        
    0 Results Found
            
    try increasing the search distance or changing the bounding box coordinates or the locations may not exist on Open Street Map
        
    ********************************************
    \x1b[0m
    """)
        
    else:
        print(f"""
    \x1b[0m\x1b[38;5;46m\x1b[1m
    ********************************************
        
    {counter} Results Found!
    Map saved to map.html
            
    """)
    count = 0
    for sublist in result:
        print(f"\x1b[38;5;38m{count}. \x1b[38;5;46m\x1b[1m{sublist}\n")
        count +=1
    print('\x1b[0m')



    with open('confirmed.json', 'w') as f:
        json.dump(result, f, indent=2)




loading_thread = threading.Thread(target=animate_loading)
additional_task_thread = threading.Thread(target=main)

loading_thread.start()
additional_task_thread.start()

additional_task_thread.join()

print()

loading_thread.join()




# create map


with open("confirmed.json", 'r') as f:
    coord_list = json.load(f)


coord_list = [[[float(coord[0]), float(coord[1])] for coord in sublist] for sublist in coord_list]



map_object = folium.Map(location=[35.2405494, -106.6962442], zoom_start=14)

coordSpl = searchLatLon.split(',')

box_coordinates = [[float(coordSpl[0]), float(coordSpl[1])], [float(coordSpl[2]), float(coordSpl[3])]]

folium.Rectangle(
    bounds=box_coordinates,
    color='green',
    fill=True,
    fill_color='green',
    fill_opacity=0.1,
).add_to(map_object)


for sublist in coord_list:
    folium.PolyLine(sublist, color="blue", weight=2.5, opacity=1).add_to(map_object)

for sublist in coord_list:
    for point in sublist:
        folium.CircleMarker(point, radius=10, color='red', fill=True, fill_color='red').add_to(map_object)

draw = plugins.Draw(export=True)
draw.add_to(map_object)

map_object.save("map.html")

