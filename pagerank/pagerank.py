from hashlib import new
import os
import random
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
    new_dict = {}
    if len(corpus[page]) == 0 or corpus[page] == {page}:
        prob = 1 / len(corpus.keys())
        for key in corpus:
            new_dict[key] = prob
    else:
        num_linked_pages = len(corpus[page])
        num_total_pages = len(corpus.keys())

        for linked_page in corpus[page]:
            new_dict[linked_page] = damping_factor / num_linked_pages
        
        for page in corpus.keys():
            if page not in new_dict:
                new_dict[page] = (1 - damping_factor) / num_total_pages
            else:
                new_dict[page] += (1 - damping_factor) / num_total_pages
    return new_dict


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    random_page = random.choices(population=list(corpus.keys()), weights=None, k=1)[0]

    dict_num_times = {}
    num_times = 0

    page_rank = {}
    
    for _ in range(n):
        new_dict = transition_model(corpus, random_page, damping_factor)
        random_page = random.choices(population=list(new_dict.keys()), weights=list(new_dict.values()), k=1)[0]
        if random_page not in dict_num_times:
            dict_num_times[random_page] = 1
        else:
            dict_num_times[random_page] += 1
        num_times += 1
    
    for key in dict_num_times:
        page_rank[key] = dict_num_times[key] / n
    
    return page_rank

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    page_rank = {}

    for page in corpus.keys():
        page_rank[page] = 1 / len(corpus.keys())
    
    accurate = False
    while not accurate:
        accurate = True
        for page in corpus.keys():
            cur_rank_value = page_rank[page]
            sum = 0
            for other in corpus.keys():
                if page != other and page in corpus[other]:
                    sum += page_rank[other] / len(corpus[other])
            new_rank_value = (1- damping_factor) / len(corpus.keys()) + (damping_factor * sum)

            if abs(new_rank_value - cur_rank_value) > 0.001:
                accurate = False
            
            page_rank[page] = new_rank_value
    
    return page_rank

if __name__ == "__main__":
    main()
