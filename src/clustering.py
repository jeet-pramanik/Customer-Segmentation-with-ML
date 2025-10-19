"""
Clustering Module
Implements K-Means, DBSCAN, Hierarchical Clustering, and GMM.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.mixture import GaussianMixture
from sklearn.neighbors import NearestNeighbors
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt
import joblib


class ClusteringModel:
    """Base class for clustering models."""
    
    def __init__(self, model_type='kmeans', **kwargs):
        """
        Initialize clustering model.
        
        Parameters:
        -----------
        model_type : str
            Type of clustering algorithm
        **kwargs : dict
            Algorithm-specific parameters
        """
        self.model_type = model_type
        self.model = None
        self.labels = None
        self.n_clusters = None
        self.params = kwargs
    
    def fit(self, X):
        """Fit the clustering model."""
        raise NotImplementedError
    
    def predict(self, X):
        """Predict cluster labels."""
        raise NotImplementedError
    
    def save_model(self, filepath):
        """Save the model."""
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """Load the model."""
        self.model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")


class KMeansClusterer(ClusteringModel):
    """K-Means clustering implementation."""
    
    def __init__(self, n_clusters=5, init='k-means++', n_init=10, 
                 max_iter=300, random_state=42):
        """
        Initialize K-Means clusterer.
        
        Parameters:
        -----------
        n_clusters : int
            Number of clusters
        init : str
            Initialization method
        n_init : int
            Number of initializations
        max_iter : int
            Maximum iterations
        random_state : int
            Random seed
        """
        super().__init__(model_type='kmeans')
        self.n_clusters = n_clusters
        self.model = KMeans(
            n_clusters=n_clusters,
            init=init,
            n_init=n_init,
            max_iter=max_iter,
            random_state=random_state
        )
        self.cluster_centers = None
        self.inertia = None
    
    def fit(self, X):
        """
        Fit K-Means model.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
            
        Returns:
        --------
        array
            Cluster labels
        """
        self.labels = self.model.fit_predict(X)
        self.cluster_centers = self.model.cluster_centers_
        self.inertia = self.model.inertia_
        
        print(f"K-Means fitted with {self.n_clusters} clusters")
        print(f"Inertia: {self.inertia:.2f}")
        
        return self.labels
    
    def predict(self, X):
        """
        Predict cluster labels for new data.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
            
        Returns:
        --------
        array
            Cluster labels
        """
        return self.model.predict(X)
    
    def find_optimal_clusters(self, X, k_range=range(2, 11), method='all'):
        """
        Find optimal number of clusters using multiple methods.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
        k_range : range
            Range of k values to test
        method : str
            'elbow', 'silhouette', 'all'
            
        Returns:
        --------
        dict
            Metrics for each k value
        """
        from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
        
        print(f"Finding optimal clusters for k in {list(k_range)}...")
        
        results = {
            'k_values': [],
            'inertias': [],
            'silhouette_scores': [],
            'calinski_harabasz_scores': [],
            'davies_bouldin_scores': []
        }
        
        for k in k_range:
            # Fit model
            kmeans = KMeans(n_clusters=k, init='k-means++', n_init=10, 
                             max_iter=300, random_state=42)
            labels = kmeans.fit_predict(X)
            
            # Calculate metrics
            results['k_values'].append(k)
            results['inertias'].append(kmeans.inertia_)
            
            if k > 1:  # Silhouette requires at least 2 clusters
                results['silhouette_scores'].append(silhouette_score(X, labels))
                results['calinski_harabasz_scores'].append(calinski_harabasz_score(X, labels))
                results['davies_bouldin_scores'].append(davies_bouldin_score(X, labels))
            
            print(f"k={k}: Inertia={kmeans.inertia_:.2f}", end="")
            if k > 1:
                print(f", Silhouette={results['silhouette_scores'][-1]:.3f}")
            else:
                print()
        
        return results
    
    def plot_elbow_curve(self, results, save_path=None):
        """
        Plot elbow curve.
        
        Parameters:
        -----------
        results : dict
            Results from find_optimal_clusters()
        save_path : str
            Path to save figure
        """
        plt.figure(figsize=(10, 6))
        plt.plot(results['k_values'], results['inertias'], 'bo-', linewidth=2, markersize=8)
        plt.xlabel('Number of Clusters (k)', fontsize=12)
        plt.ylabel('Within-Cluster Sum of Squares (Inertia)', fontsize=12)
        plt.title('Elbow Method for Optimal k', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.xticks(results['k_values'])
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Elbow curve saved to {save_path}")
        
        plt.tight_layout()
        plt.show()


class DBSCANClusterer(ClusteringModel):
    """DBSCAN clustering implementation."""
    
    def __init__(self, eps=0.5, min_samples=5, metric='euclidean'):
        """
        Initialize DBSCAN clusterer.
        
        Parameters:
        -----------
        eps : float
            Maximum distance between two samples
        min_samples : int
            Minimum samples in neighborhood
        metric : str
            Distance metric
        """
        super().__init__(model_type='dbscan')
        self.eps = eps
        self.min_samples = min_samples
        self.model = DBSCAN(eps=eps, min_samples=min_samples, metric=metric)
        self.n_noise = None
    
    def fit(self, X):
        """
        Fit DBSCAN model.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
            
        Returns:
        --------
        array
            Cluster labels (-1 for noise)
        """
        self.labels = self.model.fit_predict(X)
        self.n_clusters = len(set(self.labels)) - (1 if -1 in self.labels else 0)
        self.n_noise = list(self.labels).count(-1)
        
        print(f"DBSCAN identified {self.n_clusters} clusters")
        print(f"Noise points: {self.n_noise} ({self.n_noise/len(X)*100:.2f}%)")
        
        return self.labels
    
    def predict(self, X):
        """DBSCAN doesn't have native predict, returns -1 for new points."""
        print("Warning: DBSCAN doesn't support prediction. Returning noise label (-1).")
        return np.full(X.shape[0], -1)
    
    def find_optimal_eps(self, X, k=5):
        """
        Find optimal eps using k-distance graph.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
        k : int
            Number of neighbors (typically = min_samples)
            
        Returns:
        --------
        array
            Sorted k-distances
        """
        print(f"Computing {k}-nearest neighbors for optimal eps...")
        
        neighbors = NearestNeighbors(n_neighbors=k)
        neighbors.fit(X)
        distances, indices = neighbors.kneighbors(X)
        
        # Sort distances
        distances = np.sort(distances[:, k-1], axis=0)
        
        return distances
    
    def plot_k_distance(self, distances, save_path=None):
        """
        Plot k-distance graph to find optimal eps.
        
        Parameters:
        -----------
        distances : array
            Sorted k-distances
        save_path : str
            Path to save figure
        """
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(distances)), distances, 'b-', linewidth=1)
        plt.xlabel('Data Points sorted by distance', fontsize=12)
        plt.ylabel('k-th Nearest Neighbor Distance', fontsize=12)
        plt.title('K-Distance Graph for Optimal Eps', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"K-distance graph saved to {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    def grid_search_parameters(self, X, eps_values, min_samples_values):
        """
        Grid search for optimal DBSCAN parameters.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
        eps_values : list
            List of eps values to test
        min_samples_values : list
            List of min_samples values to test
            
        Returns:
        --------
        pd.DataFrame
            Results for each parameter combination
        """
        from sklearn.metrics import silhouette_score
        
        print("Performing grid search for DBSCAN parameters...")
        
        results = []
        
        for eps in eps_values:
            for min_samples in min_samples_values:
                dbscan = DBSCAN(eps=eps, min_samples=min_samples)
                labels = dbscan.fit_predict(X)
                
                n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
                n_noise = list(labels).count(-1)
                noise_pct = (n_noise / len(X)) * 100
                
                # Calculate silhouette score (only if we have clusters)
                if n_clusters > 1 and n_noise < len(X):
                    # Exclude noise points for silhouette calculation
                    mask = labels != -1
                    if mask.sum() > n_clusters:
                        silhouette = silhouette_score(X[mask], labels[mask])
                    else:
                        silhouette = -1
                else:
                    silhouette = -1
                
                results.append({
                    'eps': eps,
                    'min_samples': min_samples,
                    'n_clusters': n_clusters,
                    'n_noise': n_noise,
                    'noise_pct': noise_pct,
                    'silhouette_score': silhouette
                })
                
                print(f"eps={eps}, min_samples={min_samples}: "
                      f"{n_clusters} clusters, {noise_pct:.1f}% noise, "
                      f"silhouette={silhouette:.3f}")
        
        return pd.DataFrame(results)


class HierarchicalClusterer(ClusteringModel):
    """Hierarchical clustering implementation."""
    
    def __init__(self, n_clusters=5, linkage='ward'):
        """
        Initialize Hierarchical clusterer.
        
        Parameters:
        -----------
        n_clusters : int
            Number of clusters
        linkage : str
            Linkage criterion
        """
        super().__init__(model_type='hierarchical')
        self.n_clusters = n_clusters
        self.model = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage)
        self.linkage_matrix = None
    
    def fit(self, X):
        """
        Fit hierarchical clustering model.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
            
        Returns:
        --------
        array
            Cluster labels
        """
        self.labels = self.model.fit_predict(X)
        
        # Create linkage matrix for dendrogram
        self.linkage_matrix = linkage(X, method='ward')
        
        print(f"Hierarchical clustering fitted with {self.n_clusters} clusters")
        
        return self.labels
    
    def predict(self, X):
        """Hierarchical clustering doesn't have native predict."""
        print("Warning: Hierarchical clustering doesn't support prediction.")
        return None
    
    def plot_dendrogram(self, max_d=None, save_path=None):
        """
        Plot dendrogram.
        
        Parameters:
        -----------
        max_d : float
            Maximum distance for horizontal line
        save_path : str
            Path to save figure
        """
        plt.figure(figsize=(14, 8))
        dendrogram(self.linkage_matrix, truncate_mode='level', p=10)
        
        if max_d:
            plt.axhline(y=max_d, color='r', linestyle='--', linewidth=2)
        
        plt.xlabel('Sample Index or Cluster Size', fontsize=12)
        plt.ylabel('Distance', fontsize=12)
        plt.title('Hierarchical Clustering Dendrogram', fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3, axis='y')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dendrogram saved to {save_path}")
        
        plt.tight_layout()
        plt.show()


class GMMClusterer(ClusteringModel):
    """Gaussian Mixture Model clustering implementation."""
    
    def __init__(self, n_components=5, covariance_type='full', random_state=42):
        """
        Initialize GMM clusterer.
        
        Parameters:
        -----------
        n_components : int
            Number of mixture components
        covariance_type : str
            Type of covariance parameters
        random_state : int
            Random seed
        """
        super().__init__(model_type='gmm')
        self.n_clusters = n_components
        self.model = GaussianMixture(
            n_components=n_components,
            covariance_type=covariance_type,
            random_state=random_state
        )
    
    def fit(self, X):
        """
        Fit GMM model.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
            
        Returns:
        --------
        array
            Cluster labels
        """
        self.model.fit(X)
        self.labels = self.model.predict(X)
        
        print(f"GMM fitted with {self.n_clusters} components")
        print(f"BIC: {self.model.bic(X):.2f}")
        print(f"AIC: {self.model.aic(X):.2f}")
        
        return self.labels
    
    def predict(self, X):
        """
        Predict cluster labels with probabilities.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
            
        Returns:
        --------
        array
            Cluster labels
        """
        return self.model.predict(X)
    
    def predict_proba(self, X):
        """Get probability distributions."""
        return self.model.predict_proba(X)


# Example usage
if __name__ == "__main__":
    # Generate sample data
    from sklearn.datasets import make_blobs
    
    X, y_true = make_blobs(n_samples=1000, centers=5, n_features=10, random_state=42)
    
    # K-Means
    kmeans = KMeansClusterer(n_clusters=5)
    results = kmeans.find_optimal_clusters(X, k_range=range(2, 11))
    kmeans.plot_elbow_curve(results)
    
    labels = kmeans.fit(X)
    print(f"K-Means labels: {labels[:10]}")
    
    # DBSCAN
    dbscan = DBSCANClusterer(eps=0.5, min_samples=5)
    labels = dbscan.fit(X)
    print(f"DBSCAN labels: {labels[:10]}")
