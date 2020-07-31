import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


# TODO - conventions for tiud?
# TODO - handle exceptions better

class WebCrawler(object):
    """ Retrieves links in a given website, alerts when a broken link is found, and reports it's depth """

    def __init__(self, website_url: str):
        self.website_url = website_url
        self.bs_parser = 'html.parser'
        self.http_header = {'User-Agent': 'Chrome/35.0.1916.47'}
        pass

    def get_response_from_url(self, url: str) -> requests.Response: # TODO - might need a removal
        """
        Get an HTTP response form a given url
        :param url: URL to get a response from
        :return: the response from the given URL
        """
        return requests.get(url, headers=self.http_header)

    def get_links_from_url(self, url: str) -> set:
        """
        Get a list of URLs under a given URL
        :param url: URL to get links from
        :return: all links found in the given URL
        """
        response = self.get_response_from_url(url)
        soup = BeautifulSoup(response.content, self.bs_parser, from_encoding=response.encoding)
        return {urljoin(url, link['href']) for link in soup.find_all(href=True)}

    def check_if_link_is_broken(self) -> bool:
        """ Check if s link is broken """
        pass

    def main(self):
        """ Get a report of all links under a given website and their depth. check if they are broken """
        pass


if __name__ == '__main__':
    main_url = 'https://www.neave.com'
    wc = WebCrawler(main_url)
    print(wc.get_links_from_url(main_url))
