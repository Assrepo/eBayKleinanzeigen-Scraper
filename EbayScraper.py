# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from progress.bar import Bar
from category import category_dict
from config import DEBUG
import json


class EbayScraper(object):

    def __init__(self, location, job):
        """
        Initialize by setting location, the job's parameters and the already viewed offers
        :param location: str
        :param job: dict
        """

        self.agent = {
            "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
        self.location = self.get_location_id(location)
        self.category = category_dict.get(job.get('Category', ""), "")
        self.mode = job.get('Mode')
        self.price = job.get('Max_price')
        self.vb = job.get('Include_VB')
        self.search_for = job.get('Search_for', "")
        self.filters = job.get('Filters')
        self.path = "viewed_offers.json"

        with open(self.path, "r", encoding='utf8') as file:
            self.viewed_offers = json.load(file)
        self.content = list()

    def get_job_hash(self):
        """
        Converts the job arguments into a unique string that is used for storing the last viewed offer for this job
        :return: str
        """

        return f"{self.category or 'None'}-{self.mode}-{self.price}-{self.vb}-{self.search_for}-{self.filters}"

    def get_location_id(self, location):
        """
        Finds the id of the location via json query
        :param location: string
        :return: None
        """
        url = 'https://www.ebay-kleinanzeigen.de/s-ort-empfehlungen.json?query=' + location
        location_dict = requests.get(url, headers=self.agent).json()
        if location_dict:
            location_id = next(iter(location_dict))
            print('Using location', location_dict[location_id])
            return location_id.replace('_', 'l')
        else:
            print('Location could not be found, please try fewer arguments')
            print('Using "Dresden - Sachsen" as location instead')
            return 'l3820'

    def build_url_everything(self, page=0):
        """
        Builds the desired url depending on the page number for mode 'Everything'
        :param page: int
        :return: str
        """

        if self.price == 0:
            return "https://www.ebay-kleinanzeigen.de/sortierung:preis/" \
                   + ("seite:" + str(page + 1) + "/") * (page > 0) \
                   + self.category + self.location
        else:
            return "https://www.ebay-kleinanzeigen.de/" \
                   + "preis::" + self.price + "/" \
                   + ("seite:" + str(page + 1) + "/") * (page > 0) \
                   + self.category + self.location

    def build_url_specific(self, page=0):
        """
        Builds the desired url depending on the page number for mode 'Specific'
        :param page: int
        :return: str
        """

        if self.price == 0:
            return "https://www.ebay-kleinanzeigen.de/sortierung:preis/" \
                   + ("seite:" + str(page + 1) + "/") * (page > 0) \
                   + self.search_for + "/k0" + self.location
        else:
            return "https://www.ebay-kleinanzeigen.de/" \
                   + "preis::" + str(self.price) + "/" \
                   + ("seite:" + str(page + 1) + "/") * (page > 0) \
                   + self.search_for + "/k0" + self.location

    def get_page_content(self, page=0):
        """
        Requests data from the internet and returns the raw site as response
        :param page: int
        :return: str
        """

        if self.mode == 'Everything':
            url = self.build_url_everything(page)
        else:
            url = self.build_url_specific(page)
        response = requests.get(url, headers=self.agent)

        if response.history:
            return ""

        return response.content

    def extract_page_content(self, data_raw):
        """
        Gets the information from all items in the given data string.
        Stops if the current offer was either visited already or is marked as 'VB'
        :param data_raw: str
        :return: boolean
            Whether the operation was successful or not
        """
        data = BeautifulSoup(data_raw, 'html.parser')
        adtable = data.find('ul', attrs={'id': 'srchrslt-adtable'})
        if not adtable:
            if DEBUG:
                print('***DEBUG*** Adtable not found ~ Maybe there are no more sites to look at?')
            return False
        # Adds do not have class lazyload-item
        items = adtable.findChildren("li", recursive=False, attrs={'class': 'ad-listitem lazyload-item'})
        bar = Bar('Processing', max=len(items))
        for item in items:
            bar.next()
            article = item.find("article")
            if article:
                time_div = article.find('div', attrs={'class': 'aditem-main--top--right'})
                # Should be depreciated now, removing if other add filtering works
                """if addon.find('a'):
                    if DEBUG:
                        print('***DEBUG*** Ignored because of the existence of a link ~ Probably an ad')
                    continue"""
                time = time_div.text.strip('\n ')  # String look like '\n 13.08.2021'
                main = article.find('div', attrs={'class': 'aditem-main'})
                anchor = main.find('h2').find('a')
                link = "https://www.ebay-kleinanzeigen.de" + anchor['href']
                item_id = link.split('/')[-1].split('-')[0]
                if self.viewed_offers.get(self.get_job_hash()):
                    if self.viewed_offers.get(self.get_job_hash()) >= item_id:
                        if DEBUG:
                            print('***DEBUG*** Already seen offer {} ... exiting ...'.format(item_id))
                        bar.finish()
                        return False

                """if item_id in self.viewed_offers:
                    self.file.close()
                    if DEBUG:
                        print('***DEBUG*** Already seen offer {} ... exiting ...'.format(item_id))
                    bar.finish()
                    return False
                else:
                    self.file.write(item_id + '\n')
                    self.viewed_offers.append(item_id)"""
                title = anchor.text
                description = main.find('p', attrs={'class': 'aditem-main--middle--description'}).text
                for filtered_word in self.filters:
                    if filtered_word.upper() in title.upper() or filtered_word.upper() in description.upper():
                        if DEBUG:
                            print('***DEBUG*** Filtered offer with title: ' + title)
                        break
                else:
                    details = article.find('div', attrs={'class': 'aditem-main--top--left'})
                    plz = details.text.split()[0]
                    ort = " ".join(details.text.split()[1:])
                    image = article.find('div', attrs={'class': 'aditem-image'}).find('div')
                    if image.has_attr('data-imgsrc'):
                        source = image['data-imgsrc'] or ""
                    else:
                        source = ""
                    price = article.find('p', attrs={'class': 'aditem-main--middle--price'}).text.lstrip()
                    if price == "VB":
                        if self.price == 0:
                            if DEBUG:
                                print('***DEBUG*** Price is VB but I am only looking for free offers ... exiting ...')
                            bar.finish()
                            return False
                        if not self.vb:
                            if DEBUG:
                                print('***DEBUG*** Price is VB ~ Offer will be skipped')
                            continue
                    if " VB" in price:
                        number = price[:-5]
                    else:
                        number = price[:-2]
                    if number.isnumeric():
                        if int(number) > self.price:
                            if DEBUG:
                                print('***DEBUG*** Offer is too expensive at {} '
                                      '(Max price is {})'.format(price, self.price))
                            continue

                    item_details = dict()
                    item_details['src'] = source
                    item_details['link'] = link
                    item_details['title'] = title
                    item_details['description'] = description
                    item_details['plz'] = plz
                    item_details['ort'] = ort
                    item_details['price'] = price
                    item_details['time'] = time
                    item_details['id'] = item_id
                    self.content.append(item_details)
        bar.finish()
        return True

    def get_items(self):
        """
        Main loop.
        Iterates over the offer pages and gets item if they are new
        :return: list
            List containing details of all new items found
        """
        i = 0
        while True:
            print("Searching for new offers on page %u..." % (i + 1))
            data = self.get_page_content(i)
            if not data:  # If there is no page i then get_page_content will return ""
                break
            if not self.extract_page_content(data):
                break
            i += 1

        if self.content:
            self.viewed_offers[self.get_job_hash()] = self.content[0]['id']
            with open(self.path, "w", encoding='utf8') as file:
                json.dump(self.viewed_offers, file)

        return self.content
