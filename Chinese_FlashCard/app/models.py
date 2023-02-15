import json
import requests
from bs4 import BeautifulSoup as bs



with open("config.json") as f:
    cfg = json.load(f)

def extract_data(url=cfg['url']) -> str:
    """ make a get request on url
    return :: html document
    """
    return requests.get(url).text

def transform_data():
    """ parse html document
    return :: tree of Python object
    """
    return bs(extract_data(),"html.parser")
    

def data_list(soup=transform_data()) -> list:
    """ match tag with find_all method
    return :: string list
    """
    new_char = soup.find_all(cfg['html_tag'])
    return [sino.get_text() for sino in new_char ]

def create_dictionary(datalist=data_list()) -> dict:
    """ slice every 4 items
    return :: dict with sinograms as key
    """
    sino_list = datalist[0::4]
    pinyin_list =  datalist[1::4]
    role_list = datalist[2::4]
    def_list =  datalist[3::4]
    return dict(zip(sino_list,zip(pinyin_list,role_list,def_list)))