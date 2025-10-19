"""
Cluster Profiling Module
Analyzes and creates detailed profiles for each customer segment.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


class ClusterProfiler:
    """Profile customer clusters and generate insights."""
    
    def __init__(self):
        """Initialize profiler."""
        self.profiles = {}
        self.segment_names = {}
    
    def create_cluster_profiles(self, df, labels, label_column='Cluster'):
        """
        Create detailed profiles for each cluster.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Original dataframe with features
        labels : array
            Cluster labels
        label_column : str
            Name for cluster label column
            
        Returns:
        --------
        dict
            Profiles for each cluster
        """
        df_copy = df.copy()
        df_copy[label_column] = labels
        
        print("="*80)
        print("CLUSTER PROFILING")
        print("="*80)
        
        profiles = {}
        unique_labels = sorted([l for l in df_copy[label_column].unique() if l != -1])
        
        for cluster_id in unique_labels:
            cluster_data = df_copy[df_copy[label_column] == cluster_id]
            
            profile = {
                'cluster_id': cluster_id,
                'size': len(cluster_data),
                'percentage': len(cluster_data) / len(df_copy) * 100
            }
            
            # Demographic profile
            if 'Age' in cluster_data.columns:
                profile['avg_age'] = cluster_data['Age'].mean()
            if 'Income' in cluster_data.columns:
                profile['avg_income'] = cluster_data['Income'].mean()
            if 'Gender' in cluster_data.columns:
                profile['gender_dist'] = cluster_data['Gender'].value_counts().to_dict()
            
            # Behavioral profile (RFM)
            if 'Recency' in cluster_data.columns:
                profile['avg_recency'] = cluster_data['Recency'].mean()
            if 'Frequency' in cluster_data.columns:
                profile['avg_frequency'] = cluster_data['Frequency'].mean()
            if 'Monetary' in cluster_data.columns:
                profile['avg_monetary'] = cluster_data['Monetary'].mean()
            
            # Engagement profile
            if 'WebsiteVisits' in cluster_data.columns:
                profile['avg_website_visits'] = cluster_data['WebsiteVisits'].mean()
            if 'EmailOpenRate' in cluster_data.columns:
                profile['avg_email_open_rate'] = cluster_data['EmailOpenRate'].mean()
            
            # Store all numeric means
            numeric_cols = cluster_data.select_dtypes(include=[np.number]).columns
            numeric_cols = [c for c in numeric_cols if c != label_column]
            profile['numeric_means'] = cluster_data[numeric_cols].mean().to_dict()
            
            profiles[cluster_id] = profile
            
            # Print summary
            print(f"\nCluster {cluster_id}:")
            print(f"  Size: {profile['size']} ({profile['percentage']:.1f}%)")
            if 'avg_recency' in profile:
                print(f"  Avg Recency: {profile['avg_recency']:.1f} days")
            if 'avg_frequency' in profile:
                print(f"  Avg Frequency: {profile['avg_frequency']:.1f} purchases")
            if 'avg_monetary' in profile:
                print(f"  Avg Monetary: ${profile['avg_monetary']:.2f}")
        
        self.profiles = profiles
        return profiles
    
    def assign_segment_names(self, profiles):
        """
        Assign business-friendly names to segments based on characteristics.
        
        Parameters:
        -----------
        profiles : dict
            Cluster profiles
            
        Returns:
        --------
        dict
            Mapping of cluster_id to segment name
        """
        segment_names = {}
        
        # Sort by monetary value if available
        if all('avg_monetary' in p for p in profiles.values()):
            sorted_clusters = sorted(profiles.items(), 
                                      key=lambda x: x[1].get('avg_monetary', 0), 
                                      reverse=True)
            
            for idx, (cluster_id, profile) in enumerate(sorted_clusters):
                recency = profile.get('avg_recency', 0)
                frequency = profile.get('avg_frequency', 0)
                monetary = profile.get('avg_monetary', 0)
                
                # High value segments
                if monetary > 5000 and frequency > 15:
                    name = "VIP Champions"
                elif monetary > 3000 and recency < 30:
                    name = "High-Value Loyalists"
                elif monetary > 2000 and frequency > 8:
                    name = "Loyal Customers"
                elif monetary > 1000 and recency < 60:
                    name = "Potential Loyalists"
                elif frequency < 5:
                    name = "Occasional Shoppers"
                elif recency > 90:
                    name = "At-Risk/Dormant"
                else:
                    name = f"Segment {cluster_id}"
                
                segment_names[cluster_id] = name
        else:
            # Default naming
            for cluster_id in profiles.keys():
                segment_names[cluster_id] = f"Segment {cluster_id}"
        
        self.segment_names = segment_names
        return segment_names
    
    def plot_cluster_heatmap(self, df, labels, features=None, save_path=None):
        """
        Create heatmap showing average feature values per cluster.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Feature dataframe
        labels : array
            Cluster labels
        features : list
            Features to include (None = all numeric)
        save_path : str
            Path to save figure
        """
        df_copy = df.copy()
        df_copy['Cluster'] = labels
        
        if features is None:
            features = df_copy.select_dtypes(include=[np.number]).columns.tolist()
            features = [f for f in features if f != 'Cluster']
        
        # Calculate means per cluster
        cluster_means = df_copy.groupby('Cluster')[features].mean()
        
        # Normalize for better visualization
        cluster_means_norm = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min())
        
        plt.figure(figsize=(12, 8))
        sns.heatmap(cluster_means_norm.T, annot=True, fmt='.2f', cmap='RdYlGn', 
                     cbar_kws={'label': 'Normalized Value'})
        plt.xlabel('Cluster', fontsize=12)
        plt.ylabel('Features', fontsize=12)
        plt.title('Cluster Feature Heatmap', fontsize=14, fontweight='bold')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.tight_layout()
        plt.show()
    
    def generate_marketing_strategies(self, profiles, segment_names):
        """
        Generate marketing strategies for each segment.
        
        Parameters:
        -----------
        profiles : dict
            Cluster profiles
        segment_names : dict
            Segment names
            
        Returns:
        --------
        dict
            Marketing strategies per segment
        """
        strategies = {}
        
        for cluster_id, profile in profiles.items():
            name = segment_names.get(cluster_id, f"Segment {cluster_id}")
            
            strategy = {
                'segment_name': name,
                'size': profile['size'],
                'strategy': '',
                'tactics': [],
                'channel': '',
                'offer_type': ''
            }
            
            # Determine strategy based on segment characteristics
            if "VIP" in name or "Champions" in name:
                strategy['strategy'] = "VIP retention and advocacy program"
                strategy['tactics'] = [
                    "Exclusive early access to new products",
                    "Personal account manager",
                    "Premium loyalty rewards"
                ]
                strategy['channel'] = "Personal email, Phone"
                strategy['offer_type'] = "Exclusive experiences, Premium benefits"
            
            elif "Loyal" in name:
                strategy['strategy'] = "Strengthen loyalty and increase share of wallet"
                strategy['tactics'] = [
                    "Cross-sell complementary products",
                    "Loyalty program tier upgrades",
                    "Regular engagement campaigns"
                ]
                strategy['channel'] = "Email, Mobile app"
                strategy['offer_type'] = "Bundle discounts, Loyalty points"
            
            elif "At-Risk" in name or "Dormant" in name:
                strategy['strategy'] = "Win-back and re-engagement campaign"
                strategy['tactics'] = [
                    "Special comeback offers",
                    "Survey to understand concerns",
                    "Personalized product recommendations"
                ]
                strategy['channel'] = "Email, Retargeting ads"
                strategy['offer_type'] = "Significant discount, Free shipping"
            
            elif "Potential" in name:
                strategy['strategy'] = "Nurture and convert to loyal customers"
                strategy['tactics'] = [
                    "Educational content about products",
                    "First purchase incentives",
                    "Onboarding campaigns"
                ]
                strategy['channel'] = "Email, Social media"
                strategy['offer_type'] = "Welcome discount, Free trial"
            
            else:
                strategy['strategy'] = "General engagement and conversion"
                strategy['tactics'] = [
                    "Targeted product recommendations",
                    "Seasonal promotions",
                    "Value demonstration"
                ]
                strategy['channel'] = "Email, Display ads"
                strategy['offer_type'] = "Time-limited discounts"
            
            strategies[cluster_id] = strategy
        
        return strategies
    
    def print_segment_report(self, profiles, segment_names, strategies):
        """Print comprehensive segment report."""
        print("\n" + "="*80)
        print("CUSTOMER SEGMENTATION REPORT")
        print("="*80)
        
        for cluster_id, profile in profiles.items():
            name = segment_names.get(cluster_id, f"Segment {cluster_id}")
            strategy = strategies.get(cluster_id, {})
            
            print(f"\n{'='*80}")
            print(f"SEGMENT: {name}")
            print(f"{'='*80}")
            print(f"Cluster ID: {cluster_id}")
            print(f"Size: {profile['size']} customers ({profile['percentage']:.1f}%)")
            
            print(f"\nKey Characteristics:")
            if 'avg_recency' in profile:
                print(f"  • Average Days Since Last Purchase: {profile['avg_recency']:.1f}")
            if 'avg_frequency' in profile:
                print(f"  • Average Purchase Frequency: {profile['avg_frequency']:.1f}")
            if 'avg_monetary' in profile:
                print(f"  • Average Total Spending: ${profile['avg_monetary']:.2f}")
            if 'avg_age' in profile:
                print(f"  • Average Age: {profile['avg_age']:.1f}")
            if 'avg_income' in profile:
                print(f"  • Average Income: ${profile['avg_income']:.2f}")
            
            if strategy:
                print(f"\nMarketing Strategy: {strategy.get('strategy', 'N/A')}")
                print(f"Communication Channel: {strategy.get('channel', 'N/A')}")
                print(f"Offer Type: {strategy.get('offer_type', 'N/A')}")
                print(f"\nRecommended Tactics:")
                for i, tactic in enumerate(strategy.get('tactics', []), 1):
                    print(f"  {i}. {tactic}")
        
        print("\n" + "="*80)


# Example usage
if __name__ == "__main__":
    # Sample usage
    from data_loader import CustomerDataLoader
    from sklearn.cluster import KMeans
    
    loader = CustomerDataLoader(data_dir='../data')
    df = loader.generate_synthetic_data(n_customers=1000)
    
    # Simple clustering for demo
    features = ['Recency', 'Frequency', 'Monetary']
    X = df[features].values
    
    kmeans = KMeans(n_clusters=5, random_state=42)
    labels = kmeans.fit_predict(X)
    
    # Profile clusters
    profiler = ClusterProfiler()
    profiles = profiler.create_cluster_profiles(df, labels)
    segment_names = profiler.assign_segment_names(profiles)
    strategies = profiler.generate_marketing_strategies(profiles, segment_names)
    profiler.print_segment_report(profiles, segment_names, strategies)
