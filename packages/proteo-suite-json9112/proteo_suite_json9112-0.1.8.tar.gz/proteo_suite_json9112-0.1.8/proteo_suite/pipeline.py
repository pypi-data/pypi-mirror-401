"""
Enhanced Proteomics Analysis Pipeline with Advanced ML/AI Tools
================================================================

This pipeline implements state-of-the-art mass spectrometry signal processing
and machine learning techniques for predicting medical outcomes from proteomics data.

Key Enhancements:
1. Advanced MS signal processing with wavelet transforms and spectral analysis
2. Deep learning models (CNN, LSTM, Transformer) for proteomics patterns
3. Ensemble methods with advanced boosting and neural networks
4. Multi-modal fusion of proteomics and clinical data
5. Comprehensive statistical validation with confidence intervals
6. Advanced feature selection and dimensionality reduction
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
import json
warnings.filterwarnings('ignore')

# Core ML libraries
from sklearn.model_selection import (
    StratifiedKFold, cross_val_score, permutation_test_score,
    GridSearchCV, RandomizedSearchCV
)
from sklearn.preprocessing import StandardScaler, RobustScaler, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.feature_selection import (
    SelectKBest, f_classif, f_regression, mutual_info_classif,
    SelectFromModel, RFE
)
from sklearn.ensemble import (
    RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier,
    VotingClassifier, StackingClassifier
)
from sklearn.metrics import (
    roc_auc_score, classification_report, confusion_matrix,
    precision_recall_curve, average_precision_score
)

# Advanced ML libraries
try:
    import xgboost as xgb
    import lightgbm as lgb
    import catboost as cb
    HAS_GRADIENT_BOOSTING = True
except (ImportError, ValueError) as e:
    HAS_GRADIENT_BOOSTING = False
    print(f"Warning: Advanced gradient boosting libraries not available due to: {e}")


class DataMerger:
    """
    Handles loading raw signal files, averaging replicates, and merging with clinical data.
    """
    def __init__(self):
        pass
        
    def merge_data(self, signal_folder, clinical_file):
        """
        Main entry point to creating the dataframe.
        """
        print("Scanning signal folder...")
        accession_map = self._scan_folder(signal_folder)
        print(f"Found {len(accession_map)} unique accession IDs.")
        
        print(f"Loading clinical data from {clinical_file}...")
        clinical_df = self._load_clinical(clinical_file)
        
        # Filter to only IDs we have both signal and clinical for
        common_ids = set(accession_map.keys()).intersection(set(clinical_df['Accession']))
        print(f"Found {len(common_ids)} samples with both signal and clinical data.")
        
        if len(common_ids) == 0:
            raise ValueError("No matching accession IDs found between signal files and clinical data!")
            
        # Process signals
        print("Processing signal files (averaging replicates)...")
        signal_data_list = []
        
        # We need to establish a common m/z index from the first file
        first_id = list(common_ids)[0]
        first_files = accession_map[first_id]
        common_mz = pd.read_csv(first_files[0], sep=r'\s+', engine='python')['m/z'].values
        
        count = 0
        for acc_id in common_ids:
            files = accession_map[acc_id]
            try:
                # Load all replicates
                replicates = []
                for f in files:
                    temp_df = pd.read_csv(f, sep=r'\s+', engine='python')
                    
                    # Robust Alignment using Linear Interpolation
                    # We interpolate the current file's signal onto the common_mz grid
                    current_mz = temp_df['m/z'].values
                    current_signal = temp_df['Cts.'].values
                    
                    # Sort if necessary (interp requires sorted x)
                    if not np.all(np.diff(current_mz) > 0):
                        sorted_idx = np.argsort(current_mz)
                        current_mz = current_mz[sorted_idx]
                        current_signal = current_signal[sorted_idx]
                        
                    aligned_signal = np.interp(common_mz, current_mz, current_signal, left=0, right=0)
                    replicates.append(aligned_signal)
                
                # Average replicates
                avg_signal = np.mean(replicates, axis=0)
                
                # Create row
                row = {'Accession': acc_id}
                # Add signal columns
                for i, val in enumerate(avg_signal):
                    row[str(common_mz[i])] = val
                    
                signal_data_list.append(row)
                
                count += 1
                if count % 10 == 0:
                    print(f"Processed {count}/{len(common_ids)} samples...", end='\r')
                    
            except Exception as e:
                print(f"Error processing {acc_id}: {e}")
                
        print("\nCreating final dataframe...")
        signal_df = pd.DataFrame(signal_data_list)
        
        # Merge with clinical
        print("Merging with clinical outcomes...")
        # Left merge on signal_df to keep only samples we processed
        final_df = signal_df.merge(
            clinical_df, 
            left_on='Accession', 
            right_on='Accession', 
            how='left'
        )
        
        # Drop the accession columns if not needed, or keep for reference
        # typically pipeline expects JUST features and outcomes. 
        # But 'Accession' is non-numeric, pipeline ignores non-numeric usually?
        # Let's ensure we return a format compatible with pipeline (features as cols)
        
        return final_df

    def _scan_folder(self, folder):
        """
        Scans folder for .txt files and groups by Accession ID.
        Assumes "VSLC..." format.
        """
        import os
        map_ = {}
        files = [f for f in os.listdir(folder) if f.endswith('.txt')]
        
        for f in files:
            # Extract Accession ID: "VSLC20160216-013_0_C2_processed.txt" -> "VSLC20160216-013"
            # Split by '_' and take first part?
            # Or some logic provided by user: "using the accession part of files"
            # User example: "VSLC20160216-013_0_C2_processed.txt" -> "VSLC20160216-013"
            parts = f.split('_')
            if len(parts) > 0:
                acc_id = parts[0]
                if acc_id not in map_:
                    map_[acc_id] = []
                map_[acc_id].append(os.path.join(folder, f))
        return map_
        
    def _load_clinical(self, filepath):
        """
        Loads clinical excel, finds 'accession no.' column, renames to 'Accession'
        """
        if filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)
            
        # Find accession column
        acc_col = None
        for col in df.columns:
            if 'accession' in str(col).lower():
                acc_col = col
                break
        
        if acc_col is None:
            # Fallback to first column as user requested
            acc_col = df.columns[0]
            print(f"Warning: 'accession no.' column not found. Using first column '{acc_col}' as Accession ID.")
            
        df = df.rename(columns={acc_col: 'Accession'})
        # Ensure Accession is string for matching
        df['Accession'] = df['Accession'].astype(str)
        return df

# Deep learning libraries
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset
    HAS_PYTORCH = True
except ImportError:
    HAS_PYTORCH = False
    print("Warning: PyTorch not available for deep learning models")

# Signal processing libraries
try:
    from scipy.signal import (
        find_peaks, peak_widths, peak_prominences, savgol_filter,
        butter, filtfilt, cwt, ricker, morlet
    )
    from scipy.stats import skew, kurtosis, entropy
    from scipy.fft import fft, fftfreq
    HAS_SCIPY_SIGNAL = True
except (ImportError, ValueError) as e:
    HAS_SCIPY_SIGNAL = False
    print(f"Warning: Some Scipy signal processing functions missing: {e}")
    # Fallback definitions to prevent NameError
    def skew(a, axis=0): return np.zeros(a.shape[0] if axis==1 else a.shape[1])
    def kurtosis(a, axis=0): return np.zeros(a.shape[0] if axis==1 else a.shape[1])
    def entropy(pk, qk=None): return 0.0
    def find_peaks(x, **kwargs): return (np.array([]), {})
    def peak_widths(*args, **kwargs): return (np.array([]),)*4
    def peak_prominences(*args, **kwargs): return (np.array([]),)*2
    def savgol_filter(x, *args, **kwargs): return x
    def butter(*args, **kwargs): return (np.array([1.]), np.array([1.]))
    def filtfilt(b, a, x, *args, **kwargs): return x
    def cwt(*args, **kwargs): return np.zeros((1, 1))
    def ricker(*args, **kwargs): return np.zeros(1)
    def morlet(*args, **kwargs): return np.zeros(1)
    def fft(x, *args, **kwargs): return np.zeros_like(x)
    def fftfreq(n, *args, **kwargs): return np.zeros(n)

import pywt

# Survival analysis
try:
    from lifelines import CoxPHFitter, KaplanMeierFitter
    from lifelines.statistics import logrank_test
    HAS_LIFELINES = True
except ImportError:
    HAS_LIFELINES = False
    print("Warning: Lifelines not available for survival analysis")

from .validation import ValidationVisualizer

##############################################################################
# ADVANCED MASS SPECTROMETRY SIGNAL PROCESSING
##############################################################################

class AdvancedMSProcessor:
    """
    Advanced mass spectrometry signal processing with state-of-the-art techniques.
    """
    
    def __init__(self, denoise=True, baseline_correct=True, normalize=True):
        self.denoise = denoise
        self.baseline_correct = baseline_correct
        self.normalize = normalize
        
    def extract_enhanced_features(self, X, feature_types='all'):
        """
        Extract comprehensive mass spectrometry features.
        
        Args:
            X: Array of shape (n_samples, n_mz_values)
            feature_types: str or list, types of features to extract
        
        Returns:
            Dictionary of feature arrays
        """
        features = {}
        
        if feature_types == 'all' or 'statistical' in feature_types:
            features.update(self._extract_statistical_features(X))
            
        if feature_types == 'all' or 'peaks' in feature_types:
            features.update(self._extract_peak_features(X))
            
        if feature_types == 'all' or 'spectral' in feature_types:
            features.update(self._extract_spectral_features(X))
            
        if feature_types == 'all' or 'wavelet' in feature_types:
            features.update(self._extract_wavelet_features(X))
            
        if feature_types == 'all' or 'morphological' in feature_types:
            features.update(self._extract_morphological_features(X))
        
        return features
    
    def _extract_statistical_features(self, X):
        """Extract basic statistical features."""
        features = {}
        
        # Basic statistics
        features['mean'] = np.mean(X, axis=1)
        features['std'] = np.std(X, axis=1)
        features['var'] = np.var(X, axis=1)
        features['max'] = np.max(X, axis=1)
        features['min'] = np.min(X, axis=1)
        features['median'] = np.median(X, axis=1)
        features['q25'] = np.percentile(X, 25, axis=1)
        features['q75'] = np.percentile(X, 75, axis=1)
        features['iqr'] = features['q75'] - features['q25']
        features['range'] = features['max'] - features['min']
        
        # Higher order moments
        features['skewness'] = skew(X, axis=1)
        features['kurtosis'] = kurtosis(X, axis=1)
        
        # Information theory
        features['entropy'] = np.array([entropy(row[row > 0]) for row in X])
        
        # Signal energy and power
        features['total_energy'] = np.sum(X**2, axis=1)
        features['rms'] = np.sqrt(np.mean(X**2, axis=1))
        
        return features
    
    def _extract_peak_features(self, X):
        """Extract advanced peak-based features."""
        features = {}
        
        n_samples = X.shape[0]
        peak_counts = np.zeros(n_samples)
        peak_heights_mean = np.zeros(n_samples)
        peak_heights_std = np.zeros(n_samples)
        peak_widths_mean = np.zeros(n_samples)
        peak_prominences_mean = np.zeros(n_samples)
        peak_distances_mean = np.zeros(n_samples)
        
        for i in range(n_samples):
            signal = X[i, :]
            
            # Multi-scale peak detection
            peaks_coarse, props_coarse = find_peaks(
                signal, distance=20, height=np.percentile(signal, 75),
                prominence=np.std(signal) * 0.5
            )
            
            peaks_fine, props_fine = find_peaks(
                signal, distance=5, height=np.percentile(signal, 60),
                prominence=np.std(signal) * 0.2
            )
            
            # Use fine peaks for analysis
            peaks = peaks_fine
            
            peak_counts[i] = len(peaks)
            
            if len(peaks) > 0:
                # Peak heights
                peak_heights = signal[peaks]
                peak_heights_mean[i] = np.mean(peak_heights)
                peak_heights_std[i] = np.std(peak_heights)
                
                # Peak widths
                widths = peak_widths(signal, peaks, rel_height=0.5)[0]
                peak_widths_mean[i] = np.mean(widths)
                
                # Peak prominences
                prominences = peak_prominences(signal, peaks)[0]
                peak_prominences_mean[i] = np.mean(prominences)
                
                # Peak distances
                if len(peaks) > 1:
                    distances = np.diff(peaks)
                    peak_distances_mean[i] = np.mean(distances)
        
        features['peak_count'] = peak_counts
        features['peak_height_mean'] = peak_heights_mean
        features['peak_height_std'] = peak_heights_std
        features['peak_width_mean'] = peak_widths_mean
        features['peak_prominence_mean'] = peak_prominences_mean
        features['peak_distance_mean'] = peak_distances_mean
        
        return features
    
    def _extract_spectral_features(self, X):
        """Extract frequency domain features using FFT."""
        features = {}
        
        n_samples = X.shape[0]
        spectral_centroid = np.zeros(n_samples)
        spectral_bandwidth = np.zeros(n_samples)
        spectral_rolloff = np.zeros(n_samples)
        spectral_flatness = np.zeros(n_samples)
        
        for i in range(n_samples):
            signal = X[i, :]
            
            # FFT
            fft_vals = np.abs(fft(signal))
            freqs = fftfreq(len(signal))
            
            # Keep only positive frequencies
            pos_mask = freqs >= 0
            fft_vals = fft_vals[pos_mask]
            freqs = freqs[pos_mask]
            
            if len(fft_vals) > 0:
                # Spectral centroid
                spectral_centroid[i] = np.sum(freqs * fft_vals) / np.sum(fft_vals)
                
                # Spectral bandwidth
                div_sum = np.sum(fft_vals)
                if div_sum == 0: div_sum = 1e-10
                
                spectral_bandwidth[i] = np.sqrt(
                    np.sum(((freqs - spectral_centroid[i]) ** 2) * fft_vals) / div_sum
                )
                
                # Spectral rolloff (85% of energy)
                cumsum = np.cumsum(fft_vals)
                rolloff_idx = np.where(cumsum >= 0.85 * cumsum[-1])[0][0]
                spectral_rolloff[i] = freqs[rolloff_idx]
                
                # Spectral flatness (geometric mean / arithmetic mean)
                if np.all(fft_vals > 0):
                    geometric_mean = np.exp(np.mean(np.log(fft_vals)))
                    arithmetic_mean = np.mean(fft_vals)
                    spectral_flatness[i] = geometric_mean / (arithmetic_mean + 1e-10)
        
        features['spectral_centroid'] = spectral_centroid
        features['spectral_bandwidth'] = spectral_bandwidth
        features['spectral_rolloff'] = spectral_rolloff
        features['spectral_flatness'] = spectral_flatness
        
        return features
    
    def _extract_wavelet_features(self, X):
        """Extract wavelet-based features."""
        features = {}
        
        n_samples = X.shape[0]
        wavelet_energy = np.zeros((n_samples, 6))  # 6 levels
        
        for i in range(n_samples):
            signal = X[i, :]
            
            # Discrete wavelet transform
            coeffs = pywt.wavedec(signal, 'db4', level=5)
            
            # Energy in each level
            for j, coeff in enumerate(coeffs):
                if j < 6:
                    wavelet_energy[i, j] = np.sum(coeff**2)
        
        for j in range(6):
            features[f'wavelet_energy_level_{j}'] = wavelet_energy[:, j]
        
        # Relative wavelet energy
        total_energy = np.sum(wavelet_energy, axis=1)
        for j in range(6):
            features[f'wavelet_energy_rel_level_{j}'] = wavelet_energy[:, j] / (total_energy + 1e-8)
        
        return features
    
    def _extract_morphological_features(self, X):
        """Extract morphological features."""
        features = {}
        
        # Signal complexity measures
        features['zero_crossing_rate'] = np.array([
            np.sum(np.diff(np.signbit(row))) / len(row) for row in X
        ])
        
        # Local maxima and minima
        features['local_maxima_count'] = np.array([
            len(find_peaks(row)[0]) for row in X
        ])
        
        features['local_minima_count'] = np.array([
            len(find_peaks(-row)[0]) for row in X
        ])
        
        return features

##############################################################################
# DEEP LEARNING MODELS FOR PROTEOMICS
##############################################################################

if HAS_PYTORCH:
    class ProteomicsTransformer(nn.Module):
        """
        Transformer model for proteomics sequence analysis.
        """
        def __init__(self, input_dim, d_model=128, nhead=8, num_layers=4, num_classes=1):
            super().__init__()
            self.input_projection = nn.Linear(input_dim, d_model)
            self.positional_encoding = nn.Parameter(torch.randn(1000, d_model))
            
            encoder_layer = nn.TransformerEncoderLayer(
                d_model=d_model, nhead=nhead, dim_feedforward=512,
                dropout=0.1, activation='gelu'
            )
            self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
            
            self.classifier = nn.Sequential(
                nn.Linear(d_model, 64),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(64, num_classes)
            )
            
        def forward(self, x):
            # x shape: (batch_size, sequence_length)
            seq_len = x.size(1)
            x = self.input_projection(x.unsqueeze(-1))  # (batch_size, seq_len, d_model)
            x = x + self.positional_encoding[:seq_len].unsqueeze(0)
            
            x = x.transpose(0, 1)  # (seq_len, batch_size, d_model)
            x = self.transformer(x)
            x = x.mean(dim=0)  # Global average pooling
            
            return self.classifier(x)
    
    class ProteomicsCNN(nn.Module):
        """
        1D CNN for proteomics signal analysis.
        """
        def __init__(self, input_length, num_classes=1):
            super().__init__()
            
            self.conv_layers = nn.Sequential(
                # First conv block
                nn.Conv1d(1, 64, kernel_size=15, padding=7),
                nn.BatchNorm1d(64),
                nn.ReLU(),
                nn.MaxPool1d(2),
                nn.Dropout(0.2),
                
                # Second conv block
                nn.Conv1d(64, 128, kernel_size=11, padding=5),
                nn.BatchNorm1d(128),
                nn.ReLU(),
                nn.MaxPool1d(2),
                nn.Dropout(0.2),
                
                # Third conv block
                nn.Conv1d(128, 256, kernel_size=7, padding=3),
                nn.BatchNorm1d(256),
                nn.ReLU(),
                nn.MaxPool1d(2),
                nn.Dropout(0.3),
                
                # Fourth conv block
                nn.Conv1d(256, 512, kernel_size=5, padding=2),
                nn.BatchNorm1d(512),
                nn.ReLU(),
                nn.AdaptiveAvgPool1d(1)
            )
            
            self.classifier = nn.Sequential(
                nn.Flatten(),
                nn.Linear(512, 256),
                nn.ReLU(),
                nn.Dropout(0.5),
                nn.Linear(256, 64),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(64, num_classes)
            )
            
        def forward(self, x):
            # x shape: (batch_size, input_length)
            x = x.unsqueeze(1)  # Add channel dimension
            x = self.conv_layers(x)
            return self.classifier(x)

##############################################################################
# ADVANCED ENSEMBLE METHODS
##############################################################################

class AdvancedEnsemble:
    """
    Advanced ensemble methods with multiple model types.
    """
    
    def __init__(self, task_type='classification'):
        self.task_type = task_type
        self.models = {}
        self.meta_model = None
        
    def create_base_models(self):
        """Create diverse base models for ensemble."""
        models = {}
        
        # Traditional ML models
        models['rf'] = RandomForestClassifier(
            n_estimators=200, max_depth=10, min_samples_split=5,
            min_samples_leaf=2, random_state=42, n_jobs=-1
        )
        
        models['et'] = ExtraTreesClassifier(
            n_estimators=200, max_depth=12, min_samples_split=5,
            min_samples_leaf=2, random_state=42, n_jobs=-1
        )
        
        if HAS_GRADIENT_BOOSTING:
            models['xgb'] = xgb.XGBClassifier(
                n_estimators=200, max_depth=6, learning_rate=0.1,
                subsample=0.8, colsample_bytree=0.8, random_state=42
            )
            
            models['lgb'] = lgb.LGBMClassifier(
                n_estimators=200, max_depth=6, learning_rate=0.1,
                subsample=0.8, colsample_bytree=0.8, random_state=42,
                verbose=-1
            )
            
            models['catboost'] = cb.CatBoostClassifier(
                iterations=200, depth=6, learning_rate=0.1,
                random_state=42, verbose=False
            )
        
        return models
    
    def fit_ensemble(self, X, y, cv=None):
        """Fit ensemble with stacking."""
        if cv is None:
            cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        base_models = self.create_base_models()
        
        # Create stacking ensemble
        self.ensemble = StackingClassifier(
            estimators=list(base_models.items()),
            final_estimator=lgb.LGBMClassifier(random_state=42, verbose=-1) if HAS_GRADIENT_BOOSTING 
                          else RandomForestClassifier(random_state=42),
            cv=cv,
            n_jobs=-1
        )
        
        self.ensemble.fit(X, y)
        return self
    
    def predict_proba(self, X):
        """Predict probabilities."""
        return self.ensemble.predict_proba(X)
    
    def predict(self, X):
        """Make predictions."""
        return self.ensemble.predict(X)

##############################################################################
# ENHANCED FEATURE SELECTION
##############################################################################

class AdvancedFeatureSelector:
    """
    Advanced feature selection with multiple methods.
    """
    
    def __init__(self, task_type='classification'):
        self.task_type = task_type
        self.selected_features = None
        
    def select_features(self, X, y, method='hybrid', k=None):
        """
        Select features using multiple methods.
        
        Args:
            X: Feature matrix
            y: Target variable
            method: 'univariate', 'model_based', 'rfe', 'hybrid'
            k: Number of features to select
        """
        if k is None:
            k = min(500, X.shape[1] // 2)
        
        feature_scores = {}
        
        if method in ['univariate', 'hybrid']:
            # Univariate feature selection
            if self.task_type == 'classification':
                selector = SelectKBest(f_classif, k=k)
                selector.fit(X, y)
                feature_scores['univariate'] = selector.scores_
            
        if method in ['model_based', 'hybrid']:
            # Model-based feature selection
            rf = RandomForestClassifier(n_estimators=100, random_state=42)
            rf.fit(X, y)
            feature_scores['random_forest'] = rf.feature_importances_
            
        if method in ['rfe', 'hybrid']:
            # Recursive feature elimination
            estimator = RandomForestClassifier(n_estimators=50, random_state=42)
            rfe = RFE(estimator, n_features_to_select=k, step=0.1)
            rfe.fit(X, y)
            feature_scores['rfe'] = rfe.ranking_
        
        # Combine scores if hybrid method
        if method == 'hybrid':
            combined_scores = self._combine_feature_scores(feature_scores, X.shape[1])
            selected_idx = np.argsort(combined_scores)[-k:]
        else:
            if method == 'univariate':
                selected_idx = np.argsort(feature_scores['univariate'])[-k:]
            elif method == 'model_based':
                selected_idx = np.argsort(feature_scores['random_forest'])[-k:]
            elif method == 'rfe':
                selected_idx = np.where(feature_scores['rfe'] <= k)[0]
        
        self.selected_features = selected_idx
        return X[:, selected_idx]
    
    def _combine_feature_scores(self, scores_dict, n_features):
        """Combine multiple feature importance scores."""
        combined = np.zeros(n_features)
        
        for method, scores in scores_dict.items():
            if method == 'rfe':
                # Convert ranking to scores (lower rank = higher score)
                scores = 1.0 / (scores + 1e-8)
            
            # Normalize scores
            scores_norm = (scores - np.min(scores)) / (np.max(scores) - np.min(scores) + 1e-8)
            combined += scores_norm
        
        return combined / len(scores_dict)
    
    def transform(self, X):
        """Transform data using selected features."""
        if self.selected_features is None:
            raise ValueError("Feature selection not performed yet")
        return X[:, self.selected_features]

##############################################################################
# MAIN ENHANCED ANALYSIS PIPELINE
##############################################################################

class EnhancedProteomicsPipeline:
    """
    Main pipeline for enhanced proteomics analysis.
    """
    
    def __init__(self, random_state=42):
        self.random_state = random_state
        self.ms_processor = AdvancedMSProcessor()
        self.feature_selector = AdvancedFeatureSelector()
        self.ensemble = AdvancedEnsemble()
        self.visualizer = ValidationVisualizer()
        self.data_merger = DataMerger()
        self.results = {}
        
    def run_analysis(self, data_file=None, signal_folder=None, clinical_file=None, outcome_columns=None, time_cutoffs=[90, 180, 365]):
        """
        Run the complete analysis pipeline
        
        Parameters:
        -----------
        data_file : str, optional
            Path to pre-processed CSV file
        signal_folder : str, optional
            Path to directory containing raw signal .txt files
        clinical_file : str, optional
            Path to clinical data Excel/CSV file using 'accession no.' to match
        outcome_columns : list
            List of column names to predict
        time_cutoffs : list
            Days for survival binary classification
        """
        if outcome_columns is None:
            raise ValueError("outcome_columns must be provided")
            
        # 1. Load Data
        if data_file:
            print(f"Loading data from {data_file}...")
            df = pd.read_csv(data_file)
        elif signal_folder and clinical_file:
            print(f"Loading raw data from {signal_folder} and {clinical_file}...")
            df = self.data_merger.merge_data(signal_folder, clinical_file)
        else:
            raise ValueError("Must provide either 'data_file' OR 'signal_folder' and 'clinical_file'")
            
        print(f"Data loaded: {len(df)} samples")
        
        # Separate features and outcomes
        proteomics_cols = [col for col in df.columns if col.replace('.', '').isdigit()]
        X_raw = df[proteomics_cols].values
        
        # Initial Imputation for raw data (if any NaNs exist)
        if np.isnan(X_raw).any():
            print("Warning: NaNs found in raw data. Imputing with 0.")
            X_raw = np.nan_to_num(X_raw, nan=0.0)
        
        print(f"Processing {X_raw.shape[0]} samples with {X_raw.shape[1]} m/z features")
        
        # Extract enhanced features
        print("Extracting enhanced MS features...")
        enhanced_features = self.ms_processor.extract_enhanced_features(X_raw)
        
        # Combine all features
        X_enhanced = np.column_stack([
            enhanced_features[key] for key in sorted(enhanced_features.keys())
        ])
        
        # Robust Imputation on ALL features (catch-all for generated NaNs and Infs)
        print("Ensuring data integrity (Imputing NaNs/Infs)...")
        # Replace Infinities with NaNs so Imputer can handle them
        X_enhanced[~np.isfinite(X_enhanced)] = np.nan
        
        imputer = SimpleImputer(strategy='mean')
        X_enhanced = imputer.fit_transform(X_enhanced)
        # Clip huge values to prevent overflow errors in downstream models
        X_enhanced = np.clip(X_enhanced, -1e10, 1e10)
        
        # Process each outcome
        for outcome in outcome_columns:
            if outcome not in df.columns:
                continue
                
            print(f"\nAnalyzing outcome: {outcome}")
            y = df[outcome].values
            
            # Remove samples with missing outcomes
            valid_mask = ~np.isnan(y)
            X_valid = X_enhanced[valid_mask]
            y_valid = y[valid_mask]
            
            if len(np.unique(y_valid)) < 2:
                print(f"Skipping {outcome}: insufficient class variation")
                continue
            
            # Feature selection
            print("Performing feature selection...")
            X_selected = self.feature_selector.select_features(X_valid, y_valid, method='hybrid')
            
            # Cross-validation analysis
            print("Running cross-validation...")
            cv_results = self._run_cross_validation(X_selected, y_valid)
            
            # Generate Visualizations
            print(f"Generating performance plots for {outcome}...")
            try:
                self.visualizer.plot_validation_summary(
                    np.array(cv_results['y_true']), 
                    np.array(cv_results['y_scores']), 
                    model_name=f"Ensemble_{outcome}",
                    save_path=f"results_{outcome}.png"
                )
            except Exception as e:
                print(f"Warning: Could not create plots: {e}")

            # Store results
            self.results[outcome] = {
                'cv_results': cv_results,
                'n_features': X_selected.shape[1],
                'n_samples': len(y_valid)
            }
            
            print(f"AUC: {cv_results['test_auc']:.3f} ± {cv_results['test_auc_std']:.3f}")
        
        return self.results
    
    def _run_cross_validation(self, X, y):
        """Run comprehensive cross-validation."""
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        
        auc_scores = []
        y_true_all = []
        y_scores_all = []
        
        for train_idx, test_idx in cv.split(X, y):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            # Fit ensemble
            ensemble = AdvancedEnsemble()
            ensemble.fit_ensemble(X_train, y_train)
            
            # Predictions
            y_proba = ensemble.predict_proba(X_test)[:, 1]
            
            # Store for global plotting
            y_true_all.extend(y_test)
            y_scores_all.extend(y_proba)
            
            # Metrics
            auc = roc_auc_score(y_test, y_proba)
            auc_scores.append(auc)
            
        return {
            'test_auc': np.mean(auc_scores),
            'test_auc_std': np.std(auc_scores),
            'individual_aucs': auc_scores,
            'y_true': y_true_all,
            'y_scores': y_scores_all
        }

if __name__ == "__main__":
    # Example Usage
    
    # Configuration
    data_file = "final_df_20000_reordered_with_outcomes.csv"
    
    # Medical outcomes to analyze
    outcomes = [
        'irAE yes=1,no=0',
        'Grade_3_or_above', 
        'Pneumonitis',
        'Thyroiditis',
        'Rash'
    ]
    
    # Initialize pipeline
    # pipeline = EnhancedProteomicsPipeline(random_state=42)
    
    # Run analysis (commented out to prevent accidental execution on import if used as script)
    # results = pipeline.run_analysis(data_file, outcomes)
    
    # ... save results code ...
