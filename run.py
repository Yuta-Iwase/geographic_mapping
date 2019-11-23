import requests
import csv
import json
import xmltodict
import folium
from progressbar import progressbar 


zoom_start = 13
longitude_start = 35.681382
latitude_start = 139.76608399999998
csv_file_path = './example.csv'
output_file_path = './example.html'

folium_map = folium.Map(location=[longitude_start, latitude_start], zoom_start=zoom_start) #東京駅の緯度経度

with open('./ClientID.txt') as f:
    appid = f.read()

with open(csv_file_path) as f:
    reader = csv.reader(f)
    table = [row for row in reader]

API_URL = 'https://map.yahooapis.jp/geocode/V1/geoCoder'
popup_wrapper = ['<div style="width: 240px;">', '</div>']
label_wpapper = ['<span style="font-size: 120%; font-weight: bolder;">', '</span>']

error_address_list = []
for row in progressbar(table):
    for column in row:
        marker_label = row[0]
        address = row[1]
        discriptions = []
        i = 0
        for i in range(len(row)-2):
            discriptions.append(row[i+2])

    response = requests.get(API_URL,
                            params={
                                'appid': appid,
                                'query': address
                            })
    resp_xml = response.text
    resp_dict = xmltodict.parse(resp_xml)
    try:
        feature_list = resp_dict['YDF']['Feature']
        try:
            coord=resp_dict['YDF']['Feature']['Geometry']['Coordinates'].split(',')
        except:
            coord=resp_dict['YDF']['Feature'][0]['Geometry']['Coordinates'].split(',')
    except:
        error_address_list.append(address)
        continue
    (latitude, longitude) = (float(coord[0]), float(coord[1]))
    popup = popup_wrapper[0] + label_wpapper[0] + marker_label + label_wpapper[1] + '<br>'
    for disc in discriptions:
        popup = popup + disc + '<br>'
    popup = popup + popup_wrapper[1]
    folium.Marker([longitude, latitude], popup=popup, icon=folium.Icon(color='blue')).add_to(folium_map)
        
filename = './map.html'
folium_map.save(output_file_path)

with open('./error_address.txt', 'w') as f:
    for address in error_address_list:
        f.write(address)

print('complete. please open: ' + output_file_path)