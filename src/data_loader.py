"""
Data Loading and Generation Module
Handles data loading from various sources and synthetic data generation.
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os


class CustomerDataLoader:
    """Load customer data from various sources."""
    
    def __init__(self, data_dir='data'):
        """
        Initialize the data loader.
        
        Parameters:
        -----------
        data_dir : str
            Base directory for data files
        """
        self.data_dir = data_dir
        self.raw_dir = os.path.join(data_dir, 'raw')
        self.processed_dir = os.path.join(data_dir, 'processed')
        self.synthetic_dir = os.path.join(data_dir, 'synthetic')
    
    def load_csv(self, filename, subdirectory='raw'):
        """
        Load data from CSV file.
        
        Parameters:
        -----------
        filename : str
            Name of the CSV file
        subdirectory : str
            Subdirectory ('raw', 'processed', 'synthetic')
            
        Returns:
        --------
        pd.DataFrame
            Loaded dataframe
        """
        filepath = os.path.join(self.data_dir, subdirectory, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} records from {filename}")
        print(f"Shape: {df.shape}")
        
        return df
    
    def save_csv(self, df, filename, subdirectory='processed'):
        """
        Save dataframe to CSV file.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Dataframe to save
        filename : str
            Output filename
        subdirectory : str
            Subdirectory to save to
        """
        filepath = os.path.join(self.data_dir, subdirectory, filename)
        df.to_csv(filepath, index=False)
        print(f"Saved {len(df)} records to {filepath}")
    
    def generate_synthetic_data(self, n_customers=2000, random_state=42):
        """
        Generate synthetic customer data for analysis.
        
        Parameters:
        -----------
        n_customers : int
            Number of customer records to generate
        random_state : int
            Random seed for reproducibility
            
        Returns:
        --------
        pd.DataFrame
            Synthetic customer dataset
        """
        np.random.seed(random_state)
        fake = Faker()
        Faker.seed(random_state)
        
        print(f"Generating {n_customers} synthetic customer records...")
        
        # Generate customer IDs
        customer_ids = [f"CUST_{str(i).zfill(6)}" for i in range(1, n_customers + 1)]
        
        # Demographic features
        ages = np.random.normal(45, 15, n_customers).astype(int)
        ages = np.clip(ages, 18, 80)
        
        genders = np.random.choice(['Male', 'Female', 'Other'], 
                                    n_customers, 
                                    p=[0.48, 0.48, 0.04])
        
        marital_status = np.random.choice(['Single', 'Married', 'Divorced', 'Widowed'],
                                           n_customers,
                                           p=[0.30, 0.50, 0.15, 0.05])
        
        education = np.random.choice(['High School', 'Bachelor', 'Master', 'PhD'],
                                      n_customers,
                                      p=[0.25, 0.45, 0.25, 0.05])
        
        # Income based on age and education (with correlation)
        base_income = np.random.normal(60000, 25000, n_customers)
        education_bonus = np.where(education == 'PhD', 40000,
                                    np.where(education == 'Master', 25000,
                                             np.where(education == 'Bachelor', 10000, 0)))
        age_factor = (ages - 18) * 500
        incomes = base_income + education_bonus + age_factor
        incomes = np.clip(incomes, 20000, 200000).astype(int)
        
        # Geographic location
        cities = [fake.city() for _ in range(n_customers)]
        
        # Behavioral features (RFM)
        # Create distinct customer groups through different distributions
        segment_distribution = np.random.choice([0, 1, 2, 3, 4], n_customers, 
                                                 p=[0.15, 0.25, 0.30, 0.20, 0.10])
        
        recency = []
        frequency = []
        monetary = []
        
        for segment in segment_distribution:
            if segment == 0:  # VIP Champions
                recency.append(np.random.randint(1, 15))
                frequency.append(np.random.randint(15, 30))
                monetary.append(np.random.randint(8000, 20000))
            elif segment == 1:  # Loyal Customers
                recency.append(np.random.randint(15, 45))
                frequency.append(np.random.randint(8, 20))
                monetary.append(np.random.randint(3000, 10000))
            elif segment == 2:  # Potential Loyalists
                recency.append(np.random.randint(20, 60))
                frequency.append(np.random.randint(5, 12))
                monetary.append(np.random.randint(1500, 5000))
            elif segment == 3:  # Price Sensitive
                recency.append(np.random.randint(30, 90))
                frequency.append(np.random.randint(3, 8))
                monetary.append(np.random.randint(500, 2500))
            else:  # At Risk/Dormant
                recency.append(np.random.randint(90, 365))
                frequency.append(np.random.randint(1, 5))
                monetary.append(np.random.randint(200, 1500))
        
        recency = np.array(recency)
        frequency = np.array(frequency)
        monetary = np.array(monetary)
        
        # Calculate derived metrics
        avg_order_value = monetary / frequency
        
        # Engagement features
        website_visits = np.random.poisson(frequency * 2, n_customers)
        email_open_rate = np.random.uniform(0.1, 0.9, n_customers)
        email_click_rate = email_open_rate * np.random.uniform(0.1, 0.5, n_customers)
        
        # Tenure (days as customer)
        tenure_days = np.random.randint(30, 1825, n_customers)  # 1 month to 5 years
        
        # Channel preference
        channel_pref = np.random.choice(['Online', 'In-Store', 'Mobile', 'Mixed'],
                                         n_customers,
                                         p=[0.35, 0.25, 0.20, 0.20])
        
        # Product categories (number of different categories purchased)
        num_categories = np.random.randint(1, 8, n_customers)
        
        # Discount usage
        discount_usage = np.random.uniform(0, 0.8, n_customers)
        
        # Returns
        num_returns = np.random.poisson(frequency * 0.1, n_customers)
        
        # Payment method
        payment_method = np.random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Cash'],
                                           n_customers,
                                           p=[0.45, 0.30, 0.15, 0.10])
        
        # Customer service interactions
        cs_interactions = np.random.poisson(2, n_customers)
        
        # Loyalty program
        loyalty_member = np.random.choice([True, False], n_customers, p=[0.65, 0.35])
        
        # Create DataFrame
        df = pd.DataFrame({
            'CustomerID': customer_ids,
            'Age': ages,
            'Gender': genders,
            'MaritalStatus': marital_status,
            'Education': education,
            'Income': incomes,
            'City': cities,
            'Recency': recency,
            'Frequency': frequency,
            'Monetary': monetary,
            'AvgOrderValue': avg_order_value,
            'WebsiteVisits': website_visits,
            'EmailOpenRate': email_open_rate,
            'EmailClickRate': email_click_rate,
            'TenureDays': tenure_days,
            'ChannelPreference': channel_pref,
            'NumCategories': num_categories,
            'DiscountUsage': discount_usage,
            'NumReturns': num_returns,
            'PaymentMethod': payment_method,
            'CSInteractions': cs_interactions,
            'LoyaltyMember': loyalty_member
        })
        
        # Add some missing values to make it realistic
        missing_indices = np.random.choice(df.index, size=int(n_customers * 0.03), replace=False)
        df.loc[missing_indices, 'Income'] = np.nan
        
        missing_indices = np.random.choice(df.index, size=int(n_customers * 0.02), replace=False)
        df.loc[missing_indices, 'EmailOpenRate'] = np.nan
        
        print(f"Generated dataset shape: {df.shape}")
        print(f"Features: {df.columns.tolist()}")
        
        return df
    
    def get_data_summary(self, df):
        """
        Get comprehensive summary of the dataset.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
            
        Returns:
        --------
        dict
            Dictionary containing summary statistics
        """
        summary = {
            'shape': df.shape,
            'columns': df.columns.tolist(),
            'dtypes': df.dtypes.to_dict(),
            'missing_values': df.isnull().sum().to_dict(),
            'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict(),
            'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
            'numeric_summary': df.describe().to_dict(),
            'categorical_columns': df.select_dtypes(include=['object', 'bool']).columns.tolist(),
            'numeric_columns': df.select_dtypes(include=[np.number]).columns.tolist()
        }
        
        return summary
    
    def print_data_summary(self, df):
        """
        Print comprehensive data summary.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Input dataframe
        """
        print("=" * 80)
        print("DATASET SUMMARY")
        print("=" * 80)
        
        print(f"\nShape: {df.shape[0]} rows × {df.shape[1]} columns")
        print(f"Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print("\n" + "-" * 80)
        print("DATA TYPES")
        print("-" * 80)
        print(df.dtypes.value_counts())
        
        print("\n" + "-" * 80)
        print("MISSING VALUES")
        print("-" * 80)
        missing = df.isnull().sum()
        missing_pct = (missing / len(df)) * 100
        missing_df = pd.DataFrame({
            'Missing Count': missing[missing > 0],
            'Percentage': missing_pct[missing > 0]
        })
        if len(missing_df) > 0:
            print(missing_df.sort_values('Percentage', ascending=False))
        else:
            print("No missing values found!")
        
        print("\n" + "-" * 80)
        print("FIRST 5 ROWS")
        print("-" * 80)
        print(df.head())
        
        print("\n" + "-" * 80)
        print("NUMERICAL FEATURES STATISTICS")
        print("-" * 80)
        print(df.describe())
        
        print("\n" + "-" * 80)
        print("CATEGORICAL FEATURES")
        print("-" * 80)
        cat_cols = df.select_dtypes(include=['object', 'bool']).columns
        for col in cat_cols:
            print(f"\n{col}:")
            print(df[col].value_counts())
        
        print("\n" + "=" * 80)


# Example usage
if __name__ == "__main__":
    # Initialize loader
    loader = CustomerDataLoader(data_dir='../data')
    
    # Generate synthetic data
    df = loader.generate_synthetic_data(n_customers=2000, random_state=42)
    
    # Print summary
    loader.print_data_summary(df)
    
    # Save the data
    loader.save_csv(df, 'customer_data.csv', subdirectory='synthetic')
