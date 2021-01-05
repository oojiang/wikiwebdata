import time
import os.path
from os import path
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

def page(name, scrape=False, prnt=False):
    """Returns the Page object with name NAME. Constructs it if necessary."""
    if scrape or name not in Page.pages:
        return Page(name, scrape=scrape, prnt=prnt)
    else:
            return Page.pages[name]
class Page:
    """
    Represents a wikipedia page.
    attributes:
        _name = a string that identifies an article. ("https://en.wikipedia.org/wiki/" + self._name) is the article's url.
        _neighbors = a set of strings. Stores all article names that self links to.
    """
    pages = {}              # A dictionary of all Page objects that have been created. Used by the page() class method to prevent creation of duplicate Page objects. Keys are the str names of the articles, and values are Page objects.
    pagedir = "pages/"      # The directory where data is saved.
    rawdir = "raw/"         # The directory where the original html is saved.


    def __init__(self, page_str, scrape=False, prnt=False):
        """
        DO NOT construct Page objects with this constructor!!!
        Use the class method page() instead.
        """
        self.pages[page_str] = self
        self._name = page_str
        self._neighbors = set()
        if scrape or not path.exists(self.pagedir + page_str) or not path.exists(self.rawdir + page_str):
            self.__scrape_data(prnt=prnt)
        else:
            self.__load_data(prnt=prnt)

    def __load_data(self, prnt=False):
        """Helper method for init for when the page has been downloaded locally."""
        if prnt:
            print("Loading : " + self._name)
        f = open(self.pagedir + self._name)
        for page_line in f:
            page_name = page_line.strip()
            self._neighbors.add(page_name)
        f.close()

    def __scrape_data(self, prnt=False):
        """Helper method for init for when the page needs to be scraped from online."""
        if prnt:
            print("Scraping: " + self._name)

        headers = {"User-Agent" : "Learning web scraping. Contact me at ojiang@berkeley.edu"}

        time.sleep(1); # Delay to prevent spamming requests
        page_url = "https://en.wikipedia.org/wiki/" + self._name
        req = urllib.request.Request(page_url, headers=headers)
        try:
            html = urllib.request.urlopen(req).read()
        except Exception as e:
            print(str(e))
            print("Exception when requesting " + self._name)
            return

        soup0 = BeautifulSoup(html, features="html.parser")
        div = soup0.find(id='bodyContent')
        divstr = '<html><body>' + str(div) + '</body></html>'

        rawf = open(self.rawdir + self._name, "wt+")
        rawf.write(divstr)
        rawf.close()

        soup = BeautifulSoup(divstr, features="html.parser")
        url_list = [link.get('href') for link in soup.find_all('a') 
                    if link.get('href') is not None and is_valid_url(link.get('href'))]

        pagef = open(self.pagedir + self._name, "wt+")
        for url in url_list:
            self._neighbors.add(urllib.parse.urlparse(url).path.rsplit("/", 1)[-1])
        for page_name in self._neighbors:
            pagef.write(page_name + '\n')
        pagef.close()

def is_valid_url(url):
    if '#' in url:
        return 0
    elif url[0:6] != '/wiki/':
        return 0
    elif 'File:' in url:
        return 0
    elif '_(disambiguation)' in url:
        return 0
    elif 'Protection_policy' in url:
        return 0
    elif 'Special:BookSources/' in url:
        return 0
    elif '/wiki/Help:' in url:
        return 0
    elif 'ISBN_(identifier)' in url:
        return 0
    elif 'OCLC_(identifier)' in url:
        return 0
    elif 'Wikipedia_indefinitely_semi-protected_pages' in url:
        return 0
    elif 'Wikipedia_articles_needing_clarification' in url:
        return 0
    elif 'All_articles_lacking_in-text_citations' in url:
        return 0
    elif 'Articles_lacking_in-text_citations' in url:
        return 0
    elif 'All_articles_lacking_in-text_citations' in url:
        return 0
    elif 'rticles_containing_potentially_dated_statements' in url:
        return 0
    elif 'Articles_with_short_description' in url:
        return 0
    elif 'Articles_with_failed_verification' in url:
        return 0
    elif 'Commons_category_link_from_Wikidata' in url:
        return 0
    elif 'Wikipedia_articles_with_KULTURNAV_identifiers' in url:
        return 0
    elif 'Wikipedia_indefinitely_move-protected_pages' in url:
        return 0
    elif 'Commons_category_link_is_on_Wikidata' in url:
        return 0
    elif 'All_articles_with_failed_verification' in url:
        return 0
    elif 'Harv_and_Sfn_template_errors' in url:
        return 0
    elif 'Harv_and_Sfn_no-target_errors' in url:
        return 0
    elif 'Wikipedia_articles_with_GND_identifiers' in url:
        return 0
    elif 'Wikipedia_articles_with_LCCN_identifiers' in url:
        return 0
    elif 'Wikipedia_articles_with_SUDOC_identifiers' in url:
        return 0
    elif 'Wikipedia_articles_with_NDL_identifiers' in url:
        return 0
    elif 'Wikipedia_articles_with_BNF_identifiers' in url:
        return 0
    elif 'Wikipedia_articles_with_BNE_identifiers' in url:
        return 0
    elif 'with_unsourced_statements' in url:
        return 0
    elif 'Articles_containing_Italian-language_text' in url:
        return 0
    elif 'dead_external_links' in url:
        return 0
    elif 'lacking_reliable_references' in url:
        return 0
    elif 'Pages_using_multiple_image_with_auto_scaled_images' in url:
        return 0
    elif 'needing_additional_references' in url:
        return 0
    elif 'Articles_using_small_message_boxes' in url:
        return 0
    elif 'Articles_to_be_expanded_' in url:
        return 0
    elif 'Category:CS1' in url:
        return 0
    elif 'Wikipedia_articles_incorporating_text_from_Citizendium' in url:
        return 0
    elif 'Webarchive_template_wayback_links' in url:
        return 0
    elif 'ISSN_(identifier)' in url:
        return 0
    elif 'GND_(identifier)' in url:
        return 0
    #elif 'Template:Metalworking_navbox' in url:
    #    return 0
    #elif 'GND_(identifier)' in url:
    #    return 0
    elif 'Wikipedia:NOTRS' in url:
        return 0
    elif 'Use_mdy_dates_from' in url:
        return 0
    elif 'Use_dmy_dates_from' in url:
        return 0
    elif 'templatetemplate' in url:
        return 0
    return 1

