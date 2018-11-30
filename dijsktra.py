import pandas as pd
import numpy as np
inputPath = 'input.csv'
df = pd.read_csv(inputPath)

vertexMap = df.values


startNode = 0
endNode = 11
VERTEX_NAME = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'z']


class Vertex:

    def __init__(self, index, weight, fromVertex):
        self.index = index
        self.weight = weight
        self.fromVertex = fromVertex
        if self.fromVertex == None:
            self.weightSum = self.weight
        else:
            self.weightSum = self.weight + self.fromVertex.weightSum

    def __str__(self):
        return 'index:{}#{} weight:{} fromVertex:{}#{} weightSum:{}\n'.format(self.index,  VERTEX_NAME[self.index], self.weight, self.fromVertex.index, VERTEX_NAME[self.fromVertex.index], self.weightSum)

    def getPath(self, path=None):
        if path == None:
            path = []
        if self.fromVertex != None:

            self.fromVertex.getPath(path).append(self)
            return path
        else:
            path.append(self)
            return path


class Graph:
    def __init__(self, weightMap, srcIndex, destIndex):
        self.edges = [Vertex(srcIndex, 0, None)]
        self.srcIndex = srcIndex
        self.destIndex = destIndex
        self.checkedIndexs = [srcIndex]
        self.weightMap = weightMap
        np.place(self.weightMap, self.weightMap == 0, 10**2)

    def dijsktra(self):

        while self.edges[-1].index != self.destIndex:
            availableEdges = []
            for edge in self.edges:
                weights = self.weightMap[edge.index, :].tolist()
                index = 0
                weights[0] = 10**2
                for i in range(1, len(weights)):
                    if i in self.checkedIndexs:
                        weights[i] = 10**2
                    if weights[i] < weights[index] and i not in self.checkedIndexs:
                        index = i
                availableEdges.append(Vertex(index, weights[index], edge))
            print(''.join([str(vertex) for vertex in availableEdges]))
            availableEdges.sort(key=lambda vertex: vertex.weightSum)
            nextEdge = availableEdges[0]
            self.edges.append(nextEdge)
            self.checkedIndexs.append(nextEdge.index)
            print('select {}'.format(str(nextEdge)))
            print('visited {}'.format(', '.join([VERTEX_NAME[v] for v in self.checkedIndexs])))
            print('='*40)
        return self.edges[-1]


graph = Graph(vertexMap, startNode, endNode)

edge = graph.dijsktra()

print(' -> '.join([VERTEX_NAME[v.index] for v in edge.getPath()]))
print('distance {}'.format(edge.weightSum))
