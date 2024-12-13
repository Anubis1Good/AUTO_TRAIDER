from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import numpy.typing as npt

def most_similar_point_knn(points:npt.NDArray,size_cluster:int=10,size_predict:int=5):
    data = points[:-size_predict]
    for i,point in enumerate(data):
        slice = points[i:i+size_cluster]