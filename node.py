import sys
import Queue as queue

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}

    def __str__(self):
        return str(self.id)

    def addNeighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def removeNeighbor(self, neighbor):
        print('removing %s from %s' %(str(neighbor), self.id))
        for x in self.adjacent:
            if str(neighbor) == x.id:
                del self.adjacent[x]
                break
        
    def getNeighbors(self):
        return self.adjacent.keys()

    def getID(self):
        return self.id

    def getWeight(self, neighbor):
        return self.adjacent[neighbor]

class Graph:
    def __init__(self, width, height):
        self.vert_dict = {}
        self.width = width
        self.height = height
        self.generateMap()
        self.getShortestDistance(12)

    def __iter__(self):
        return iter(self.vert_dict.values())

    def addVertex(self, node):
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def getVertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def addEdge(self, frm, to, cost= 0):

        self.vert_dict[frm].addNeighbor(self.vert_dict[to], cost)
        self.vert_dict[to].addNeighbor(self.vert_dict[frm], cost)

    def removeEdge(self, frm, direction):
        print(self.mapNavigation(int(frm), direction))
        self.vert_dict[frm].removeNeighbor(self.mapNavigation(int(frm), direction))

    def cordsConversion(self, x, y):
        return (y * self.width) + x

    def generateMap(self):
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.addVertex(self.cordsConversion(x, y))

        for y in range(0, self.height):
            for x in range(0, self.width):
                self.addEdge(self.cordsConversion(x, y),
                        self.mapNavigation(self.cordsConversion(x, y), 'north'),
                        1)
                self.addEdge(self.cordsConversion(x, y),
                        self.mapNavigation(self.cordsConversion(x, y), 'east'),
                        1)
                self.addEdge(self.cordsConversion(x, y),
                        self.mapNavigation(self.cordsConversion(x, y), 'south'),
                        1)
                self.addEdge(self.cordsConversion(x, y),
                        self.mapNavigation(self.cordsConversion(x, y), 'west'),
                        1)
                
        
    def mapNavigation(self, getPosition, getDirection):
        if getPosition % self.width == 0:
            #Left side
            if getDirection == "northwest":
                    return ((self.height - 1)*(self.width) + (getPosition+(self.width-1))) % (self.width * self.height)
            elif getDirection == "north":
                    return ((self.height - 1)*(self.width) + getPosition) % (self.width * self.height)
            elif getDirection == "northeast":
                    return ((self.height - 1)*(self.width) + (getPosition+1)) % (self.width * self.height)
            elif getDirection == "west":
                    return getPosition + (self.width-1)
            elif getDirection == "east":
                    return getPosition + 1
            elif getDirection == "southwest":
                    return (getPosition + (2*self.width - 1)) % (self.width * self.height)
            elif getDirection == "south":
                    return (getPosition + self.width) % (self.width * self.height)
            elif getDirection == "southeast":
                    return (getPosition + self.width + 1) % (self.width * self.height)
            else: return -1
        elif getPosition%self.width == self.width-1:
            #Right Side
            if getDirection == "northwest":
                    return ((self.height - 1)*(self.width) + (getPosition - 1)) % (self.width * self.height)
            elif getDirection == "north":
                    return ((self.height - 1)*(self.width) + getPosition) % (self.width * self.height)
            elif getDirection == "northeast":
                    return ((self.height - 1)*(self.width) + (getPosition - (self.width - 1))) % (self.width * self.height)
            elif getDirection == "west":
                    return getPosition - 1
            elif getDirection == "east":
                    return getPosition - (self.width - 1)
            elif getDirection == "southwest":
                    return (self.width + (getPosition - 1)) % (self.width * self.height)
            elif getDirection == "south":
                    return (getPosition + self.width) % (self.width * self.height)
            elif getDirection == "southeast":
                    return (self.width + (getPosition - (self.width - 1))) % (self.width * self.height)
            else: return -1
        else:
            #mids
            if getDirection == "northwest":
                    return ((self.height - 1)*(self.width) + (getPosition - 1)) % (self.width * self.height)
            elif getDirection == "north":
                    return ((self.height - 1)*(self.width) + getPosition) % (self.width * self.height)
            elif getDirection == "northeast":
                    return ((self.height - 1)*(self.width) + (getPosition+1)) % (self.width * self.height)
            elif getDirection == "west":
                    return getPosition - 1
            elif getDirection == "east":
                    return getPosition + 1
            elif getDirection == "southwest":
                    return (self.width + (getPosition - 1)) % (self.width * self.height)
            elif getDirection == "south":
                    return (getPosition + self.width) % (self.width * self.height)
            elif getDirection == "southeast":
                    return (getPosition + self.width + 1) % (self.width * self.height)
            else: return -1

    class DijkstraDistance:
        def __init__(self, vertex, distance):
            self.vertex = vertex
            self.distance = distance

    def getShortestDistance(self, source):
        vertexQueue = queue.PriorityQueue()
        distances = {}

        #initialize all distances to 0
        distances[source] = self.DijkstraDistance(source, 0)
        for x in range(0, len(self.vert_dict)):
            if x <> source:
                distances[x] = self.DijkstraDistance(x, sys.maxint)
            vertexQueue.put(self.DijkstraDistance(x, sys.maxint))

        while (vertexQueue.qsize() > 1):
            tempDijk = vertexQueue.get(True)
            tempNode = self.vert_dict[tempDijk.vertex]
            for x in tempNode.getNeighbors():
                currentNode = self.vert_dict[x.id]
                disComparison = float(distances[tempNode.id].distance) + float(tempNode.getWeight(x))
                if disComparison <  float(distances[x.id].distance):
                    vertexQueue.put(self.DijkstraDistance(x.id, disComparison))
                    distances[x.id].distance = disComparison

        for x in distances:
            print('%s: %s' %(x, distances[x].distance))
