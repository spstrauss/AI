# put your 15 puzzle solver here!

# print the original board configuration
fname = open(sys.argv[1],"r")
fname = fname.readlines()
for line in fname:
    lst = line
    print (lst)
    
    
# compare two list (current state against goal state)
def complst(state,goal):
    print [x for x, y in goal(state,goal) if x == y]
    print (x,y)
    return

# iterate through the list and change the order of the items in the list

state = [1,2,3,4,
         5,6,7,8,
         9,10,0,12,
         13,14,15,11]

move = True
mcount = 0


# sort until move = false
while move: 
    move = False

    # loop entire list
    # changes move to True if a move was made
    # prints the number of moves made to get to the goal state
    
    for i in range(len(state) -1): 
        stemp = state[i]
        k = i + 1
        if state[i] > state[k]:
            mcount = mcount + 1
            print ("Move", mcount)
            state[i] = state[k]
            state[k] = stemp
            move = True 

print k
print (move)
print state
