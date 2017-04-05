class PageNode():
    def __init__(self, title):
        self.title = title
        self.parent = None
        self.children = []
        self.distance = 0
