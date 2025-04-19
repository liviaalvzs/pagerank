import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1]) # read the pages and return links that each page contains
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
    probs = {}
    
    for p in corpus: # initializing all pages with prob equal to none
        probs[p] = None
        
    total_n_pages = len(corpus)
    
    # verify if there are links referenced in page
    if corpus[page]:
        referenced = corpus[page]
    else:
        referenced = corpus.keys()
        
    for p in probs:
        probs[p] = (1 - damping_factor) / total_n_pages
        if p in referenced: # more chance
            probs[p] += damping_factor / len(referenced)
    
    return probs 

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    visits_rank = {}
    
    for page in corpus: # initializing all pages with visits equal to none
        visits_rank[page] = 0

    page = random.choice(list(corpus.keys()))
    
    for _ in range(n):
        visits_rank[page] += 1
        model = transition_model(corpus, page, damping_factor)
        page = random.choices(list(model.keys()), list(model.values()))[0] # choosing randomly the next page, considering their probabilities as weights
        
    # converting the visit nums in probabilities
    page_rank_normalized = {}
    
    page_rank_normalized = {page: visits / n for page, visits in visits_rank.items()}

    return page_rank_normalized
        
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Returns:
        A dictionary where keys are page names, and values are their estimated 
        PageRank value (a value between 0 and 1). All PageRank values should sum to 1.
    """

    n_total = len(corpus)

    # all pages start with equal probability
    page_rank = {page: 1 / n_total for page in corpus}

    # convergence threshold
    threshold = 0.001

    while True:
        new_page_rank = {}

        # ppdate the page rank for each page
        for page in corpus:
            # start with the random jump factor
            total = (1 - damping_factor) / n_total

            # loop over all pages in the corpus
            for p in corpus:
                # if page p has no referenced links, treat it as linking to all pages
                if len(corpus[p]) == 0:
                    total += damping_factor * (page_rank[p] / n_total)
                # if some page has links to the current page add > prob
                elif page in corpus[p]:
                    total += damping_factor * (page_rank[p] / len(corpus[p]))

            # store the new page rank value for this page
            new_page_rank[page] = total

        # check if values have converged
        converged = all(abs(new_page_rank[p] - page_rank[p]) < threshold for p in corpus)

        # update the page rank dictionary with new values
        page_rank = new_page_rank

        # if all values have converged (small changes), stop iterating
        if converged:
            break

    return page_rank



if __name__ == "__main__":
    main()
