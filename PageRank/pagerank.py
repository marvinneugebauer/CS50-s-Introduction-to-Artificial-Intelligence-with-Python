import os
import random
import re  # Regular expression operations
import sys

sys.setrecursionlimit(11000)

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
    Parse (analyse) a directory of HTML pages and check for links to other pages.
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
    """ 
    We create a dictionary, by assigning each page of the corpus to its probability distribution. Therefore 
    we check the number of linked pages for the current page and calculate the probability distribution 
    for every single page that is linked
    """

    prob_dist = dict()
    damping_dist = (1 - damping_factor) / len(corpus)

    for p in corpus:
        if p == page:
            for link in corpus[p]:
                prob_dist[link] = (damping_factor / len(corpus[p])) + damping_dist

    if not prob_dist:
        for p in corpus:
            prob_dist[p] = 1 / len(corpus)

    for p in corpus:
        if p not in prob_dist:
            prob_dist[p] = damping_dist
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    page_rank = dict()
    page_sampling = []
    first_page = random.choice(list(corpus.keys()))
    page_sampling.append(first_page)
    new_dist = transition_model(corpus, first_page, damping_factor)
    pages = sampling(corpus, damping_factor, new_dist, 1, n, page_sampling)

    for p in corpus:
        number_page = pages.count(p)
        page_rank[p] = number_page / n

    return page_rank



def sampling(corpus, damping_factor, prob_dist, i, n, page_sampling):
    """
    For a given n the sampling function returns  a list that documents how many times each page of the corpus
    was chosen randomly by regarding its probability distribution.
    """
    if i < n:
        sequence = []
        probabilities = []
        for p in prob_dist:
            sequence.append(p)
            probabilities.append(prob_dist[p])
        list_page = random.choices(sequence, weights=probabilities, k=1)
        for q in list_page:
            page = q
        page_sampling.append(page)
        i += 1
        return sampling(corpus, damping_factor, transition_model(corpus, page, damping_factor), i, n, page_sampling)
    else:
        print(page_sampling)
        return page_sampling


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    pagerank_dist = dict()
    links = {}

    for p in corpus:
        pagerank_dist[p] = 1 / len(corpus)

    section_1 = ((1 - damping_factor) / len(corpus))

    # Checks if a page has no links and mapping links to each pages from that given page

    for page in corpus:
        if not corpus[page]:
            store = set()
            for j in corpus:
                store.add(j)
            corpus[page] = store

    # Determine all pages i that link to a given page p. We define a dictionary, where page p is the key
    # and maps to all pages, where the page p is linked by.

    for page in corpus:
        for i in corpus:
            if corpus[i]:
                for p in corpus[i]:
                    if p == page:
                        links.setdefault(page, set()).add(i)

    new_page_rank = dict()
    page_rank = iteration(corpus, links, pagerank_dist, section_1, damping_factor, new_page_rank)

    return page_rank


def iteration(corpus, links, pagerank_dist, section_1, damping_factor, new_page_rank):
    if new_page_rank:
        for s in new_page_rank:
            if abs(new_page_rank[s] - pagerank_dist[s]) < 0.001:
                return new_page_rank
            else:
                pagerank_dist = new_page_rank.copy()
                for page in links:
                    section_2 = 0
                    for j in links[page]:
                        section_2 = section_2 + (pagerank_dist[j] / len(corpus[j]))
                        new_page_rank[page] = section_1 + damping_factor * section_2
                a = 0
                for l in new_page_rank:
                    a = a + new_page_rank[l]
                return iteration(corpus, links, pagerank_dist, section_1, damping_factor, new_page_rank)
    else:
        for page in links:
            section_2 = 0
            for j in links[page]:
                section_2 = section_2 + (pagerank_dist[j] / len(corpus[j]))
                new_page_rank[page] = section_1 + damping_factor * section_2
        a = 0
        for l in new_page_rank:
            a = a + new_page_rank[l]
        return iteration(corpus, links, pagerank_dist, section_1, damping_factor, new_page_rank)


if __name__ == "__main__":
    main()
