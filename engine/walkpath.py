class Edge(object):
    def __init__(self, a, b, anim=None, annotations=None):
        self.a = a
        self.b = b
        self.anim = anim
        self.annotations = annotations or set()
        self.counterpart = None
        

class WalkPath(object):
    def __init__(self, dict_repr=None):
        self.points = {}
        self.edges = {}
        if dict_repr:
            for identifier, point_dict in dict_repr['points'].items():
                self.points[identifier] = (int(point_dict['x']), int(point_dict['y']))
            for edge_dict in dict_repr['edges']:
                new_edge = self.add_edge(edge_dict['a'], edge_dict['b'])
                if edge_dict.has_key('anim'):
                    new_edge.anim = edge_dict['anim']
    
    def add_point(self, x, y, identifier=None):
        if identifier is None:
            next_identifier = 1
            while self.points.has_key("point_%d" % next_identifier):
                next_identifier += 1
            identifier = "point_%d" % next_identifier
        self.points[identifier] = (x, y)
    
    def add_edge(self, p1, p2, *args, **kwargs):
        if self.edges.has_key((p1, p2)):
            return self.edges[(p1, p2)]
        else:
            new_edge = Edge(p1, p2, *args, **kwargs)
            self.edges[(p1, p2)] = new_edge
            if self.edges.has_key((p2, p1)):
                other_way = self.edges[(p2, p1)]
                new_edge.counterpart = other_way
                other_way.counterpart = new_edge
            return new_edge
    
    def path_point_near_point(self, mouse):
        close = lambda a, b: a-5 <= b <= a+5
        for identifier, point in self.points.items():
            if close(point[0], mouse[0]) and close(point[1], mouse[1]):
                return identifier
    

