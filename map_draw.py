import random

def generateSeed():
    count = 0
    seed = ""
    while count < 10:
        seed += str(random.randint(0,9))
        count += 1

    return seed

def generateMap():
    mapFile = open("mapp4.txt", "w")
    gridList = []
    rowList = []
    count = 0
    rowCount = 0
    lineString = ""
    mapSize = 37

   
    totalEnemies = int(1/8 * mapSize)

    while rowCount < mapSize:
        while count < mapSize:
            randomNum = random.randint(0,100)
            if randomNum % 8 == 0:
                rowList.append("#")
            elif randomNum % 44 == 0:
                rowList.append("$")
            else:
                rowList.append(" ")
            count += 1
        count = 0
        gridList.append(rowList[:])
        rowList = []
        rowCount += 1
    rowCount = 0
    count = 0

    gridList[mapSize//2][0] = "O"
    exitRow = random.randint(0,mapSize)
    while exitRow == mapSize//2:
        exitRow = random.randint(0,mapSize-1)
    exitColumn = random.randint(1,mapSize-1)
    gridList[exitRow][exitColumn] = "E"

    topBar = ""
    bottomBar = ""
    while count < mapSize*3:
        topBar += "_"
        bottomBar += "-"
        count += 1
    count = 0

    mapFile.write(bottomBar + "\n")
    mapFile.write("   You are -> O   Obstacles are -> #    Treasure is -> $   Exit is -> E\n")
    mapFile.write(topBar + "\n")

    while rowCount < mapSize:
        while count < mapSize:
            lineString += gridList[rowCount][count]
            count += 1
        mapFile.write(lineString + "\n")
        lineString = ""
        count = 0
        rowCount += 1
    mapFile.write(bottomBar + "\n")
    print("New map created!")
    mapFile.close()
    return gridList

def main():

      
       
    gameMap = generateMap()

    playerHP = 10
    alive = True
    

main()
