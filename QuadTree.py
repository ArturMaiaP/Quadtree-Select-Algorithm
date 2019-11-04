
from math import ceil
import matplotlib.pyplot as plt
import pandas as pd
from Point import *
from Node import *
from operator import itemgetter
import random
from Imagem import *
from OpPts import *

class QuadTree():

    def __init__(self):

    	#Dataframe with the points' coordinates
        self.dfQuadtree = pd.read_csv('Anno/points.txt')

        #index of each region
        self.counter = 0
        
        #stops to divide a region if reach these limits (points/depth)
        self.limit = 6
        self.limDepth = 10

        self.eps = 0.001

    def ptRegQuadtree(self,dfAttr,samples):

    	#Input: dataframe with coordinates / Output: list of objects (Point Class) that represents the points
        pontos = self.extractPointsDf(self.dfQuadtree)

        xmax = self.dfQuadtree['X'].max() + self.eps
        xmin = self.dfQuadtree['X'].min()

        ymax = self.dfQuadtree['Y'].max() + self.eps
        ymin = self.dfQuadtree['Y'].min()
        
        #Root node with all points available
        root = Node(xMin= xmin, yMin= ymin, xMax=xmax, yMax= ymax, points=pontos, number=self.counter)

        #Create the Quadtree structure 
        root = self.constructQuadtree(root,0)
        
        #Select elements from the Quadtree structure
        ptsQTree = self.selectQuadtree(region=root,n=samples)
        
        self.plotQuadtree()

        return ptsQTree


    #This function will receive a Node and then will divide it into four new Nodes(quadrants) creating a tree structure.
    #region = parent node
    #R1,R2,R3,R4 = child nodes
    def constructQuadtree(self,region,level):
       
    	#Stop the division if reaches one of these conditions
        if len(region.getPoints()) <= self.limit or level >= self.limDepth:
            return
        else:
            listReg = self.splitRegion(region)
            listRegSorted = self.sortRegAsc(listReg)

            R1 = listRegSorted[0]
            self.constructQuadtree(R1, level+1)

            R2 = listRegSorted[1]
            self.constructQuadtree(R2,level+1)

            R3 = listRegSorted[2]
            self.constructQuadtree(R3, level+1)

            R4 = listRegSorted[3]
            self.constructQuadtree(R4, level+1)

            region.childrens = [R1,R2,R3,R4]

            #Returns the region with the correspondents child nodes
            return region


    #This function will select n points of the space based on the leaf nodes
    def selectQuadtree(self,region,n):
        ptsQTree = []

        #stopping criterias
        if len(region.getChildrens()) ==0:
            ptsQTree = ptsQTree + random.sample(region.getPoints(), min(n,len(region.getPoints())))

        elif len(region.getPoints()) <= n:
            ptsQTree = ptsQTree + region.getPoints()

        elif n<4:
            missing = n
            while missing>0:
                R = region.getChildrens()[random.randint(1,4) -1]
                if len(R.getPoints()) > 0:
                    ptSelect = random.choice(region.getPoints())
                    ptsQTree.append(ptSelect)
                    region.removePt(ptSelect)
                    missing = missing - 1

        #The recursive part that will navigate until reach a leaf node            
        else:
            listReg = region.getChildrens()
            listRegSorted = self.sortRegAsc(listReg)

            missing = n
            samplesize = ceil(missing/4)

            R1 = listRegSorted[0]
            ptsQTree = ptsQTree + self.selectQuadtree(R1,min( samplesize, len(R1.getPoints())))
            missing = missing - min(samplesize,len(R1.getPoints()))

            if missing <= 0:
                return

            samplesize = ceil(missing/3)
            R2 = listRegSorted[1]
            ptsQTree= ptsQTree + self.selectQuadtree(R2, min(samplesize, len(R2.getPoints())))
            missing = missing - min(samplesize, len(R2.getPoints()))

            if missing <= 0:
                return

            samplesize = ceil(missing / 2)
            R3 = listRegSorted[2]
            ptsQTree = ptsQTree + self.selectQuadtree(R3, min(samplesize, len(R3.getPoints())))
            missing = missing - min(samplesize, len(R3.getPoints()))

            if missing <= 0:
                return
            R4 = listRegSorted[3]
            ptsQTree = ptsQTree + self.selectQuadtree(R4, missing)
            missing = missing - min(samplesize, len(R4.getPoints()))

            if missing >0:
                pts = self.selectQuadtree(region,missing)
                ptsQTree = ptsQTree + pts

            print(len(ptsQTree))

        return ptsQTree


    #Sort the regions based on the quantity of points (ascending)
    def sortRegAsc(self, listReg):
        dicRegions = {}
        for reg in listReg:
            regPtsQt = len(reg.getPoints())
            dicRegions[reg] = regPtsQt

        dicRegions = dict(sorted(dicRegions.items(), key=itemgetter(1)))
        
        listNodesSorted = list(dicRegions.keys())
        return listNodesSorted

    def splitRegion(self,parent=Node):
    	#Midpoint of each axis used to divide the regions in the half
        PmX = (parent.getxMax() + parent.getxMin())/2
        PmY = (parent.getyMax() + parent.getyMin())/2

        #3ºQuadrant
        self.addCounter()
        ptsReg1 = self.getPointsReg(parent.getPoints(), parent.getxMin(), parent.getyMin(), PmX, PmY)
        R1 = Node(parent.getxMin(), parent.getyMin(), PmX, PmY,ptsReg1,self.counter)

        #2ºQuadrant
        self.addCounter()
        ptsReg2 = self.getPointsReg(parent.getPoints(), parent.getxMin(), PmY, PmX, parent.getyMax())
        R2 = Node(parent.getxMin(), PmY, PmX, parent.getyMax(),ptsReg2,self.counter)

        #4ºQuadrant
        self.addCounter()
        ptsReg3 = self.getPointsReg(parent.getPoints(), PmX, parent.getyMin(), parent.getxMax(), PmY)
        R3 = Node(PmX, parent.getyMin(), parent.getxMax(), PmY,ptsReg3,self.counter)

        #1ºQuadrant
        self.addCounter()
        ptsReg4 = self.getPointsReg(parent.getPoints(), PmX, PmY, parent.getxMax(), parent.getyMax())
        R4 = Node(PmX, PmY, parent.getxMax(), parent.getyMax(),ptsReg4,self.counter)

        return [R1,R2,R3,R4]

    #separete the points of each region
    def getPointsReg(self,points,xmin,ymin,xmax,ymax):
        #print(xmin,ymin,xmax,ymax)
        pts = []
        for point in points:
            if point.x >= xmin and point.x < xmax and point.y >= ymin and point.y < ymax:
                pts.append(point)
        return pts

    #Return a list of points (objects of Point class)
    def extractPointsDf(self,df):
        objPts = []

        for index,row in df.iterrows():
            pt = Point(row['X'],row['Y'],index)
            objPts.append(pt)

        return objPts


    def addCounter(self):
        self.counter = self.counter+1


    def plotQuadtree(self):
        print(len(self.ptsQTree))
        listPts = []
        for pt in self.ptsQTree:
            pt = [pt.x,pt.y]
            listPts.append(pt)

        df = pd.DataFrame(data=listPts, columns=['X','Y'])
        #print(df)

        plt.figure(figsize=(10, 5))
        plt.subplot(121)

        plt.scatter(df.X, df.Y)
        plt.show(block=False)
