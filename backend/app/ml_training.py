import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional
from collections import Counter
import joblib
import os
from pathlib import Path

class GreenCodingModelTrainer:
    """Trainer for Green Coding Advisor AI models"""
    
    def __init__(self, model_name: str = "microsoft/codebert-base", dataset_path: Optional[str] = None):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Set up paths
        app_dir = Path(__file__).resolve().parent
        self.models_dir = app_dir / "models"
        project_root = Path(__file__).resolve().parents[2]
        default_dataset_path = project_root / "dataset" / "code_dataset.csv"
        self.dataset_path = Path(dataset_path).expanduser() if dataset_path else default_dataset_path
        
        # Cache for feature extraction to avoid recomputation
        self._feature_cache = {}
        
    def _load_dataset_samples(self) -> List[Dict]:
        """Load samples from dataset/code_dataset.csv if it exists - Optimized with vectorized operations."""
        
        path = Path(self.dataset_path)
        if not path.exists():
            print(f"⚠️  Dataset file not found at {path}. Falling back to synthetic data only.")
            return []
        
        df = pd.read_csv(path)
        
        # Vectorized filtering: filter out invalid codes
        valid_mask = df["code"].notna() & df["code"].astype(str).str.strip().astype(bool)
        df_valid = df[valid_mask].copy()
        
        if len(df_valid) == 0:
            return []
        
        # Vectorized language extraction with fallback
        languages = df_valid["language"].fillna("python").astype(str).str.strip()
        
        # Prepare metrics columns in one go
        metric_columns = [
            "green_score", "energy_wh", "co2_g", "cpu_time_ms", "memory_mb",
            "complexity", "duration", "emissions", "emissions_rate", "energy_consumed",
            "country_name", "region", "cloud_provider", "cloud_region", "os",
            "cpu_model", "gpu_model", "ram_total_size", "tracking_mode", "on_cloud", "pue"
        ]
        
        # Build samples using vectorized operations
        samples = [
            {
                "code": code,
                "language": lang,
                "metrics": {col: row.get(col) for col in metric_columns}
            }
            for code, lang, row in zip(
                df_valid["code"].astype(str),
                languages,
                df_valid[metric_columns].to_dict('records')
            )
        ]
        
        print(f"📂 Loaded {len(samples)} rows from {path}")
        return samples
    
    def prepare_training_data(self) -> Tuple[List[str], List[Dict]]:
        """Prepare training data from the curated dataset plus synthetic sources."""
        
        dataset_samples = self._load_dataset_samples()
        
        # Combine all data sources efficiently
        synthetic_data = self._generate_synthetic_code_samples()
        open_source_data = self._collect_open_source_metrics()
        benchmark_data = self._collect_benchmark_data()
        quality_data = self._collect_quality_metrics()
        
        combined = dataset_samples + synthetic_data + open_source_data + benchmark_data + quality_data
        print(f"🧮 Total training samples prepared: {len(combined)}")
        return combined
    
    def _generate_synthetic_code_samples(self) -> List[Dict]:
        """Generate synthetic code samples with known efficiency metrics - Optimized with vectorized generation."""
        
        # Pre-defined inefficient and efficient samples
        base_samples = [
            {
                "code": """
def inefficient_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total
""",
                "metrics": {
                    "green_score": 45,
                    "energy_wh": 0.05,
                    "co2_g": 12.5,
                    "cpu_time_ms": 2.3,
                    "memory_mb": 8.2,
                    "complexity": 3
                },
                "language": "python"
            },
            {
                "code": """
def efficient_sum(numbers):
    return sum(numbers)
""",
                "metrics": {
                    "green_score": 85,
                    "energy_wh": 0.02,
                    "co2_g": 5.1,
                    "cpu_time_ms": 0.8,
                    "memory_mb": 3.1,
                    "complexity": 1
                },
                "language": "python"
            }
        ]
        
        # Vectorized pattern generation
        n_samples = 1000
        pattern_types = np.random.choice(["loop", "recursion", "comprehension", "builtin"], size=n_samples)
        efficiency_levels = np.random.choice(["inefficient", "moderate", "efficient"], size=n_samples)
        
        # Generate samples efficiently
        generated_samples = []
        for pattern_type, efficiency in zip(pattern_types, efficiency_levels):
            code, metrics = self._generate_code_pattern(pattern_type, efficiency)
            generated_samples.append({
                "code": code,
                "metrics": metrics,
                "language": "python"
            })
        
        return base_samples + generated_samples
    
    def _generate_code_pattern(self, pattern_type: str, efficiency: str) -> Tuple[str, Dict]:
        """Generate specific code patterns with efficiency metrics."""
        
        if pattern_type == "loop" and efficiency == "inefficient":
            code = """
def process_list(items):
    result = []
    for i in range(len(items)):
        if items[i] > 0:
            result.append(items[i] * 2)
    return result
"""
            metrics = {
                "green_score": 40,
                "energy_wh": 0.06,
                "co2_g": 15.2,
                "cpu_time_ms": 2.8,
                "memory_mb": 12.5,
                "complexity": 4
            }
        
        elif pattern_type == "comprehension" and efficiency == "efficient":
            code = """
def process_list(items):
    return [item * 2 for item in items if item > 0]
"""
            metrics = {
                "green_score": 88,
                "energy_wh": 0.018,
                "co2_g": 4.5,
                "cpu_time_ms": 0.6,
                "memory_mb": 2.8,
                "complexity": 2
            }
        
        else:
            # Generic fallback snippet
            code = """
def generic_handler(items):
    total = 0
    for item in items:
        total += item
    return total / len(items) if items else 0
"""
            metrics = {
                "green_score": 60,
                "energy_wh": 0.035,
                "co2_g": 9.0,
                "cpu_time_ms": 1.5,
                "memory_mb": 6.0,
                "complexity": 3
            }
        
        return code, metrics
    
    def _collect_open_source_metrics(self) -> List[Dict]:
        """Collect metrics from open source repositories."""
        
        return [
            {
                "code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
                "metrics": {
                    "green_score": 25,
                    "energy_wh": 0.15,
                    "co2_g": 38.0,
                    "cpu_time_ms": 8.5,
                    "memory_mb": 25.0,
                    "complexity": 6
                },
                "language": "python"
            }
        ]
    
    def _collect_benchmark_data(self) -> List[Dict]:
        """Collect performance benchmarking data."""
        return []
    
    def _collect_quality_metrics(self) -> List[Dict]:
        """Collect code quality metrics using static analysis."""
        return []
    
    def _train_model_generic(
        self, 
        training_data: List[Dict], 
        target_key: str, 
        model_name: str,
        model_params: Optional[Dict] = None
    ) -> RandomForestRegressor:
        """Generic model training method to eliminate code duplication."""
        
        # Extract features and targets using list comprehension (vectorized)
        # Cache features to avoid recomputation
        feature_target_pairs = [
            (
                self._extract_code_features_cached(sample["code"], sample["language"]),
                sample["metrics"].get(target_key, 0.0)
            )
            for sample in training_data
            if target_key in sample["metrics"] and sample["metrics"][target_key] is not None
        ]
        
        if not feature_target_pairs:
            raise ValueError(f"No valid training data for {model_name}")
        
        # Unpack and convert to numpy arrays in one step
        features, targets = zip(*feature_target_pairs)
        X = np.array(features, dtype=np.float32)  # Use float32 for memory efficiency
        y = np.array(targets, dtype=np.float32)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model with configurable parameters
        default_params = {
            "n_estimators": 100,
            "max_depth": 10,
            "random_state": 42,
            "n_jobs": -1  # Use all CPU cores
        }
        if model_params:
            default_params.update(model_params)
        
        model = RandomForestRegressor(**default_params)
        model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        print(f"{model_name} - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}, MAE: {mae:.3f}, RMSE: {rmse:.3f}")
        
        # Save model
        os.makedirs(self.models_dir, exist_ok=True)
        joblib.dump(model, self.models_dir / f"{model_name.lower().replace(' ', '_')}_model.pkl")
        
        return model
    
    def train_green_score_model(self, training_data: List[Dict]) -> RandomForestRegressor:
        """Train the Green Score prediction model."""
        return self._train_model_generic(
            training_data, 
            "green_score", 
            "Green Score",
            {"max_depth": 10}
        )
    
    def train_energy_model(self, training_data: List[Dict]) -> RandomForestRegressor:
        """Train energy consumption prediction model."""
        return self._train_model_generic(
            training_data, 
            "energy_wh", 
            "Energy"
        )
    
    def train_co2_model(self, training_data: List[Dict]) -> RandomForestRegressor:
        """Train CO2 emissions prediction model."""
        return self._train_model_generic(
            training_data, 
            "co2_g", 
            "CO2"
        )
    
    def _extract_code_features_cached(self, code: str, language: str) -> List[float]:
        """Extract features with caching to avoid recomputation."""
        cache_key = (code, language)
        if cache_key not in self._feature_cache:
            self._feature_cache[cache_key] = self._extract_code_features(code, language)
        return self._feature_cache[cache_key]
    
    def _extract_code_features(self, code: str, language: str) -> List[float]:
        """Extract numerical features from code - Optimized with single-pass counting."""
        
        # Pre-compile patterns for faster counting
        patterns = {
            'for': 'for ',
            'while': 'while ',
            'if': 'if ',
            'def': 'def ',
            'class': 'class ',
            'range_len': 'range(len(',
            'sum': 'sum(',
            'map': 'map(',
            'lambda': 'lambda ',
            'import': 'import ',
            'from': 'from '
        }
        
        # Single-pass feature extraction
        code_len = len(code)
        newlines = code.count('\n')
        spaces = code.count(' ')
        tabs = code.count('\t')
        
        # Count patterns efficiently
        pattern_counts = {key: code.count(pattern) for key, pattern in patterns.items()}
        
        # List/dict comprehension indicators (count brackets)
        list_brackets = code.count('[')
        
        # Build feature vector
        features = [
            code_len,
            newlines,
            spaces,
            tabs,
            pattern_counts['for'],
            pattern_counts['while'],
            pattern_counts['if'],
            pattern_counts['def'],
            pattern_counts['class'],
            pattern_counts['range_len'],
            list_brackets,
            pattern_counts['sum'],
            pattern_counts['map'],
            pattern_counts['lambda'],
            pattern_counts['import'],
            pattern_counts['from']
        ]
        
        # Add AST features
        ast_features = self._extract_ast_features(code, language)
        features.extend(ast_features)
        
        return features
    
    def _extract_ast_features(self, code: str, language: str) -> List[float]:
        """Extract features using Abstract Syntax Tree analysis - Optimized with Counter."""
        
        try:
            if language == "python":
                import ast
                tree = ast.parse(code)
                
                # Use Counter for efficient counting
                node_types = [type(node).__name__ for node in ast.walk(tree)]
                node_counts = Counter(node_types)
                
                # Extract specific features in order
                feature_names = [
                    'For', 'While', 'If', 'FunctionDef', 'ClassDef',
                    'ListComp', 'DictComp', 'SetComp'
                ]
                
                return [node_counts.get(name, 0) for name in feature_names]
                
        except SyntaxError:
            pass
        
        return [0] * 8
    
    def train_all_models(self):
        """Train all models for the Green Coding Advisor."""
        
        print("Starting Green Coding Advisor Model Training...")
        
        # Prepare training data
        print("Preparing training data...")
        training_data = self.prepare_training_data()
        print(f"Prepared {len(training_data)} training samples")
        
        # Create models directory once
        os.makedirs(self.models_dir, exist_ok=True)
        
        # Train individual models
        print("Training Green Score model...")
        green_score_model = self.train_green_score_model(training_data)
        
        print("Training Energy consumption model...")
        energy_model = self.train_energy_model(training_data)
        
        print("Training CO2 emissions model...")
        co2_model = self.train_co2_model(training_data)
        
        print("All models trained successfully!")
        
        return {
            "green_score": green_score_model,
            "energy": energy_model,
            "co2": co2_model
        }


# Usage example
if __name__ == "__main__":
    trainer = GreenCodingModelTrainer()
    models = trainer.train_all_models()
