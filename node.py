import sys
from multiprocessing import Queue
import heapq
import datetime
import Person

class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        self.existance = None
        self.tile = None
        self.menuOptions = {}

    def __str__(self):
        return "vertex: " + str(self.id)

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

class PriorityQueue:
    def __init__(self):
        self.elements = []
    
    def empty(self):
        return len(self.elements) == 0
    
    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))
    
    def get(self):
        return heapq.heappop(self.elements)[1]
    
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

    def setTile(self, arg1, arg2, arg3 = None):
        if arg3 is None:
            self.vert_dict[arg1].tile = arg2
        else:
            self.vert_dict[self.cordsConversion(arg1, arg2)].tile = arg3
        
    def getTile(self, n):
        return self.vert_dict[n].tile

    def addEdge(self, frm, to, cost= 0):
        self.vert_dict[frm].addNeighbor(self.vert_dict[to], cost)

    #Can Enter into frm from specific direction
    def addEdgesFrom(self, frm, direction, cost = 0):
        if direction == 'all':
            self.addEdge(frm, self.mapNavigation(frm, 'north'), 1)
            self.addEdge(frm, self.mapNavigation(frm, 'east'), 1)
            self.addEdge(frm, self.mapNavigation(frm, 'south'), 1)
            self.addEdge(frm, self.mapNavigation(frm, 'west'), 1)
            self.addEdge(self.mapNavigation(frm, 'north'), frm, 1)
            self.addEdge(self.mapNavigation(frm, 'east'), frm, 1)
            self.addEdge(self.mapNavigation(frm, 'south'), frm, 1)
            self.addEdge(self.mapNavigation(frm, 'west'), frm, 1)
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
                self.vert_dict[self.cordsConversion(x, y)].tile = 'Grass'
                self.vert_dict[self.cordsConversion(x, y)].menuOptions[0] = 'Walk'                

        self.setTile(7, 2, 'Dirt')
        self.setTile(7, 3, 'Dirt')
        self.setTile(7, 4, 'Dirt')
        self.setTile(7, 5, 'Dirt')
        self.setTile(7, 6, 'Dirt')
        self.vert_dict[self.cordsConversion(7, 2)].menuOptions[1] = 'Test'
        self.vert_dict[self.cordsConversion(7, 2)].menuOptions[2] = 'Auto run'
        self.vert_dict[self.cordsConversion(7, 3)].menuOptions[1] = 'Crawl'
        
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

    def aStar(self, source, goal):
        queues = PriorityQueue()
        queues.put(source, 0)
        came_from = {}
        currentCost = {}
        came_from[source] = None
        currentCost[source] = 0

        while not queues.empty():
            current = queues.get()

            if current == goal:
                break
            
            for next in self.vert_dict[current].getNeighbors():
                newCost = currentCost[current] + self.vert_dict[current].getWeight(next)
                if next.id not in came_from or newCost < currentCost[next.id]:
                    currentCost[next.id] = newCost
                    priority = newCost
                    queues.put(next.id, priority)
                    came_from[next.id] = current
        return came_from, currentCost

    def shortestPath(self, start, goal):
        if self.checkEnterable(goal):
            cameFrom, currentCost = self.aStar(start, goal)
            current = goal
            path = []
            while current != start:
                path.append(current)
                current = cameFrom[current]
        else:
            self.addEdgesFrom(goal, 'all')
            cameFrom, currentCost = self.aStar(start, goal)
            self.removeEdgesFrom(goal, 'into')
            current = goal
            path = []
            while current != start:
                path.append(current)
                current = cameFrom[current]
            path[0] = "f%d" %(path[0])
            print(path[0])
        return path

    def checkEnterable(self, check):
        pathsInto = []
        for checking in self.vert_dict[check].getNeighbors():
            for checkingNext in self.vert_dict[checking.id].getNeighbors():
                if checkingNext.id == check:
                    pathsInto.append(checkingNext.id)
        return pathsInto

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

    def smartMovePerson(self, person, goal):
        current = self.cordsConversion(person.x, person.y)
        path = self.shortestPath(current, goal)
        while path:
            person = self.vert_dict[current].existance
            self.removeExistance(current)
            current = path.pop()
            self.putExistance(person, current)
            
