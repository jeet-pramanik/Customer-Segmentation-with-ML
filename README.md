# Customer Segmentation with Machine Learning

## 🎯 Project Overview

This project implements an advanced **Customer Segmentation system** using unsupervised machine learning techniques to help businesses identify distinct customer groups based on behavioral, demographic, and transactional data. The insights enable personalized marketing strategies and improved customer relationship management.

## 🚀 Key Features

- **Multiple Clustering Algorithms**: K-Means, DBSCAN, Hierarchical Clustering, and Gaussian Mixture Models
- **Optimal Cluster Detection**: Elbow Method, Silhouette Analysis, Calinski-Harabasz, Davies-Bouldin Index
- **Comprehensive Customer Profiling**: Demographic, behavioral, engagement, and value-based analysis
- **Actionable Marketing Strategies**: Personalized recommendations for each customer segment
- **Interactive Visualizations**: Plotly-based dashboard for stakeholder communication
- **Production-Ready Pipeline**: API endpoints and batch scoring capabilities

## 📊 Business Impact

- **Improve Marketing ROI** by 15-30%
- **Increase Customer Retention** by 10-20%
- **Boost Cross-sell/Upsell** by 25%+
- **Reduce Customer Acquisition Costs** through optimized targeting
- **Enhance Customer Satisfaction** via personalization

## 🗂️ Project Structure

```
Customer Segmentation with ML/
├── data/                          # Data directory
│   ├── raw/                       # Raw data files
│   ├── processed/                 # Cleaned and processed data
│   └── synthetic/                 # Generated synthetic data
├── notebooks/                     # Jupyter notebooks
│   ├── 01_data_exploration.ipynb
│   ├── 02_preprocessing.ipynb
│   ├── 03_kmeans_clustering.ipynb
│   ├── 04_dbscan_clustering.ipynb
│   ├── 05_cluster_profiling.ipynb
│   └── 06_business_insights.ipynb
├── src/                           # Source code
│   ├── __init__.py
│   ├── data_loader.py            # Data loading utilities
│   ├── preprocessing.py          # Data preprocessing pipeline
│   ├── clustering.py             # Clustering algorithms
│   ├── evaluation.py             # Model evaluation metrics
│   ├── profiling.py              # Cluster profiling
│   ├── visualization.py          # Visualization functions
│   └── deployment.py             # Production pipeline
├── models/                        # Saved model files
│   ├── kmeans_model.pkl
│   ├── scaler.pkl
│   └── preprocessing_pipeline.pkl
├── reports/                       # Generated reports
│   ├── figures/                  # Saved visualizations
│   ├── segment_profiles.pdf
│   └── marketing_strategies.pdf
├── visualizations/                # Interactive dashboards
│   └── dashboard.html
├── requirements.txt              # Project dependencies
├── project.docs.md              # Detailed development documentation
└── README.md                    # This file
```

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd "Customer Segmentation with ML"
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 📈 Usage

### Running Jupyter Notebooks

```bash
jupyter notebook
```

Navigate to the `notebooks/` directory and run the notebooks in sequence:

1. **01_data_exploration.ipynb** - Understand the data
2. **02_preprocessing.ipynb** - Clean and prepare data
3. **03_kmeans_clustering.ipynb** - K-Means implementation
4. **04_dbscan_clustering.ipynb** - DBSCAN implementation
5. **05_cluster_profiling.ipynb** - Analyze segments
6. **06_business_insights.ipynb** - Generate strategies

### Using the Python Pipeline

```python
from src.deployment import CustomerSegmentationPipeline

# Initialize pipeline
pipeline = CustomerSegmentationPipeline()
pipeline.load_model('models/kmeans_model.pkl')

# Predict segment for new customer
customer_data = {
    'age': 35,
    'income': 75000,
    'recency': 15,
    'frequency': 8,
    'monetary': 2500
}

segment = pipeline.predict_segment(customer_data)
recommendations = pipeline.get_recommendations(segment)
print(f"Customer Segment: {segment}")
print(f"Recommendations: {recommendations}")
```

### Running the API (Flask)

```bash
python src/deployment.py
```

API Endpoints:
- `POST /predict_segment` - Predict customer segment
- `GET /segment_profile/<segment_name>` - Get segment details
- `GET /recommendations/<segment_name>` - Get marketing recommendations

## 📊 Customer Segments

The analysis identifies distinct customer segments such as:

1. **High-Value Loyalists** - Premium customers with high engagement
2. **Price-Sensitive Shoppers** - Budget-conscious, frequent buyers
3. **New Explorers** - Recent customers with growth potential
4. **Dormant Customers** - Inactive customers needing re-engagement
5. **VIP Champions** - Top-tier customers driving revenue

*Note: Actual segments are data-dependent*

## 🔬 Methodology

### Data Features
- **Demographic**: Age, Gender, Income, Location, Education
- **Behavioral**: Recency, Frequency, Monetary (RFM), Purchase patterns
- **Engagement**: Website visits, Email interactions, Social media activity
- **Transactional**: Order value, Product categories, Payment methods

### Algorithms
- **K-Means Clustering** - Partitioning-based approach
- **DBSCAN** - Density-based with noise detection
- **Hierarchical Clustering** - Dendrogram-based segmentation
- **Gaussian Mixture Models** - Probabilistic clustering

### Evaluation Metrics
- Silhouette Score
- Calinski-Harabasz Index
- Davies-Bouldin Index
- Within-Cluster Sum of Squares (WCSS)

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - *Initial work*

## 🙏 Acknowledgments

- Dataset sources: UCI ML Repository, Kaggle
- Inspired by industry best practices in customer analytics
- Built with scikit-learn and the Python data science ecosystem

## 📞 Contact

For questions or feedback, please reach out at [your-email@example.com]

---

**Built with ❤️ for better customer understanding**
