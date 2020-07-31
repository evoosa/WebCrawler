import threading
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BS_PARSER = 'html.parser'
MAX_THREADS = 5
NOW = time.strftime("%Y%m%d-%H%M%S")


class WebCrawler(object):
    """ Retrieves links in a given website, alerts when a broken link is found, and reports it's depth """

    def __init__(self, root_url: str):
        self.root_url = root_url
        self.parsed_links = set()
        self.report_path = '.\\links_{}.txt'.format(NOW)
        self.broken_links_report = '.\\broken_links_{}.txt'.format(NOW)

    def get_links_from_url(self, url: str) -> set:
        """
        Get a list of URLs under a given URL.
        If a the URL is broken, write it in the broken links report.
        :param url: URL to get links from
        :return: all links found in the given URL
        """
        response = requests.get(url)
        if response.status_code == 404:
            with open(self.broken_links_report, 'a', encoding='utf-8') as broken_links_file:
                broken_links_file.write('\n' + url)
            return set()
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
            if link not in self.parsed_links:
                with open(self.report_path, 'a', encoding='utf-8') as report_file:
                    report_line = "depth: {0}, link: {1}".format(depth, link)
                    report_file.write("\n" + report_line)
                    print(report_line)
                new_report_thread = threading.Thread(target=self.get_links_report, args=(link, depth + 1))
                new_report_thread.start()
