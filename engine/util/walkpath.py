import collections
import draw, vector, dijkstra

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
    
    def dijkstra_repr(self):
        G = collections.defaultdict(dict)
        for edge in self.edges.viewvalues():
            G[edge.a][edge.b] = vector.dist_between(self.points[edge.a], self.points[edge.b])
        return G
    
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
    
    def point_near(self, x, y, exclude=None):
        dest_coords = (x, y)
        dest_edge = self.closest_edge_to_point(dest_coords, exclude)
        dist_sq_to_a = vector.dist_squared_between(dest_coords, self.points[dest_edge.a])
        dist_sq_to_b = vector.dist_squared_between(dest_coords, self.points[dest_edge.b])
        if dist_sq_to_a < dist_sq_to_b:
            return dest_edge.a
        else:
            return dest_edge.b
    
    def move_sequence_between(self, src_point, dest_point):
        path = dijkstra.shortest_path(self.dijkstra_repr(), src_point, dest_point)
        previous_identifier = path[0]
        move_dests = []
        for identifier in path[1:]:
            move_dests.append((self.points[identifier], self.edges[(previous_identifier, identifier)].anim))
            previous_identifier = identifier
        return dest_point, move_dests
    
    def path_point_near_point(self, mouse):
        close = lambda a, b: abs(a-b) <= 5
        for identifier, point in self.points.viewitems():
            if close(point[0], mouse[0]) and close(point[1], mouse[1]):
                return identifier
        return None
    
    def closest_edge_to_point(self, point, exclude=None):
        # Optimize me! Use rectangles.
        
        exclude = exclude or set()
        closest_point = None
        closest_dist = None
        closest_edge = None
        for edge in [e for e in self.edges.viewvalues() \
                     if e.a not in exclude and e.b not in exclude]:
            cp = self.closest_edge_point_to_point(edge, point)
            test_dist = vector.length_squared((point[0]-cp[0], point[1]-cp[1]))
            if closest_dist is None or test_dist < closest_dist:
                closest_point = cp
                closest_edge = edge
                closest_dist = test_dist
        return closest_edge
    
    def closest_edge_point_to_point(self, edge, point):
        return vector.closest_point_on_line(point, self.points[edge.a], self.points[edge.b])
    
    def draw(self):
        for edge in self.edges.viewvalues():
            ax, ay = self.points[edge.a]
            bx, by = self.points[edge.b]
            if edge.counterpart:
                draw.line(ax, ay, bx, by, colors=(0, 255, 0, 255, 0, 255, 0, 255))
            else:
                draw.line(ax, ay, bx, by, colors=(255, 0, 0, 255, 0, 0, 255, 255))
        draw.set_color(1,0,0,1)
        for point in self.points.viewvalues():
            draw.rect(point[0]-5, point[1]-5, point[0]+5, point[1]+5)
    

