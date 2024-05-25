import numpy as np
from sklearn.cluster import KMeans

def recommend_colors(image, n_colors=10):
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=n_colors)
    kmeans.fit(pixels)
    return kmeans.cluster_centers_

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % tuple(rgb)
