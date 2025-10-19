"""
Customer Segmentation with Machine Learning
A comprehensive system for customer segmentation using unsupervised ML techniques.
"""

__version__ = '1.0.0'
__author__ = 'Your Name'

from . import data_loader
from . import preprocessing
from . import clustering
from . import evaluation
from . import profiling
from . import visualization

__all__ = [
    'data_loader',
    'preprocessing',
    'clustering',
    'evaluation',
    'profiling',
    'visualization'
]
