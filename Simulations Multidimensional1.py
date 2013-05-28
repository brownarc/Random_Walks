import random

finalX = []
finalY = []
visited = []
points = {}

class AlphaWalk (object):
    def __init__ (self, Dimension, JumpAmount, AlphaAmount, WalkAmount):
        self.AlphaAmount = AlphaAmount
        self.Dimension = Dimension
        self.JumpAmount = JumpAmount
        self.WalkAmount = WalkAmount
        self.StepType = []
        self.Probabilities = []

        self.Locations (self.Dimension, self.JumpAmount)

               
    def Compute_Probabilities (self, Dimension, Jump, Alpha):
        self.Chances = []
        self.Constant = 0

        if Dimension == 1:
            for num in range (0, Jump):
                self.Constant += 1.0 / (abs(self.AvailableSpots[num])**Alpha)
        else:
            for num in range (0, Jump):
                self.Constant += 1.0 / (abs(self.AvailableSpots[num][0])**Alpha)
            
        if Dimension == 1:
            self.Constant = 0.5 / self.Constant
            for num in self.AvailableSpots:
                self.Probabilities.append (self.Constant/(abs(num)**Alpha))
            
        elif Dimension == 2:
            self.Constant = 0.25 / self.Constant
            
        elif Dimension == 3:
            self.Constant = (1.0 / 6.0) / self.Constant

        if Dimension > 1:
            for num in range (0, Jump*2):
                self.Probabilities.append (self.Constant/(abs(self.AvailableSpots[num][0])**Alpha))

            self.Probabilities.extend (self.Probabilities)

            if Dimension == 3:
                for num in range (0, (len (self.Probabilities))/2):
                    self.Probabilities.append (self.Probabilities[num])

        count = 0

        for num in self.Probabilities:
            self.Chances.append ((self.AvailableSpots[count], "%0.2f" %(100*num)))
            if count == 0:
                count += 1
            else:
                self.Probabilities [count] += self.Probabilities [count - 1]
                count += 1

        self.RandomWalk (self.WalkAmount)
        
                    
    def Graph (self):
        #import matplotlib.pyplot as plt
        
        count = 0               
        for num in self.PositionsX:
            if count == 0:
                count += 1
                continue
            else:
                self.PositionsX [count] += self.PositionsX [count - 1]
                visited.append (self.PositionsX [count])
                if self.Dimension > 1:
                    self.PositionsY [count] += self.PositionsY [count - 1]
                    if self.Dimension == 3:
                        self.PositionsZ [count] += self.PositionsZ [count - 1]
                count += 1
##        for num in self.PositionsX:
##            if num not in points:
##                points.append (num)


        finalX.append (self.PositionsX[len(self.PositionsX)-1])
                
##        if self.Dimension == 1:
##            plt.plot (self.PositionsX)
##            plt.show()
##        elif self.Dimension == 2:
##            plt.plot (self.PositionsX, self.PositionsY)
##            plt.show()
##        elif self.Dimension == 3:
##            from mpl_toolkits.mplot3d import Axes3D
##            Fig = plt.figure()
##            ax = Fig.gca (projection = '3d')
##            ax.plot (self.PositionsX, self.PositionsY, self.PositionsZ)
##            plt.show()

            
    def Locations (self, Dimension, Jump):
        self.PositionsX = [0]

        if Dimension >= 2:
            self.PositionsY = [0]
            if Dimension == 3:
                self.PositionsZ = [0]
                self.AvailableSpots = [(x, 0, 0) for x in range (-Jump, Jump + 1)]           #next three lines sets up possible 
                self.AvailableSpots.extend ((0, y, 0) for y in range (-Jump, Jump + 1))      #locations 
                self.AvailableSpots.extend ((0, 0, z) for z in range (-Jump, Jump + 1))
                self.AvailableSpots.remove ((0,0,0))                                         #removes (0,0,0) possibilities 
                self.AvailableSpots.remove ((0,0,0))
                self.AvailableSpots.remove ((0,0,0))
            else:
                self.AvailableSpots = [(x, 0) for x in range (-Jump, Jump+1)]
                self.AvailableSpots.extend ((0, y) for y in range (-Jump, Jump+1))
                self.AvailableSpots.remove ((0,0))
                self.AvailableSpots.remove ((0,0))
        else:
            self.AvailableSpots = range ((-Jump), (Jump + 1))
            self.AvailableSpots.remove (0)

        for num in self.AvailableSpots:
            self.StepType.append (0)

        self.Compute_Probabilities (self.Dimension, self.JumpAmount, self.AlphaAmount)


    def Possibilities (self):
        count = 0
        for num in self.Chances:
            print str (num[0]) + "\t   " + str (num[1]) + "%\t" + str (self.StepType[count])
            count += 1
        print "\n\n"
            

    def RandomWalk (self, Walk):
        count = 0
        self.PositionsX = [0]

        while count < Walk:
            RandomNumber = random.random()

            for num in self.Probabilities:
                if RandomNumber < num:
                    if self.Dimension == 1:
                        self.PositionsX.append (self.AvailableSpots[self.Probabilities.index(num)])
                    elif self.Dimension > 1:
                        self.PositionsX.append (self.AvailableSpots[self.Probabilities.index(num)][0])
                        self.PositionsY.append (self.AvailableSpots[self.Probabilities.index(num)][1])
                        if self.Dimension == 3:
                            self.PositionsZ.append (self.AvailableSpots[self.Probabilities.index(num)][2])
                    self.StepType [self.Probabilities.index(num)] += 1
                    break
                if RandomNumber > num:
                    continue
            count += 1
        #self.Possibilities ()
        self.Graph()


    def Simulate (self, Steps, Times):
        count = 0

        while count < Times:
            self.RandomWalk (Steps)
            count += 1


    def Collection (self):
        for num in visited:
            if num in points.keys():
                points[num] += 1
            if num not in points.keys():
                points.update({num:1})



    def Ex_Excel (self, filename):
        filename = filename + ".xls"

        f = open (filename, "w")
        spot = 0
        for item in points.items():
            f.write ("%d\t" % item[0])
            f.write ("%d\n" % item[1])
            spot += 1
        f.close()
