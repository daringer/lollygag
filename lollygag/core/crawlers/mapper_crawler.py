"""
Holds the MapperCrawler class and
helper methods to create maps from the crawling.
"""
import sys 

from lollygag.core.crawlers.domain_crawler import DomainCrawler
from lollygag.core.crawlers.crawler import Crawler

class Node(object):
    """Simple tree implementation""" 
    def __init__(self, name, parent=None):
        self.name = name 
        self.parent = parent
        self.children = {} 

        if parent is None:
            self.root = self 
            self.depth = 0  
        else:
            self.root = parent.root 
            self.depth = parent.depth + 1

    def extend(self, nodes):
        """Extend 'children' with 'nodes'""" 
        #return map(self.add, nodes)
        for n in nodes:
            self.add(n)

    def add(self, node):
        """'node' added to 'children'"""
        
        dist = self.root.dist
        name2node = self.root.name_node
        q = node.name

        # node (link) already mapped and dist < new-dist!
        if q in dist and self.depth + 1 > dist.get(q):
            return None

        node.parent = self
        node.root = self.root
        self.children[q] = node
        name2node[q] = node
        dist[q] = self.depth + 1
        return node
        
    def search(self, name):
        """Search 'name'"""
        if name == self.name:
          return self
        return self.root.name_node.get(name)

class RootNode(Node):
    """Single difference to regular 'Node', global visited-links-index"""
    def __init__(self, name):
      super(RootNode, self).__init__(name, None)
      self.name_node = {}
      self.dist = {}

class MapperCrawler(Crawler):
    """
    An unrestricted `MapperCrawler`, which maintains a 'crawling-tree'
    """

    max_depth = None

    def __init__(self, *args, **kwargs):
        super(MapperCrawler, self).__init__(*args, **kwargs)
        self.tree = None

    def reset(self, url):
        """
        Resets the crawler's state.
        """
        super(MapperCrawler, self).reset(url)
        self.tree = RootNode(url)

    def process_links(self, origin, links):
        """
        Adds the processed links from super to the graph.
        """
        # create root-node, if not existing
        root = RootNode(origin) if self.tree is None else self.tree

        p_node = root.search(origin) or Node(origin, root)
        # max-depth constraint:
        if p_node.depth + 1 > self.max_depth:
            return []
        
        # make canonical link (process_link) and check if-visited 
        # (@todo: this 'is_new_link()' seems not to work correctly)
        #         might be a threading issue or simply me not understanding it...
        out = []
        for link in links:
            uri = super(MapperCrawler, self).process_link(origin, link)
            if self.is_new_link(uri):
                out.append(uri)
        self.status.urls_to_crawl |= set(out) 
        p_node.extend( map(lambda n: Node(n, p_node), out) )
        
        print (len(root.name_node), len(self.status.visited_urls))

        return out
