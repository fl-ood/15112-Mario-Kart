from cmu_graphics import *
import numpy, math

ar1 = numpy.array([9,8,7]) 
ar2 = numpy.array([3,2,1])


print(ar1,ar2)
test1 = numpy.dot(ar1, ar2) # 9*3 = 27 + 8*2 = 16 + 7*1 = 7
print(test1) # 27 + 16 + 7 = 50 prints 50

# has a matrix class for faster matrix operations
def normal():
    nums = [0,1,2,3,4,5,6,7,8,9]
    matrix = []
    matrix.append(nums)
    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            matrix[row][col] = float(matrix[row][col])
    print(matrix)

def numpymatrix():
    nums = [0,1,2,3,4,5,6,7,8,9]
    matrix = numpy.matrix(nums,dtype = float)
    print(matrix)

normal()
numpymatrix()
# much easier to use numpy here

