#str = input()
import time
print()


print("please enter sudoku size (9 or 16): ", end=" ")
size1 = int(input())
size2 = int(size1**0.5)

print("please enter the sudoku in this way: number, space, number. For blank square write zero. ")
print("Example:")
print()
print("1 0 0 0 0 7 0 9 0")
print("0 3 0 0 2 0 0 0 8")
print("0 0 9 6 0 0 5 0 0")
print("0 0 5 3 0 0 9 0 0")
print("0 1 0 0 8 0 0 0 2")
print("6 0 0 0 0 4 0 0 0")
print("3 0 0 0 0 0 0 1 0")
print("0 4 0 0 0 0 0 0 7")
print("0 0 7 0 0 0 3 0 0")

print()
print()
print()
print("Now your sudoku:")
print()



optionsColl = [[(size1) for i in range(size1)] for j in range(size1)]
optionsRow = [[(size1) for i in range(size1)] for j in range(size1)]
optionSquare = [[[(size1) for i in range(size1)] for j in range(size2)]for z in range(size2)]

rows = [[False] * size1 for _ in range(size1)]
columns = [[False] * size1 for _ in range(size1)]
boxes = [[[False] * size1 for _ in range(size2)] for _ in range(size2)]

count = 0
arr1 = [input().split() for i in range(size1)]

class cell:
    def __init__(self):
        self.value = 0
        self.boolArr = [False for i in range(size1)]
        self.fixed = False
        self.chacked = False
        
    def isItKnown(self):
        count = 0
        for i in self.boolArr:
            if i == True:
                count += 1
        if (count == size1 - 1):
            for i in range(size1):
                if self.boolArr[i] == False:
                    self.value = i+1
                    for z in range(size1):
                        self.boolArr[z] = True
        return count == size1 - 1
            
arr = [[cell() for i in range(size1)] for j in range(size1)]

def fill(i, j):
    rows[i][arr[i][j].value-1] = True
    columns[j][arr[i][j].value-1] = True
    boxes[(i - i%size2)//size2][(j - j%size2)//size2][arr[i][j].value-1] = True
    
def fill2(i, j, value):
    optionsColl[j][value] -= 1
    optionsRow[i][value] -= 1
    optionSquare[(i - i%size2)//size2][(j - j%size2)//size2][value] -= 1 

for i in range(size1):
    for j in range(size1):
        arr[i][j].value = int(arr1[i][j])
        if arr[i][j].value != 0:
            fill(i,j)
            for z in range(len(arr[i][j].boolArr)):
                arr[i][j].boolArr[z] = True
                fill2(i, j, z)

def remove(i, j, x):
    rows[i][x] = False
    columns[j][x] = False
    boxes[(i - i%size2)//size2][(j - j%size2)//size2][x] = False

def solve0(i, j):
    arr[i][j].fixed = True
    if arr[i][j].value != 0:
        for x in range(size1):
            if(not arr[i][x].boolArr[arr[i][j].value - 1]):
                arr[i][x].boolArr[arr[i][j].value - 1] = True
                fill2(i,x,arr[i][j].value - 1)

            if (not arr[i][x].fixed):
                if (arr[i][x].isItKnown()):
                    fill(i, x)
                    solve0(i, x)
            
            if(not arr[x][j].boolArr[arr[i][j].value - 1]):
                arr[x][j].boolArr[arr[i][j].value - 1] = True
                fill2(x,j,arr[i][j].value - 1)
         
            if (not arr[x][j].fixed):
                if (arr[x][j].isItKnown()):
                    fill(x, j)
                    solve0(x, j)

        for m in range(size2):
            for n in range(size2):
                if(not arr[m + i - i%size2][n + j - j%size2].boolArr[arr[i][j].value - 1]):
                    arr[m + i - i%size2][n + j - j%size2].boolArr[arr[i][j].value - 1] = True
                    fill2(m + i - i%size2, n + j - j%size2, arr[i][j].value - 1)
                    
                if (not arr[m + i - i%size2][n + j - j%size2].fixed):
                    if (arr[m + i - i%size2][n + j - j%size2].isItKnown()):
                        fill(m + i - i%size2, n + j - j%size2)
                        solve0(m + i - i%size2, n + j - j%size2)
                               
def solve1():
    for i in range(size1):
        for x in range(size1):
            if optionsRow[i][x] == 1:
                for j in range(size1):
                    if not arr[i][j].boolArr[x] and not arr[i][j].fixed:
                        arr[i][j].value = x + 1
                        for z in range(size1):
                            if (not arr[i][j].boolArr[z]):
                                arr[i][j].boolArr[z] = True
                                fill2(i, j, z)
                        fill(i,j)
                        solve0(i,j)
                        solve1()
                        return
            if optionsColl[i][x] == 1:
                for j in range(size1):
                    if not arr[j][i].boolArr[x] and not arr[j][i].fixed:
                        arr[j][i].value = x + 1
                        for z in range(size1):
                            if (not arr[j][i].boolArr[z]):
                                arr[j][i].boolArr[z] = True
                                fill2(j, i, z)
                        fill(j,i)
                        solve0(j,i)
                        solve1()
                        return
                        
            if optionSquare[i//size2][i%size2][x] == 1:
                for m in range(size2):
                    for n in range(size2):
                        row = (i - i%size2) + m
                        col = (size2*(i%size2)) + n
                        if not arr[row][col].boolArr[x] and not arr[row][col].fixed:
                            arr[row][col].value = x + 1
                            for z in range(size1):
                                if (not arr[row][col].boolArr[z]):
                                    arr[row][col].boolArr[z] = True
                                    fill2(row, col, z)
                            fill(row, col)
                            solve0(row, col)
                            solve1()
                            return


def isOkTotal():
    if (not isFull()):
        return False
    for i in range(size1):
        for j in range(size1):
            if (arr[i][j].value != 0):
                if (any(arr[i][m].value == arr[i][j].value for m in range(0,j)) or any(arr[i][m].value == arr[i][j].value for m in range(j + 1,len(arr[i])))):
                    return False
                if any(arr[i1][j].value == arr[i][j].value for i1 in range(0,i)) or any(arr[i2][j].value == arr[i][j].value for i2 in range(i+1, size1)):
                    return False
    for n in range(size2):
        for m in range(size2):
            for i in range(size2):
                for j in range(size2):
                    if arr[n*size2 + i][m*size2 + j].value != 0:
                        temp = arr[n*size2 + i][m*size2 + j].value
                        arr[n*size2 + i][m*size2 + j].value = 0
                        for k in range(size2):
                            if (any(arr[n*size2 + k][p].value == temp for p in range(m*size2,(m*size2)+size2))):
                                arr[n*size2 +i][m*size2 +j].value = temp
                                return False                             
                        arr[n*size2 +i][m*size2 +j].value = temp
    return True


def isOk(row, col):
    if (rows[row][arr[row][col].value - 1]):
        return False
    if (columns[col][arr[row][col].value - 1]):
        return False
    if (boxes[(row - row%size2)//size2][(col - col%size2)//size2][arr[row][col].value - 1]):
        return False
    return True

def isFull():
    for i in range(size1):
        for j in range(size1):
            if arr[i][j].value == 0:
                return False
    return True

def copy(optionsRow, optionsColl, optionSquare, rows, columns, boxes, arr):
    _arr = [[cell() for i in range(size1)] for j in range(size1)]
    _optionsColl = [[(size1) for i in range(size1)] for j in range(size1)]
    _optionsRow = [[(size1) for i in range(size1)] for j in range(size1)]
    _optionSquare = [[[(size1) for i in range(size1)] for j in range(size2)]for z in range(size2)]
    _rows = [[False] * size1 for _ in range(size1)]
    _columns = [[False] * size1 for _ in range(size1)]
    _boxes = [[[False] * size1 for _ in range(size2)] for _ in range(size2)]
    for i in range(size1):
        for j in range(size1):
            _optionsRow[i][j] = optionsRow[i][j]
    for i in range(size1):
        for j in range(size1):
            _optionsColl[i][j] = optionsColl[i][j]
    
    for i in range(size2):
        for j in range(size2):
            for z in range(size1):
                _optionSquare[i][j][z] = optionSquare[i][j][z]        

    for i in range(size1):
        for j in range(size1):
            _rows[i][j] = rows[i][j]
            
    for i in range(size1):
        for j in range(size1):
            _columns[i][j] = columns[i][j]
            
    for i in range(size2):
        for j in range(size2):
            for z in range(size1):
                _boxes[i][j][z] = boxes[i][j][z]        
            
    for i in range(size1):
        for j in range(size1):
            _arr[i][j].value = arr[i][j].value 
            _arr[i][j].fixed = arr[i][j].fixed
            _arr[i][j].chacked = arr[i][j].chacked
            for z in range(size1):
                _arr[i][j].boolArr[z] = arr[i][j].boolArr[z]

    return (_optionsRow, _optionsColl, _optionSquare, _rows, _columns, _boxes, _arr)

def Next():
    min = size1 + 1
    _i = 0
    _j = 0
    count1 = size1
    for i in range(size1):
        for j in range (size1):
            if not arr[i][j].fixed:
                count1 = size1
                for r in arr[i][j].boolArr:
                    if r:
                        count1 -= 1
                if (count1 < min) and (count1 != 0) and not (arr[i][j].chacked):
                    _i = i
                    _j = j
                    min = count1
    arr[_i][_j].chacked = True
    if (count1 == size1 + 1):
        return(_i, _j, True)
    return(_i, _j, False)
    
def solve(i, j, i1, j1):
    global optionsRow
    global optionsColl
    global optionSquare
    global rows
    global columns
    global boxes
    global arr
    
    if (arr[i][j].value != 0):
        if isOkTotal():
            return True
        return False
    
    _optionsRow, _optionsColl, _optionSquare, _rows, _columns, _boxes, _arr = copy(optionsRow, optionsColl, optionSquare, rows, columns, boxes, arr)
    
    global count
    if count%100 == 0 and count != 0:
        print (count, " recursive calls")
    
    if (i == size1):
        return True
    
    if (j1 != -1):
        solve0(i1, j1)
        solve1()
        
    count += 1  
    while (arr[i][j].value != 0):
        fill(i, j)
        row, col, finish = Next()
        if finish:
            if isOkTotal():
                return True
            return False
        else:
            if (solve(row, col, i, j)):
                return True
            optionsRow, optionsColl, optionSquare, rows, columns, boxes, arr = copy(_optionsRow, _optionsColl, _optionSquare, _rows, _columns, _boxes, _arr)
            return False
    
    if (arr[i][j].value == 0):
        arr[i][j].fixed = True
        while (arr[i][j].value < size1):
            arr[i][j].value += 1
            if (not arr[i][j].boolArr[arr[i][j].value - 1]):
                if isOk(i, j):
                    fill(i, j)
                    row, col, finish = Next()
                    if finish:
                        if isOkTotal():
                            return True
                    else:
                        if (solve(row, col, i, j)):
                            return True
                    remove(i, j, arr[i][j].value-1)
        optionsRow, optionsColl, optionSquare, rows, columns, boxes, arr = copy(_optionsRow, _optionsColl, _optionSquare, _rows, _columns, _boxes, _arr)
        
        return False

print("")
print("")


start_time = time.time()

print("Stage one: ")
for i in range(size1):
    for j in range(size1):
        if(arr[i][j].value != 0 and not arr[i][j].fixed):
            solve0(i,j)
            
for i in arr:
    for j in i:
        print(j.value, end=' ')
    print("")
print("")

print("")
print("")
print("Stage two: ")
solve1()

for i in arr:
    for j in i:
        print(j.value, end=' ')
    print("")
print("")

if not isOkTotal():
    print("Stage three: ")
    row, col, _ = Next()
    solve(row,col, -1, -1)
    print (count, " recursive calls")
    print("")
    print("")
    for i in range(size1):
        for j in range(size1):
            print(arr[i][j].value, end=' ')
        print("")
    print("")
    print(isOkTotal())
    print("")

print("--- %s seconds ---" % (time.time() - start_time))
print ("")
print ("press enter to exit")

stop = input()

''' hard 25*25 sudoku (approximate 878 seconds --- 23840 recursive calls):
2 0 0 25 9 0 16 0 20 0 5 0 14 0 0 4 0 8 0 0 0 0 7 17 0
0 0 0 24 0 2 0 0 25 0 15 16 3 20 0 0 0 14 1 10 0 22 8 6 12
0 0 6 0 0 0 7 17 24 19 2 0 0 25 0 15 16 0 20 0 5 0 0 1 10
0 0 1 0 5 0 0 6 12 4 23 0 0 0 19 0 0 0 25 9 15 16 0 0 0
16 0 0 11 15 0 0 1 0 5 0 8 0 0 4 23 7 17 0 0 0 0 13 25 9
0 0 0 0 0 11 15 16 3 0 10 0 0 0 1 12 0 0 0 6 0 19 0 7 17
0 0 7 17 24 0 2 0 0 0 0 0 16 3 0 0 5 18 14 0 12 0 22 0 0
0 22 0 0 0 0 23 7 0 24 0 2 21 0 0 0 15 16 0 0 10 5 0 0 0
5 0 0 0 0 0 22 8 6 0 0 0 7 0 0 0 0 0 13 0 0 15 0 0 20
0 16 0 0 0 5 18 14 0 0 0 22 0 6 0 19 0 7 17 24 0 0 0 0 25
0 0 2 0 13 0 0 0 16 3 0 0 5 18 14 6 0 4 22 8 0 0 0 0 7
24 19 23 0 17 25 0 2 21 0 0 0 15 0 0 0 10 0 18 14 6 0 4 0 8
12 0 0 0 0 24 19 23 7 0 0 9 0 21 0 0 0 15 16 3 1 10 0 0 14
10 0 0 0 1 12 4 22 8 6 24 0 23 7 0 0 9 0 21 0 0 11 15 16 0
11 15 0 3 0 10 5 0 0 0 12 4 0 8 0 0 0 23 7 17 25 9 2 21 0
0 25 0 0 21 0 0 11 15 0 14 1 10 5 0 8 0 12 0 0 0 17 24 19 0
17 24 19 23 0 13 0 9 2 0 3 0 11 15 0 0 1 0 5 0 8 0 0 4 22
6 12 4 0 0 0 24 19 0 0 0 0 0 2 0 3 20 11 15 0 14 00 10 0 18
0 0 5 0 0 6 12 0 0 0 0 24 0 23 7 0 25 0 2 0 3 0 0 15 16
20 11 0 16 0 1 0 5 18 14 6 12 4 22 8 17 0 19 0 7 0 0 9 2 21
0 13 25 0 0 0 3 20 11 15 0 0 1 10 0 0 0 0 12 0 0 7 0 24 0
7 17 0 19 0 0 13 25 9 0 0 0 0 0 0 0 0 1 0 0 22 0 6 0 4
0 6 12 0 0 0 17 24 19 23 21 0 0 0 2 0 3 20 11 0 18 14 1 10 0
0 0 0 5 0 0 6 0 4 22 0 17 24 19 0 0 13 25 0 0 0 3 20 0 15
0 20 11 0 16 14 0 10 5 0 8 0 0 0 0 7 17 24 0 23 0 0 25 9 2
'''

''' easy 16*16 sudoku (approximate 0.12 seconds --- 1 recursive calls): 
0 15 0 1 0 2 10 14 12 0 0 0 0 0 0 0 
0 6 3 16 12 0 8 4 14 15 1 0 2 0 0 0 
14 0 9 7 11 3 15 0 0 0 0 0 0 0 0 0 
4 13 2 12 0 0 0 0 6 0 0 0 0 15 0 0 
0 0 0 0 14 1 11 7 3 5 10 0 0 8 0 12 
3 16 0 0 2 4 0 0 0 14 7 13 0 0 5 15 
11 0 5 0 0 0 0 0 0 9 4 0 0 6 0 0 
0 0 0 0 13 0 16 5 15 0 0 12 0 0 0 0 
0 0 0 0 9 0 1 12 0 8 3 10 11 0 15 0 
2 12 0 11 0 0 14 3 5 4 0 0 0 0 9 0 
6 3 0 4 0 0 13 0 0 11 9 1 0 12 16 2 
0 0 10 9 0 0 0 0 0 0 12 0 8 0 6 7 
12 8 0 0 16 0 0 10 0 13 0 0 0 5 0 0 
5 0 0 0 3 0 4 6 0 1 15 0 0 0 0 0 
0 9 1 6 0 14 0 11 0 0 2 0 0 0 10 8 
0 14 0 0 0 13 9 0 4 12 11 8 0 0 2 0 
'''
''' medium 16*16 sudoku (approximate 3.05 seconds --- 222 recursive calls): 
 0  3  2  0  0  8  1  0  0  9 12  0  0 11  4 15 
 0  0  0  0  0  0  0 16  3  0  0  0  0  0  0  0 
 4  9  0  0 15  0  0  5  7  0  0  6  0  0  8  3 
13  0  0 16  0  0 12  0  0  8 11  0  2  9  0  0 
 9  0 14  0  6  7  0  3 11  0  5 10  0 15  0  0 
 0  0  4  0  0  0  9  0  0  1  0  0  0  2  0  0 
 2 13  0  0 11  0 15  0  0  7  0  4  0  0 14 16 
 0  0 11  8 13 16  0  0  6  0  3 14  7  0  0  0 
 0  0  0  2 12  4  0 11  0  0  7 15  9  0  0  0 
 8  5  0  0 16  0  3  0  0  0  0 12  0  0  2  7 
 0  0  9  0  0  0  7  0  0 10  0  0  0  5  0  0 
16  0  1  0 14  5  0  2  4  0  8  0  0  0  0 11 
 0  0 12 13  0 14  8  0  0  0 15  0  3  1  0  0 
11  8  0  0  0  0  0  4 10  0  0  7  0  0 15 14 
 0  0  0  0  0  0  0 12  9  0  0  0  0  0  0  0 
 7  0 15  0  0 11  5  0  0 14  4  0  0 12 13  0 
'''
''' very hard, tricky and extreme shit, 16*16 sudoku (approximate 20 seconds --- 1668 recursive calls): 
11 0 5 0 0 12 0 0 13 0 0 10 0 0 0 0
0 13 0 0 0 0 5 0 1 0  14 0 2 0 0 0
0 0 0 9 0 0 0 2 0 5 0 0 14 0 7 0
4 0 12 0 8 0 0 0 0 0 0 16 0 10 0 0
0 9 0 11 0 0 4 0 3 6 0 0 0 0 0 7
6 0 8 0 10 13 0 16 0 0 11 0 15 0 9 0
0 3 0 0 0 0 2 0 15 0 0 0 0 13 0 1
16 0 0 2 0 1 0 5 0 14 0 8 0 0 0 0
0 0 16 0 13 4 0 0 0 0 0 0 0 0 12 0
0 0 10 3 0 7 0 0 5 0 16 0 9 0 0 15
15 0 11 0 1 0 0 9 0 2 0 3 0 4 0 0
0 0 0 0 0 0 8 0 0 0 4 0 10 0 0 0
2 0 4 0 0 0 0 0 0 0 0 12 0 0 5 0
0 12 0 13 0 0 0 1 0 0 10 0 0 3 0 8
8 0 9 0 4 0 3 0 0 7 0 0 11 0 13 0
0 5 0 14 0 0 0 11 0 0 1 6 0 0 0 10
'''
''' easy 9*9 sudoku (approximate 0.08 seconds --- 0 recursive calls): 
7 9 0 0 0 0 3 0 0
0 0 0 0 0 6 9 0 0
8 0 0 0 3 0 0 7 6
0 0 0 0 0 5 0 0 2
0 0 5 4 1 8 7 0 0
4 0 0 7 0 0 0 0 0
6 1 0 0 9 0 0 0 8
0 0 2 3 0 0 0 0 0
0 0 9 0 0 0 0 5 4
'''
''' easy, 9*9 sudoku (approximate 0.06 seconds --- 0 recursive calls): 
0 0 8 0 0 0 0 7 0
1 4 0 2 5 0 0 0 0
0 0 3 0 0 0 9 0 0
2 0 0 1 0 5 0 8 9
0 0 0 0 2 0 0 0 0
4 0 0 0 7 0 1 0 0
8 0 5 0 0 4 0 0 0
0 0 0 9 1 0 5 0 0
0 0 2 5 0 0 0 4 0
'''
''' medium, 9*9 sudoku (approximate 0.12 seconds --- 12 recursive calls): 
0 0 0 9 0 3 0 0 0
0 0 5 4 0 8 1 0 0
0 9 0 0 2 0 0 3 0
1 2 0 0 0 0 0 5 3
0 0 0 0 0 0 0 0 0
9 5 0 0 0 0 0 7 8
0 7 0 0 4 0 0 1 0
0 0 9 6 0 1 3 0 0
0 0 0 7 0 5 0 0 0
'''
''' hard, 9*9 sudoku (approximate 1.8 seconds --- 525 recursive calls): 
8 0 0 0 0 0 0 0 0
0 0 3 6 0 0 0 0 0
0 7 0 0 9 0 2 0 0
0 5 0 0 0 7 0 0 0
0 0 0 0 4 5 7 0 0
0 0 0 1 0 0 0 3 0
0 0 1 0 0 0 0 6 8
0 0 8 5 0 0 0 1 0
0 9 0 0 0 0 4 0 0
'''
''' very hard, 9*9 sudoku (approximate 0.2 seconds --- 46 recursive calls): 
1 0 0 0 0 7 0 9 0
0 3 0 0 2 0 0 0 8
0 0 9 6 0 0 5 0 0
0 0 5 3 0 0 9 0 0
0 1 0 0 8 0 0 0 2
6 0 0 0 0 4 0 0 0
3 0 0 0 0 0 0 1 0
0 4 0 0 0 0 0 0 7
0 0 7 0 0 0 3 0 0
'''
''' very hard, extreme shit, 9*9 sudoku (approximate 0.13 seconds --- 18 recursive calls): 
0 0 2 0 9 0 3 0 0
8 0 5 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0
0 9 0 0 6 0 0 4 0
0 0 0 0 0 0 0 5 8
0 0 0 0 0 0 0 0 1
0 7 0 0 0 0 2 0 0
3 0 0 5 0 0 0 0 0
0 0 0 1 0 0 0 0 0
'''