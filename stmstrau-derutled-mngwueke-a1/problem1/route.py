# put your routing program here!
#i defined the state space as a map of nodes connected by roads.  Each of these roads had 2 different types of edge weights; time and distance.  I searched for the successors by expanding on the appropriate node (depending on the algorithm used).  So if start city is Bothell,WA, its successors are Bellevue,WA, Lynnwood,WA, and Monroe,WA and the fringe would then look like this [[Bothell,Bellevue],[Bothell,Lynnwood],[Bothell,Monroe]].
#So bfs would set up a queue and expand on the first possible solution, popping off the first solution and adding successor nodes to the end [[Bothell,Lynnwood],[Bothell,Monroe],[Bothell,Bellevue,Preston],[Bothell,Bellevue,Renton],[Bothell,Bellevue,Seattle]].
#Uniform search does the same method as bfs, but sorts the fringe in order by how far you've gone, beginning with lowest mileage.
#dfs sets up as a stack, so pops off the last state and expands. [[Bothell,Bellevue],[Bothell,Lynnwood],[Bothell,Monroe,Dryden],[Bothell,Monroe,Everett],[Bothell,Monroe,NorthBend]].
#astar works similar to uniform, but takes coordinates of the last node in each solution listed in the fringe and figures out how far away it is with the function coordist (formula found on the web, description below in code).  it then adds this distance to the distance you've already gone and sorts based on that, with lowest mileage being in the beginning.
#assumptions: if speed limit is 0, I treated that like the speed is 0 and time spent on the road is infinite.  It can still be a possiibility if distance is chosen as the cost function, but not accessible if time is the cost function (since there are other ways to go that don't take an infinite amount of time).  I decided to go with this because the nodes I was playing around with had a good amount of these (lots of ferries in Seattle) and its miles were listed as 0, but others had miles to them, so I just wanted to make them all infnite time to take.
#I immediately take the files, put them into lists, and, for the route file, figure out the time spent on each road, based on mph and miles, then append that to each route list as time.  Then depending on either the cost function distance or time, I have it reference that.
#anytime segments is used as the edge weight, I ignore the edge weights, and run uniform and astar algorithms as bfs (dfs is still treated as dfs).


import sys
from math import sin, cos, sqrt, atan2, radians
import csv
import timeit
start_time = timeit.default_timer()
##############################################################
roads = []
roadsfile = open("road-segments.txt","r")
roadslines = roadsfile.readlines()
for i in roadslines:
    roadstemp = i.split(' ')
    if roadstemp[3] == '0':
        time = float("inf")
    elif roadstemp[3] == '':
        time = float("inf")
    else:
        time = round(float(roadstemp[2]) / float(roadstemp[3]),4)
    timestr = str(time)
    roadstemp.append(timestr)
    roads.append(roadstemp)

city = []
cityfile = open("city-gps.txt","r")
citylines = cityfile.readlines()
for i in citylines:
    citytemp = i.split(' ')
    city.append(citytemp)
##############################################################

start = sys.argv[1]
end = sys.argv[2]
routing = sys.argv[3]
cost = sys.argv[4]

#start = "Elmo,_Montana"
#end = "Preston,_Washington"
#routing = "astar"
#cost = "time"
fringe = [[[start], '0', '0', [], '0', '0']]
goal = 0
currentcity = start
currentlist = [[start], 0, 0, [], 0]
astarcity = []

if routing == "astar" and cost == "segments":
    routing = "bfs"

def coordist(latBEG, lonBEG, latEND, lonEND):
    #http://andrew.hedges.name/experiments/haversine/
    #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(latBEG)
    lon1 = radians(lonBEG)
    lat2 = radians(latEND)
    lon2 = radians(lonEND)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancekm = R * c
    distance = distancekm / 1.609344
    return(distance)

def successor(routing, roads, currentcity, fringe, currentlist, astarcity):
    if routing == "dfs":
        fringe.pop(-1)
    else:
        fringe.pop(0)
    for i in roads:
        tempfringe = []
        tempstartcities = []
        tempstartroutes = []
        if i[0] == currentcity:
            repeat = 0
            for j in currentlist[0]:
                if i[1] == j:
                    repeat = 1
            if repeat == 0:
                tempfringe = list(i)
                tempfringe.pop(0)
                tempstartcities = list(currentlist[0])
                tempstartcities.append(tempfringe[0])
                tempfringe[0] = tempstartcities
                tempfringe[1] = str(float(tempfringe[1]) + float(currentlist[1]))
                tempfringe[4] = str(float(tempfringe[4]) + float(currentlist[2]))
                tempstartroutes = list(currentlist[3])
                tempstartroutes.append(tempfringe[3])
                tempfringe[3] = tempstartroutes
                if routing == "astar":
                    astarcity2 = [item[0] for item in astarcity]
                    if cost == "distance":
                        a = 1
                        b = 2
                    elif cost == "time":
                        a = 4
                        b = 5
                    if i[1] not in astarcity2:
                        tempfringe[2] = float(currentlist[4]) - float(i[b])
                    else:
                        indexcity = astarcity2.index(i[1])
                        tempfringe[2] = str(astarcity[indexcity][3])
                    newdis = float(tempfringe[2]) + float(tempfringe[a])
                    tempfringe.append(str(newdis))
                fringe.append(tempfringe)
            elif repeat == 1:
                do = "nothing"
        elif i[1] == currentcity:
            repeat = 0
            for j in currentlist[0]:
                if i[0] == j:
                    repeat = 1
            if repeat == 0:
                switch = i[0]
                i[0] = i[1]
                i[1] = switch
                tempfringe = list(i)
                tempfringe.pop(0)
                tempstartcities = list(currentlist[0])
                tempstartcities.append(tempfringe[0])
                tempfringe[0] = tempstartcities
                tempfringe[1] = str(float(tempfringe[1]) + float(currentlist[1]))
                tempfringe[4] = str(float(tempfringe[4]) + float(currentlist[2]))
                tempstartroutes = list(currentlist[3])
                tempstartroutes.append(tempfringe[3])
                tempfringe[3] = tempstartroutes
                if routing == "astar":
                    astarcity2 = [item[0] for item in astarcity]
                    if cost == "distance":
                        a = 1
                        b = 2
                    elif cost == "time":
                        a = 4
                        b = 5
                    if i[1] not in astarcity2:
                        tempfringe[2] = float(currentlist[4]) - float(i[b])
                    else:
                        indexcity = astarcity2.index(i[1])
                        tempfringe[2] = str(astarcity[indexcity][3])
                    newdis = float(tempfringe[2]) + float(tempfringe[a])
                    tempfringe.append(str(newdis))
                fringe.append(tempfringe)
            elif repeat == 1:
                do = "nothing"
    return (fringe)

def goalcheck(fringe, end, goal, routing):
    Tmiles = 0
    Ttime = 0
    if routing == "bfs" or routing == "dfs":
        b = 0  ## tried using infinity/blank, not working so had to duplicate code so range would do [0:] for Bfs/DFS and [0:1] for uniform
        for i in fringe[b:]:
            for j in i[0:1]:
                if j[-1] == end:
                    Tmiles = float(i[1])
                    Ttime = float(i[4])
                    goal = 1
                    #print fringe
                    print "Start in "
                    for c, r in zip(i[0],i[3]):
                        print c, "then travel on", r.strip('\n'), "to "
                    print end, ".  You have reached your final destination."
                    print ""
                    print "Total Distance in miles: ", Tmiles
                    print "Total Time in Hours: ", Ttime
                    print ""
                    printresult = str(Tmiles) + " " + str(Ttime)
                    for k in i[0]:
                        printresult = printresult + " " + k
                    print printresult

    elif routing == "uniform" or routing == "astar":
        b,e = 0,1
        for i in fringe[b:e]:
            for j in i[0:1]:
                if j[-1] == end:
                    Tmiles = float(i[1])
                    Ttime = float(i[4])
                    goal = 1
                    #print fringe
                    print "Start in "
                    for c, r in zip(i[0],i[3]):
                        print c, "then travel on", r.strip('\n'), "to "
                    print end, ".  You have reached your final destination."
                    print ""
                    print "Total Distance in miles: ", Tmiles
                    print "Total Time in Hours: ", Ttime
                    print ""
                    printresult = str(Tmiles) + " " + str(Ttime)
                    for k in i[0]:
                        printresult = printresult + " " + k
                    print printresult

    return (goal)

def newcity(fringe, currentcity, currentlist, routing):
    if routing == "dfs":
        r = -1
    else:
        r = 0
    currentlist[0] = fringe[r][0]
    currentlist[1] = fringe[r][1]
    currentlist[2] = fringe[r][4]
    currentlist[3] = fringe[r][3]
    currentlist[4] = fringe[r][2]
    currentcity = currentlist[0][-1]
    return (fringe, currentcity, currentlist)

def uniformsort(fringe, cost):
    if cost == "time":
        fringe.sort(key=lambda x: float(x[4]))  ### 1 = Miles   4 = time    ** segments is just edges, so no sort, just runs BFS
    elif cost == "distance":
        fringe.sort(key=lambda x: float(x[1]))
    return (fringe)

def astarsort(fringe, cost):
    fringe.sort(key=lambda x: float(x[5]))
    return fringe

if routing == "astar":
    for i in city:
        if i[0] == end:
            latEND = float(i[1])
            lonEND = float(i[2])
    for i in city:
        latBEG = float(i[1])
        lonBEG = float(i[2])
        if cost == "distance":
            h = coordist(latBEG, lonBEG, latEND, lonEND)
        elif cost == "time":
            h = coordist(latBEG, lonBEG, latEND, lonEND)/65
        elif cost == "segments":
            temph = coordist(latBEG, lonBEG, latEND, lonEND)
            if i[0] == end:
                h = 0
            else:
                if temph <924:
                    h = 1
                elif temph >923:
                    h = 2
        i.append(h)
        astarcity.append(i)

while goal == 0:
#c=0
#while c<10:
#    print fringe
    fringe = successor(routing, roads, currentcity, fringe, currentlist, astarcity)
#    print fringe
    if routing == "uniform":
        fringe = uniformsort(fringe, cost)
    elif routing == "astar":
        fringe = astarsort(fringe, cost)
    goal = goalcheck(fringe, end, goal, routing)
    fringe, currentcity, currentlist = newcity(fringe, currentcity, currentlist, routing)
#    print currentlist
#    c = c + 1




#elapsed = timeit.default_timer() - start_time
#print elapsed





