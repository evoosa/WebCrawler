from web_crawler import WebCrawler

if __name__ == '__main__':
    website_url = 'https://www.guardicore.com'
    wc = WebCrawler(website_url)
    wc.get_links_report(website_url)
