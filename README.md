# Customer Segmentation with Machine Learning

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0%2B-orange.svg)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

An advanced **Customer Segmentation System** using unsupervised machine learning to identify distinct customer groups based on behavioral, demographic, and transactional data. This production-ready solution enables personalized marketing strategies and improved customer relationship management.

**Built with 2,260+ lines of production-ready Python code** featuring multiple clustering algorithms, comprehensive evaluation metrics, and a REST API for deployment.

## 🚀 Key Features

- **Multiple Clustering Algorithms**: K-Means, DBSCAN, Hierarchical Clustering, and Gaussian Mixture Models
- **Optimal Cluster Detection**: Elbow Method, Silhouette Analysis, Calinski-Harabasz Index, Davies-Bouldin Index
- **Comprehensive Customer Profiling**: Demographic, behavioral, engagement, and value-based analysis
- **Actionable Marketing Strategies**: Personalized recommendations for each customer segment
- **Interactive Visualizations**: Matplotlib, Seaborn, and Plotly-based dashboards
- **Production-Ready API**: Flask REST API with 5 endpoints for real-time predictions
- **Synthetic Data Generation**: Built-in synthetic customer data generator with 22+ features

## 📊 Business Impact

- **Improve Marketing ROI** by targeting the right customers with the right message
- **Increase Customer Retention** through personalized engagement strategies
- **Boost Cross-sell/Upsell** by identifying high-value customer segments
- **Reduce Customer Acquisition Costs** through optimized targeting
- **Enhance Customer Satisfaction** via personalized experiences

## 🗂️ Project Structure

```
Customer Segmentation with ML/
├── src/                           # Source code (2,260+ lines)
│   ├── __init__.py               # Package initialization
│   ├── data_loader.py            # Data loading & synthetic data generation (330 lines)
│   ├── preprocessing.py          # Data preprocessing pipeline (550 lines)
│   ├── clustering.py             # 4 clustering algorithms (520 lines)
│   ├── evaluation.py             # Evaluation metrics (420 lines)
│   ├── profiling.py              # Customer profiling (350 lines)
│   ├── visualization.py          # Visualizations (280 lines)
│   └── deployment.py             # Flask REST API (320 lines)
│
├── notebooks/                     # Jupyter notebooks
│   └── 01_data_exploration.ipynb # Complete EDA workflow
│
├── data/                          # Data directories
│   ├── raw/                      # Raw data files
│   ├── processed/                # Cleaned and processed data
│   └── synthetic/                # Generated synthetic data
│
├── models/                        # Saved model files (.pkl, .joblib)
├── reports/                       # Generated reports
│   └── figures/                  # Saved visualizations
├── visualizations/                # Interactive dashboards
│
├── requirements.txt              # Python dependencies (35 packages)
├── .gitignore                   # Git ignore configuration
├── README.md                    # This file
└── QUICKSTART.md               # Quick setup guide
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Quick Start

1. **Clone the Repository**
```bash
git clone https://github.com/jeet-pramanik/Customer-Segmentation-ML.git
cd Customer-Segmentation-ML
```

2. **Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

**For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)**

## 📈 Usage

### Quick Start with Jupyter Notebook

```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

This notebook demonstrates:
- Synthetic customer data generation (2000+ customers, 22+ features)
- Exploratory data analysis (EDA)
- Data visualization and statistics
- Feature correlation analysis

### Using Python Modules

#### 1. Generate Synthetic Data
```python
from src.data_loader import CustomerDataLoader

# Generate synthetic customer data
loader = CustomerDataLoader()
data = loader.generate_synthetic_data(n_customers=2000)
print(f"Generated {len(data)} customer records")
```

#### 2. Preprocess Data
```python
from src.preprocessing import DataPreprocessor

# Initialize preprocessor
preprocessor = DataPreprocessor()

# Complete preprocessing pipeline
processed_data = preprocessor.get_preprocessing_pipeline(data)
```

#### 3. Perform Clustering
```python
from src.clustering import KMeansClusterer

# K-Means clustering
kmeans = KMeansClusterer()
optimal_k = kmeans.find_optimal_clusters(processed_data, method='elbow')
labels = kmeans.fit_predict(processed_data, n_clusters=optimal_k)
```

#### 4. Evaluate Clustering
```python
from src.evaluation import ClusterEvaluator

# Evaluate clustering quality
evaluator = ClusterEvaluator()
metrics = evaluator.evaluate_clustering(processed_data, labels)
print(f"Silhouette Score: {metrics['silhouette']:.3f}")
```

#### 5. Profile Customer Segments
```python
from src.profiling import ClusterProfiler

# Create customer profiles
profiler = ClusterProfiler()
profiles = profiler.create_cluster_profiles(data, labels)
strategies = profiler.generate_marketing_strategies(profiles)
```

### Running the Flask API

```bash
python src/deployment.py
```

The API will start on `http://localhost:5000` with the following endpoints:

- **GET** `/health` - Health check
- **POST** `/predict` - Predict customer segment
- **GET** `/segment/<segment_id>` - Get segment profile
- **GET** `/recommendations/<segment_id>` - Get marketing recommendations
- **GET** `/segments` - List all segments

**Example API Request:**
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "income": 75000,
    "recency": 15,
    "frequency": 8,
    "monetary": 2500
  }'
```

## 📊 Data Features

The system analyzes 22+ customer features across multiple dimensions:

### Demographic Features
- Age, Gender, Marital Status
- Income Level, Education
- Geographic Location
- Homeownership Status

### Behavioral Features (RFM Analysis)
- **Recency**: Days since last purchase
- **Frequency**: Number of purchases
- **Monetary**: Total spending amount
- Average Order Value
- Product Category Preferences

### Engagement Features
- Website Visit Frequency
- Email Engagement (open rate, click rate)
- Social Media Activity
- Customer Service Interactions
- Loyalty Program Participation

### Transactional Features
- Purchase Channel (online, in-store, mobile)
- Payment Method Preferences
- Return/Exchange History
- Lifetime Value (LTV)

## 🔬 Methodology

### Clustering Algorithms Implemented

1. **K-Means Clustering**
   - Partitioning-based approach
   - Optimal k selection via Elbow Method and Silhouette Analysis
   - Fast and scalable

2. **DBSCAN (Density-Based Spatial Clustering)**
   - Density-based clustering
   - Automatic noise detection
   - No need to specify number of clusters

3. **Hierarchical Clustering**
   - Agglomerative clustering
   - Dendrogram visualization
   - Multiple linkage methods (ward, average, complete)

4. **Gaussian Mixture Models (GMM)**
   - Probabilistic clustering
   - Soft cluster assignments
   - BIC/AIC for model selection

### Evaluation Metrics

- **Silhouette Score**: Measures cluster cohesion and separation (-1 to 1)
- **Calinski-Harabasz Index**: Ratio of between-cluster to within-cluster dispersion
- **Davies-Bouldin Index**: Average similarity between clusters (lower is better)
- **Within-Cluster Sum of Squares (WCSS)**: For Elbow Method

## � Dependencies

**Core Libraries:**
- **Python**: 3.8+
- **scikit-learn**: 1.0+ (ML algorithms)
- **pandas**: 1.3+ (data manipulation)
- **numpy**: 1.21+ (numerical computing)
- **matplotlib**: 3.4+ (visualizations)
- **seaborn**: 0.11+ (statistical visualizations)
- **plotly**: 5.0+ (interactive dashboards)
- **Flask**: 2.0+ (REST API)
- **scipy**: 1.7+ (statistical analysis)

See [requirements.txt](requirements.txt) for the complete list of 35 dependencies.

## 🎯 Project Highlights

- ✅ **2,260+ lines** of production-ready Python code
- ✅ **8 modular components** for easy maintenance and extensibility
- ✅ **4 clustering algorithms** with comprehensive evaluation
- ✅ **REST API** with 5 endpoints for production deployment
- ✅ **Synthetic data generator** for testing and demos
- ✅ **Interactive visualizations** for stakeholder presentations
- ✅ **Comprehensive documentation** with code examples

## 🚧 Roadmap

- [ ] Additional Jupyter notebooks (preprocessing, clustering workflows)
- [ ] Unit tests and integration tests
- [ ] CI/CD pipeline setup
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/Azure/GCP)
- [ ] Real-time dashboard with live updates
- [ ] A/B testing framework integration

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit your changes**: `git commit -m 'Add AmazingFeature'`
4. **Push to the branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

**Areas for Contribution:**
- Additional clustering algorithms (OPTICS, Mean Shift, etc.)
- Enhanced visualization features
- Performance optimizations
- Documentation improvements
- Bug fixes and testing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## � Author

**Jeet Pramanik**
- GitHub: [@jeet-pramanik](https://github.com/jeet-pramanik)
- Email: jeetpramanik516@gmail.com

## 🙏 Acknowledgments

- **scikit-learn** for excellent ML algorithms and documentation
- **Plotly** for interactive visualization capabilities
- **Flask** for lightweight API framework
- The open-source community for inspiration and tools

## 📚 Resources

- [scikit-learn Clustering Documentation](https://scikit-learn.org/stable/modules/clustering.html)
- [Customer Segmentation Best Practices](https://www.kaggle.com/code)
- [RFM Analysis Guide](https://en.wikipedia.org/wiki/RFM_(market_research))

## 📞 Support

If you have questions or need help:
- Open an [Issue](https://github.com/jeet-pramanik/Customer-Segmentation-ML/issues)
- Check the [QUICKSTART.md](QUICKSTART.md) guide
- Review the code examples above

---

**⭐ If you find this project useful, please consider giving it a star!**

**Built with ❤️ for better customer understanding and data-driven marketing**
