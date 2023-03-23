import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Crawler:
    def __init__(self, max_pages, urls=[]):
        self.max_pages=max_pages
        self.urls_to_visit=urls
        self.visited_urls=[]

    def valid_url(self, url):
        r=requests.get(url)
        if r.status_code==200:
            soup=BeautifulSoup(r.content, "html.parser")
            return soup
        else:
            print(f"Erreur {r.status_code}")
            return None

    def domaine(self,url):
        domaine=re.search(r"w?[a-v|x-z][\w%\+-\.]+\.(org|fr|com|net)", url)
        domaine_site=domaine.group()
        return domaine_site

    def get_internal_urls(self, url):
        html=self.valid_url(url)
        domaine_site=self.domaine(url)
        for link in html.find_all('a'):
            if 'href' in link.attrs:
                if domaine_site in link.attrs['href']:
                    if "http" in link.attrs['href']:
                        internal_link=link.attrs["href"]
                        self.add_urls_to_visit(internal_link)
                else:
                    if link.attrs['href'].startswith('/'):
                        internal_link=urljoin(url,link.attrs["href"])
                        if domaine_site in internal_link:
                            self.add_urls_to_visit(internal_link)

    def add_urls_to_visit(self,internal_link):
        if internal_link not in self.urls_to_visit and internal_link not in self.visited_urls:
            self.urls_to_visit.append(internal_link)

    def run(self):
        while self.urls_to_visit and len(self.visited_urls) < self.max_pages:
            url=self.urls_to_visit[0]
            print(f"On crawle {url}")
            try:
                self.get_internal_urls(url)
                self.visited_urls.append(url)
            except AttributeError:
                print("On ne peut pas crawler cette url.")
            finally:
                self.urls_to_visit.pop(0)
        print(self.urls_to_visit)
        print(self.visited_urls)
        print(f"On a crawlé {len(self.visited_urls)} urls")

Crawler(max_pages=100, urls=["http://nsimonge.atwebpages.com/index.php"]).run()