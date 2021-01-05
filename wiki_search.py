from wiki_page import *

def search(start_page, depth=0, prnt=True):
    """
    Create a web centered around a wikipedia article.
    str start_page is the name of the article to start on.
    """
    p = page(start_page, prnt=prnt)
    if depth > 0:
        for neigh in sorted(list(p._neighbors)):
            search(neigh, depth = depth - 1)

search("Mathematics", depth=2)
