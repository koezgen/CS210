import os, sys, glob, re
import json
from pprint import pprint
from html import unescape

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid

# Global variables
SEHIRLER = ["Adana", "Adıyaman", "Afyon", "Ağrı", "Amasya", "Ankara", "Antalya", "Artvin", "Aydın", "Balıkesir", "Bilecik", "Bingöl", "Bitlis", "Bolu", "Burdur", "Bursa", "Çanakkale", "Çankırı", "Çorum", "Denizli", "Diyarbakır", "Edirne", "Elazığ", "Erzincan", "Erzurum", "Eskişehir", "Gaziantep", "Giresun", "Gümüşhane", "Hakkari", "Hatay", "Isparta", "İçel (Mersin)", "İstanbul", "İzmir", "Kars", "Kastamonu", "Kayseri", "Kırklareli", "Kırşehir", "Kocaeli", "Konya", "Kütahya", "Malatya", "Manisa", "Kahramanmaraş", "Mardin", "Muğla", "Muş", "Nevşehir", "Niğde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdağ", "Tokat", "Trabzon", "Tunceli", "Şanlıurfa", "Uşak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman", "Kırıkkale", "Batman", "Şırnak", "Bartın", "Ardahan", "Iğdır", "Yalova", "Karabük", "Kilis", "Osmaniye", "Düzce"]
LINK_LIST_PATH = "C:\\Repositories\\CS210\\Term_Project\\data\\MV_List"
ENCODING = "utf-8"

def save_link(mv_link, mv_name, party, city):
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([mv_link, mv_name, party, city]) + "\n")

def download_links_from_index():
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["MV_LINK", "MV_NAME", "MV_PARTY", "MV_CITY"]) + "\n")
        downloaded_url_list = []

    else:
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            downloaded_url_list = []
        else:
            downloaded_url_list = data["MV_LINK"].to_list()

    for i in range(0, 81):

        singlePage = "https://www.tbmm.gov.tr/milletvekili/liste#{}-{}".format(SEHIRLER[i], f"{i:02}")
        page = requests.get(singlePage)
        parsed_dom = bs(page.text, 'html.parser')

        for item in parsed_dom.find_all("div", {"class": "card"}):

            # TODO Duzgun bir şekilde token string'i parse edebilmeli
            onclick_element = item.attrs.get('onclick', '')
            token = onclick_element[onclick_element.find("('") + 2:onclick_element.find("')")]

            collected_MV_link = "https://www.tbmm.gov.tr/milletvekili/milletvekilidetay?Id=" + token
            
            card_body = item.find("div", {"class": "card-body"})
            collected_MV_name = card_body.find("p", {"class": "milletvekili-isim"}).text.strip()
            political_affiliation = card_body.find("p", {"class": "parti-isim"}).text.strip()

            if collected_MV_link not in downloaded_url_list:
                save_link(collected_MV_link, collected_MV_name, political_affiliation, SEHIRLER[i])

if __name__ == "__main__":
    download_links_from_index()