from typing import Dict, List, Any
import ast

# Optional heavy deps – gracefully degrade if unavailable
try:
    import torch  # type: ignore
except Exception:  # pragma: no cover
    torch = None  # type: ignore

try:
    import joblib  # type: ignore
except Exception:  # pragma: no cover
    joblib = None  # type: ignore

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover
    np = None  # type: ignore

try:
    from transformers import AutoTokenizer, AutoModel  # type: ignore
except Exception:  # pragma: no cover
    AutoTokenizer = None  # type: ignore
    AutoModel = None  # type: ignore

try:
    import radon.complexity  # type: ignore
    import radon.metrics  # type: ignore
except Exception:  # pragma: no cover
    radon = None  # type: ignore

try:
    from .ml_training import GreenCodingModelTrainer  # type: ignore
except Exception:  # pragma: no cover
    GreenCodingModelTrainer = None  # type: ignore

class GreenCodingPredictor:
    """AI-powered code analysis and prediction system"""
    
    def __init__(self):
        self.models = {}
        self.codebert_tokenizer = None
        self.codebert_model = None
        self._models_loaded = False
    
    def _load_models(self):
        """Load pre-trained models"""
        if self._models_loaded:
            return
            
        try:
            # Load custom trained models (if joblib available)
            if joblib is not None:
                try:
                    self.models["green_score"] = joblib.load("models/green_score_model.pkl")
                    self.models["energy"] = joblib.load("models/energy_model.pkl")
                    self.models["co2"] = joblib.load("models/co2_model.pkl")
                except Exception:
                    pass
            
            # Load CodeBERT for code understanding (if transformers available)
            if AutoTokenizer is not None and AutoModel is not None:
                try:
                    self.codebert_tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
                    self.codebert_model = AutoModel.from_pretrained("microsoft/codebert-base")
                except Exception:
                    # Fall back silently if model cannot be downloaded/loaded
                    self.codebert_tokenizer = None
                    self.codebert_model = None
            
            self._models_loaded = True
            
        except Exception:
            # Any unexpected issue – still allow startup with fallback analysis
            self._models_loaded = True
    
    def _train_models(self):
        """Train models if they don't exist"""
        trainer = GreenCodingModelTrainer()
        self.models = trainer.train_all_models()
    
    def analyze_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        """Comprehensive code analysis using AI models"""
        
        # Load models if not already loaded
        self._load_models()
        
        # Extract features
        features = self._extract_code_features(code, language)
        
        # Predict metrics using trained models
        predictions = {
            "green_score": self._predict_green_score(features),
            "energy_consumption_wh": self._predict_energy(features),
            "co2_emissions_g": self._predict_co2(features),
            "cpu_time_ms": self._predict_cpu_time(features),
            "memory_usage_mb": self._predict_memory(features),
            "complexity_score": self._calculate_complexity(code, language)
        }
        
        # Generate optimization suggestions
        suggestions = self._generate_suggestions(code, language, predictions)
        
        # Calculate real-world impact
        impact = self._calculate_real_world_impact(predictions)
        
        return {
            "metrics": predictions,
            "suggestions": suggestions,
            "real_world_impact": impact,
            "analysis_details": self._get_detailed_analysis(code, language)
        }
    
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
        
        # Add AST-based features
        ast_features = self._extract_ast_features(code, language)
        features.extend(ast_features)
        
        # Add CodeBERT embeddings (simplified)
        bert_features = self._extract_bert_features(code)
        features.extend(bert_features)
        
        return features
    
    def _extract_ast_features(self, code: str, language: str) -> List[float]:
        """Extract features using Abstract Syntax Tree analysis"""
        
        try:
            if language == "python":
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
            return [0] * 8
        
        return [0] * 8
    
    def _extract_bert_features(self, code: str) -> List[float]:
        """Extract features using CodeBERT (simplified)"""
        
        try:
            if self.codebert_tokenizer is None or self.codebert_model is None or torch is None:
                return [0] * 10
            inputs = self.codebert_tokenizer(code, return_tensors="pt", truncation=True, max_length=512)
            with torch.no_grad():  # type: ignore
                outputs = self.codebert_model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1).squeeze()
            return embeddings[:10].tolist()
        except Exception:
            return [0] * 10
    
    def _predict_green_score(self, features: List[float]) -> float:
        """Predict Green Score (0-100)"""
        if "green_score" in self.models:
            score = self.models["green_score"].predict([features])[0]
            return max(0, min(100, score))  # Clamp between 0-100
        return 50.0  # Default score
    
    def _predict_energy(self, features: List[float]) -> float:
        """Predict energy consumption in watt-hours"""
        if "energy" in self.models:
            return max(0, self.models["energy"].predict([features])[0])
        return 0.05  # Default energy consumption
    
    def _predict_co2(self, features: List[float]) -> float:
        """Predict CO2 emissions in grams"""
        if "co2" in self.models:
            return max(0, self.models["co2"].predict([features])[0])
        return 12.5  # Default CO2 emissions
    
    def _predict_cpu_time(self, features: List[float]) -> float:
        """Predict CPU time in milliseconds"""
        # Simple heuristic based on complexity
        complexity = features[4] + features[5] + features[6]  # loops + conditions
        return max(0.1, complexity * 0.5)
    
    def _predict_memory(self, features: List[float]) -> float:
        """Predict memory usage in MB"""
        # Simple heuristic based on code size and imports
        code_size = features[0]
        imports = features[14] + features[15]
        return max(1.0, (code_size / 1000) + (imports * 2))
    
    def _calculate_complexity(self, code: str, language: str) -> float:
        """Calculate code complexity using radon"""
        try:
            if language == "python":
                if 'radon' in globals() and radon is not None:  # type: ignore
                    # Cyclomatic complexity
                    cc = radon.complexity.cc_visit(ast.parse(code))  # type: ignore
                    total_cc = sum([func.complexity for func in cc])
                    # Maintainability index (not used directly in score yet)
                    _ = radon.metrics.mi_visit(ast.parse(code), multi=True)  # type: ignore
                    return min(10, total_cc / 10)  # Normalize to 0-10 scale
        except Exception:
            pass
        
        return 5.0  # Default complexity
    
    def _generate_suggestions(self, code: str, language: str, predictions: Dict) -> List[Dict]:
        """Generate AI-powered optimization suggestions"""
        
        suggestions = []
        
        # Analyze code patterns and suggest improvements
        if "range(len(" in code:
            suggestions.append({
                "finding": "Index-based iteration detected",
                "before_code": "for i in range(len(items)):",
                "after_code": "for item in items:",
                "explanation": "Direct iteration is more efficient than index-based iteration",
                "predicted_improvement": {"green_score": 8, "energy_wh": -0.01},
                "severity": "medium"
            })
        
        if code.count("for ") > 2:
            suggestions.append({
                "finding": "Multiple nested loops detected",
                "before_code": "Multiple for loops",
                "after_code": "Consider using list comprehensions or built-in functions",
                "explanation": "Nested loops can be optimized using more efficient patterns",
                "predicted_improvement": {"green_score": 12, "energy_wh": -0.02},
                "severity": "high"
            })
        
        if predictions["green_score"] < 40:
            suggestions.append({
                "finding": "Low Green Score detected",
                "before_code": "Current implementation",
                "after_code": "Consider algorithmic improvements",
                "explanation": "The code has significant efficiency issues that should be addressed",
                "predicted_improvement": {"green_score": 20, "energy_wh": -0.05},
                "severity": "high"
            })
        
        return suggestions
    
    def _calculate_real_world_impact(self, predictions: Dict) -> Dict[str, Any]:
        """Calculate real-world environmental impact"""
        
        energy_wh = predictions["energy_consumption_wh"]
        co2_g = predictions["co2_emissions_g"]
        
        # Convert to real-world equivalents
        light_bulb_hours = energy_wh / 0.06  # 60W light bulb
        tree_planting_days = co2_g / 22  # Average CO2 absorbed by tree per day
        car_miles = co2_g / 404  # CO2 per mile for average car
        
        return {
            "light_bulb_hours": round(light_bulb_hours, 2),
            "tree_planting_days": round(tree_planting_days, 2),
            "car_miles": round(car_miles, 4),
            "description": f"Running this code 1M times = powering a light bulb for {light_bulb_hours:.1f} hours"
        }
    
    def _get_detailed_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Get detailed analysis breakdown"""
        
        return {
            "lines_of_code": code.count('\n') + 1,
            "cyclomatic_complexity": self._calculate_complexity(code, language),
            "maintainability_index": 70,  # Placeholder
            "code_smells": self._detect_code_smells(code),
            "algorithm_complexity": self._estimate_algorithm_complexity(code),
            "memory_patterns": self._analyze_memory_patterns(code),
            "performance_bottlenecks": self._identify_bottlenecks(code)
        }
    
    def _detect_code_smells(self, code: str) -> List[str]:
        """Detect common code smells"""
        smells = []
        
        if "range(len(" in code:
            smells.append("Index-based iteration")
        if code.count("for ") > 3:
            smells.append("Excessive loops")
        if "import *" in code:
            smells.append("Wildcard import")
        if len(code) > 1000:
            smells.append("Long function")
        
        return smells
    
    def _estimate_algorithm_complexity(self, code: str) -> str:
        """Estimate algorithmic complexity"""
        if "for " in code and "for " in code[code.find("for ")+4:]:
            return "O(n²)"
        elif "for " in code:
            return "O(n)"
        else:
            return "O(1)"
    
    def _analyze_memory_patterns(self, code: str) -> Dict[str, Any]:
        """Analyze memory usage patterns"""
        return {
            "imports_count": code.count("import "),
            "function_definitions": code.count("def "),
            "class_definitions": code.count("class "),
            "estimated_memory_footprint": "Low" if code.count("import ") < 5 else "Medium"
        }
    
    def _identify_bottlenecks(self, code: str) -> List[str]:
        """Identify potential performance bottlenecks"""
        bottlenecks = []
        
        if "range(len(" in code:
            bottlenecks.append("Index-based iteration")
        if code.count("for ") > 2:
            bottlenecks.append("Nested loops")
        if "recursive" in code.lower():
            bottlenecks.append("Recursive calls")
        
        return bottlenecks


# Global predictor instance
green_predictor = GreenCodingPredictor()
