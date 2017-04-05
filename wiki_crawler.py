'''
Class definition of WikiCrawler
'''

import threading
import pickle

from page_node import PageNode
from helpers import get_random_page, get_page_html, get_link

class WikiCrawler():
    '''
    A class designed for crawling Wikipedia articles in search of a target page.

    Uses Python threads for concurrent HTTP requests.

    A tree of pages is constructed inside of a dictionary. Each node contains
    references to other nodes, and nodes can be quickly accessed by their title.

    Can be pickled by using the associated methods.
    '''

    def __init__(self, target, baseurl='https://en.wikipedia.org/api/rest_v1'):
        '''
        members:
            self.target:str - a target page title for the crawler
            self.baseurl:str - the baseurl for API requests
            self.nodes:dict - the node tree
            self.starters:list - a list of starting articles
            self._lock:Lock - a mutex for access to the tree
            self._threads:list - a list of threads

        '''
        self.target = target
        self.baseurl = baseurl
        self.nodes = {}
        self.starters = []
        self._lock = threading.Lock()
        self._threads = []

    def _add_node(self, title):
        '''
        Attempt to insert a new node into the nodes tree, given its title

        arguments:
            title:str

        returns:
            PageNode | None
        '''
        with self._lock:
            if title not in self.nodes:
                node = PageNode(title)
                self.nodes[title] = node
                return node
            else:
                return None

    def _crawl(self, title):
        '''
        Callback function used by threads to begin their crawl towards the target,
        given an initial page title.

        Threads will terminate if they encounter an article that has already been seen.

        arguments:
            title:str
        '''
        node = self._add_node(title)

        print('THREAD %d: starting with title %s' % (threading.current_thread().ident, title))

        while title != self.target:
            print('THREAD %d: fetching page %s' % (threading.current_thread().ident, title))

            content = get_page_html(title, baseurl=self.baseurl)
            new_title = get_link(content)

            if new_title is None:
                print(
                    'THREAD %d: %s contains no valid links, terminating' % \
                    (threading.current_thread().ident, title)
                )
                return

            new_node = self._add_node(new_title)

            if new_node is None:
                print(
                    'THREAD %d: %s already visited, terminating' % \
                    (threading.current_thread().ident, new_title)
                )
                with self._lock:
                    self.nodes[new_title].children.append(node)
                return

            if node is not None:
                with self._lock:
                    new_node.children.append(node)
                    node.parent = new_node

            node = new_node
            title = new_node.title

        print('THREAD %d: reached target %s, terminating' % (threading.current_thread().ident, self.target))

    def start(self, title=''):
        '''
        Start a new threaded crawl towards the target, given an initial page title.
        If none is given, a random one is chosen.

        arguments:
            title:str
        '''
        if not title:
            title = get_random_page(baseurl=self.baseurl)
        self.starters.append(title)
        thread = threading.Thread(target=self._crawl, args=[title], daemon=True)
        self._threads.append(thread)
        thread.start()

    def join_all(self):
        '''
        Wait for all threads to terminate
        '''

        for thread in self._threads:
            thread.join()

        self._threads = []

    def save(self, filename):
        '''
        Pickle the entire WikiCrawler object in a file for later use

        arguments:
            filename:str
        '''
        with open(filename, 'wb') as f:
            self._lock = None
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        '''
        Static method for unpickling a WikiCrawler object from a file

        arguments:
            filename:str
        '''
        with open(filename, 'rb') as f:
            crawler = pickle.load(f)
            crawler._lock = threading.Lock()
            return crawler
