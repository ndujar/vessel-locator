#module import
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime


def get_ships(imo_list):
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    items = []
    for IMO in imo_list:
        print(IMO)
        url = r'https://www.vesselfinder.com/en/vessels/VOS-TRAVELLER-IMO-' + str(IMO)
        req = urllib.request.Request(url, None, hdr)
        with urllib.request.urlopen(req) as response:
            the_page = response.read()
        parsed_html = BeautifulSoup(the_page, features="lxml")
        tables = parsed_html.findAll("table")
        coords = "0,0"

        for table in tables:
            if table.findParent("table") is None:
                for row in table.findAll('tr'):
                    aux = row.findAll('td')
                    
                    try:
                        if aux[0].string == "Coordinates":
                            coords = aux[1].string
                        if aux[0].string == "Vessel Name":
                            name = aux[1].string
                        if aux[0].string == "Position received":
                            print(aux[1].get("data-title"))
                            time = datetime.strptime(aux[1].get("data-title"), '%b %d, %Y %H:%M %Z')
                            print(time)
                    except: 
                        print("strange table found")
        lat = parsed_html.find('div', class_ = "coordinate lat").string
        lng = parsed_html.find('div', class_ = "coordinate lon").string
        # name = parsed_html.find('td', class_ = "title").string
        # time = parsed_html.find('td', class_ = 'v3 ttt1 valm0').string
        coordsSplit = coords.split("/")
        # def dms2dd(degrees,direction):
        #     dd = float(degrees) ;
        #     if direction == 'S' or direction == 'W':
        #         dd *= -1
        #     return dd
        # def parse_dms(dms):
        #     parts = re.split(' ', dms)
        #     lat = dms2dd(parts[0], parts[1])
        #     return lat
        # lat = parse_dms(coordsSplit[0])
        # lng = parse_dms(coordsSplit[1])
        items.append((lat, lng, name, time))
    return items
