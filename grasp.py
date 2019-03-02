import random,time

class HamiltonianPath:

    def __init__(self,numOfNodes):
        if numOfNodes > 0:
            self.numOfNodes = numOfNodes
        else:
            print("Error")

    def calculateMaxPairs(self):
        self.maxPairs = self.numOfNodes*(self.numOfNodes - 1)//2

    def formHP(self):
        self.hamiltonianPath = []
        while len(self.hamiltonianPath) != self.numOfNodes:
            randomNode = random.randint(1,self.numOfNodes)
            if randomNode not in self.hamiltonianPath:
                self.hamiltonianPath.append(randomNode)

    def generateHPPairs(self):
        self.formHP()
        self.hamiltonianPairs = []
        for x in range (len(self.hamiltonianPath)-1):
            pair = (self.hamiltonianPath[x], self.hamiltonianPath[x+1])
            self.hamiltonianPairs.append(pair)
        self.generatePairs(self.hamiltonianPairs)
        random.shuffle(self.hamiltonianPairs)
        self.pairs = self.hamiltonianPairs

    def generatePairs(self, pairs = []):
        self.calculateMaxPairs()
        self.pairs = pairs
        if self.numOfNodes >= 10:
            startRange = self.numOfNodes
            endRange = (self.numOfNodes - 10)*3 + 18
            numOfPairs = random.randint(startRange, endRange)
        else:
            numOfPairs = random.randint(self.numOfNodes - 1, self.maxPairs)
        print("Random total of pairs:", numOfPairs)

        while len(self.pairs) != numOfPairs:
            try:
                startNode = random.randint(1, self.numOfNodes)
                endNode = random.randint(1, self.numOfNodes)
                if startNode == endNode:
                    raise ValueError
            except ValueError:
                pass
            else:
                pair = (startNode, endNode)
                invertedPair = (endNode, startNode)
                if pair not in self.pairs and invertedPair not in self.pairs:
                    self.pairs.append(pair)

        print("Pairs:", self.pairs)

    def generatePathLink(self):
        self.graphLink = {}
        for x in self.pairs:
            x = str(x)
            splitNode = x.split(', ')
            a = int(splitNode[0][1:])
            b = int(splitNode[1][:-1])
            try:
                if b not in self.graphLink[a]:
                    self.graphLink[a].append(b)
            except KeyError:
                self.graphLink[a] = []
                self.graphLink[a].append(b)
            finally:
                try:
                    if a not in self.graphLink[b]:
                        self.graphLink[b].append(a)
                except KeyError:
                    self.graphLink[b] = []
                    self.graphLink[b].append(a)
                finally:
                    pass

        print("Graph linkage:", self.graphLink)


    def grasp(self):
        solutionList = []
        firstSolution = []
        previousStartNode = []

        tempNode = len(self.pairs)
        startNode = 0

        for start in range(1, len(self.graphLink)):
            if len(self.graphLink[start]) < tempNode:
                tempNode = len(self.graphLink[start])
                startNode = start

        firstSolution.append(startNode)
        previousStartNode.append(startNode)
        firstSearch = self.greedySearch(firstSolution)

        if firstSearch[0] == False:
            solutionList.append(firstSearch[1])

            for y in range(1, 101):
                randomIndex = random.randint(0,len(solutionList)-1)
                randomSolution = solutionList[randomIndex].copy()
                randomPosition = random.randint(1,len(randomSolution)-1)
                randomNum = random.randint(1, 3)
 
                if randomNum == 1: #remove second half
                    randomSolution = randomSolution[:randomPosition]

                elif randomNum == 2: #remove first half
                    randomSolution = randomSolution[randomPosition:]

                else:
                    randomSolution = self.restartSearch()

                newSearch = self.greedySearch(randomSolution)
                newSolution = newSearch[1]

                if newSearch[0]:
                    newBestSolution = newSolution
                    break

                if newSolution not in solutionList:
                    solutionList.append(newSolution)

                newBestSolution = max(solutionList, key = len)

            if len(newBestSolution) == numOfNodes:
                print("\nHamiltonian Path Found!\nHP:", newBestSolution)
                return [True,newBestSolution]

            else:
                print("\nBest Solution Found:", newBestSolution)
                print("\nLength of path:", len(newBestSolution))
                print("\nLength of solution list:",len(solutionList))
                return [False,newBestSolution]

        else:
            print("\nHamiltonian Path Found!\nHP:", firstSearch[1])
            return [True,firstSearch[1]]

    def isHamiltonianPathExist(self):
        time_start = time.clock()
        self.generatePathLink()
        print("Finding Hamiltonian Paths...")

        if len(self.graphLink) != self.numOfNodes:
            print("The graph is not connected.\nHence, there is no Hamiltoninan Paths.\n")
            time_elapsed = (time.clock() - time_start)
            return [-1, time_elapsed]
        else:
            result = self.grasp()
            time_elapsed = (time.clock() - time_start)
            if result[0]:
                print("Computing time:", round(time_elapsed, 2), "seconds\n")
                return [result[1], time_elapsed]
            else:
                print("Computing time:", round(time_elapsed, 2), "seconds\n")
                return [result[1], time_elapsed]

    def greedySearch(self, solution):
        newLastNode = solution[-1]
        while True:
            lastNode = solution[-1]
            possibleNode = self.graphLink[lastNode]
            random.shuffle(possibleNode)
            if len(solution) == self.numOfNodes:
                return (True, solution)
            else:
                for x in range(0, len(possibleNode)):
                    if possibleNode[x] not in solution:
                        solution.append(possibleNode[x])
                        newLastNode = possibleNode[x]
                        break
                if lastNode == newLastNode:
                    solution.reverse()
                    while True:
                        lastNode = solution[-1]
                        newLastNode = solution[-1]
                        possibleNode = self.graphLink[lastNode]
                        if len(solution) == self.numOfNodes:
                            return (True, solution)
                        else:
                            for x in range(0, len(possibleNode)):
                                if possibleNode[x] not in solution:
                                    solution.append(possibleNode[x])
                                    newLastNode = possibleNode[x]
                                    break
                            if lastNode == newLastNode:
                                return (False, solution)

    def restartSearch(self):
        randomStartNode = random.randint(1,self.numOfNodes)
        newSolution = []
        newSolution.append(randomStartNode)
        return newSolution

numOfNodes = 20
yes = 0
no = 0

loop_start_time = time.clock()
for x in range(1,101):
    print(x)
    graph = HamiltonianPath(numOfNodes)
    graph.generateHPPairs()
    output = graph.isHamiltonianPathExist()
    solution = output[0]
    if len(solution) == numOfNodes:
        yes += 1
    else:
        no += 1

loop_time_elapsed = (time.clock() - loop_start_time)
print("Accuracy:", yes,"%")
print("Time taken for 100 runs:", round(loop_time_elapsed, 2))
