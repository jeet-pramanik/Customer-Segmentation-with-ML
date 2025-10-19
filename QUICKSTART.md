# Quick Start Guide - Customer Segmentation Project

## 🚀 Getting Started

This guide will help you set up and run the Customer Segmentation project from scratch.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- 4GB+ RAM recommended
- Git (optional)

## Step-by-Step Setup

### 1. Navigate to Project Directory

```bash
cd "Customer Segmentation with ML"
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Core libraries: numpy, pandas, scipy
- ML libraries: scikit-learn
- Visualization: matplotlib, seaborn, plotly
- Jupyter for notebooks
- Flask for API deployment
- Additional utilities

### 4. Verify Installation

```bash
python -c "import pandas, sklearn, matplotlib; print('All dependencies installed successfully!')"
```

## Running the Project

### Option 1: Using Jupyter Notebooks (Recommended for Learning)

1. **Start Jupyter Notebook:**
   ```bash
   jupyter notebook
   ```

2. **Run notebooks in sequence:**
   - `notebooks/01_data_exploration.ipynb` - Generate and explore data
   - `notebooks/02_preprocessing.ipynb` - Clean and prepare data
   - `notebooks/03_kmeans_clustering.ipynb` - K-Means implementation
   - `notebooks/04_dbscan_clustering.ipynb` - DBSCAN implementation
   - `notebooks/05_cluster_profiling.ipynb` - Analyze segments
   - `notebooks/06_business_insights.ipynb` - Generate strategies

### Option 2: Using Python Scripts

1. **Generate synthetic data:**
   ```bash
   cd src
   python data_loader.py
   ```

2. **Run complete pipeline:**
   ```bash
   python -c "
   from data_loader import CustomerDataLoader
   from preprocessing import DataPreprocessor
   from clustering import KMeansClusterer
   from evaluation import ClusterEvaluator
   
   # Load data
   loader = CustomerDataLoader(data_dir='../data')
   df = loader.generate_synthetic_data(n_customers=2000)
   
   # Preprocess
   preprocessor = DataPreprocessor()
   df_processed = preprocessor.get_preprocessing_pipeline(df)
   
   # Cluster
   kmeans = KMeansClusterer(n_clusters=5)
   labels = kmeans.fit(df_processed.values)
   
   # Evaluate
   evaluator = ClusterEvaluator()
   evaluator.evaluate_clustering(df_processed.values, labels, 'K-Means')
   
   print('Pipeline completed successfully!')
   "
   ```

### Option 3: API Deployment

1. **Train and save models first** (use notebooks or scripts)

2. **Start Flask API:**
   ```bash
   cd src
   python deployment.py
   ```

3. **Test API endpoints:**
   ```bash
   # Health check
   curl http://localhost:5000/health
   
   # Predict segment
   curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"Age": 35, "Income": 75000, "Recency": 15, "Frequency": 10, "Monetary": 3000}'
   
   # Get recommendations
   curl http://localhost:5000/recommendations/0
   ```

## Project Structure

```
Customer Segmentation with ML/
├── data/                          # Data directory
│   ├── raw/                       # Raw data files
│   ├── processed/                 # Cleaned data
│   └── synthetic/                 # Generated data
├── notebooks/                     # Jupyter notebooks (main workflow)
├── src/                           # Source code modules
│   ├── data_loader.py            # Data loading/generation
│   ├── preprocessing.py          # Data preprocessing
│   ├── clustering.py             # Clustering algorithms
│   ├── evaluation.py             # Model evaluation
│   ├── profiling.py              # Cluster profiling
│   ├── visualization.py          # Visualizations
│   └── deployment.py             # Production API
├── models/                        # Saved models
├── reports/                       # Generated reports
│   └── figures/                  # Saved visualizations
├── requirements.txt              # Dependencies
└── README.md                     # Full documentation
```

## Common Tasks

### Generate New Dataset

```python
from src.data_loader import CustomerDataLoader

loader = CustomerDataLoader(data_dir='data')
df = loader.generate_synthetic_data(n_customers=5000, random_state=123)
loader.save_csv(df, 'my_customers.csv', subdirectory='synthetic')
```

### Train New Model

```python
from src.clustering import KMeansClusterer

# Find optimal k
kmeans = KMeansClusterer()
results = kmeans.find_optimal_clusters(X, k_range=range(2, 11))
kmeans.plot_elbow_curve(results)

# Train with optimal k
optimal_k = 5
kmeans = KMeansClusterer(n_clusters=optimal_k)
labels = kmeans.fit(X)
kmeans.save_model('models/my_model.pkl')
```

### Score New Customers

```python
from src.deployment import CustomerSegmentationPipeline

pipeline = CustomerSegmentationPipeline()
pipeline.load_model('models/kmeans_model.pkl')
pipeline.load_preprocessor('models/preprocessor.pkl')

# Single customer
result = pipeline.predict_segment({'Age': 30, 'Income': 60000, ...})
print(f"Segment: {result['segment_name']}")

# Batch scoring
import pandas as pd
new_customers = pd.read_csv('new_customers.csv')
scored = pipeline.batch_score(new_customers)
```

## Troubleshooting

### Issue: Import errors

**Solution:** Make sure you're in the correct directory and virtual environment is activated
```bash
# Check if venv is active (you should see (venv) in prompt)
# If not, activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

### Issue: Faker not found

**Solution:** Install faker explicitly
```bash
pip install faker
```

### Issue: Jupyter kernel not found

**Solution:** Install ipykernel in your venv
```bash
python -m ipykernel install --user --name=customer_segmentation
```

### Issue: Plotly visualizations not showing

**Solution:** Update plotly and dependencies
```bash
pip install --upgrade plotly kaleido nbformat
```

## Next Steps

1. ✅ Complete setup following this guide
2. 📊 Run `01_data_exploration.ipynb` to generate and understand data
3. 🔧 Run `02_preprocessing.ipynb` to prepare data
4. 🎯 Run `03_kmeans_clustering.ipynb` to create segments
5. 📈 Run `05_cluster_profiling.ipynb` to analyze segments
6. 💼 Run `06_business_insights.ipynb` to generate strategies
7. 🚀 Deploy using `deployment.py` for production use

## Resources

- **Full Documentation:** See `README.md`
- **Project Documentation:** See `project.docs.md`
- **Code Examples:** Check notebooks/ directory
- **API Reference:** See docstrings in src/ modules

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the comprehensive `project.docs.md`
3. Examine code examples in notebooks
4. Check docstrings in source files

---

**Happy Segmenting! 🎯📊**
