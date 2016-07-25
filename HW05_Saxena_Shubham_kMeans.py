__author__ = 'Shubham Saxena'
import math
import sys

import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
import random


def main():
     #opening file
    file = open(sys.argv[1], 'r')
    #number of clusters
    #k = int(sys.argv[2])
    #read data into a list
    lines = file.readlines()
    dataList = []
    for line in lines:
        line = line.replace("\n", "")
        tup =  [float(x) for x in line.split(',')]
        dataList.append(tup)

    print("Before Cleaning #pts:",len(dataList))
    #removing the noise / far away points
    dataList = clean(dataList)
    #number points after cleaning
    print("after Cleaning #pts:",len(dataList))

    sse = []
    for i in range(1, 11):
        sse.append(kmeans(dataList, i))


    print(sse)
    plotKvSSE(10, sse)

#main functio that runs k means
def kmeans(dataList, k):

    clusterCentr = []

    #for k number of clusters find k random points
    for x in range(0,k):
        clusterCentr.append(random.choice(dataList))

    print("Initial Cluster Centers",clusterCentr)

    #clustering iterations. Runs till clusters have converged.
    while True:
        cluster = []
        euc = []
        for x in range(0,k):
            cluster.append([])
            euc.append([])

        for d in dataList:
            ctr = 0
            for i in range(0,k):
                euc[i] = eucledianD(d, clusterCentr[i])
            minCluster = euc.index(min(euc))
            cluster[minCluster].append(d)

        #centroids of respective clusters
        newCentrs = []
        for i in range(0,k):
            newCentrs.append(centroid(cluster[i])) #difference in the old and new centroids

        #to check convergence condition: if centroid of clusters remain unchanged. .
        done = True
        for i in range(0,k):
            if newCentrs[i] != clusterCentr[i]:
                done = False
        if done:
            for i in range(0, k):
                print("size of Cluster",i,len(cluster[i]))

            break
        else:
            for i in range(0,k):
                clusterCentr[i] = centroid(cluster[i])
                #print(i, len(cluster[0]))

    sse = 0;
    for i in range(0,k):
        sum = 0;
        for d in cluster[i]:
            sum = sum + eucledianD(d,clusterCentr[i])**2
        sse = sse + sum

    print(sse)
    plot(cluster, k)
    return sse


# calculates centroid for a set of points
def centroid(data):
    if len(data) < 1 :
        pt = [0,0,0]
        return pt
    xsum = 0
    ysum = 0
    zsum = 0
    for d in data:
        xsum = xsum + d[0]
        ysum = ysum + d[1]
        zsum = zsum + d[2]
    pt = [float(xsum) / float(len(data)), float(ysum) / float(len(data)), float(zsum) / float(len(data))]

    return pt

# calculates the eucledian distance between 2 points
def eucledianD(pt1, pt2):
    dist = math.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2 + (pt1[2]-pt2[2])**2)
    return dist

#plotting function for the clusters
def plot(datalist, k):
    fig =  plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ['r', 'g', 'b', 'yellow', 'magenta','black',  'grey',  'brown', 'orange' 'pink' 'cyan',]
    for i in range(0,k):
        x,y,z = zip(*datalist[i])
        ax.scatter(x, y, z, c=colors[i], marker='o')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()

#removes the noise from data
def clean(dataList):
    for d in list(dataList):
        ctr =0
        for d2 in list(dataList):
            if eucledianD(d, d2) < 1:
                ctr += 1
        if ctr<10:
            dataList.remove(d)
    return dataList

#plots K vs SSE
def plotKvSSE(k, sse):
    for i in range(0,k):
        x = i
        y = sse[i]
        plt.plot(x, y, 'ro')
    plt.axis([0, 11, 0, 5000])
    plt.show()

#call to main function
main()
