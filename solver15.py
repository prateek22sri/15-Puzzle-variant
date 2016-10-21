# solver15.py : Solve the 15-Puzzle problem!
# Prateek Srivastava, September 2016
#Variant of the 15-puzzle, but with the following important change: when the empty tile is
#on the edge of the board, the tile on the opposite side of the board can be slid into the opening.
#The goal of the puzzle is tofind the shortest possible sequence of moves that restores the canonical configuration
#given an initial board configuration provided in a text file called "input.txt" by the user.

#The heuristic function I tried was number of misplaced tiles, manhattan distance without considering the variation of circularity,
#and manhattan distance along with the variation. Misplaced tiles was very slow, however, Manhattan distance (with the variation) without the cost function
#gave a faster solution but the solution was not optimal. The manhattan distance when used with the cost function behaves like a BFS if the goal state is at
#a worst case which makes it very slow for a few inputs. To optimize that I even tried to find out a solution by implementing A* search by recursively limiting
# the depth of the tree similar to the IDS.
# In the end the best possible solution I found was Manhattan Distance of a tile considering the circularity along with the cost function.

from sys import argv
from copy import deepcopy
#import time

#start_time = time.time()
filename = argv[1]

#reads the text file and converts string to a list
def initial_state(filename):
    filename = argv[1]
    text=open(filename)
    lines=[]
    for line in text:
        lines.append(line.split())
    for row in range(0,4):
        for col in range(0,4):
            lines[row][col]=int(lines[row][col])
    return lines

#prints the board in human readable format
def printable_board(board):
    b=""
    for row in board:
        for col in row:
            if col>9:
                b= b+ str(col) +"   "
            else:
                b= b+ str(col) +"    "
        b=b+ "\n"
    return b


#successor function
def successor(board):
    child = 0
    successor_boards = []
    temp1 = deepcopy(board)
    temp2 = deepcopy(board)
    temp3 = deepcopy(board)
    temp4 = deepcopy(board)
    for row in range(0, 4):
        for col in range(0, 4):
            if board[0][row][col] == 0 and child < 4:

                # movement up
                if row == 3:
                    a = board[0][row][col]
                    b = board[0][0][col]
                    a, b = b, a
                    temp1[0][row][col] = a
                    temp1[0][0][col] = b
                    log=temp1[1]
                    log.append('U')
                    successor_boards.append([temp1[0],log])
                    child += 1
                else:
                    a = board[0][row][col]
                    b = board[0][row + 1][col]
                    a, b = b, a
                    temp1[0][row][col] = a
                    temp1[0][row + 1][col] = b
                    log=temp1[1]
                    log.append('U')
                    successor_boards.append([temp1[0],log])
                    child += 1

                # movement down
                if row == 0:
                    a = board[0][row][col]
                    b = board[0][3][col]
                    a, b = b, a
                    temp2[0][row][col] = a
                    temp2[0][3][col] = b
                    log=temp2[1]
                    log.append('D')
                    successor_boards.append([temp2[0],log])
                    child += 1
                else:
                    a = board[0][row][col]
                    b = board[0][row - 1][col]
                    a, b = b, a
                    temp2[0][row][col] = a
                    temp2[0][row - 1][col] = b
                    log=temp2[1]
                    log.append('D')
                    successor_boards.append([temp2[0], log])
                    child += 1

                # movement left
                if col == 3:
                    a = board[0][row][col]
                    b = board[0][row][0]
                    a, b = b, a
                    temp3[0][row][col] = a
                    temp3[0][row][0] = b
                    log = temp3[1]
                    log.append('L')
                    successor_boards.append([temp3[0], log])
                    child += 1
                else:
                    a = board[0][row][col]
                    b = board[0][row][col + 1]
                    a, b = b, a
                    temp3[0][row][col] = a
                    temp3[0][row][col + 1] = b
                    log = temp3[1]
                    log.append('L')
                    successor_boards.append([temp3[0], log])
                    child += 1

                # movement right
                if col == 0:
                    a = board[0][row][col]
                    b = board[0][row][3]
                    a, b = b, a
                    temp4[0][row][col] = a
                    temp4[0][row][3] = b
                    log = temp4[1]
                    log.append('R')
                    successor_boards.append([temp4[0], log])
                    child += 1
                else:
                    a = board[0][row][col]
                    b = board[0][row][col - 1]
                    a, b = b, a
                    temp4[0][row][col] = a
                    temp4[0][row][col - 1] = b
                    log = temp4[1]
                    log.append('R')
                    successor_boards.append([temp4[0], log])
                    child += 1
    return successor_boards

#check goal state
def is_goal(board):
    if board==goal_board:
        return True

#calculate manhattan distance of two numbers (row numbers/column numbers)
def get_element_distance(a,b):
    if a==0 and b==0:
        return 0
    elif a==1 and b==0:
        return 1
    elif a==2 and b==0:
        return 2
    elif a==3 and b==0:
        return 1

    elif a==0 and b==1:
        return 1
    elif a==1 and b==1:
        return 0
    elif a==2 and b==1:
        return 1
    elif a==3 and b==1:
        return 2

    elif a==0 and b==2:
        return 2
    elif a==1 and b==2:
        return 1
    elif a==2 and b==2:
        return 0
    elif a==3 and b==2:
        return 1

    elif a==0 and b==3:
        return 1
    elif a==1 and b==3:
        return 2
    elif a==2 and b==3:
        return 1
    elif a==3 and b==3:
        return 0

# gives manhattan distance of the board
def get_board_distance(board):
    map = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0),(3, 1), (3, 2), (3, 3)]
    distance = 0
    for r in range(0, 4):
        for c in range(0, 4):
            if board[r][c]!=0:
                row = map[board[r][c] - 1][0]
                col = map[board[r][c] - 1][1]
                distance = distance + get_element_distance(row, r) + get_element_distance(col, c)
    return distance

#poping of fringe based on f(s) i.e. heuristic and the cost function
def fringe_pop(fringe):
    ind=0
    fos=999999999999
    for f in fringe:
        if f[2]< fos:
            fos=f[2]
            ind=fringe.index(f)
    return fringe.pop(ind)

#appends the fringe with a successor of minimum heuristics
def fringe_append(successor_boards,fringe,popped_elements):
    fos = 999999999999
    for s in range(0,4):
        add=1
        cos=len(successor_boards[s][1])
        hos = get_board_distance(successor_boards[s][0])
        #fos_current=hos+cos
        fos_current=hos+cos
        successor_boards[s]=[successor_boards[s][0],successor_boards[s][1],fos_current]
        for elements in popped_elements:
            if successor_boards[s][0]==elements[0]:
                add=0
        if add==1:
            fringe.append(successor_boards[s])

#checks the permutation inversion to check whether the start state is solvable or not
def check_parity(board):
    pi=0
    for row in range(0,4):
        for col in range(0,4):
            pi_current=0
            if board[row][col]==0:
                pi_current+=row
            for r in range(0,4):
                for c in range(0,4):
                    if (((r>row) or (c>col and r==row)) and board[row][col]>board[r][c] and board[row][col]!=0 and board[r][c]!=0):
                        pi_current+=1
            pi+=pi_current
    if pi%2==0:
        return True
    else:
        return False

############## PROGRAM EXECUTION ##################
board=initial_state(filename)
goal_board=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]

print "The program will try to solve a solution for the following board: \n"
print printable_board(board)
print "\nFinding a solution ...\n"
if check_parity(board)==True:
    print "failed !!!! no solution possible"
    print "%f minutes" % ((time.time() - start_time) / 60)
    exit(1)
else:
    fringe=[]
    temp=[]
    log=[]
    fos=0           #f(s) -> sum of cost function and heuristic function
    popped_elements=[]
    if is_goal(board):
        print "Eureka !!! Found the solution"
        print printable_board(board)
        print "initial state is the goal state"
        #print "%f minutes" % ((time.time() - start_time) / 60)
        exit(0)
    fos=get_board_distance(board)
    fringe.append([board,log,fos])

    while 1:
        if fringe == []:
            print "failed !!!! no solution found"
            #print "%f minutes" % ((time.time() - start_time) / 60)
            exit(1)
        else:
            s=fringe_pop(fringe)
            popped_elements.append(s)
            if s:
                if is_goal(s[0]):
                    print "Eureka !!! Found the solution"
                    print printable_board(s[0])
                    print ''.join(a+' ' for a in s[1])
                    #print "%f minutes" % ((time.time() - start_time) / 60)
                    exit(0)
                else:
                    successor_boards=successor(s)
                    fringe_append(successor_boards,fringe,popped_elements)