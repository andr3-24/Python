import matplotlib.pyplot as plt
import random


'''
You can change the variables: X,Y,CENTERS,POINTS 
to the values you want 
'''

#variables used as constants
X = 1000 #x axis length
Y = 1000 #y axis length
CENTERS = 2 #number of centers
POINTS = 10 #number of points 

#array declarations
xAxis = [0]*POINTS
yAxis = [0]*POINTS

xCenter = [0]*CENTERS
yCenter = [0]*CENTERS




def printStartingData():
    print("*********************")
    print("K-means algorithm\nData:")
    print("All points: ", POINTS)
    print("All centers: ", CENTERS)
    print("*********************")
    print("\n")

def generateRandomPoints():
    for i in range(0,POINTS,1):
        xAxis[i] = random.randint(0, X)
        yAxis[i] = random.randint(0, Y)
        
def generateRandomCenters():
    lst = []
    for i in range(0,CENTERS,1):
        xCenter[i] = random.randint(0, X)
        yCenter[i] = random.randint(0, Y)
        temp = [xCenter[i], yCenter[i]]
        lst.append(temp)  
    return lst
        

        
def makePlot(loop):
    
    plt.scatter(xAxis, yAxis, label= "point", color= "red",
    			marker= "*", s=8)
    plt.scatter(xCenter, yCenter, label= "center", color= "green",
    			marker= "+", s=50)
    
    # x-axis label
    plt.xlabel('x - axis')
    # frequency label
    plt.ylabel('y - axis')
    # plot title
    if(loop == 0):
        mes = "Starting data:"
    else:
        mes = "loop: " + str(loop)
    plt.title('2D map - ' + mes)
    # showing legend
    plt.legend()

    # function to show the plot
    plt.show()
    
def ManhattanDistance(x,y):
   
    '''
    This function computs the Manhattan distance
    of a given point (x,y) for each center and returns 
    the coordinates of the closest center.
    '''
    
    CDcenters = [0]*CENTERS
    for i in range(0,CENTERS,1):
        CDcenters[i] = abs(x - xCenter[i]) + abs(y - yCenter[i])
        
    minValue = min(CDcenters)
    for i in range(0,CENTERS,1):
        if (CDcenters[i] == minValue):
            return xCenter[i], yCenter[i];
            break;
    
def CDBForEveryPoint(lst):
    
    '''
         It groups the points based on their distance from 
         their nearest center
         and it returns a list of each cluster
         and its points
        
         Note: the spaces of the cluster cover them with '-1'
         In each case, the set of positions of the points which
         taken for the points
         of each cluster corresponds to the number of points that have been set
    '''
    
    
    
    #cd block for every point
    # lst = 'katalogos' (lista) me tis sintetagmenes olwn twn kentrwn
    clustersPoints = [[-1]*(POINTS+1) for _ in range(CENTERS)]
    for i in range(0, CENTERS, 1):
        clustersPoints[i][0] = lst[i]
 #   print("Calculation of Manhattan distance for each point and center:\n")
 #   print("Format: [Point],[Closest center]\n\n")
    
    for i in range(0, POINTS, 1):
        x,y = ManhattanDistance(xAxis[i], yAxis[i])
     #   print("Point ",i+1,": [", xAxis[i],",",yAxis[i],"] , [", x,", " ,y, "]")
        tempCenter = [x,y]
        tempPoint = [xAxis[i], yAxis[i]]
        for j in range(0, CENTERS, 1):
            if(clustersPoints[j][0] == tempCenter):
                for r in range(1, POINTS+1, 1):
                    if(clustersPoints[j][r] == -1):
                        clustersPoints[j][r] = tempPoint
                        break
                    
#    printClustersToConsole(clustersPoints)
    return clustersPoints

def clusterPointsNum(cp):
    elCount = [0]*CENTERS
    for i in range(0, CENTERS, 1):
        counter = 0
        for j in range(1, POINTS+1, 1):
            if (cp[i][j] == -1):
                elCount[i] = 0
                break
            else:
                counter += 1
        elCount[i] = counter
    return elCount

def percentage(sumOfPoints):
    #returns the percentages of the points for each center
    perc = [0]*CENTERS
    for i in range(0, CENTERS, 1):
        perc[i] = round(sumOfPoints[i]/POINTS*100, 1)
    return perc
    

def printClustersToConsole(cp):
    
    '''
    prints the each cluster with its points every time it is called
    
    This function is made only for debugging purposes. 
    I recommend to not use it if there is no reason 
    cause it makes the program significantly slower.
    
    '''
    
    
    print("\nFormat: [Center] { [Closest Point1][Closest Point2], ... ,[Closest Pointx] } \nClusters:")
    ClusterCounter = 1
    i = 0
    for r in cp:
      j=0
      print("Cluster ", ClusterCounter, ":")
      ClusterCounter+=1
      i+=1
      for c in r:
          if(j==1):
              print(" { ",end = " ")
              if (c == -1):
                   print("null",end = " ") #keno cluster
                   break        
          if(c == -1):
              continue
          print(c,end = " ")
          j+=1
      print(" } \n")
    
def centerRedefinition(cp, clusterSum):    
    cluster = [0] * POINTS
    
    for i in range(0, CENTERS, 1):
        cluster = cp[i]
        num=0
        if (clusterSum[i] != 0):
            for x in range(1, POINTS+1, 1):
                if(cluster[x] == -1):
                    break
                num += cluster[x][0]
            newX = round(num/clusterSum[i],2)
            
            num = 0
            for y in range(1, POINTS+1, 1):
                if(cluster[y] == -1):
                    break
                num += cluster[y][1]
            newY = round(num/clusterSum[i],2)
            
            cp[i][0][0] = newX
            cp[i][0][1] = newY
    
    return cp

def updateGlobalLists(cp):
    
    '''
    Function usage:
    1) Check for any change (if yes -> keep going)
    2) Update global coordinate center lists for x and y axis 
    
    If there is nothing to be updated, then it returns 
    False so the while loop stops, meaning the final 
    center coordinates have been found.
    Otherwise, if this function detects atleast one change 
    comparing to the previous coordinates it returns 
    true, so while loop in main() will keep going.
    '''
    
    change = False
    lock = False
    
    for i in range(0, CENTERS, 1):
        for j in range(0, 2, 1):
            if(j == 0):
                if(xCenter[i] != cp[i][0][0] and lock == False):
                    change = True
                    lock = True
                xCenter[i] = cp[i][0][0]
            else:
                if(yCenter[i] != cp[i][0][1] and lock == False):
                    change = True
                    lock = True
                yCenter[i] = cp[i][0][1]
    return change
    
def mapInitialization():
    
    '''
     1) prints the starting data
     2) The number of points requested by the user is randomly placed on the grid
     3) The number of centers requested by the builder is randomly placed on the grid
    
     Return:
         Returns a list of initialized centers
    '''
    
    printStartingData() 
    generateRandomPoints() 
    cenLst = generateRandomCenters() 
    
    return cenLst

                       
def main():
      
    whileLoop = 0  
    changeDetected = True           
    cenLst = mapInitialization() #prwto vhma
    
    
    while(changeDetected == True): #oso yparxei allagh
    
        clustersPoints = CDBForEveryPoint(cenLst) 
        makePlot(whileLoop)
        sumOfPoints = clusterPointsNum(clustersPoints)

        clustersPoints = centerRedefinition(clustersPoints, sumOfPoints)
        changeDetected = updateGlobalLists(clustersPoints)
        
        '''
        (if changeDetected == False
            break)
        '''

        whileLoop += 1 
        
    #percentages = percentage(sumOfPoints)

    print("k-means finished.")
        
    
main()
