import util

class Edge(object):
    def __init__(self, a, b, anim=None, annotations=None):
        self.a = a
        self.b = b
        self.anim = anim
        if self.anim == '':
            self.anim = None
        self.annotations = annotations or []
        self.counterpart = None
    
    def dict_repr(self):
        dict_repr = {'a': self.a, 'b': self.b}
        if self.anim:
            dict_repr['anim'] = self.anim
        if self.annotations:
            dict_repr['annotations'] = self.annotations
        return dict_repr
    

class WalkPath(object):
    def __init__(self, dict_repr=None):
        self.points = {}
        self.edges = {}
        if dict_repr:
            for identifier, point_dict in dict_repr['points'].viewitems():
                self.points[identifier] = (int(point_dict['x']), int(point_dict['y']))
            for edge_dict in dict_repr['edges']:
                new_edge = self.add_edge(edge_dict['a'], edge_dict['b'])
                if edge_dict.has_key('anim'):
                    new_edge.anim = edge_dict['anim']
    
    def dict_repr(self):
        return {'points': {identifier : {'x': point[0], 'y': point[1]} \
                           for identifier, point in self.points.viewitems()},
                'edges': [edge.dict_repr() for edge in self.edges.viewvalues()]}
    
    def add_point(self, x, y, identifier=None):
        if self.points.has_key(identifier):
            return self.points[identifier]
        if identifier is None:
            next_identifier = 1
            while self.points.has_key("point_%d" % next_identifier):
                next_identifier += 1
            identifier = "point_%d" % next_identifier
        self.points[identifier] = (x, y)
        return identifier
    
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
    
    def remove_point(self, identifier):
        try:
            del self.points[identifier]
        except KeyError:
            return
    
    def remove_edge(self, p1, p2):
        if self.edges.has_key((p1, p2)):
            e = self.edges[(p1, p2)]
            if e.counterpart:
                e.counterpart.counterpart = None
            del self.edges[(p1, p2)]
    
    def path_point_near_point(self, mouse):
        close = lambda a, b: abs(a-b) <= 5
        for identifier, point in self.points.viewitems():
            if close(point[0], mouse[0]) and close(point[1], mouse[1]):
                return identifier
        return None
    
    def closest_edge_point_to_point(self, edge, point):
        return util.closest_point_on_line(point, self.points[edge.a], self.points[edge.b])
    

