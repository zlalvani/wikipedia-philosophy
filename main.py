'''
Main entrypoint
'''

import argparse
import pickle
import threading
import matplotlib.pyplot as plt
import numpy as np

from page_node import PageNode
from wiki_crawler import WikiCrawler

def traverse(root, distance=0):
    '''
    Traverse the page tree, updating each node with its distance from the root (target)

    arguments:
        distance:int (optional)
    '''

    if root is None:
        return
    root.distance = distance

    for child in root.children:
        traverse(child, distance + 1)

def generate_plot(nodes, starters, target):
    '''
    Generate and save a plot of the distribution

    arguments:
        nodes: \{node_title:str : node:PageNode\}
        starters: [starter:str]
        target:str
    '''
    data = [nodes[s].distance for s in starters if nodes[s].distance > 0]

    fig = plt.hist(
        data,
        50,
        facecolor='r',
        alpha=.75
    )

    terminal = len(data) / len(starters) * 100

    plt.xlabel('Distance from %s' % target)
    plt.ylabel('Number of Pages')
    plt.title('Distribution of distance to %s, with %.2f%% finishing' % (target, terminal))
    plt.grid(True)
    plt.savefig('output.png')



def main():
    '''
    Main function, parses command line arguments and starts the crawler
    '''

    parser = argparse.ArgumentParser(description='Crawl Wikipedia articles to reach the philosophy page.')
    parser.add_argument('target_page', type=str, help='Target page (e.g. Philosophy)')
    parser.add_argument('num_crawlers', type=int, help='The number of initial pages to start with')
    parser.add_argument('--plot', dest='plot', action='store_true', help='Make a plot of the results')
    parser.add_argument('--save', dest='save', action='store_true', help='Save the crawled data')
    parser.add_argument('--load', dest='load', action='store_true', help='Use saved data')

    args = parser.parse_args()

    target_page = args.target_page

    if args.load:
        crawler = WikiCrawler.load('data.pkl')
    else:
        crawler = WikiCrawler(target_page)


        print('\n' + '=' * 25 + ' Beginning crawl... ' + '=' * 25 + '\n')

        for i in range(args.num_crawlers):
            crawler.start()

        crawler.join_all()
        print('\n' + '=' * 25 + ' Crawling complete ' + '=' * 25 + '\n')

    if crawler.target in crawler.nodes:
        traverse(crawler.nodes[crawler.target])
    else:
        print('No starting pages reached target %s!' % crawler.target)

    if args.plot:
        generate_plot(crawler.nodes, crawler.starters, crawler.target)

    if args.save:
        crawler.save('data.pkl')

if __name__ == '__main__':
    main()
