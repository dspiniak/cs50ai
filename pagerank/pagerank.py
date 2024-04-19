import os
import random
import copy
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # initialize
    prob_dist = dict()
    outgoing_links = len(corpus[page])
    n = len(corpus) # all pages in corpus
    alpha = (1-damping_factor)/n
    # implement get NumLinks(page) via Crawl function
    
    # if page has no outgoing links, then equal probability distribution for all pages
    if not corpus[page]:
        for page in corpus:
            prob_dist[page] = 1/n
    else:
        # traverse all pages within corpus
        for corpus_page in corpus:
            # if page is not in outgoing links of current page, then prob is alpha
            if corpus_page in corpus[page]:
                prob_dist[corpus_page] = alpha + damping_factor/outgoing_links
            else:
                prob_dist[corpus_page] = alpha
    return prob_dist

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # initialize
    page_rank = dict()
    pages = list()
    
    # start at a random page, add to list
    current_page = random.choice(list(corpus.keys()))
    pages.append(current_page)

    # loop for "n-1" times, given already chose first sample
    for sample in range(0, n-1):
        # choose next page based on transition model probabilities, and add to list - do this by:
        # extract weights from transition model (how to extract second column of dict?)
        transition = transition_model(corpus, current_page, damping_factor)
        current_page = random.choices(list(transition.keys()), list(transition.values()), k = 1 )[0]
        pages.append(current_page)
    # for each page in corpus, count number of pages in sample, and add to page_rank 
    for page in corpus:
        page_rank[page] = pages.count(page)/n
    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # initialize pageRank
    pageRank = dict()
    
    # initialize pagerank with 1/n and create newPageRank with copy of pageRank
    for page in corpus:
        pageRank[page] = 1/len(corpus.keys())
    new_pageRank = pageRank.copy()

    # initialize diff with large number
    max_difference = 999

    while max_difference > 0.001:
        for page_p in corpus:
            print(f"ENTERED page_p: {page_p}")
            # print(f"LINKS in {page_p} are: {corpus[page_p]}")
            gamma = 0
            # print(f"GAMMMA: gamma is 0")
                        
            # traverse all pages that link to page_p
            for page_i in corpus.keys():
                print(f"    entered page_i: {page_i}")
                # only if they link to page_p

                if not corpus[page_i]:
                    gamma += pageRank[page_i]/len(corpus)
                    print(f"        gamma without links: {gamma}")
                else:
                    if page_p in corpus[page_i]:
                        # print(f"page_i: {page_i} links to page_p: {page_p}, as links in page_i are: {corpus[page_i]}")
                        gamma += pageRank[page_i]/len(corpus[page_i])
                        print(f"        gamma with links: {gamma}")                        
                        
            # update new_pageRank
            new_pageRank[page_p] = (1-damping_factor)/len(corpus) + damping_factor*gamma
            print(f"new pagerank of: {page_p} is: {new_pageRank[page_p]}")
        
        # update diff
        # print(f"pageRank: {pageRank}, \n new_pageRank: {new_pageRank}")
        differences = {key: abs(pageRank[key] - new_pageRank[key]) for key in pageRank.keys() & new_pageRank.keys()}
        max_difference = max(differences.values())
        pageRank = new_pageRank.copy()
        # print(f"max_difference: {max_difference}")

    return new_pageRank


if __name__ == "__main__":
    main()
