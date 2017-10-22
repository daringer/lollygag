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
        self.children = {} #set()

        if parent is None:
            self.root = self 
            self.depth = 0  
        else:
            self.root = parent.root 
            self.depth = parent.depth + 1

    def add(self, name):
        """Add node named: 'name' as child to 'self'"""
        node = Node(name, self)
        self.children[name] = node
        self.root.visited.add(name)
        return node

    def search(self, name):
        """Search 'name' in all children (breadth-first)"""
        if name == self.name:
          return self

        #match = lambda n: n.name == name
        #res = list(filter(match, self.children) or \
         #          filter(bool, map(n.search(name), self.children)) )
        #return res.pop() if len(res) > 0 else None
        res = list([self.children.get(name)] or \
            filter(bool, map(lambda n: n.search(name), self.children.values())))
        return res.pop() if len(res) > 0 else None

class RootNode(Node):
    """Single difference to regular 'Node', global visited-links-index"""
    def __init__(self, name):
      super(RootNode, self).__init__(name, None)
      self.visited = set()

class MapperCrawler(Crawler):
    """
    An unrestricted `MapperCrawler`, which maintains a 'crawling-tree'
    """

    max_depth = None
    max_children = None

    def __init__(self, *args, **kwargs):
        super(MapperCrawler, self).__init__(*args, **kwargs)
        self.tree = None

    def reset(self, url):
        """
        Resets the crawler's state.
        """
        super(MapperCrawler, self).reset(url)
        self.tree = RootNode(url)

    def process_link(self, origin, link):
        """
        Adds the processed links from super to the graph.
        """
        #print ("FROM: {} TO: {}".format(origin, link)) 
        
        #if link is None:
        #  return None

        # create root-node, if not existing
        root = RootNode(origin) if self.tree is None else self.tree

        # get origin-node, 
        p_node = root
        if origin != p_node.name:
            p_node = root.search(origin)
            if p_node is None:
              p_node = root.add(origin)
        
        result = super(MapperCrawler, self).process_link(origin, link)
        if result is None: 
            #print ("OUT NO RESULT", result)
            return None
        
        if not p_node:
          #print ("OUT NO ORIGIN-NODE")
          return None

        # already in database (technically one should ask self.root)
        if result in root.visited:
          #self.seen = 1 if not hasattr(self, "seen") else self.seen + 1
          #print ("OUT ALREADY SEEN", result, self.seen)
          return None
        
        # children max reached?
        if self.max_children and self.max_children <= len(p_node.children):
          #print ("OUT MAX CHILDREN", p_node.name, len(p_node.children))
          return None

        # new location
        node = p_node.add(result)
        if node.depth == self.max_depth:
          #print ("OUT DEPTH", node.depth, result)
          return None
        #print ("IN", node.depth, "CHILDREN #:", len(node.children), result)
        return result
