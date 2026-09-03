import os
import json

try:
    import requests
    from bs4 import BeautifulSoup as bs
    HAS_SCRAPING_DEPS = True
except ImportError:
    HAS_SCRAPING_DEPS = False



CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

FALLBACK_DICTIONARY = {
    "你好": ["nǐ hǎo", "greeting", "hello / hi"],
    "谢谢": ["xiè xie", "expression", "thank you / thanks"],
    "再见": ["zài jiàn", "expression", "goodbye / see you"],
    "中国": ["zhōng guó", "noun", "China"],
    "朋友": ["péng you", "noun", "friend"],
    "学习": ["xué xí", "verb", "to study / to learn"],
    "高兴": ["gāo xìng", "adjective", "happy / glad"],
    "老师": ["lǎo shī", "noun", "teacher"]
}

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "html_tag": "td",
        "url": "https://blog.lingodeer.com/chinese-hsk-1-vocabulary-list"
    }

def extract_data(url=None) -> str:
    if not HAS_SCRAPING_DEPS:
        raise ImportError("Scraping dependencies (requests, bs4) are missing.")
    cfg = load_config()
    target_url = url or cfg.get('url')
    response = requests.get(target_url, timeout=5)
    response.raise_for_status()
    return response.text


def transform_data(html_content=None):
    if html_content is None:
        html_content = extract_data()
    return bs(html_content, "html.parser")

def data_list(soup=None) -> list:
    cfg = load_config()
    if soup is None:
        soup = transform_data()
    new_char = soup.find_all(cfg.get('html_tag', 'td'))
    return [sino.get_text().strip() for sino in new_char]

def create_dictionary(datalist=None) -> dict:
    try:
        if datalist is None:
            datalist = data_list()
        if len(datalist) >= 4:
            sino_list = datalist[0::4]
            pinyin_list = datalist[1::4]
            role_list = datalist[2::4]
            def_list = datalist[3::4]
            res_dict = dict(zip(sino_list, zip(pinyin_list, role_list, def_list)))
            if res_dict:
                return res_dict
    except Exception:
        pass

    return FALLBACK_DICTIONARY