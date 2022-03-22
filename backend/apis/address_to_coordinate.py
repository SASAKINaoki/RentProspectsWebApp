import requests
import xmltodict
import config

def address_to_coordinate(location):

    #住所が存在しない場合の処理


    appid = config.yahoo_appid
    base_url = "https://map.yahooapis.jp/geocode/V1/geoCoder?appid={appid}&query={location}"
    req_url = base_url.replace("{appid}", appid)
    req_url = req_url.replace("{location}", str(location))
    r = requests.get(req_url)
    xml = r.content
    this_dict = xmltodict.parse(xml)
    try:
        lonlat = this_dict["YDF"]["Feature"][0]["Geometry"]["Coordinates"]
        lon, lat = lonlat.split(",")
        return lon,lat
    except KeyError:
        return None,None
    except requests.exceptions.ConnectionError:
        return None,None
    except TimeoutError:
        return None,None