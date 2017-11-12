import sys
import Queue as queue
import datetime
import person

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.existance = None;

    def __str__(self):
        return str(self.id)

    def addNeighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def getNeighbors(self):
        return self.adjacent.keys()

    def removeNeighbor(self, neighbor):
        for x in self.adjacent:
            if neighbor == x.id:
                del self.adjacent[x]
                break
            
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

    #Can Enter into frm from specific direction
    def addEdgesFrom(self, frm, direction, cost = 0):
        if direction == 'all':
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'east')], cost)
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'west')], cost)
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'south')], cost)
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'north')], cost)
            self.vert_dict[self.mapNavigation(frm, 'east')].addNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'west')].addNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'south')].addNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'north')].addNeighbor(frm)
        elif direction == 'into':
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'east')], cost)
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'west')], cost)
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'south')], cost)
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, 'north')], cost)
        else:            
            self.vert_dict[frm].addNeighbor(self.vert_dict[self.mapNavigation(frm, direction)], cost)
        

    #Can't Enter into frm from specific direction
    def removeEdgesFrom(self, frm, direction):
        if direction == 'all':
            self.vert_dict[frm].removeNeighbor(self.mapNavigation(frm, 'east'))
            self.vert_dict[frm].removeNeighbor(self.mapNavigation(frm, 'west'))
            self.vert_dict[frm].removeNeighbor(self.mapNavigation(frm, 'south'))
            self.vert_dict[frm].removeNeighbor(self.mapNavigation(frm, 'north'))
            self.vert_dict[self.mapNavigation(frm, 'east')].removeNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'west')].removeNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'south')].removeNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'north')].removeNeighbor(frm)
        elif direction == 'into':
            self.vert_dict[self.mapNavigation(frm, 'east')].removeNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'west')].removeNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'south')].removeNeighbor(frm)
            self.vert_dict[self.mapNavigation(frm, 'north')].removeNeighbor(frm)
        else:
            self.vert_dict[frm].removeNeighbor(self.mapNavigation(frm, direction))

    def cordsConversion(self, x, y = None):
        if y is None:
            return x % self.width, x / self.width
        else:
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
        def __init__(self, vertex, distance, nextNode):
            self.vertex = vertex
            self.distance = distance
            self.nextNode = nextNode

        def __str__(self):
            return str(self.distance)

    def getAllShortestDistance(self, source):
        a = datetime.datetime.now()
        vertexQueue = queue.PriorityQueue()
        distances = {}
        
        distances[source] = self.DijkstraDistance(source, 0, 'x')
        for x in range(0, len(self.vert_dict)):
            if x <> source:
                distances[x] = self.DijkstraDistance(x, sys.maxint, 'x')
            vertexQueue.put(self.DijkstraDistance(x, sys.maxint, 'x'))

        while (vertexQueue.qsize() > 1):
            tempDijk = vertexQueue.get(True)
            tempNode = self.vert_dict[tempDijk.vertex]
            for x in tempNode.getNeighbors():
                currentNode = self.vert_dict[x.id]
                disComparison = float(distances[tempNode.id].distance) + float(tempNode.getWeight(x))
                if disComparison <  float(distances[x.id].distance):
                    vertexQueue.put(self.DijkstraDistance(x.id, disComparison, tempNode.id))
                    distances[x.id].distance = disComparison
                    distances[x.id].nextNode = tempNode.id


        b = datetime.datetime.now()
        print(b-a)
        self.printSet(distances)
        return distances

    def printSet(self, distances):
        for y in range(0, self.height):
            for x in range(0, self.width):
                print('%3s: %4s [%4s]' %(self.cordsConversion(x, y), distances[self.cordsConversion(x,y)], distances[self.cordsConversion(x,y)].nextNode)),
            print('')
                
    def getExits(self, xPos, yPos = None):
        if yPos is None:
            print('%s: ' %xPos),
            for x in self.vert_dict[xPos].getNeighbors():
                print('%s, ' %x.id),
        else:
            print('%s: ' %self.cordsConversion(xPos, yPos)),
            for x in self.vert_dict[self.cordsConversion(xPos, yPos)].getNeighbors():
                print('%s, ' %x.id),
                
    def putExistance(self, person, xPos, yPos = None):
        if yPos is None:
            self.vert_dict[xPos].existance = person
        else:
            self.vert_dict[self.cordsConversion(xPos, yPos)].existance = person

    def removeExistance(self, xPos, yPos = None):
        if yPos is None:
            self.vert_dict[xPos].existance = None
        else:
            self.vert_dict[self.cordsConversion(xPos, yPos)].existance = None     
        
    def getExistance(self, xPos, yPos):
        return self.vert_dict[self.cordsConversion(xPos, yPos)].existance

    def movePerson(self, person, direction):
        frm = self.cordsConversion(person.x, person.y)
        toX, toY = self.cordsConversion(self.mapNavigation(frm, direction))
        if self.vert_dict[self.cordsConversion(toX, toY)].existance is None:
            for x in self.vert_dict[frm].getNeighbors():
                if x.id == self.cordsConversion(toX, toY):        
                    person = self.vert_dict[frm].existance
                    self.putExistance(person, toX, toY)
                    self.removeExistance(frm)
                    return toX, toY
            return person.x, person.y
        else: return person.x, person.y
