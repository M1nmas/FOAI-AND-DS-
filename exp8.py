import numpy as np
import pandas as pd

data = pd.read_csv('data.csv')

X = data.values

X_meaned = X - np.mean(X, axis=0)

cov_matrix = np.cov(X_meaned, rowvar=False)
print("Covariance Matrix:\n", cov_matrix)

eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

sorted_index = np.argsort(eigenvalues)[::-1]

sorted_eigenvalue = eigenvalues[sorted_index]
sorted_eigenvectors = eigenvectors[:, sorted_index]

print("\nEigenvalues:\n", sorted_eigenvalue)

explained_variance = sorted_eigenvalue / np.sum(sorted_eigenvalue)

cumulative_variance = np.cumsum(explained_variance)

print("\nExplained Variance:\n", explained_variance)
print("\nCumulative Variance:\n", cumulative_variance)

optimal_components = np.argmax(cumulative_variance >= 0.95) + 1

print("\nOptimal Number of PCA Components =", optimal_components)

eigenvector_subset = sorted_eigenvectors[:, 0:optimal_components]

X_reduced = np.dot(X_meaned, eigenvector_subset)

print("\nReduced Data (After PCA):\n", X_reduced)