import dionysus as d
import matplotlib.pyplot as plt
import numpy as np

# Create a random point cloud
points = np.random.random((200, 2))  # 200 points in a 2D space

# Initialize a filtration
f = d.Filtration()

# Add vertices to the filtration
for i in range(len(points)):
    f.append(d.Simplex([i], 0))

# Create the Vietoris-Rips complex and add simplices to the filtration
rips = d.fill_rips(points, 2, 2)  # Dimension 2, max edge length 2
for simplex in rips:
    f.append(simplex)

# Sort the filtration
f.sort()

# Compute persistent homology
p = d.homology_persistence(f)
dgms = d.init_diagrams(p, f)

# Function to plot a persistent diagram
def plot_persistent_diagram(diagrams):
    plt.figure(figsize=(8, 4))
    colors = ['bo', 'go']  # Blue for H_0, Green for H_1
    labels = ['H_0', 'H_1']
    
    for i, dgm in enumerate(diagrams):
        plt.subplot(1, len(diagrams), i + 1)
        plt.title(f"Persistent Diagram for {labels[i]}")
        plt.xlabel("Birth")
        plt.ylabel("Death")
        for p in dgm:
            if p.death - p.birth > 0.001:  # Filter out near-instantaneous features
                plt.plot(p.birth, p.death, colors[i])
        max_death = max([p.death for p in dgm if p.death < float('inf')], default=0)
        plt.plot([0, max_death], [0, max_death], "k--")

    plt.show()

# Plot the persistent diagram
plot_persistent_diagram(dgms)
