import sys
import heapq

for major in sys.argv[1:3]:
    if major.upper() not in ["COMP SCI", "DATA SCI", "L I S", "STAT", "MATH"]:
        sys.exit(f"ERROR: DID NOT FIND MATCH FOR {major} IN KNOWN DATABASE")
        


for major in sys.argv[1:3]:
    if major.upper() not in ["COMP SCI", "DATA SCI", "L I S", "STAT", "MATH"]:
        sys.exit(f"ERROR: DID NOT FIND MATCH FOR {major} IN KNOWN DATABASE")
        

#CLASSES TO ORGANIZE COURSE/CATEGORIES for MAJORS:
class Course:
    def __init__(self, dpt, num, prqs): 
        self.name = (dpt, num)
        self.prqs = prqs
        
    def __str__(self):
        return f"{self.name[0].upper()}:{self.name[1]} ({len(self.prqs)} prereqs)"
    def __repr__(self):
        return f"{self.name[0].upper()}:{self.name[1]} ({len(self.prqs)} prereqs)"

class Category:
    def __init__(self, maj, name, num):
        self.major = maj
        self.name = name
        self.num = num
        self.courses = set()
        self.edges = set()

    def __lt__(self, other):
        return len(self.edges) < len(other.edges)
        
    def __str__(self):
        return f"{self.name} - N:{self.num}, C:{self.courses}, D:{len(self.edges)}"
        
    def __repr__(self):
        return f"{self.name} - N:{self.num}, C:{self.courses}, D:{len(self.edges)}"

Courses = dict() #Keys are course names, values are sets of edges
Categories = dict() #Keys are category names, vals are category objects

#PARSE CLASSES FROM TODD's FILE:


#ITERATE THROUGH RORY's FILES
NAMES = [argv[1].upper(), argv[2].upper()] #["COMP SCI", "DATA SCI", "L I S", "STAT", "MATH"]

for FILENAME in NAMES:
    with open(f"{FILENAME}.txt") as f:
        for row in f:
            r = row.split(",")
            catName = r[0].strip()
            catNum = int(r[1].strip())
            category = Category(FILENAME, catName, catNum)
            for i in range(2,len(r)):
                s = r[i].strip()
                dpts = "/".join( sorted(s[:-3].strip().split("/") ) )
                num = int(s[-3:].strip()) 
                course = (dpts, num)
                category.courses.add( course )
                for otherName in Categories:
                    other = Categories[otherName]
                    if course in other.courses and category.major!=other.major:
                        if course not in Courses:
                            Courses[course] = set()
                        Courses[course].add( (category.name, other.name) )
                        category.edges.add(course)
                        other.edges.add(course)
            Categories[category.name] = category

#Produce first output to query
output = []

nodeList = [Categories[key] for key in Categories]
heapq.heapify(nodeList)


def courseStr(dpt, num):
    return f"{dpt} {num}"

def popCourse(course, cat1=None, cat2=None):
    output.append(f"{course[0].upper()} {course[1]}")
    Categories[cat1].courses.discard(course)
    Categories[cat1].num-=1
    Categories[cat1].edges.discard(course)
    if cat2 != None:
        Categories[cat2].num-=1
        Categories[cat2].edges.discard(course)
        Categories[cat2].courses.discard(course)
    if course not in Courses:
        return
    edges = Courses[course]
    Courses.pop(course)
    for e in edges:
        for i in range(2):
            Categories[ e[i] ].courses.discard(course)
            Categories[ e[i] ].edges.discard(course)
    
            
for catName in Categories:
    cat = Categories[catName]
    if len(cat.courses) < cat.num:
        sys.exit("CATEGORY NEEDS MORE COURSES THAN IT HAS!")
    if len(cat.courses) ==  cat.num:
        while len(cat.edges) != 0:
            course = cat.edges.pop()
            options = [e for e in Courses[course] if catName in e]
            best = min(options)
            popCourse(course, best[0], best[1])
        while len(cat.courses) != 0:
            course = cat.courses.pop()
            output.append(f"{course[0]} {course[1]}")
            cat.num-=1
        assert(len(cat.courses) == len(cat.edges) == 0)
nodeList = [Categories[key] for key in Categories]
query = []

def update(nodeList, Courses):
    nodeList.sort(key = lambda a: a.num)
    l = 0
    maxLen = len(nodeList)
    for i in range(maxLen):
        if(nodeList[i].num <= 0):
            Categories.pop(nodeList[i].name)
            l = i + 1
    if l == maxLen:
        return []
    else:
        nodeList = nodeList[l:]
        for c in Courses:
            for e in Courses[c]:
                gone = set()
                if e[0] not in Categories or e[1] not in Categories:
                    gone.add(e)
            for e in gone:
                Courses[c].discard(e)
        return nodeList[l:]

def bestTarget(cat1):
    targets = dict()
    for course in cat1.edges:
        for e in Courses[course]:
            if e[0] == cat1.name:
                targets[e[1]] = course
            elif e[1] == cat1.name:
                targets[e[0]] = course
    keys = list(targets.keys())
    keys.sort(key = lambda e: Categories[e])
    return (targets[keys[0]], cat1, keys[0])

def store():
    f = open("MEM.txt", "w")
    f.write(f"{output}\n{nodeList}\n{Courses}\n{Categories}\n")
    pass

while len(nodeList) != 0:
    nodeList = update(nodeList, Courses)
    if len(nodeList) == 0:
        store()
        print([])
        break
    minNodes = []
    minDegree = len(nodeList[0].edges)
    if minDegree == 0: #
        select = nodeList[0].num
        query = [f"{c[0].upper(), c[1]}" for c in nodeList[0].courses]
        print(query)
        store()
        break
    else:
        for n in nodeList:
            if len(n.edges) == minDegree:
                minNodes.append(n)
            else:
                break
        if len(minNodes) == 1:
            cat1 = minNodes[0]
            popCourse(bestTarget(cat1))
        else:
            stringSet = set()
            for n in minNodes:
                for c in n.edges:
                    s = f"{c[0].upper()} {c[1]}"
                    if s not in stringSet:
                        query.append(s)
                    stringSet.add(s)
            store()
            print(query)
            break