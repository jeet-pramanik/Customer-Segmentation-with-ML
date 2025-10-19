"""
Deployment Module
Production pipeline for customer segmentation with API endpoints.
"""

import pandas as pd
import numpy as np
import joblib
import json
from flask import Flask, request, jsonify
import os


class CustomerSegmentationPipeline:
    """Production pipeline for customer segmentation."""
    
    def __init__(self):
        """Initialize pipeline."""
        self.model = None
        self.scaler = None
        self.pca = None
        self.preprocessor = None
        self.feature_names = None
        self.segment_profiles = None
        self.segment_names = {}
        self.marketing_strategies = {}
    
    def load_model(self, model_path='models/kmeans_model.pkl'):
        """
        Load trained clustering model.
        
        Parameters:
        -----------
        model_path : str
            Path to model file
        """
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print(f"Model loaded from {model_path}")
        else:
            print(f"Model file not found: {model_path}")
    
    def load_preprocessor(self, preprocessor_path='models/preprocessor.pkl'):
        """
        Load preprocessing pipeline.
        
        Parameters:
        -----------
        preprocessor_path : str
            Path to preprocessor file
        """
        if os.path.exists(preprocessor_path):
            preprocessor_objects = joblib.load(preprocessor_path)
            self.scaler = preprocessor_objects.get('scaler')
            self.pca = preprocessor_objects.get('pca')
            self.feature_names = preprocessor_objects.get('feature_names')
            print(f"Preprocessor loaded from {preprocessor_path}")
        else:
            print(f"Preprocessor file not found: {preprocessor_path}")
    
    def load_segment_info(self, profiles_path='models/segment_profiles.json',
                           names_path='models/segment_names.json',
                           strategies_path='models/marketing_strategies.json'):
        """
        Load segment profiles, names, and strategies.
        
        Parameters:
        -----------
        profiles_path : str
            Path to segment profiles JSON
        names_path : str
            Path to segment names JSON
        strategies_path : str
            Path to marketing strategies JSON
        """
        if os.path.exists(profiles_path):
            with open(profiles_path, 'r') as f:
                self.segment_profiles = json.load(f)
            print(f"Segment profiles loaded from {profiles_path}")
        
        if os.path.exists(names_path):
            with open(names_path, 'r') as f:
                # Convert string keys back to integers
                self.segment_names = {int(k): v for k, v in json.load(f).items()}
            print(f"Segment names loaded from {names_path}")
        
        if os.path.exists(strategies_path):
            with open(strategies_path, 'r') as f:
                self.marketing_strategies = json.load(f)
            print(f"Marketing strategies loaded from {strategies_path}")
    
    def preprocess_customer(self, customer_data):
        """
        Preprocess customer data for prediction.
        
        Parameters:
        -----------
        customer_data : dict or pd.DataFrame
            Customer features
            
        Returns:
        --------
        np.array
            Preprocessed features
        """
        if isinstance(customer_data, dict):
            df = pd.DataFrame([customer_data])
        else:
            df = customer_data.copy()
        
        # Apply scaling if scaler is loaded
        if self.scaler is not None and self.feature_names is not None:
            # Ensure all required features are present
            missing_features = set(self.feature_names) - set(df.columns)
            if missing_features:
                print(f"Warning: Missing features: {missing_features}")
                # Fill missing with zeros or median
                for feat in missing_features:
                    df[feat] = 0
            
            # Select and order features
            X = df[self.feature_names].values
            X_scaled = self.scaler.transform(X)
            
            # Apply PCA if available
            if self.pca is not None:
                X_scaled = self.pca.transform(X_scaled)
            
            return X_scaled
        else:
            return df.values
    
    def predict_segment(self, customer_data):
        """
        Predict customer segment.
        
        Parameters:
        -----------
        customer_data : dict or pd.DataFrame
            Customer features
            
        Returns:
        --------
        dict
            Prediction results with segment info
        """
        if self.model is None:
            return {"error": "Model not loaded"}
        
        # Preprocess
        X = self.preprocess_customer(customer_data)
        
        # Predict
        cluster_id = int(self.model.predict(X)[0])
        
        # Get segment name
        segment_name = self.segment_names.get(cluster_id, f"Segment {cluster_id}")
        
        # Prepare response
        result = {
            'cluster_id': cluster_id,
            'segment_name': segment_name,
            'confidence': 'high'  # Could calculate distance to centroid
        }
        
        # Add segment characteristics if available
        if self.segment_profiles and str(cluster_id) in self.segment_profiles:
            result['segment_characteristics'] = self.segment_profiles[str(cluster_id)]
        
        return result
    
    def get_recommendations(self, segment_id_or_name):
        """
        Get marketing recommendations for a segment.
        
        Parameters:
        -----------
        segment_id_or_name : int or str
            Segment ID or name
            
        Returns:
        --------
        dict
            Marketing recommendations
        """
        # Try to find by ID first
        segment_key = str(segment_id_or_name)
        
        if segment_key in self.marketing_strategies:
            return self.marketing_strategies[segment_key]
        
        # Try to find by name
        for seg_id, name in self.segment_names.items():
            if name == segment_id_or_name:
                segment_key = str(seg_id)
                if segment_key in self.marketing_strategies:
                    return self.marketing_strategies[segment_key]
        
        return {"error": "Segment not found"}
    
    def batch_score(self, customers_df, output_path='data/processed/scored_customers.csv'):
        """
        Score entire customer database.
        
        Parameters:
        -----------
        customers_df : pd.DataFrame
            Customer dataframe
        output_path : str
            Path to save scored results
            
        Returns:
        --------
        pd.DataFrame
            Dataframe with segment assignments
        """
        if self.model is None:
            print("Error: Model not loaded")
            return None
        
        print(f"Scoring {len(customers_df)} customers...")
        
        # Preprocess
        X = self.preprocess_customer(customers_df)
        
        # Predict
        cluster_ids = self.model.predict(X)
        
        # Add to dataframe
        result_df = customers_df.copy()
        result_df['Cluster'] = cluster_ids
        result_df['Segment'] = [self.segment_names.get(cid, f"Segment {cid}") 
                                  for cid in cluster_ids]
        
        # Save
        result_df.to_csv(output_path, index=False)
        print(f"Scored customers saved to {output_path}")
        
        # Summary
        print(f"\nSegment Distribution:")
        print(result_df['Segment'].value_counts())
        
        return result_df
    
    def save_all_artifacts(self, model, scaler, pca, feature_names, 
                            segment_profiles, segment_names, marketing_strategies,
                            models_dir='models'):
        """
        Save all pipeline artifacts.
        
        Parameters:
        -----------
        model : clustering model
            Trained clustering model
        scaler : scaler object
            Fitted scaler
        pca : PCA object
            Fitted PCA
        feature_names : list
            Feature names
        segment_profiles : dict
            Segment profiles
        segment_names : dict
            Segment names
        marketing_strategies : dict
            Marketing strategies
        models_dir : str
            Directory to save models
        """
        os.makedirs(models_dir, exist_ok=True)
        
        # Save model
        joblib.dump(model, os.path.join(models_dir, 'kmeans_model.pkl'))
        print(f"Model saved")
        
        # Save preprocessor
        preprocessor = {
            'scaler': scaler,
            'pca': pca,
            'feature_names': feature_names
        }
        joblib.dump(preprocessor, os.path.join(models_dir, 'preprocessor.pkl'))
        print(f"Preprocessor saved")
        
        # Save segment info as JSON
        with open(os.path.join(models_dir, 'segment_profiles.json'), 'w') as f:
            json.dump(segment_profiles, f, indent=2)
        
        with open(os.path.join(models_dir, 'segment_names.json'), 'w') as f:
            # Convert int keys to strings for JSON
            json.dump({str(k): v for k, v in segment_names.items()}, f, indent=2)
        
        with open(os.path.join(models_dir, 'marketing_strategies.json'), 'w') as f:
            json.dump(marketing_strategies, f, indent=2)
        
        print(f"All artifacts saved to {models_dir}/")


# Flask API
app = Flask(__name__)
pipeline = CustomerSegmentationPipeline()


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "model_loaded": pipeline.model is not None})


@app.route('/predict', methods=['POST'])
def predict_segment():
    """
    Predict customer segment.
    
    Request body: JSON with customer features
    Returns: Segment prediction
    """
    try:
        customer_data = request.json
        result = pipeline.predict_segment(customer_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/segment/<segment_id>', methods=['GET'])
def get_segment_profile(segment_id):
    """Get segment profile by ID."""
    try:
        segment_key = str(segment_id)
        if segment_key in pipeline.segment_profiles:
            return jsonify(pipeline.segment_profiles[segment_key])
        else:
            return jsonify({"error": "Segment not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/recommendations/<segment_id>', methods=['GET'])
def get_recommendations(segment_id):
    """Get marketing recommendations for segment."""
    try:
        recommendations = pipeline.get_recommendations(segment_id)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/segments', methods=['GET'])
def list_segments():
    """List all available segments."""
    return jsonify({
        "segments": pipeline.segment_names,
        "count": len(pipeline.segment_names)
    })


def initialize_app():
    """Initialize the Flask app with model loading."""
    print("Initializing Customer Segmentation API...")
    pipeline.load_model('models/kmeans_model.pkl')
    pipeline.load_preprocessor('models/preprocessor.pkl')
    pipeline.load_segment_info()
    print("API ready!")


if __name__ == "__main__":
    initialize_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
