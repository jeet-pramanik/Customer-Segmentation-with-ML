"""
Visualization Module
Creates comprehensive visualizations for customer segmentation analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class SegmentationVisualizer:
    """Create visualizations for customer segmentation."""
    
    def __init__(self, style='seaborn'):
        """Initialize visualizer."""
        self.figures = []
    
    def plot_cluster_scatter_2d(self, X, labels, feature_names=None, title='Cluster Visualization', save_path=None):
        """
        2D scatter plot of clusters using first 2 features/components.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix (uses first 2 columns)
        labels : array
            Cluster labels
        feature_names : list
            Names of features
        title : str
            Plot title
        save_path : str
            Path to save figure
        """
        if feature_names is None:
            feature_names = [f'Feature {i+1}' for i in range(X.shape[1])]
        
        plt.figure(figsize=(10, 8))
        scatter = plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', 
                               alpha=0.6, edgecolors='w', linewidth=0.5, s=50)
        plt.colorbar(scatter, label='Cluster')
        plt.xlabel(feature_names[0], fontsize=12)
        plt.ylabel(feature_names[1], fontsize=12)
        plt.title(title, fontsize=14, fontweight='bold')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
    
    def plot_cluster_scatter_3d(self, X, labels, feature_names=None, title='3D Cluster Visualization'):
        """
        Interactive 3D scatter plot using Plotly.
        
        Parameters:
        -----------
        X : array-like
            Feature matrix (uses first 3 columns)
        labels : array
            Cluster labels
        feature_names : list
            Names of features
        title : str
            Plot title
        """
        if feature_names is None:
            feature_names = [f'Feature {i+1}' for i in range(min(3, X.shape[1]))]
        
        df = pd.DataFrame({
            feature_names[0]: X[:, 0],
            feature_names[1]: X[:, 1],
            feature_names[2]: X[:, 2] if X.shape[1] > 2 else np.zeros(len(X)),
            'Cluster': labels
        })
        
        fig = px.scatter_3d(df, x=feature_names[0], y=feature_names[1], z=feature_names[2],
                             color='Cluster', title=title,
                             color_continuous_scale='viridis')
        fig.update_layout(height=700)
        fig.show()
    
    def plot_rfm_analysis(self, df, labels, save_path=None):
        """
        RFM analysis visualization.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataframe with RFM columns
        labels : array
            Cluster labels
        save_path : str
            Path to save figure
        """
        df_copy = df.copy()
        df_copy['Cluster'] = labels
        
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        
        # Recency by cluster
        df_copy.boxplot(column='Recency', by='Cluster', ax=axes[0])
        axes[0].set_title('Recency by Cluster', fontweight='bold')
        axes[0].set_xlabel('Cluster')
        axes[0].set_ylabel('Days Since Last Purchase')
        
        # Frequency by cluster
        df_copy.boxplot(column='Frequency', by='Cluster', ax=axes[1])
        axes[1].set_title('Frequency by Cluster', fontweight='bold')
        axes[1].set_xlabel('Cluster')
        axes[1].set_ylabel('Number of Purchases')
        
        # Monetary by cluster
        df_copy.boxplot(column='Monetary', by='Cluster', ax=axes[2])
        axes[2].set_title('Monetary by Cluster', fontweight='bold')
        axes[2].set_xlabel('Cluster')
        axes[2].set_ylabel('Total Spending ($)')
        
        plt.suptitle('RFM Analysis by Cluster', fontsize=16, fontweight='bold', y=1.02)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
    
    def create_interactive_dashboard(self, df, labels, segment_names=None):
        """
        Create interactive dashboard using Plotly.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Customer dataframe
        labels : array
            Cluster labels
        segment_names : dict
            Mapping of cluster IDs to names
            
        Returns:
        --------
        plotly.graph_objects.Figure
            Interactive dashboard
        """
        df_copy = df.copy()
        df_copy['Cluster'] = labels
        
        if segment_names:
            df_copy['Segment'] = df_copy['Cluster'].map(segment_names)
        else:
            df_copy['Segment'] = 'Cluster ' + df_copy['Cluster'].astype(str)
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Segment Distribution', 'RFM by Segment', 
                             'Customer Value', 'Segment Characteristics'),
            specs=[[{'type': 'pie'}, {'type': 'bar'}],
                   [{'type': 'scatter'}, {'type': 'bar'}]]
        )
        
        # 1. Segment distribution pie chart
        segment_counts = df_copy['Segment'].value_counts()
        fig.add_trace(
            go.Pie(labels=segment_counts.index, values=segment_counts.values, 
                    name='Segments'),
            row=1, col=1
        )
        
        # 2. Average RFM by segment
        if all(col in df_copy.columns for col in ['Recency', 'Frequency', 'Monetary']):
            rfm_avg = df_copy.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean()
            
            for col in ['Recency', 'Frequency', 'Monetary']:
                fig.add_trace(
                    go.Bar(name=col, x=rfm_avg.index, y=rfm_avg[col]),
                    row=1, col=2
                )
        
        # 3. Scatter: Frequency vs Monetary
        if 'Frequency' in df_copy.columns and 'Monetary' in df_copy.columns:
            for segment in df_copy['Segment'].unique():
                segment_data = df_copy[df_copy['Segment'] == segment]
                fig.add_trace(
                    go.Scatter(x=segment_data['Frequency'], y=segment_data['Monetary'],
                                mode='markers', name=segment, opacity=0.6),
                    row=2, col=1
                )
        
        # 4. Segment sizes
        fig.add_trace(
            go.Bar(x=segment_counts.index, y=segment_counts.values, 
                    marker_color='steelblue'),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=True, 
                           title_text="Customer Segmentation Dashboard",
                           title_font_size=20)
        
        return fig
    
    def plot_pca_variance(self, explained_variance_ratio, save_path=None):
        """
        Plot PCA explained variance.
        
        Parameters:
        -----------
        explained_variance_ratio : array
            Explained variance ratios from PCA
        save_path : str
            Path to save figure
        """
        cumsum = np.cumsum(explained_variance_ratio)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Scree plot
        ax1.bar(range(1, len(explained_variance_ratio) + 1), explained_variance_ratio, 
                 alpha=0.7, color='steelblue')
        ax1.set_xlabel('Principal Component', fontsize=12)
        ax1.set_ylabel('Explained Variance Ratio', fontsize=12)
        ax1.set_title('Scree Plot', fontweight='bold')
        ax1.grid(True, alpha=0.3)
        
        # Cumulative variance
        ax2.plot(range(1, len(cumsum) + 1), cumsum, 'bo-', linewidth=2, markersize=8)
        ax2.axhline(y=0.9, color='r', linestyle='--', label='90% Variance')
        ax2.set_xlabel('Number of Components', fontsize=12)
        ax2.set_ylabel('Cumulative Explained Variance', fontsize=12)
        ax2.set_title('Cumulative Explained Variance', fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.suptitle('PCA Analysis', fontsize=14, fontweight='bold', y=1.02)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    from sklearn.datasets import make_blobs
    from sklearn.cluster import KMeans
    
    X, y = make_blobs(n_samples=500, centers=4, n_features=3, random_state=42)
    
    kmeans = KMeans(n_clusters=4, random_state=42)
    labels = kmeans.fit_predict(X)
    
    viz = SegmentationVisualizer()
    viz.plot_cluster_scatter_2d(X, labels, feature_names=['PC1', 'PC2'])
    viz.plot_cluster_scatter_3d(X, labels, feature_names=['PC1', 'PC2', 'PC3'])
