'''
Class definition for PageNode
'''

class PageNode():
    '''
    Node class to represent individual articles and their relation to others
    '''
    def __init__(self, title):
        self.title = title
        self.parent = None
        self.children = []
        self.distance = 0
