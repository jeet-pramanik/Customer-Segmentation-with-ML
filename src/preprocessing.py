"""
Data Preprocessing Module
Handles missing values, outliers, feature engineering, encoding, and scaling.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.decomposition import PCA
import joblib
import warnings
warnings.filterwarnings('ignore')


class DataPreprocessor:
    """Comprehensive data preprocessing pipeline."""
    
    def __init__(self):
        """Initialize preprocessor with transformation objects."""
        self.scaler = None
        self.pca = None
        self.label_encoders = {}
        self.imputers = {}
        self.feature_names = None
        self.numeric_features = None
        self.categorical_features = None
    
    def handle_missing_values(self, df, strategy='auto', numeric_strategy='median', 
                               categorical_strategy='most_frequent'):
        """
        Handle missing values in the dataset.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        strategy : str
            'auto', 'drop', 'impute'
        numeric_strategy : str
            'mean', 'median', 'knn'
        categorical_strategy : str
            'most_frequent', 'constant'
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with handled missing values
        """
        print("Handling missing values...")
        df_copy = df.copy()
        
        # Get numeric and categorical columns
        numeric_cols = df_copy.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df_copy.select_dtypes(include=['object']).columns.tolist()
        
        # Remove ID columns from processing
        numeric_cols = [col for col in numeric_cols if 'ID' not in col.upper()]
        categorical_cols = [col for col in categorical_cols if 'ID' not in col.upper()]
        
        if strategy == 'auto':
            # Drop columns with >40% missing
            missing_pct = (df_copy.isnull().sum() / len(df_copy)) * 100
            cols_to_drop = missing_pct[missing_pct > 40].index.tolist()
            
            if cols_to_drop:
                print(f"Dropping columns with >40% missing: {cols_to_drop}")
                df_copy = df_copy.drop(columns=cols_to_drop)
                numeric_cols = [col for col in numeric_cols if col not in cols_to_drop]
                categorical_cols = [col for col in categorical_cols if col not in cols_to_drop]
        
        # Impute numeric features
        if numeric_cols:
            if numeric_strategy == 'knn':
                imputer = KNNImputer(n_neighbors=5)
                self.imputers['numeric'] = imputer
            else:
                imputer = SimpleImputer(strategy=numeric_strategy)
                self.imputers['numeric'] = imputer
            
            df_copy[numeric_cols] = imputer.fit_transform(df_copy[numeric_cols])
            print(f"Imputed {len(numeric_cols)} numeric features using {numeric_strategy}")
        
        # Impute categorical features
        if categorical_cols:
            imputer = SimpleImputer(strategy=categorical_strategy, fill_value='Unknown')
            self.imputers['categorical'] = imputer
            df_copy[categorical_cols] = imputer.fit_transform(df_copy[categorical_cols])
            print(f"Imputed {len(categorical_cols)} categorical features using {categorical_strategy}")
        
        print(f"Remaining missing values: {df_copy.isnull().sum().sum()}")
        
        return df_copy
    
    def detect_outliers(self, df, columns=None, method='iqr', threshold=3):
        """
        Detect outliers in numerical features.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        columns : list
            Columns to check for outliers (None = all numeric)
        method : str
            'iqr' or 'zscore'
        threshold : float
            Threshold for outlier detection
            
        Returns:
        --------
        dict
            Dictionary with outlier information per column
        """
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
            columns = [col for col in columns if 'ID' not in col.upper()]
        
        outliers_info = {}
        
        for col in columns:
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
            
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers = df[z_scores > threshold]
            
            if len(outliers) > 0:
                outliers_info[col] = {
                    'count': len(outliers),
                    'percentage': (len(outliers) / len(df)) * 100,
                    'indices': outliers.index.tolist()
                }
        
        return outliers_info
    
    def handle_outliers(self, df, method='cap', outlier_info=None):
        """
        Handle outliers using capping or removal.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        method : str
            'cap', 'remove', 'none'
        outlier_info : dict
            Output from detect_outliers()
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with handled outliers
        """
        df_copy = df.copy()
        
        if method == 'none':
            return df_copy
        
        if outlier_info is None:
            outlier_info = self.detect_outliers(df_copy)
        
        if method == 'cap':
            for col in outlier_info.keys():
                Q1 = df_copy[col].quantile(0.25)
                Q3 = df_copy[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                df_copy[col] = df_copy[col].clip(lower=lower_bound, upper=upper_bound)
                print(f"Capped outliers in {col}")
        
        elif method == 'remove':
            all_outlier_indices = set()
            for info in outlier_info.values():
                all_outlier_indices.update(info['indices'])
            
            df_copy = df_copy.drop(index=list(all_outlier_indices))
            print(f"Removed {len(all_outlier_indices)} outlier rows")
        
        return df_copy
    
    def feature_engineering(self, df):
        """
        Create new features from existing ones.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with engineered features
        """
        print("Engineering new features...")
        df_copy = df.copy()
        
        # RFM Score (if RFM columns exist)
        if all(col in df_copy.columns for col in ['Recency', 'Frequency', 'Monetary']):
            # Normalize RFM values to 1-5 scale
            df_copy['R_Score'] = pd.qcut(df_copy['Recency'], q=5, labels=[5, 4, 3, 2, 1], duplicates='drop')
            df_copy['F_Score'] = pd.qcut(df_copy['Frequency'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
            df_copy['M_Score'] = pd.qcut(df_copy['Monetary'], q=5, labels=[1, 2, 3, 4, 5], duplicates='drop')
            
            # Convert to numeric
            df_copy['R_Score'] = df_copy['R_Score'].astype(int)
            df_copy['F_Score'] = df_copy['F_Score'].astype(int)
            df_copy['M_Score'] = df_copy['M_Score'].astype(int)
            
            # Combined RFM Score
            df_copy['RFM_Score'] = (df_copy['R_Score'] + df_copy['F_Score'] + df_copy['M_Score']) / 3
            print("Created RFM scores")
        
        # Customer Value Tier
        if 'Monetary' in df_copy.columns:
            df_copy['ValueTier'] = pd.cut(df_copy['Monetary'],
                                           bins=[0, 1000, 3000, 7000, np.inf],
                                           labels=['Low', 'Medium', 'High', 'Premium'])
            print("Created ValueTier feature")
        
        # Engagement Score
        if all(col in df_copy.columns for col in ['WebsiteVisits', 'EmailOpenRate', 'Frequency']):
            # Normalize components
            visits_norm = (df_copy['WebsiteVisits'] - df_copy['WebsiteVisits'].min()) / \
                          (df_copy['WebsiteVisits'].max() - df_copy['WebsiteVisits'].min())
            email_norm = df_copy['EmailOpenRate']
            freq_norm = (df_copy['Frequency'] - df_copy['Frequency'].min()) / \
                        (df_copy['Frequency'].max() - df_copy['Frequency'].min())
            
            df_copy['EngagementScore'] = (visits_norm * 0.3 + email_norm * 0.3 + freq_norm * 0.4)
            print("Created EngagementScore")
        
        # Average days between purchases
        if all(col in df_copy.columns for col in ['TenureDays', 'Frequency']):
            df_copy['AvgDaysBetweenPurchase'] = df_copy['TenureDays'] / (df_copy['Frequency'] + 1)
            print("Created AvgDaysBetweenPurchase")
        
        # Discount affinity
        if 'DiscountUsage' in df_copy.columns:
            df_copy['DiscountAffinity'] = pd.cut(df_copy['DiscountUsage'],
                                                   bins=[0, 0.2, 0.5, 1.0],
                                                   labels=['Low', 'Medium', 'High'])
            print("Created DiscountAffinity")
        
        # Return rate
        if all(col in df_copy.columns for col in ['NumReturns', 'Frequency']):
            df_copy['ReturnRate'] = df_copy['NumReturns'] / (df_copy['Frequency'] + 1)
            print("Created ReturnRate")
        
        # Customer lifecycle stage
        if 'TenureDays' in df_copy.columns:
            df_copy['LifecycleStage'] = pd.cut(df_copy['TenureDays'],
                                                bins=[0, 90, 365, 730, np.inf],
                                                labels=['New', 'Growing', 'Mature', 'Veteran'])
            print("Created LifecycleStage")
        
        print(f"Total features after engineering: {len(df_copy.columns)}")
        
        return df_copy
    
    def encode_categorical(self, df, encoding_method='onehot', exclude_columns=None):
        """
        Encode categorical variables.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        encoding_method : str
            'onehot' or 'label'
        exclude_columns : list
            Columns to exclude from encoding
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with encoded features
        """
        print(f"Encoding categorical variables using {encoding_method}...")
        df_copy = df.copy()
        
        if exclude_columns is None:
            exclude_columns = []
        
        # Get categorical columns
        cat_cols = df_copy.select_dtypes(include=['object', 'category']).columns.tolist()
        cat_cols = [col for col in cat_cols if col not in exclude_columns and 'ID' not in col.upper()]
        
        if encoding_method == 'onehot':
            # One-hot encoding
            df_copy = pd.get_dummies(df_copy, columns=cat_cols, drop_first=True, dtype=int)
            print(f"One-hot encoded {len(cat_cols)} categorical features")
        
        elif encoding_method == 'label':
            # Label encoding
            for col in cat_cols:
                le = LabelEncoder()
                df_copy[col] = le.fit_transform(df_copy[col].astype(str))
                self.label_encoders[col] = le
            print(f"Label encoded {len(cat_cols)} categorical features")
        
        print(f"Total features after encoding: {len(df_copy.columns)}")
        
        return df_copy
    
    def scale_features(self, df, method='standard', exclude_columns=None):
        """
        Scale numerical features.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        method : str
            'standard', 'minmax', or 'robust'
        exclude_columns : list
            Columns to exclude from scaling
            
        Returns:
        --------
        pd.DataFrame, scaler
            Scaled dataframe and fitted scaler
        """
        print(f"Scaling features using {method} scaling...")
        df_copy = df.copy()
        
        if exclude_columns is None:
            exclude_columns = []
        
        # Get numeric columns to scale
        numeric_cols = df_copy.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in exclude_columns and 'ID' not in col.upper()]
        
        # Initialize scaler
        if method == 'standard':
            self.scaler = StandardScaler()
        elif method == 'minmax':
            self.scaler = MinMaxScaler()
        elif method == 'robust':
            self.scaler = RobustScaler()
        else:
            raise ValueError(f"Unknown scaling method: {method}")
        
        # Fit and transform
        df_copy[numeric_cols] = self.scaler.fit_transform(df_copy[numeric_cols])
        
        print(f"Scaled {len(numeric_cols)} numerical features")
        self.feature_names = numeric_cols
        
        return df_copy
    
    def apply_pca(self, df, n_components=None, variance_threshold=0.90, exclude_columns=None):
        """
        Apply Principal Component Analysis for dimensionality reduction.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe (should be scaled)
        n_components : int
            Number of components (None = auto based on variance)
        variance_threshold : float
            Cumulative variance threshold for auto component selection
        exclude_columns : list
            Columns to exclude from PCA
            
        Returns:
        --------
        pd.DataFrame, explained_variance
            Transformed dataframe and explained variance ratios
        """
        print("Applying PCA...")
        
        if exclude_columns is None:
            exclude_columns = []
        
        # Get numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [col for col in numeric_cols if col not in exclude_columns]
        
        X = df[numeric_cols].values
        
        if n_components is None:
            # Determine optimal number of components
            pca_temp = PCA()
            pca_temp.fit(X)
            cumsum = np.cumsum(pca_temp.explained_variance_ratio_)
            n_components = np.argmax(cumsum >= variance_threshold) + 1
            print(f"Auto-selected {n_components} components for {variance_threshold*100}% variance")
        
        # Apply PCA
        self.pca = PCA(n_components=n_components)
        X_pca = self.pca.fit_transform(X)
        
        # Create DataFrame
        pca_cols = [f'PC{i+1}' for i in range(n_components)]
        df_pca = pd.DataFrame(X_pca, columns=pca_cols, index=df.index)
        
        # Add back excluded columns
        for col in exclude_columns:
            if col in df.columns:
                df_pca[col] = df[col].values
        
        print(f"PCA reduced {len(numeric_cols)} features to {n_components} components")
        print(f"Explained variance: {self.pca.explained_variance_ratio_.sum()*100:.2f}%")
        
        return df_pca, self.pca.explained_variance_ratio_
    
    def get_preprocessing_pipeline(self, df, 
                                     handle_missing=True,
                                     handle_outliers=True,
                                     engineer_features=True,
                                     encode_categorical=True,
                                     scale_features=True,
                                     apply_pca=False,
                                     scaling_method='standard',
                                     pca_components=None):
        """
        Complete preprocessing pipeline.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        handle_missing : bool
            Whether to handle missing values
        handle_outliers : bool
            Whether to handle outliers
        engineer_features : bool
            Whether to engineer new features
        encode_categorical : bool
            Whether to encode categorical variables
        scale_features : bool
            Whether to scale features
        apply_pca : bool
            Whether to apply PCA
        scaling_method : str
            Scaling method to use
        pca_components : int
            Number of PCA components
            
        Returns:
        --------
        pd.DataFrame
            Fully preprocessed dataframe
        """
        print("="*80)
        print("STARTING PREPROCESSING PIPELINE")
        print("="*80)
        
        df_processed = df.copy()
        
        # Store ID column if exists
        id_col = None
        for col in df_processed.columns:
            if 'ID' in col.upper():
                id_col = col
                break
        
        # Step 1: Handle missing values
        if handle_missing:
            df_processed = self.handle_missing_values(df_processed)
        
        # Step 2: Handle outliers
        if handle_outliers:
            outlier_info = self.detect_outliers(df_processed)
            print(f"\nDetected outliers in {len(outlier_info)} features")
            df_processed = self.handle_outliers(df_processed, method='cap', outlier_info=outlier_info)
        
        # Step 3: Feature engineering
        if engineer_features:
            df_processed = self.feature_engineering(df_processed)
        
        # Step 4: Encode categorical
        if encode_categorical:
            exclude = [id_col] if id_col else []
            df_processed = self.encode_categorical(df_processed, encoding_method='onehot', 
                                                     exclude_columns=exclude)
        
        # Step 5: Scale features
        if scale_features:
            exclude = [id_col] if id_col else []
            df_processed = self.scale_features(df_processed, method=scaling_method, 
                                                exclude_columns=exclude)
        
        # Step 6: Apply PCA
        if apply_pca:
            exclude = [id_col] if id_col else []
            df_processed, var_ratios = self.apply_pca(df_processed, n_components=pca_components,
                                                        exclude_columns=exclude)
        
        print("\n" + "="*80)
        print("PREPROCESSING COMPLETE")
        print("="*80)
        print(f"Final shape: {df_processed.shape}")
        print(f"Final features: {df_processed.columns.tolist()}")
        
        return df_processed
    
    def save_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Save preprocessing objects."""
        preprocessing_objects = {
            'scaler': self.scaler,
            'pca': self.pca,
            'label_encoders': self.label_encoders,
            'imputers': self.imputers,
            'feature_names': self.feature_names
        }
        joblib.dump(preprocessing_objects, filepath)
        print(f"Saved preprocessor to {filepath}")
    
    def load_preprocessor(self, filepath='models/preprocessor.pkl'):
        """Load preprocessing objects."""
        preprocessing_objects = joblib.load(filepath)
        self.scaler = preprocessing_objects['scaler']
        self.pca = preprocessing_objects['pca']
        self.label_encoders = preprocessing_objects['label_encoders']
        self.imputers = preprocessing_objects['imputers']
        self.feature_names = preprocessing_objects['feature_names']
        print(f"Loaded preprocessor from {filepath}")


# Example usage
if __name__ == "__main__":
    # Example with synthetic data
    from data_loader import CustomerDataLoader
    
    loader = CustomerDataLoader(data_dir='../data')
    df = loader.generate_synthetic_data(n_customers=1000)
    
    preprocessor = DataPreprocessor()
    df_processed = preprocessor.get_preprocessing_pipeline(
        df,
        handle_missing=True,
        handle_outliers=True,
        engineer_features=True,
        encode_categorical=True,
        scale_features=True,
        apply_pca=False
    )
    
    print("\nProcessed data shape:", df_processed.shape)
    print(df_processed.head())
