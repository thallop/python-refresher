"""
Tutorial: K-means clustering and data visualization, application to a 2D dataset of fruit measurements
"""

from random import randint, sample
from math import sqrt
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
import csv


def distance(p, q):
    """Compute Euclidean distance between two points of any dimension."""
    return sqrt(sum((p[i] - q[i]) ** 2 for i in range(len(p))))


def barycentre(points):
    """Compute barycenter of a list of points."""
    n = len(points)
    dim = len(points[0])
    return [sum(p[i] for p in points) / n for i in range(dim)]


def repartition(data, barycentres):
    """Assign each point in data to the nearest barycenter."""
    k = len(barycentres)
    clusters = [[] for _ in range(k)]
    for point in data:
        distances = [distance(point, b) for b in barycentres]
        idx = distances.index(min(distances))
        clusters[idx].append(point)
    return clusters


def kmeans(data, k, max_iter=100):
    """Run K-means algorithm until stabilization or max_iter reached."""
    barycentres = sample(data, k)
    for _ in range(max_iter):
        clusters = repartition(data, barycentres)
        new_barycentres = [barycentre(c) for c in clusters if c]
        if new_barycentres == barycentres:
            break
        barycentres = new_barycentres
    return clusters, barycentres


def plot_kmeans_result(clusters, barycentres):
    """Display 3D scatter plot of clusters and barycenters."""
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    colors = plt.cm.tab10(np.linspace(0, 1, len(clusters)))

    for i, cluster in enumerate(clusters):
        x = [p[0] for p in cluster]
        y = [p[1] for p in cluster]
        z = [p[2] for p in cluster]
        ax.scatter(x, y, z, color=colors[i])

    bx = [b[0] for b in barycentres]
    by = [b[1] for b in barycentres]
    bz = [b[2] for b in barycentres]
    ax.scatter(bx, by, bz, color='black', marker='D', s=100)
    ax.set_title('K-means Clustering Result')
    plt.show()


def mean_squared_distance(clusters, barycentres):
    """Compute mean of squared distances from points to their cluster barycenter."""
    total = 0
    count = 0
    for cluster, b in zip(clusters, barycentres):
        for point in cluster:
            total += distance(point, b) ** 2
            count += 1
    return total / count if count else 0


def analyze_k_values(data, k_min=2, k_max=10):
    """Plot mean squared distance as function of k."""
    errors = []
    ks = range(k_min, k_max + 1)
    for k in ks:
        clusters, barycentres = kmeans(data, k)
        errors.append(mean_squared_distance(clusters, barycentres))
    plt.plot(ks, errors, marker='o')
    plt.title('Mean Squared Distance vs k')
    plt.xlabel('k')
    plt.ylabel('Mean Squared Distance')
    plt.show()


# Example usage

MAX = 10
N = 100
data = [[randint(0, MAX), randint(0, MAX), randint(0, MAX)] for _ in range(N)]

clusters, barycentres = kmeans(data, 2)
plot_kmeans_result(clusters, barycentres)


# Optional: analyze evolution of mean squared distance

analyze_k_values(data, 2, 10)


# Load the dataset fruits.csv (2D features + label)

filename = "./fruits.csv"

data = []
labels = []

with open(filename, newline="") as f:
    reader = csv.reader(f)
    header = next(reader, None)  # skip header line
    for row in reader:
        # Each row: feature1, feature2, label
        x = float(row[0])
        y = float(row[1])
        label = row[2]
        data.append([x, y])
        labels.append(label)

print(data)
print(labels)


# Plot fruits according to their true class

color_map = {
    "orange": "orange",
    "apple": "green",
}

for pt, lab in zip(data, labels):
    plt.scatter(pt[0], pt[1], color=color_map.get(lab, "gray"))

plt.title("Fruits (true labels)")
plt.xlabel(f"{header[0]}")
plt.ylabel(f"{header[1]}")
plt.show()


# Apply k-means clustering (without knowing classes)

clusters, centers = kmeans(data, 2)


# Visualize clusters found by k-means

colors = plt.cm.tab10(np.linspace(0, 1, len(clusters)))

for i, cluster in enumerate(clusters):
    xs = [p[0] for p in cluster]
    ys = [p[1] for p in cluster]
    plt.scatter(xs, ys, color=colors[i])

cx = [c[0] for c in centers]
cy = [c[1] for c in centers]

plt.scatter(cx, cy, color="black", marker="x", s=100)
plt.title("Fruits clustered by k-means")
plt.xlabel(f"{header[0]}")
plt.ylabel(f"{header[1]}")
plt.show()