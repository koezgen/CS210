import os, sys, glob, re
import json
from pprint import pprint
from html import unescape

import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
import uuid

from config import LINK_LIST_PATH

# Encoding for writing the URLs to the .txt file
# Do not change unless you are getting a UnicodeEncodeError
ENCODING = "utf-8"


def save_link(url, page):
    """
    Save collected link/url and page to the .txt file in LINK_LIST_PATH
    """
    id_str = uuid.uuid3(uuid.NAMESPACE_URL, url).hex
    with open(LINK_LIST_PATH, "a", encoding=ENCODING) as f:
        f.write("\t".join([id_str, url, str(page)]) + "\n")


def download_links_from_index():
    """
    This function should go to the defined "url" and download the news page links from all
    pages and save them into a .txt file.
    """

    # Checking if the link_list.txt file exists
    if not os.path.exists(LINK_LIST_PATH):
        with open(LINK_LIST_PATH, "w", encoding=ENCODING) as f:
            f.write("\t".join(["id", "url", "page"]) + "\n")
        start_page = 1
        downloaded_url_list = []

    # If some links have already been downloaded,
    # get the downloaded links and start page
    else:
        # Get the page to start from
        data = pd.read_csv(LINK_LIST_PATH, sep="\t")
        if data.shape[0] == 0:
            start_page = 1
            downloaded_url_list = []
        else:
            start_page = data["page"].fillna(0).astype("int").max()
            downloaded_url_list = data["url"].to_list()

    # WRITE YOUR CODE HERE
    #########################################
    # Start downloading from the page "start_page"
    # which is the page you ended at the last
    # time you ran the code (if you had an error and the code stopped)

    # There are 11 pages on the swedish government press releases webpage.
    for pagenum in range(start_page, 12):
        
        # I got this link from XHR/Fetch network activities and format it according to the loop variable. There is a .format(page) at the
        # End of this very long string.
        singlePage = 'https://www.government.se/Filter/GetFilteredItems?filterType=Taxonomy&filterByType=FilterablePageBase&preFilteredCategories=2033&preFilteredBlockCategories=&rootPageReference=0&isInEditMode=&page={}&pageSize=&displayLimited=True&fromDate=&toDate=&sortAlphabetically=False&filteredContentCategories=&filteredPoliticalLevelCategories=&filteredPoliticalAreaCategories=&filteredPublisherCategories=&searchText=&searchQuery='.format(pagenum)
        req = requests.get(singlePage)

        # Here, I get the request as string and load it as json.
        data = json.loads(req.text)

        # Take the "Message" key from the json and unescape it to get raw html text that can be
        # Parsed by Beautiful Soup.
        rawHTML = unescape(data["Message"])
        parsed_dom = bs(rawHTML)
        
        # Getting the respective div's and parse them accordingly.
        for item in parsed_dom.find_all("div", {"class": "sortcompact"}):

            # Save the collected url in the variable "collected_url"
            collected_url = "https://www.government.se" + item.find("a")["href"]

            # Save the page that the url is taken from in the variable "page"
            page = pagenum

            # The following code block saves the collected url and page
            # Save the collected urls one by one so that if an error occurs
            # you do not have to start all over again
            if collected_url not in downloaded_url_list:
                print("\t", collected_url, flush=True)
                save_link(collected_url, page)

    #########################################


if __name__ == "__main__":
    download_links_from_index()
