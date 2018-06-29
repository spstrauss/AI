# put your group assignment problem here!
#This one was tricky for me. What threw me off most was that the goal node was undefined or unknown to me, so was hard to implement similar ideas I used in q1.
#Essentially, i create a random starting node (a list of single person groups) by randomizing the order of the users to come up with unique nodes.  
#For the first one, I pop off the first user and put him into a "fringe", then try to figure out if putting the user into another group saves more time.  I have it pick the one that saves the most time, then compare it back to the original node it was at and see which one's time is less. 
#I pick the lower time as the new node, make sure the group that this popped off user was added to (or put back into) is then moved to the end of the list, then redo it again with the next group.
#I continue to do this until I go through the lists multiple times with out saving anymore time (essntially now having the lowest possible time from the initial starting node) and save it as a possible solution.
#I then repeat the process (creating a new randomized starting node and shuffling users around to create perhaps a lower time) 6000 times (or until the time it takes to run this program -stoploop- exceeds (number of users)/6)**1.8 + 5.  I have run this for a longer time to come up with better numbers, but also want to be cautious of your time running this program, as the whole premise of this problem may suggest :)
#As the process keeps repeating, any exhausted nodes becomes a possible solution that gets compared to the prior solution.  If it's better, it becomes the new solution.  If not, it is deleted and process is repeated again.
#My code seems to run a long time compared to others, so this may not be the most optimal approach, but was the best I could come up with given the time and missing partner.

import sys
import operator
import random
import timeit
start_time = timeit.default_timer()

#k = 10
#n = 10
#m = 31

k = int(sys.argv[2])
m = int(sys.argv[3])
n = int(sys.argv[4])



################################## Getting class input in list
clist = []
#listfile = open('input.txt',"r")
listfile = open(sys.argv[1],"r")
listlines = listfile.readlines()
for i in listlines:
    listtemp = i.split(' ')
    clist.append(listtemp)
##################################
#Creating separate lists to reference for each users preference
prefS = [] #preference size
prefY = [] #preference of students to work with
prefN = [] #preference of students NOT to work with


glist = [] # will be the group list
ulist = [] # a list of users, used for indexing the preference lists
fringe = [] # used to pop off the first user in the first group and keep track of the list

### Creating preference lists
for i in clist:
    ulist.append(i[0])
    prefS.append([i[0],i[1]])
    if ',' in i[2]:
        Ysplit = i[2].split(',')
    elif '_' in i[2]:
        Ysplit = []
    else:
        Ysplit = [i[2]]
    prefY.append([i[0],Ysplit])
    notemp = i[3].strip('\n')
    if ',' in notemp:
        Nsplit = notemp.split(',')
    elif '_' in notemp:
        Nsplit = []
    else:
        Nsplit = [notemp]
    prefN.append([i[0],Nsplit])

#determine # of groups and time to grade
def timestats_allgroups(glist,ulist,k,prefS,prefY,n,prefN,m):
    kvalue = 0
    svalue = 0
    yvalue = 0
    nvalue = 0
    kvalue = len(glist) * k
    for i in glist:
        s = len(i)  #size of group
        for j in i: # for each user
            ps = prefS[ulist.index(j)][1] #preference size of user
            if ps == "0" or ps == str(s): #if no pref or pref matched
                do = "nothing"
            else:
                svalue = svalue + 1

            pY = prefY[ulist.index(j)][1]# preference partner of user
            if not pY: # if no preference
                do = "nothing"
            else:
                for yi in pY:
                    if yi not in i:
                        yvalue = yvalue + n

            pN = prefN[ulist.index(j)][1]# preference "I don't want this" partner of user
            if not pN: # if no preference
                do = "nothing"
            else:
                for ni in pN:
                    if ni in i:
                        nvalue = nvalue + m
    return(kvalue,svalue,yvalue,nvalue)

#determine time to grade for a specific group
def timestats_ind(fringe,ulist,k,prefS,prefY,n,prefN,m):
    kind = 0
    sind = 0
    yind = 0
    nind = 0
    if len(fringe) == 1:
        kind = k
    s = len(fringe)  #size of group
    for j in fringe:
            ps = prefS[ulist.index(j)][1] #prefernce size of user
            if ps == "0" or ps == str(s): #if no pref or pref matched
                do = "nothing"
            else:
                sind = sind + 1

            pY = prefY[ulist.index(j)][1]# prefernce partner of user
            if not pY: # if no preference
                do = "nothing"
            else:
                for yi in pY:
                    if yi not in fringe:
                        yind = yind + n

            pN = prefN[ulist.index(j)][1]# prefernce "I don't want this" partner of user
            if not pN: # if no preference
                do = "nothing"
            else:
                for ni in pN:
                    if ni in fringe:
                        nind = nind + m
    return(kind,sind,yind,nind)

#Creates initial group where each group is one person group, randomly assigned by order
shufflelist = list(ulist)
random.shuffle(shufflelist)
for i in shufflelist:
    a = list([i])
    glist.append(a)

#Creates initial group with 3 in each (unless the list is not divisible by 3, then the last group will have the remainder)
### Whenever I tried implementing start lists wih 3 each, I kept running into an issue where the final group lists had more than 3 people in them.
### I found this to be a better way to find the minimum time (since it is starting from a different node), but due to the problem I was having
### with more than 3 into the group, I had to abandon this way of search.

#glist = list(shufflelist)
#glist = [shufflelist[i:i+3] for i in range(0, len(shufflelist), 3)]



bestTime = float('inf')

### Way of making sure the loop doesn't go on forever and ends it in a reasonable amount of time.  For me, the longer it went, the better groups
### I ended up finding, but I also want to be courteous of your time when running/grading this program
### The best way I found to implement this was by randomly generating a state and seeing if there are any better successors to go off of it.  I realize when
### only running it once, it can lead to a dead end state that is not desirable, so I re-generate another state and run again multiple times and keep the best state found.
### This may not be the most ideal way to run this program but was the best way I could think of coding this problem.

loopcounter = 0
stop = len(ulist)
stoploop = float(float(stop)/6)**1.8 + 5
if stoploop < 1:
    stoploop = 1

while loopcounter<6000:
    kvalue, svalue, yvalue, nvalue = timestats_allgroups(glist, ulist, k, prefS, prefY, n, prefN, m)
    totalTotCheck = kvalue + svalue + yvalue + nvalue
    oldTotalCheck = totalTotCheck

    counter = 0
    while counter<(stop+1)*3:
        fringe = glist[0]
        kind, sind, yind, nind = timestats_ind(fringe, ulist, k, prefS, prefY, n, prefN, m)
        totalIndCheck = kind + sind + yind + nind

        ## pop off first user in first group, mark him as x
        x = glist[0][0]
        glist[0].pop(0)
        if len(glist[0]) == 0:
            glist.pop(0)


        templist = []
        templist = [q[:] for q in glist]
        tempIndCheckList = []

        ## Figure out which group popped off user is in based on min time
        for i in templist:
            if len(i) <3:
                i.append(x)
                #run stats of individual groups
                kind, sind, yind, nind = timestats_ind(i, ulist, k, prefS, prefY, n, prefN, m)
                tempIndCheck = kind + sind + yind + nind
            else:
                tempIndCheck = float('inf')
            tempIndCheckList.append(tempIndCheck)
        min_index, min_value = min(enumerate(tempIndCheckList), key=operator.itemgetter(1))

        ## New state; Figure out time stats on the original fringe group now without the user
        kf, sf, yf, nf = timestats_ind(glist[0], ulist, k, prefS, prefY, n, prefN, m)
        totalFringeInd = kf + sf + yf + nf
        ## Prior state; Figure out the old time stats on the group fringe user now joined
        kminOld, sminOld, yminOld, nminOld = timestats_ind(glist[min_index], ulist, k, prefS, prefY, n, prefN, m)
        totalMinOldInd = kminOld + sminOld + yminOld + nminOld


        NewValue = min_value + totalFringeInd      #New state; new group user joined stats + fringe group user left
        OldValue = totalMinOldInd + totalIndCheck  #Old state;  group user joined stats before joining + fringe group before user left

        ## New state; if popped off user is in group by themselves
        ksingle, ssingle, ysingle, nsingle = timestats_ind([x], ulist, k, prefS, prefY, n, prefN, m)
        singleValue = ksingle + ssingle + ysingle + nsingle
        SinValue = totalFringeInd + totalMinOldInd + singleValue  #New state; fringe group user left + group user joined stats before joining + single group

        if NewValue <= SinValue:
            if NewValue <= OldValue:   #new state (grouped) better
                glist[min_index].append(x)
                moving = list(glist[min_index])
                glist.pop(min_index)
                glist.append(moving)
            else:
                glist[0].append(x)     #old state better
                moving = list(glist[0])
                glist.pop(0)
                glist.append(moving)

        else:
            if OldValue <= SinValue:   #old state better
                glist[0].append(x)
                moving = list(glist[0])
                glist.pop(0)
                glist.append(moving)
            else:
                glist.append([x])     #new state (single) better

        #New total for all groups
        #print glist
        kvalue,svalue,yvalue,nvalue = timestats_allgroups(glist,ulist,k,prefS,prefY,n,prefN,m)
        totalTotCheck = kvalue + svalue + yvalue + nvalue

        #if new total is the same as old total (essentially, if there's no change), add 1 to the counter.  If we are in
        #a state that is good and the program won't change, then this counter will grow to the threshold that will break
        #this while loop
        if oldTotalCheck == totalTotCheck:
            counter = counter + 1
        else:
            counter = 0  #if it found a better way to group, then let is keep going through the list of users again
        oldTotalCheck = totalTotCheck
        loopElapsed = timeit.default_timer() - start_time
        if loopElapsed > .5:
            break  # breaking the loop if it's taking too much time


    if totalTotCheck < bestTime:  # keep track of new best time/group
        bestTime = totalTotCheck
        bestGlist = list(glist)
        #print bestTime, " - ", bestGlist
    loopcounter = loopcounter + 1

    #re-generate new list and try to find better successors again
    glist = []
    random.shuffle(shufflelist)
    for i in shufflelist:
        a = list([i])
        glist.append(a)
    #glist = list(shufflelist)
    #glist = [shufflelist[i:i+3] for i in range(0, len(shufflelist), 3)]
    loopElapsed = timeit.default_timer() - start_time
    if loopElapsed > stoploop:
        break  #breaking the loop if it's taking too much time


print('\n'.join(' '.join(map(str, i)) for i in bestGlist))

print bestTime


elapsed = timeit.default_timer() - start_time


#print elapsed


