import threading
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

import time

BS_PARSER = 'html.parser'
MAX_THREADS = 5


class WebCrawler(object):
    """ Retrieves links in a given website, alerts when a broken link is found, and reports it's depth """

    def __init__(self, root_url: str):
        self.root_url = root_url
        self.parsed_links = set()
        self.default_report_path = 'C:\\Temp\\links_report_{}.txt'.format(time.strftime("%Y%m%d-%H%M%S"))

    def get_links_from_url(self, url: str) -> set:
        """
        Get a list of URLs under a given URL
        :param url: URL to get links from
        :return: all links found in the given URL
        """
        response = requests.get(url)
        bs_obj = BeautifulSoup(response.content, BS_PARSER, from_encoding=response.encoding)
        return {urljoin(url, link['href']) for link in bs_obj.find_all(href=True)}

    def get_links_report(self, url: str, depth: int = 0) -> None:
        """
        Get a report of all links under a given website and their depth. check if they are broken
        :param url: URL of the website to get a report of
        :param depth: number of clicks from the root website to the current link
        """
        self.parsed_links.add(url)
        links_in_url = {link for link in self.get_links_from_url(url) if link.startswith(self.root_url)}
        for link in links_in_url:
            with open(self.default_report_path, 'a', encoding='utf-8') as report_file:
                report_file.write("\ndepth: {0}, link: {1}".format(depth, link))
                print("depth: {0} ,link: {1}".format(depth, link))
            if link not in self.parsed_links:
                new_report_thread = threading.Thread(target=self.get_links_report, args=(link, depth + 1))
                new_report_thread.start()
