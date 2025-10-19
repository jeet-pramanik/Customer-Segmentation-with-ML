"""
Evaluation Module
Contains metrics and methods to evaluate clustering quality.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import (
    silhouette_score, silhouette_samples,
    calinski_harabasz_score, davies_bouldin_score
)
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class ClusterEvaluator:
    """Evaluate clustering performance using multiple metrics."""
    
    def __init__(self):
        """Initialize evaluator."""
        self.metrics = {}
    
    def evaluate_clustering(self, X, labels, algorithm_name='Clustering'):
        """
        Comprehensive clustering evaluation.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
        labels : array
            Cluster labels
        algorithm_name : str
            Name of the algorithm
            
        Returns:
        --------
        dict
            Dictionary of evaluation metrics
        """
        print(f"\n{'='*60}")
        print(f"EVALUATION: {algorithm_name}")
        print(f"{'='*60}")
        
        # Filter out noise points if any (DBSCAN)
        mask = labels != -1
        X_filtered = X[mask]
        labels_filtered = labels[mask]
        
        n_clusters = len(set(labels_filtered))
        n_noise = np.sum(~mask)
        
        print(f"Number of clusters: {n_clusters}")
        print(f"Number of noise points: {n_noise} ({n_noise/len(labels)*100:.2f}%)")
        
        metrics = {
            'algorithm': algorithm_name,
            'n_clusters': n_clusters,
            'n_noise': n_noise,
            'noise_percentage': n_noise/len(labels)*100
        }
        
        # Calculate metrics only if we have valid clusters
        if n_clusters > 1 and len(X_filtered) > n_clusters:
            # Silhouette Score
            silhouette_avg = silhouette_score(X_filtered, labels_filtered)
            metrics['silhouette_score'] = silhouette_avg
            print(f"Silhouette Score: {silhouette_avg:.4f}")
            print(self._interpret_silhouette(silhouette_avg))
            
            # Calinski-Harabasz Index (Variance Ratio Criterion)
            ch_score = calinski_harabasz_score(X_filtered, labels_filtered)
            metrics['calinski_harabasz_score'] = ch_score
            print(f"Calinski-Harabasz Score: {ch_score:.2f}")
            print("  (Higher is better - measures cluster separation)")
            
            # Davies-Bouldin Index
            db_score = davies_bouldin_score(X_filtered, labels_filtered)
            metrics['davies_bouldin_score'] = db_score
            print(f"Davies-Bouldin Score: {db_score:.4f}")
            print("  (Lower is better - measures cluster similarity)")
            
            # Cluster size distribution
            unique, counts = np.unique(labels_filtered, return_counts=True)
            cluster_sizes = dict(zip(unique, counts))
            metrics['cluster_sizes'] = cluster_sizes
            
            print(f"\nCluster Size Distribution:")
            for cluster_id, size in sorted(cluster_sizes.items()):
                print(f"  Cluster {cluster_id}: {size} samples ({size/len(labels_filtered)*100:.1f}%)")
            
            # Check for balanced clusters
            size_std = np.std(list(cluster_sizes.values()))
            size_mean = np.mean(list(cluster_sizes.values()))
            cv = size_std / size_mean if size_mean > 0 else 0
            metrics['cluster_size_cv'] = cv
            
            if cv < 0.5:
                print(f"\n✓ Clusters are well-balanced (CV: {cv:.2f})")
            else:
                print(f"\n⚠ Clusters are imbalanced (CV: {cv:.2f})")
        
        else:
            print("⚠ Insufficient clusters or data for evaluation")
            metrics['silhouette_score'] = None
            metrics['calinski_harabasz_score'] = None
            metrics['davies_bouldin_score'] = None
        
        print(f"{'='*60}\n")
        
        self.metrics[algorithm_name] = metrics
        return metrics
    
    def _interpret_silhouette(self, score):
        """Interpret silhouette score."""
        if score > 0.7:
            return "  (Excellent - Strong cluster structure)"
        elif score > 0.5:
            return "  (Good - Reasonable cluster structure)"
        elif score > 0.25:
            return "  (Fair - Weak cluster structure)"
        else:
            return "  (Poor - No substantial cluster structure)"
    
    def plot_silhouette_analysis(self, X, labels, n_clusters, save_path=None):
        """
        Create silhouette plot for cluster analysis.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix
        labels : array
            Cluster labels
        n_clusters : int
            Number of clusters
        save_path : str
            Path to save figure
        """
        # Filter noise points
        mask = labels != -1
        X_filtered = X[mask]
        labels_filtered = labels[mask]
        
        if len(set(labels_filtered)) < 2:
            print("Cannot create silhouette plot with less than 2 clusters")
            return
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 7))
        
        # Compute silhouette scores
        silhouette_avg = silhouette_score(X_filtered, labels_filtered)
        sample_silhouette_values = silhouette_samples(X_filtered, labels_filtered)
        
        y_lower = 10
        
        for i in range(n_clusters):
            # Aggregate silhouette scores for samples in cluster i
            ith_cluster_silhouette_values = sample_silhouette_values[labels_filtered == i]
            ith_cluster_silhouette_values.sort()
            
            size_cluster_i = ith_cluster_silhouette_values.shape[0]
            y_upper = y_lower + size_cluster_i
            
            color = cm.nipy_spectral(float(i) / n_clusters)
            ax.fill_betweenx(
                np.arange(y_lower, y_upper),
                0,
                ith_cluster_silhouette_values,
                facecolor=color,
                edgecolor=color,
                alpha=0.7
            )
            
            # Label clusters
            ax.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
            y_lower = y_upper + 10
        
        ax.set_xlabel('Silhouette Coefficient', fontsize=12)
        ax.set_ylabel('Cluster Label', fontsize=12)
        ax.set_title(f'Silhouette Plot (n_clusters = {n_clusters})', 
                      fontsize=14, fontweight='bold')
        
        # Vertical line for average silhouette score
        ax.axvline(x=silhouette_avg, color='red', linestyle='--', 
                    linewidth=2, label=f'Average Score: {silhouette_avg:.3f}')
        ax.legend()
        
        ax.set_yticks([])
        ax.set_xlim([-0.1, 1])
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Silhouette plot saved to {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    def compare_algorithms(self, metrics_list=None):
        """
        Compare multiple clustering algorithms.
        
        Parameters:
        -----------
        metrics_list : list
            List of metrics dictionaries (optional, uses stored metrics if None)
            
        Returns:
        --------
        pd.DataFrame
            Comparison table
        """
        if metrics_list is None:
            if not self.metrics:
                print("No metrics to compare")
                return None
            metrics_list = list(self.metrics.values())
        
        comparison_df = pd.DataFrame(metrics_list)
        
        # Reorder columns
        col_order = ['algorithm', 'n_clusters', 'silhouette_score', 
                      'calinski_harabasz_score', 'davies_bouldin_score', 
                      'n_noise', 'noise_percentage']
        
        existing_cols = [col for col in col_order if col in comparison_df.columns]
        comparison_df = comparison_df[existing_cols]
        
        print("\n" + "="*80)
        print("CLUSTERING ALGORITHMS COMPARISON")
        print("="*80)
        print(comparison_df.to_string(index=False))
        print("="*80)
        
        # Identify best algorithm
        if 'silhouette_score' in comparison_df.columns:
            valid_scores = comparison_df[comparison_df['silhouette_score'].notna()]
            if len(valid_scores) > 0:
                best_idx = valid_scores['silhouette_score'].idxmax()
                best_algorithm = comparison_df.loc[best_idx, 'algorithm']
                best_score = comparison_df.loc[best_idx, 'silhouette_score']
                
                print(f"\n🏆 Best Algorithm: {best_algorithm} (Silhouette Score: {best_score:.4f})")
        
        return comparison_df
    
    def plot_metrics_comparison(self, comparison_df=None, save_path=None):
        """
        Visualize comparison of metrics across algorithms.
        
        Parameters:
        -----------
        comparison_df : pd.DataFrame
            Comparison dataframe (optional)
        save_path : str
            Path to save figure
        """
        if comparison_df is None:
            comparison_df = self.compare_algorithms()
        
        if comparison_df is None:
            return
        
        metrics_to_plot = ['silhouette_score', 'calinski_harabasz_score', 'davies_bouldin_score']
        available_metrics = [m for m in metrics_to_plot if m in comparison_df.columns]
        
        if not available_metrics:
            print("No metrics available for plotting")
            return
        
        fig, axes = plt.subplots(1, len(available_metrics), figsize=(15, 5))
        
        if len(available_metrics) == 1:
            axes = [axes]
        
        for i, metric in enumerate(available_metrics):
            data = comparison_df[['algorithm', metric]].dropna()
            
            axes[i].bar(data['algorithm'], data[metric], color='steelblue', alpha=0.7)
            axes[i].set_xlabel('Algorithm', fontsize=11)
            axes[i].set_ylabel(metric.replace('_', ' ').title(), fontsize=11)
            axes[i].set_title(metric.replace('_', ' ').title(), fontweight='bold')
            axes[i].tick_params(axis='x', rotation=45)
            axes[i].grid(True, alpha=0.3, axis='y')
        
        plt.suptitle('Clustering Algorithms Performance Comparison', 
                      fontsize=14, fontweight='bold', y=1.02)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Comparison plot saved to {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    def plot_cluster_distribution(self, labels, algorithm_name='Clustering', save_path=None):
        """
        Plot cluster size distribution.
        
        Parameters:
        -----------
        labels : array
            Cluster labels
        algorithm_name : str
            Name of algorithm
        save_path : str
            Path to save figure
        """
        unique, counts = np.unique(labels, return_counts=True)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Bar chart
        colors = cm.viridis(np.linspace(0, 1, len(unique)))
        ax1.bar([f'Cluster {i}' if i != -1 else 'Noise' for i in unique], 
                 counts, color=colors, alpha=0.7)
        ax1.set_xlabel('Cluster', fontsize=12)
        ax1.set_ylabel('Number of Samples', fontsize=12)
        ax1.set_title(f'Cluster Size Distribution - {algorithm_name}', fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.grid(True, alpha=0.3, axis='y')
        
        # Add value labels on bars
        for i, (cluster, count) in enumerate(zip(unique, counts)):
            ax1.text(i, count, str(count), ha='center', va='bottom', fontweight='bold')
        
        # Pie chart
        labels_pie = [f'Cluster {i}' if i != -1 else 'Noise' for i in unique]
        ax2.pie(counts, labels=labels_pie, autopct='%1.1f%%', colors=colors, startangle=90)
        ax2.set_title(f'Cluster Proportion - {algorithm_name}', fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Cluster distribution plot saved to {save_path}")
        
        plt.tight_layout()
        plt.show()
    
    def calculate_cluster_stats(self, df, labels, label_column='Cluster'):
        """
        Calculate statistics for each cluster.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Original dataframe
        labels : array
            Cluster labels
        label_column : str
            Name for cluster label column
            
        Returns:
        --------
        pd.DataFrame
            Statistics per cluster
        """
        df_copy = df.copy()
        df_copy[label_column] = labels
        
        # Get numeric columns only
        numeric_cols = df_copy.select_dtypes(include=[np.number]).columns.tolist()
        if label_column in numeric_cols:
            numeric_cols.remove(label_column)
        
        # Calculate stats for each cluster
        cluster_stats = df_copy.groupby(label_column)[numeric_cols].agg(['mean', 'median', 'std'])
        
        return cluster_stats


# Example usage
if __name__ == "__main__":
    # Generate sample data and labels
    from sklearn.datasets import make_blobs
    from sklearn.cluster import KMeans, DBSCAN
    
    X, y_true = make_blobs(n_samples=1000, centers=5, n_features=10, random_state=42)
    
    # Test with K-Means
    kmeans = KMeans(n_clusters=5, random_state=42)
    kmeans_labels = kmeans.fit_predict(X)
    
    # Test with DBSCAN
    dbscan = DBSCAN(eps=0.5, min_samples=5)
    dbscan_labels = dbscan.fit_predict(X)
    
    # Evaluate
    evaluator = ClusterEvaluator()
    kmeans_metrics = evaluator.evaluate_clustering(X, kmeans_labels, 'K-Means')
    dbscan_metrics = evaluator.evaluate_clustering(X, dbscan_labels, 'DBSCAN')
    
    # Compare
    comparison = evaluator.compare_algorithms()
    evaluator.plot_metrics_comparison(comparison)
    
    # Silhouette plot
    evaluator.plot_silhouette_analysis(X, kmeans_labels, n_clusters=5)
