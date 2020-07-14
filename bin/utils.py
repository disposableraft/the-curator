import pickle
import math
import matplotlib.pyplot as plt

def load_graph(file):
    with open(file, 'rb') as f:
        graph = pickle.load(f)
    return graph

def save_graph(graph, file):
    with open(file, 'wb') as f:
        pickle.dump(graph, f, pickle.HIGHEST_PROTOCOL)

def draw_hist(X, show=False, **kwargs):
    # Get a list of all the artists' degrees
    hist = plt.hist(X, **kwargs)
    if show:
        plt.show()
    else:
        return hist

def draw_boxplot(X, show=False, **kwargs):
    # Get a list of all the artists' degrees
    boxplot = plt.boxplot(X, **kwargs)
    if show:
        plt.show()
    else:
        return boxplot

# Yikes! Please rewrite
def pearson_r(X, Y):
    N = len(X)
    # numerator expressions
    xy = zip(X, Y)
    sum_xy = sum([x*y for x, y in xy])

    mean_sums_x_y = (sum(X) * sum(Y)) / N

    #denominator expressions
    sum_x2 = sum([x**2 for x in X])
    mean_sumx_2 = math.pow(sum(X), 2) / N
    sum_x2_minus_mean = sum_x2 - mean_sumx_2

    sum_y2 = sum([y**2 for y in Y])
    mean_sumy_2 = math.pow( sum(Y), 2 ) / N
    sum_y2_minus_mean = sum_y2 - mean_sumy_2

    return (sum_xy - mean_sums_x_y) / ( math.sqrt(sum_x2_minus_mean) * math.sqrt(sum_y2_minus_mean) )

