import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
import joblib
import os

class GreenCodingModelTrainer:
    """Trainer for Green Coding Advisor AI models"""
    
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def prepare_training_data(self) -> Tuple[List[str], List[Dict]]:
        """Prepare training data from various sources"""
        
        # 1. Synthetic Code Dataset
        synthetic_data = self._generate_synthetic_code_samples()
        
        # 2. Open Source Code Analysis
        open_source_data = self._collect_open_source_metrics()
        
        # 3. Performance Benchmarking Data
        benchmark_data = self._collect_benchmark_data()
        
        # 4. Code Quality Metrics
        quality_data = self._collect_quality_metrics()
        
        return synthetic_data + open_source_data + benchmark_data + quality_data
    
    def _generate_synthetic_code_samples(self) -> List[Dict]:
        """Generate synthetic code samples with known efficiency metrics"""
        
        samples = []
        
        # Inefficient patterns with known metrics
        inefficient_samples = [
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
        
        # Generate more samples programmatically
        for i in range(1000):
            # Generate various code patterns
            pattern_type = np.random.choice(["loop", "recursion", "comprehension", "builtin"])
            efficiency_level = np.random.choice(["inefficient", "moderate", "efficient"])
            
            code, metrics = self._generate_code_pattern(pattern_type, efficiency_level)
            samples.append({
                "code": code,
                "metrics": metrics,
                "language": "python"
            })
        
        return samples
    
    def _generate_code_pattern(self, pattern_type: str, efficiency: str) -> Tuple[str, Dict]:
        """Generate specific code patterns with efficiency metrics"""
        
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
        
        # Add more patterns...
        return code, metrics
    
    def _collect_open_source_metrics(self) -> List[Dict]:
        """Collect metrics from open source repositories"""
        
        # This would analyze real GitHub repositories
        # For now, return sample data
        return [
            {
                "code": "def fibonacci(n): return n if n <= 1 else fibonacci(n-1) + fibonacci(n-2)",
                "metrics": {
                    "green_score": 25,  # Very inefficient due to recursion
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
        """Collect performance benchmarking data"""
        
        # This would run actual benchmarks on code samples
        # For now, return sample benchmark data
        return []
    
    def _collect_quality_metrics(self) -> List[Dict]:
        """Collect code quality metrics using static analysis"""
        
        # This would use tools like pylint, radon, etc.
        return []
    
    def train_green_score_model(self, training_data: List[Dict]) -> RandomForestRegressor:
        """Train the Green Score prediction model"""
        
        # Extract features from code
        features = []
        targets = []
        
        for sample in training_data:
            # Extract code features
            code_features = self._extract_code_features(sample["code"], sample["language"])
            features.append(code_features)
            targets.append(sample["metrics"]["green_score"])
        
        # Convert to numpy arrays
        X = np.array(features)
        y = np.array(targets)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        print(f"Green Score Model - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
        
        # Save model
        joblib.dump(model, "models/green_score_model.pkl")
        
        return model
    
    def _extract_code_features(self, code: str, language: str) -> List[float]:
        """Extract numerical features from code"""
        
        features = []
        
        # Basic metrics
        features.append(len(code))  # Code length
        features.append(code.count('\n'))  # Number of lines
        features.append(code.count(' '))  # Number of spaces
        features.append(code.count('\t'))  # Number of tabs
        
        # Complexity indicators
        features.append(code.count('for '))  # For loops
        features.append(code.count('while '))  # While loops
        features.append(code.count('if '))  # If statements
        features.append(code.count('def '))  # Function definitions
        features.append(code.count('class '))  # Class definitions
        
        # Efficiency indicators
        features.append(code.count('range(len('))  # Index-based iteration
        features.append(code.count('['))  # List comprehensions
        features.append(code.count('sum('))  # Built-in functions
        features.append(code.count('map('))  # Functional programming
        features.append(code.count('lambda '))  # Lambda functions
        
        # Memory usage indicators
        features.append(code.count('import '))  # Imports
        features.append(code.count('from '))  # From imports
        
        # Add more sophisticated features using AST analysis
        ast_features = self._extract_ast_features(code, language)
        features.extend(ast_features)
        
        return features
    
    def _extract_ast_features(self, code: str, language: str) -> List[float]:
        """Extract features using Abstract Syntax Tree analysis"""
        
        try:
            if language == "python":
                import ast
                tree = ast.parse(code)
                
                features = []
                
                # Count different node types
                node_counts = {}
                for node in ast.walk(tree):
                    node_type = type(node).__name__
                    node_counts[node_type] = node_counts.get(node_type, 0) + 1
                
                # Extract specific features
                features.append(node_counts.get('For', 0))
                features.append(node_counts.get('While', 0))
                features.append(node_counts.get('If', 0))
                features.append(node_counts.get('FunctionDef', 0))
                features.append(node_counts.get('ClassDef', 0))
                features.append(node_counts.get('ListComp', 0))
                features.append(node_counts.get('DictComp', 0))
                features.append(node_counts.get('SetComp', 0))
                
                return features
                
        except SyntaxError:
            # Return zeros if code is not valid
            return [0] * 8
        
        return [0] * 8
    
    def train_energy_model(self, training_data: List[Dict]) -> RandomForestRegressor:
        """Train energy consumption prediction model"""
        
        features = []
        targets = []
        
        for sample in training_data:
            code_features = self._extract_code_features(sample["code"], sample["language"])
            features.append(code_features)
            targets.append(sample["metrics"]["energy_wh"])
        
        X = np.array(features)
        y = np.array(targets)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        print(f"Energy Model - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
        
        joblib.dump(model, "models/energy_model.pkl")
        return model
    
    def train_co2_model(self, training_data: List[Dict]) -> RandomForestRegressor:
        """Train CO2 emissions prediction model"""
        
        features = []
        targets = []
        
        for sample in training_data:
            code_features = self._extract_code_features(sample["code"], sample["language"])
            features.append(code_features)
            targets.append(sample["metrics"]["co2_g"])
        
        X = np.array(features)
        y = np.array(targets)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
        
        train_score = model.score(X_train, y_train)
        test_score = model.score(X_test, y_test)
        
        print(f"CO2 Model - Train R²: {train_score:.3f}, Test R²: {test_score:.3f}")
        
        joblib.dump(model, "models/co2_model.pkl")
        return model
    
    def train_all_models(self):
        """Train all models for the Green Coding Advisor"""
        
        print("🚀 Starting Green Coding Advisor Model Training...")
        
        # Prepare training data
        print("📊 Preparing training data...")
        training_data = self.prepare_training_data()
        print(f"✅ Prepared {len(training_data)} training samples")
        
        # Create models directory
        os.makedirs("models", exist_ok=True)
        
        # Train individual models
        print("🤖 Training Green Score model...")
        green_score_model = self.train_green_score_model(training_data)
        
        print("⚡ Training Energy consumption model...")
        energy_model = self.train_energy_model(training_data)
        
        print("🌍 Training CO2 emissions model...")
        co2_model = self.train_co2_model(training_data)
        
        print("✅ All models trained successfully!")
        
        return {
            "green_score": green_score_model,
            "energy": energy_model,
            "co2": co2_model
        }


# Usage example
if __name__ == "__main__":
    trainer = GreenCodingModelTrainer()
    models = trainer.train_all_models()
