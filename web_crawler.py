
# TODO - conventions for tiud?

class webCrawler(object):
    """ Retrieves links in a given website, alerts when a broken link is found, and reports it's depth """
    def __init__(self, website_url: str):
        self.website_url = website_url
        pass

    def get_links_from_url(self) -> set:
        """ Get a list of URLs under a given URL """
        pass

    def check_if_link_is_broken(self) -> bool:
        """ Check if s link is broken """
        pass

    def main(self):
        """ Get a report of all links under a given website and their depth. check if they are broken """
        pass