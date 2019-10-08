#https://stackoverflow.com/questions/13728392/moving-average-or-running-mean
import numpy as np

def filter(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / float(N)
