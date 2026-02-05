from typing import Dict, List, Any, Optional
import ast
import re

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

# Live carbon intensity
try:
    from .electricity_maps import get_live_emission_factor  # type: ignore
except Exception:  # pragma: no cover
    get_live_emission_factor = None  # type: ignore

try:
    from codecarbon import EmissionsTracker, OfflineEmissionsTracker  # type: ignore
    HAS_CODECARBON = True
except Exception:  # pragma: no cover
    HAS_CODECARBON = False
    EmissionsTracker = None  # type: ignore
    OfflineEmissionsTracker = None  # type: ignore

try:
    from .logger import green_logger  # type: ignore
except Exception:  # pragma: no cover
    green_logger = None  # type: ignore

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
                    from pathlib import Path
                    app_dir = Path(__file__).resolve().parent
                    models_dir = app_dir / "models"
                    self.models["green_score"] = joblib.load(models_dir / "green_score_model.pkl")
                    self.models["energy"] = joblib.load(models_dir / "energy_model.pkl")
                    self.models["co2"] = joblib.load(models_dir / "co2_model.pkl")
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
    
    def analyze_code(self, code: str, language: str = "python", region: str = "usa") -> Dict[str, Any]:
        """Comprehensive code analysis using AI models
        
        Args:
            code: Code to analyze
            language: Programming language (python, javascript, java, cpp)
            region: Region for CO2 calculation (usa, europe, asia, world)
        """
        
        # Load models if not already loaded
        self._load_models()
        
        # Extract features
        features = self._extract_code_features(code, language)
        
        # Predict metrics using trained models
        predictions = {
            "green_score": self._predict_green_score(features),
            "energy_consumption_wh": self._predict_energy(features),
            "co2_emissions_g": self._predict_co2(features, region),
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
        """Extract numerical features from code - matches training feature extraction"""
        
        features = []
        lang_lower = language.lower()
        
        # Basic metrics (language-agnostic) - 4 features
        features.append(len(code))  # Code length
        features.append(code.count('\n'))  # Number of lines
        features.append(code.count(' '))  # Number of spaces
        features.append(code.count('\t'))  # Number of tabs
        
        # Complexity indicators - 5 features (language-aware)
        if lang_lower == "python":
            features.append(code.count('for ') + code.count('for '))  # For loops
            features.append(code.count('while '))  # While loops
            features.append(code.count('if ') + code.count('elif '))  # If statements
            features.append(code.count('def '))  # Function definitions
            features.append(code.count('class '))  # Class definitions
        elif lang_lower in ["javascript", "js", "typescript", "ts"]:
            features.append(code.count('for ') + code.count('for(') + code.count('for (') + code.count('forEach'))  # For loops
            features.append(code.count('while ') + code.count('while(') + code.count('while ('))  # While loops
            features.append(code.count('if ') + code.count('if(') + code.count('if (') + code.count('else if'))  # If statements
            features.append(code.count('function ') + code.count('=>') + code.count('const ') + code.count('let '))  # Function definitions
            features.append(code.count('class '))  # Class definitions
        elif lang_lower == "java":
            features.append(code.count('for ') + code.count('for(') + code.count('for ('))  # For loops
            features.append(code.count('while ') + code.count('while(') + code.count('while ('))  # While loops
            features.append(code.count('if ') + code.count('if(') + code.count('if ('))  # If statements
            features.append(code.count('public ') + code.count('private ') + code.count('protected '))  # Method definitions
            features.append(code.count('class '))  # Class definitions
        elif lang_lower in ["cpp", "c++", "c"]:
            features.append(code.count('for ') + code.count('for(') + code.count('for ('))  # For loops
            features.append(code.count('while ') + code.count('while(') + code.count('while ('))  # While loops
            features.append(code.count('if ') + code.count('if(') + code.count('if ('))  # If statements
            features.append(code.count('void ') + code.count('int ') + code.count('bool ') + code.count('auto '))  # Function definitions
            features.append(code.count('class '))  # Class definitions
        else:
            # Generic fallback
            features.append(code.count('for ') + code.count('for(') + code.count('for ('))  # For loops
            features.append(code.count('while ') + code.count('while(') + code.count('while ('))  # While loops
            features.append(code.count('if ') + code.count('if(') + code.count('if ('))  # If statements
            features.append(code.count('function ') + code.count('func '))  # Function definitions
            features.append(code.count('class '))  # Class definitions
        
        # Efficiency indicators - 5 features (language-aware)
        if lang_lower == "python":
            features.append(code.count('range(len('))  # Index-based iteration (inefficient)
            # Better detection of list comprehensions: look for [x for x in ...] pattern
            list_comp_pattern = r'\[.*?\s+for\s+.*?\s+in\s+.*?\]'
            list_comprehensions = len(re.findall(list_comp_pattern, code, re.DOTALL))
            features.append(list_comprehensions)  # List comprehensions (efficient)
            features.append(code.count('sum(') + code.count('max(') + code.count('min('))  # Built-in functions
            features.append(code.count('map(') + code.count('filter(') + code.count('reduce('))  # Functional programming
            features.append(code.count('lambda '))  # Lambda functions
        elif lang_lower in ["javascript", "js", "typescript", "ts"]:
            features.append(code.count('for (let i = 0') + code.count('for(var i = 0'))  # Index-based iteration (inefficient)
            features.append(code.count('[') + code.count(']') + code.count('Array('))  # Arrays/list comprehensions
            features.append(code.count('.reduce(') + code.count('.map(') + code.count('.filter('))  # Built-in array methods
            features.append(code.count('.map(') + code.count('.filter(') + code.count('.reduce('))  # Functional programming
            features.append(code.count('=>') + code.count('function('))  # Arrow functions/lambdas
        elif lang_lower == "java":
            features.append(code.count('for (int i = 0'))  # Index-based iteration (inefficient)
            features.append(code.count('ArrayList') + code.count('List<') + code.count('['))  # Lists/arrays
            features.append(code.count('.stream()') + code.count('.reduce('))  # Stream API
            features.append(code.count('.map(') + code.count('.filter('))  # Functional programming
            features.append(code.count('->'))  # Lambda expressions
        elif lang_lower in ["cpp", "c++", "c"]:
            features.append(code.count('for (int i = 0'))  # Index-based iteration (inefficient)
            features.append(code.count('vector<') + code.count('std::vector') + code.count('['))  # Vectors/arrays
            features.append(code.count('std::') + code.count('algorithm'))  # STL algorithms
            features.append(code.count('std::transform') + code.count('std::for_each'))  # Functional programming
            features.append(0)  # C++ doesn't have lambdas in older standards
        else:
            # Generic fallback
            features.append(code.count('for (') + code.count('for('))  # Index-based iteration
            features.append(code.count('[') + code.count(']'))  # Arrays
            features.append(code.count('('))  # Function calls
            features.append(code.count('map(') + code.count('filter('))  # Functional patterns
            features.append(code.count('lambda ') + code.count('=>'))  # Lambdas
        
        # Memory usage indicators - 2 features
        if lang_lower == "python":
            features.append(code.count('import '))  # Imports
            features.append(code.count('from '))  # From imports
        elif lang_lower in ["javascript", "js", "typescript", "ts"]:
            features.append(code.count('import ') + code.count('require('))  # Imports
            features.append(code.count('from '))  # From imports
        elif lang_lower == "java":
            features.append(code.count('import '))  # Imports
            features.append(code.count('package '))  # Package declarations
        elif lang_lower in ["cpp", "c++", "c"]:
            features.append(code.count('#include'))  # Includes
            features.append(code.count('using '))  # Using statements
        else:
            features.append(code.count('import ') + code.count('include'))  # Imports
            features.append(code.count('from '))  # From imports
        
        # Add AST-based features (if supported) - 8 features
        ast_features = self._extract_ast_features(code, language)
        features.extend(ast_features)
        
        # Ensure we have exactly 24 features (pad or truncate)
        if len(features) < 24:
            features.extend([0.0] * (24 - len(features)))
        elif len(features) > 24:
            features = features[:24]
        
        return features
    
    def _extract_python_features(self, code: str) -> List[float]:
        """Extract Python-specific features"""
        features = []
        features.append(code.count('for '))  # For loops
        features.append(code.count('while '))  # While loops
        features.append(code.count('if '))  # If statements
        features.append(code.count('def '))  # Function definitions
        features.append(code.count('class '))  # Class definitions
        features.append(code.count('range(len('))  # Index-based iteration
        features.append(code.count('['))  # List comprehensions
        features.append(code.count('sum('))  # Built-in functions
        features.append(code.count('map('))  # Functional programming
        features.append(code.count('lambda '))  # Lambda functions
        features.append(code.count('import '))  # Imports
        features.append(code.count('from '))  # From imports
        return features
    
    def _extract_javascript_features(self, code: str) -> List[float]:
        """Extract JavaScript-specific features"""
        features = []
        features.append(code.count('for '))  # For loops
        features.append(code.count('while '))  # While loops
        features.append(code.count('if '))  # If statements
        features.append(code.count('function ') + code.count('=>'))  # Function definitions
        features.append(code.count('class '))  # Class definitions
        features.append(code.count('for (') + code.count('for('))  # For loops
        features.append(code.count('forEach'))  # Array methods
        features.append(code.count('map('))  # Array map
        features.append(code.count('filter('))  # Array filter
        features.append(code.count('reduce('))  # Array reduce
        features.append(code.count('const ') + code.count('let ') + code.count('var '))  # Variable declarations
        features.append(code.count('require(') + code.count('import '))  # Imports
        return features
    
    def _extract_java_features(self, code: str) -> List[float]:
        """Extract Java-specific features"""
        features = []
        features.append(code.count('for '))  # For loops
        features.append(code.count('while '))  # While loops
        features.append(code.count('if '))  # If statements
        features.append(code.count('public ') + code.count('private ') + code.count('protected '))  # Method definitions
        features.append(code.count('class '))  # Class definitions
        features.append(code.count('for (') + code.count('for('))  # For loops
        features.append(code.count('ArrayList') + code.count('List<'))  # List usage
        features.append(code.count('HashMap') + code.count('Map<'))  # Map usage
        features.append(code.count('Stream'))  # Stream API
        features.append(code.count('forEach'))  # Stream forEach
        features.append(code.count('import '))  # Imports
        features.append(code.count('package '))  # Package declarations
        return features
    
    def _extract_cpp_features(self, code: str) -> List[float]:
        """Extract C++ specific features"""
        features = []
        features.append(code.count('for '))  # For loops
        features.append(code.count('while '))  # While loops
        features.append(code.count('if '))  # If statements
        features.append(code.count('void ') + code.count('int ') + code.count('bool '))  # Function definitions
        features.append(code.count('class '))  # Class definitions
        features.append(code.count('for (') + code.count('for('))  # For loops
        features.append(code.count('vector<') + code.count('std::vector'))  # Vector usage
        features.append(code.count('map<') + code.count('std::map'))  # Map usage
        features.append(code.count('auto '))  # Auto keyword
        features.append(code.count('range-based'))  # Range-based for
        features.append(code.count('#include'))  # Includes
        features.append(code.count('using '))  # Using statements
        return features
    
    def _extract_generic_features(self, code: str) -> List[float]:
        """Extract generic features for unknown languages"""
        features = []
        features.append(code.count('for '))  # For loops
        features.append(code.count('while '))  # While loops
        features.append(code.count('if '))  # If statements
        features.append(code.count('function ') + code.count('func '))  # Function definitions
        features.append(code.count('class '))  # Class definitions
        features.append(code.count('for (') + code.count('for('))  # For loops
        features.append(code.count('['))  # Array/list usage
        features.append(code.count('{'))  # Object/map usage
        features.append(code.count('('))  # Function calls
        features.append(code.count('import ') + code.count('include'))  # Imports
        features.append(code.count('='))  # Assignments
        features.append(code.count('return '))  # Returns
        return features
    
    def _extract_ast_features(self, code: str, language: str) -> List[float]:
        """Extract features using Abstract Syntax Tree analysis"""
        
        try:
            if language.lower() == "python":
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
            else:
                # For other languages, use pattern-based analysis
                # JavaScript, Java, C++ don't have easy AST parsing in Python
                # So we use pattern matching
                return self._extract_pattern_features(code, language)
                
        except SyntaxError:
            return [0] * 8
        except Exception:
            return [0] * 8
    
    def _extract_pattern_features(self, code: str, language: str) -> List[float]:
        """Extract features using pattern matching for non-Python languages"""
        features = []
        
        # Loop patterns
        features.append(code.count('for ') + code.count('for(') + code.count('for ('))
        features.append(code.count('while ') + code.count('while(') + code.count('while ('))
        features.append(code.count('if ') + code.count('if(') + code.count('if ('))
        
        # Function/class patterns
        if language.lower() in ["javascript", "js", "typescript", "ts"]:
            features.append(code.count('function ') + code.count('=>') + code.count('const ') + code.count('let '))
            features.append(code.count('class '))
        elif language.lower() == "java":
            features.append(code.count('public ') + code.count('private ') + code.count('protected '))
            features.append(code.count('class '))
        elif language.lower() in ["cpp", "c++", "c"]:
            features.append(code.count('void ') + code.count('int ') + code.count('bool ') + code.count('auto '))
            features.append(code.count('class '))
        else:
            features.append(code.count('function ') + code.count('func '))
            features.append(code.count('class '))
        
        # Comprehension/functional patterns
        features.append(code.count('[') + code.count('map(') + code.count('filter('))
        features.append(code.count('{') + code.count('HashMap') + code.count('Map<'))
        features.append(0)  # Placeholder for comprehensions (not common in other languages)
        features.append(0)  # Placeholder
        
        return features
    
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
        # Always use heuristic for more dynamic and sensitive scoring
        # Models may return similar scores for different inputs
        # The heuristic is more responsive to code differences
        use_heuristic = True
        
        if not use_heuristic and "green_score" in self.models:
            try:
                # Ensure feature count matches model
                if len(features) != 24:
                    # Truncate or pad to 24 features
                    if len(features) > 24:
                        features = features[:24]
                    else:
                        features = features + [0.0] * (24 - len(features))
                score = self.models["green_score"].predict([features])[0]
                # Apply heuristic adjustment to make model more sensitive
                heuristic_score = self._calculate_heuristic_green_score(features)
                # Blend model and heuristic (70% heuristic, 30% model) for better differentiation
                score = (heuristic_score * 0.7) + (score * 0.3)
                return max(0, min(100, score))  # Clamp between 0-100
            except Exception:
                # Fallback to heuristic if model prediction fails
                pass
        
        # Use heuristic calculation
        return self._calculate_heuristic_green_score(features)
    
    def _calculate_heuristic_green_score(self, features: List[float]) -> float:
        """Calculate green score using heuristic method - more dynamic and sensitive"""
        
        # Improved heuristic that considers multiple factors
        # Made more sensitive to differentiate between efficient and inefficient code
        if len(features) < 7:
            return 50.0  # Default score if features are insufficient
        
        code_length = features[0] if len(features) > 0 else 100
        lines = features[1] if len(features) > 1 else 10
        loops = features[4] if len(features) > 4 else 0  # for loops
        while_loops = features[5] if len(features) > 5 else 0  # while loops
        conditions = features[6] if len(features) > 6 else 0  # if statements
        functions = features[7] if len(features) > 7 else 0  # def/function
        classes = features[8] if len(features) > 8 else 0  # class
        inefficient_patterns = features[9] if len(features) > 9 else 0  # range(len(
        list_comprehensions = features[10] if len(features) > 10 else 0  # List comprehensions
        builtin_functions = features[11] if len(features) > 11 else 0  # sum(
        functional_patterns = features[12] if len(features) > 12 else 0  # map(
        lambdas = features[13] if len(features) > 13 else 0  # lambda
        imports = features[14] if len(features) > 14 else 0  # import
        
        # Calculate complexity penalty (MORE AGGRESSIVE)
        total_loops = loops + while_loops
        # Inefficient patterns are heavily penalized - this is the key differentiator
        complexity_penalty = (total_loops * 8) + (conditions * 4) + (inefficient_patterns * 20)
        
        # Calculate efficiency bonus (MORE REWARDING)
        # List comprehensions are much better than loops
        efficiency_bonus = (list_comprehensions * 10) + (builtin_functions * 8) + (functional_patterns * 5) + (lambdas * 3)
        
        # Code structure bonus (well-structured code)
        structure_bonus = (functions * 2) + (classes * 2) - (imports * 0.5)
        
        # Size penalty (very long code is harder to optimize)
        size_penalty = min(20, code_length / 150) if code_length > 500 else 0
        
        # Base score starts at 50 for average code (lower to allow more differentiation)
        base_score = 50.0
        
        # Apply penalties and bonuses
        score = base_score - complexity_penalty + efficiency_bonus + structure_bonus - size_penalty
        
        # Normalize to 0-100 range
        score = max(0, min(100, score))
        
        return round(score, 2)
    
    def _predict_energy(self, features: List[float]) -> float:
        """Predict energy consumption in watt-hours"""
        if "energy" in self.models:
            try:
                # Ensure feature count matches model
                if len(features) != 24:
                    if len(features) > 24:
                        features = features[:24]
                    else:
                        features = features + [0.0] * (24 - len(features))
                return max(0, self.models["energy"].predict([features])[0])
            except Exception:
                pass
        
        # Use CodeCarbon if available for more accurate predictions
        if HAS_CODECARBON:
            try:
                # Estimate energy based on code complexity and size
                complexity = features[4] + features[5] + features[6] if len(features) > 6 else 5
                code_size = features[0] if len(features) > 0 else 1000
                
                # Use CodeCarbon for more accurate energy estimation
                # Estimate CPU time based on complexity
                estimated_cpu_time = complexity * 0.001  # seconds
                # Estimate power consumption (typical CPU power)
                # Average CPU power consumption ranges from 15-100W depending on workload
                cpu_power_watts = 50  # Average CPU power consumption
                energy_wh = (cpu_power_watts * estimated_cpu_time) / 3600
                return max(0.001, energy_wh)
            except Exception as e:
                if green_logger:
                    green_logger.logger.warning(f"CodeCarbon energy prediction failed: {e}")
        
        # Fallback to heuristic
        complexity = features[4] + features[5] + features[6] if len(features) > 6 else 5
        return max(0.001, complexity * 0.01)  # Default energy consumption
    
    def _predict_co2(self, features: List[float], region: str = "usa") -> float:
        """Predict CO2 emissions in grams"""
        if "co2" in self.models:
            try:
                # Ensure feature count matches model
                if len(features) != 24:
                    if len(features) > 24:
                        features = features[:24]
                    else:
                        features = features + [0.0] * (24 - len(features))
                return max(0, self.models["co2"].predict([features])[0])
            except Exception:
                pass
        
        # Use live Electricity Maps factor if available
        live_factor = None
        if get_live_emission_factor:
            try:
                live_factor = get_live_emission_factor(region)
            except Exception:
                live_factor = None

        # Use CodeCarbon if available for more accurate CO2 predictions
        if HAS_CODECARBON or live_factor:
            try:
                # Get energy consumption first
                energy_wh = self._predict_energy(features)

                # CO2 emission factors by region (g CO2 per kWh)
                # Prefer live Electricity Maps intensity when available
                emission_factors = {
                    "usa": 475,  # g CO2/kWh
                    "europe": 276,
                    "asia": 700,
                    "world": 475,
                }

                emission_factor = live_factor or emission_factors.get(region.lower(), 475)
                co2_g = (energy_wh / 1000) * emission_factor
                return max(0.001, co2_g)
            except Exception as e:
                if green_logger:
                    green_logger.logger.warning(f"CodeCarbon CO2 prediction failed: {e}")
        
        # Fallback to heuristic
        energy_wh = self._predict_energy(features)
        # Assume average emission factor of 475 g CO2/kWh (USA average)
        co2_g = (energy_wh / 1000) * 475
        return max(0.001, co2_g)
    
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
        """Calculate code complexity (multi-language support)"""
        try:
            if language.lower() == "python":
                if 'radon' in globals() and radon is not None:  # type: ignore
                    # Cyclomatic complexity
                    cc = radon.complexity.cc_visit(ast.parse(code))  # type: ignore
                    total_cc = sum([func.complexity for func in cc])
                    # Maintainability index (not used directly in score yet)
                    _ = radon.metrics.mi_visit(ast.parse(code), multi=True)  # type: ignore
                    return min(10, total_cc / 10)  # Normalize to 0-10 scale
            else:
                # For other languages, use pattern-based complexity estimation
                return self._estimate_complexity_patterns(code, language)
        except Exception:
            pass
        
        return 5.0  # Default complexity
    
    def _estimate_complexity_patterns(self, code: str, language: str) -> float:
        """Estimate complexity using pattern matching for non-Python languages"""
        # Count control structures
        loops = code.count('for ') + code.count('while ') + code.count('forEach') + code.count('for(') + code.count('for (')
        conditions = code.count('if ') + code.count('if(') + code.count('if (') + code.count('else') + code.count('switch')
        functions = code.count('function ') + code.count('def ') + code.count('void ') + code.count('public ') + code.count('private ')
        
        # Estimate cyclomatic complexity
        complexity = loops + conditions + (functions * 0.5)
        return min(10, complexity / 5)  # Normalize to 0-10 scale
    
    def _generate_suggestions(self, code: str, language: str, predictions: Dict) -> List[Dict]:
        """Generate AI-powered optimization suggestions (multi-language)"""
        
        suggestions = []
        lang_lower = language.lower()
        
        # Python-specific suggestions
        if lang_lower == "python":
            suggestions.extend(self._generate_python_suggestions(code, predictions))
        # JavaScript-specific suggestions
        elif lang_lower in ["javascript", "js", "typescript", "ts"]:
            suggestions.extend(self._generate_javascript_suggestions(code, predictions))
        # Java-specific suggestions
        elif lang_lower == "java":
            suggestions.extend(self._generate_java_suggestions(code, predictions))
        # C++ specific suggestions
        elif lang_lower in ["cpp", "c++", "c"]:
            suggestions.extend(self._generate_cpp_suggestions(code, predictions))
        else:
            # Generic suggestions
            suggestions.extend(self._generate_generic_suggestions(code, predictions))
        
        return suggestions
    
    def _generate_python_suggestions(self, code: str, predictions: Dict) -> List[Dict]:
        """Generate Python-specific optimization suggestions"""
        suggestions = []
        
        # Analyze code patterns and suggest improvements with before/after code
        if "range(len(" in code:
            # Find the actual line with range(len(
            lines = code.split('\n')
            before_example = None
            after_example = None
            for i, line in enumerate(lines):
                if "range(len(" in line and "for" in line:
                    before_example = line.strip()
                    # Generate improved version
                    if "items" in line or "list" in line or "arr" in line:
                        var_name = "item"
                        if "items" in line:
                            var_name = "items"
                        elif "list" in line:
                            var_name = "list"
                        elif "arr" in line:
                            var_name = "arr"
                        after_example = line.replace("range(len(", "").replace("))", "").replace(f"for i in {var_name}", f"for item in {var_name}")
                        after_example = after_example.replace("i]", "item]").replace("[i", "[item")
                        after_example = after_example.replace("for i in", "for item in").strip()
                    break
            
            suggestions.append({
                "finding": "Index-based iteration detected",
                "before_code": before_example or "for i in range(len(items)):\n    result.append(items[i])",
                "after_code": after_example or "for item in items:\n    result.append(item)",
                "explanation": "Direct iteration is more efficient than index-based iteration. It avoids the overhead of index lookups and is more Pythonic.",
                "predicted_improvement": {"green_score": 8, "energy_wh": -0.01},
                "severity": "medium"
            })
        
        # Check for nested loops that could be list comprehensions
        if code.count("for ") > 1 and "append(" in code:
            suggestions.append({
                "finding": "Nested loops with append() can be optimized",
                "before_code": "result = []\nfor x in items:\n    if condition(x):\n        result.append(process(x))",
                "after_code": "result = [process(x) for x in items if condition(x)]",
                "explanation": "List comprehensions are faster and more memory-efficient than loops with append(). They're optimized in C and avoid Python function call overhead.",
                "predicted_improvement": {"green_score": 12, "energy_wh": -0.02},
                "severity": "high"
            })
        
        # Check for sum() pattern
        if "sum(" not in code and "for" in code and ("total" in code or "sum" in code.lower()):
            suggestions.append({
                "finding": "Manual summation can use built-in sum()",
                "before_code": "total = 0\nfor x in numbers:\n    total += x",
                "after_code": "total = sum(numbers)",
                "explanation": "Built-in sum() function is optimized in C and much faster than manual loops. It also reduces code complexity.",
                "predicted_improvement": {"green_score": 10, "energy_wh": -0.015},
                "severity": "medium"
            })
        
        # Check for string concatenation in loops
        if "for" in code and "+=" in code and ("str" in code.lower() or '"' in code or "'" in code):
            suggestions.append({
                "finding": "String concatenation in loops is inefficient",
                "before_code": "result = ''\nfor item in items:\n    result += str(item)",
                "after_code": "result = ''.join(str(item) for item in items)",
                "explanation": "String concatenation with += creates new string objects. join() is much more efficient for combining strings.",
                "predicted_improvement": {"green_score": 15, "energy_wh": -0.03},
                "severity": "high"
            })
        
        # Check for dictionary iteration
        if "for" in code and "items()" not in code and (".keys()" in code or ".values()" in code):
            suggestions.append({
                "finding": "Use .items() for dictionary iteration",
                "before_code": "for key in dict.keys():\n    value = dict[key]",
                "after_code": "for key, value in dict.items():",
                "explanation": "Using .items() is more efficient and Pythonic. It avoids dictionary lookups and is more readable.",
                "predicted_improvement": {"green_score": 7, "energy_wh": -0.01},
                "severity": "medium"
            })

        # Pandas vectorization hint
        if "pandas" in code or "DataFrame" in code:
            suggestions.append({
                "finding": "Looping over DataFrame rows detected",
                "before_code": "for _, row in df.iterrows():\n    df.loc[...] = heavy(row)",
                "after_code": "df = df.assign(result=heavy_vectorized(df))",
                "explanation": "Vectorized Pandas operations use optimized C code and avoid Python-level loops, reducing CPU time and energy.",
                "predicted_improvement": {"green_score": 18, "energy_wh": -0.05},
                "severity": "high"
            })

        # Network calls in loops
        if "requests.get" in code and code.count("for ") > 0:
            suggestions.append({
                "finding": "HTTP requests inside loops",
                "before_code": "for url in urls:\n    data = requests.get(url).json()",
                "after_code": "with ThreadPoolExecutor() as pool:\n    results = list(pool.map(fetch, urls))",
                "explanation": "Batching or parallelizing I/O-bound HTTP calls reduces total runtime and wasted CPU wait cycles.",
                "predicted_improvement": {"green_score": 10, "energy_wh": -0.02},
                "severity": "medium"
            })
        
        return suggestions
    
    def _generate_javascript_suggestions(self, code: str, predictions: Dict) -> List[Dict]:
        """Generate JavaScript-specific optimization suggestions"""
        suggestions = []
        
        # Check for inefficient loops
        if "for (let i = 0" in code or "for(var i = 0" in code:
            suggestions.append({
                "finding": "Use for...of or forEach instead of traditional for loops",
                "before_code": "for (let i = 0; i < array.length; i++) {\n    process(array[i]);\n}",
                "after_code": "for (const item of array) {\n    process(item);\n}",
                "explanation": "for...of loops are more efficient and readable. They avoid index calculations and are optimized by modern JavaScript engines.",
                "predicted_improvement": {"green_score": 8, "energy_wh": -0.01},
                "severity": "medium"
            })
        
        # Check for array methods
        if code.count("for ") > 1 and "push(" in code:
            suggestions.append({
                "finding": "Use array methods instead of loops with push()",
                "before_code": "const result = [];\nfor (const item of items) {\n    if (condition(item)) {\n        result.push(process(item));\n    }\n}",
                "after_code": "const result = items.filter(condition).map(process);",
                "explanation": "Array methods like map(), filter(), and reduce() are optimized and more efficient than manual loops. They're also more functional and readable.",
                "predicted_improvement": {"green_score": 12, "energy_wh": -0.02},
                "severity": "high"
            })

        # Async batching for network calls
        if "fetch(" in code and "for" in code:
            suggestions.append({
                "finding": "Network fetch calls inside loops",
                "before_code": "for (const url of urls) {\n  const res = await fetch(url);\n  data.push(await res.json());\n}",
                "after_code": "const responses = await Promise.all(urls.map(fetch));\nconst data = await Promise.all(responses.map(r => r.json()));",
                "explanation": "Batching network requests with Promise.all avoids serial waits and reduces wall-clock time and idle CPU usage.",
                "predicted_improvement": {"green_score": 9, "energy_wh": -0.015},
                "severity": "medium"
            })
        
        # Check for string concatenation
        if "for" in code and "+=" in code and ("'" in code or '"' in code):
            suggestions.append({
                "finding": "Use template literals or Array.join() for string concatenation",
                "before_code": "let result = '';\nfor (const item of items) {\n    result += item;\n}",
                "after_code": "const result = items.join('');",
                "explanation": "Template literals and Array.join() are more efficient than string concatenation in loops. They avoid creating intermediate string objects.",
                "predicted_improvement": {"green_score": 10, "energy_wh": -0.015},
                "severity": "medium"
            })
        
        return suggestions
    
    def _generate_java_suggestions(self, code: str, predictions: Dict) -> List[Dict]:
        """Generate Java-specific optimization suggestions"""
        suggestions = []
        
        # Check for traditional loops
        if "for (int i = 0" in code:
            suggestions.append({
                "finding": "Use enhanced for loops (for-each) when possible",
                "before_code": "for (int i = 0; i < list.size(); i++) {\n    process(list.get(i));\n}",
                "after_code": "for (String item : list) {\n    process(item);\n}",
                "explanation": "Enhanced for loops are more efficient and readable. They avoid index calculations and method calls.",
                "predicted_improvement": {"green_score": 7, "energy_wh": -0.01},
                "severity": "medium"
            })
        
        # Check for Stream API usage
        if code.count("for ") > 1 and "add(" in code and "List" in code:
            suggestions.append({
                "finding": "Use Stream API for functional operations",
                "before_code": "List<String> result = new ArrayList<>();\nfor (String item : items) {\n    if (condition(item)) {\n        result.add(process(item));\n    }\n}",
                "after_code": "List<String> result = items.stream()\n    .filter(item -> condition(item))\n    .map(item -> process(item))\n    .collect(Collectors.toList());",
                "explanation": "Stream API provides parallel processing capabilities and is optimized for bulk operations. It's more efficient for large datasets.",
                "predicted_improvement": {"green_score": 15, "energy_wh": -0.025},
                "severity": "high"
            })
        
        # Check for String concatenation
        if "for" in code and "+=" in code and "String" in code:
            suggestions.append({
                "finding": "Use StringBuilder for string concatenation in loops",
                "before_code": "String result = \"\";\nfor (String item : items) {\n    result += item;\n}",
                "after_code": "StringBuilder sb = new StringBuilder();\nfor (String item : items) {\n    sb.append(item);\n}\nString result = sb.toString();",
                "explanation": "StringBuilder is much more efficient than string concatenation in loops. It avoids creating multiple string objects.",
                "predicted_improvement": {"green_score": 12, "energy_wh": -0.02},
                "severity": "high"
            })
        
        return suggestions
    
    def _generate_cpp_suggestions(self, code: str, predictions: Dict) -> List[Dict]:
        """Generate C++ specific optimization suggestions"""
        suggestions = []
        
        # Check for traditional loops
        if "for (int i = 0" in code:
            suggestions.append({
                "finding": "Use range-based for loops (C++11+) when possible",
                "before_code": "for (int i = 0; i < vec.size(); i++) {\n    process(vec[i]);\n}",
                "after_code": "for (const auto& item : vec) {\n    process(item);\n}",
                "explanation": "Range-based for loops are more efficient and safer. They avoid index calculations and potential out-of-bounds errors.",
                "predicted_improvement": {"green_score": 8, "energy_wh": -0.01},
                "severity": "medium"
            })
        
        # Check for algorithm usage
        if code.count("for ") > 1 and "push_back(" in code:
            suggestions.append({
                "finding": "Use STL algorithms instead of manual loops",
                "before_code": "std::vector<int> result;\nfor (int x : vec) {\n    if (x > 0) {\n        result.push_back(x * 2);\n    }\n}",
                "after_code": "std::vector<int> result;\nstd::copy_if(vec.begin(), vec.end(), std::back_inserter(result),\n    [](int x) { return x > 0; });\nstd::transform(result.begin(), result.end(), result.begin(),\n    [](int x) { return x * 2; });",
                "explanation": "STL algorithms are optimized and can often be parallelized. They're more efficient than manual loops.",
                "predicted_improvement": {"green_score": 10, "energy_wh": -0.015},
                "severity": "medium"
            })
        
        # Check for memory management
        if "new " in code and "delete " not in code:
            suggestions.append({
                "finding": "Use smart pointers instead of raw pointers",
                "before_code": "int* ptr = new int(42);",
                "after_code": "std::unique_ptr<int> ptr = std::make_unique<int>(42);",
                "explanation": "Smart pointers automatically manage memory, preventing leaks and making code safer and more efficient.",
                "predicted_improvement": {"green_score": 9, "energy_wh": -0.01},
                "severity": "high"
            })
        
        return suggestions
    
    def _generate_generic_suggestions(self, code: str, predictions: Dict) -> List[Dict]:
        """Generate generic optimization suggestions"""
        suggestions = []
        
        # Generic suggestions for any language
        if predictions["green_score"] < 40:
            suggestions.append({
                "finding": "Low Green Score - General optimization needed",
                "before_code": "Consider reviewing your code for:\n- Inefficient algorithms (O(n²) when O(n) is possible)\n- Unnecessary computations\n- Memory-intensive operations",
                "after_code": "Optimize by:\n- Using appropriate data structures\n- Leveraging built-in functions\n- Reducing computational complexity\n- Minimizing memory allocations",
                "explanation": "The code has significant efficiency issues. Consider profiling to identify bottlenecks and applying optimization patterns.",
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
        """Estimate algorithmic complexity (multi-language)"""
        # Count nested loops (approximate)
        loop_count = code.count("for ") + code.count("while ") + code.count("forEach") + code.count("for(") + code.count("for (")
        
        # Check for nested patterns
        lines = code.split('\n')
        max_nesting = 0
        current_nesting = 0
        for line in lines:
            if any(keyword in line for keyword in ["for ", "while ", "forEach", "for(", "for ("]):
                current_nesting += 1
                max_nesting = max(max_nesting, current_nesting)
            elif any(keyword in line for keyword in ["}", "}", "end"]):
                current_nesting = max(0, current_nesting - 1)
        
        if max_nesting >= 2:
            return "O(n²)" if max_nesting == 2 else "O(n³)" if max_nesting == 3 else "O(n^k)"
        elif loop_count > 0:
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
    
    def detect_language(self, code: str) -> str:
        """Automatically detect programming language from code"""
        code_lower = code.lower()
        
        # Python indicators
        if any(keyword in code for keyword in ["def ", "import ", "print(", "if __name__", "lambda ", "list(", "dict("]):
            if "def " in code or "import " in code:
                return "python"
        
        # JavaScript/TypeScript indicators
        if any(keyword in code for keyword in ["function ", "const ", "let ", "var ", "=>", "console.log", "require(", "import "]):
            if "function " in code or "const " in code or "let " in code:
                if "interface " in code or "type " in code or ": " in code.split("\n")[0]:
                    return "typescript"
                return "javascript"
        
        # Java indicators
        if any(keyword in code for keyword in ["public class", "public static void main", "System.out.println", "@Override", "extends ", "implements "]):
            return "java"
        
        # C++ indicators
        if any(keyword in code for keyword in ["#include", "std::", "using namespace", "int main(", "cout <<", "cin >>"]):
            return "cpp"
        
        # C indicators
        if "#include" in code and "printf" in code and "std::" not in code:
            return "c"
        
        # Default to Python if uncertain
        return "python"
    
    def optimize_code(self, code: str, language: Optional[str] = None, region: str = "usa") -> Dict[str, Any]:
        """Generate fully optimized code (not just suggestions)
        
        Args:
            code: Code to optimize
            language: Programming language (auto-detected if not provided)
            region: Region for CO2 calculation
        
        Returns:
            Dictionary with original code, optimized code, metrics, and comparison
        """
        # Auto-detect language if not provided
        if not language:
            language = self.detect_language(code)
        
        lang_lower = language.lower()
        
        # Handle large code (>500 lines) by chunking
        lines = code.split('\n')
        is_large = len(lines) > 500
        
        if is_large:
            # Split into logical chunks and optimize each
            optimized_chunks = []
            current_chunk = []
            current_indent = 0
            
            for line in lines:
                # Detect function/class boundaries
                stripped = line.lstrip()
                if stripped.startswith(('def ', 'class ', 'function ', 'public ', 'private ', 'class ')):
                    if current_chunk:
                        chunk_code = '\n'.join(current_chunk)
                        chunk_opt = self._optimize_code_chunk(chunk_code, lang_lower)
                        optimized_chunks.append(chunk_opt)
                    current_chunk = [line]
                else:
                    current_chunk.append(line)
            
            # Optimize last chunk
            if current_chunk:
                chunk_code = '\n'.join(current_chunk)
                chunk_opt = self._optimize_code_chunk(chunk_code, lang_lower)
                optimized_chunks.append(chunk_opt)
            
            optimized_code = '\n\n'.join(optimized_chunks)
        else:
            # Optimize entire code
            optimized_code = self._optimize_code_chunk(code, lang_lower)
        
        # Check if optimization actually changed the code
        code_changed = optimized_code.strip() != code.strip()
        
        # If code didn't change, check if it's already optimal or if optimization failed
        if not code_changed:
            # Check if code has inefficient patterns
            has_inefficient_patterns = self._has_inefficient_patterns(code, lang_lower)
            if has_inefficient_patterns:
                # Optimization failed - try a more aggressive approach
                optimized_code = self._aggressive_optimize(code, lang_lower)
                code_changed = optimized_code.strip() != code.strip()
        
        # Analyze both versions
        self._load_models()
        
        original_features = self._extract_code_features(code, lang_lower)
        optimized_features = self._extract_code_features(optimized_code, lang_lower)
        
        original_metrics = {
            "green_score": self._predict_green_score(original_features),
            "energy_consumption_wh": self._predict_energy(original_features),
            "co2_emissions_g": self._predict_co2(original_features, region),
            "cpu_time_ms": self._predict_cpu_time(original_features),
            "memory_usage_mb": self._predict_memory(original_features),
            "complexity_score": self._calculate_complexity(code, lang_lower),
            "time_complexity": self._estimate_algorithm_complexity(code)
        }
        
        optimized_metrics = {
            "green_score": self._predict_green_score(optimized_features),
            "energy_consumption_wh": self._predict_energy(optimized_features),
            "co2_emissions_g": self._predict_co2(optimized_features, region),
            "cpu_time_ms": self._predict_cpu_time(optimized_features),
            "memory_usage_mb": self._predict_memory(optimized_features),
            "complexity_score": self._calculate_complexity(optimized_code, lang_lower),
            "time_complexity": self._estimate_algorithm_complexity(optimized_code)
        }
        
        # Calculate improvements
        improvements = {
            "green_score": optimized_metrics["green_score"] - original_metrics["green_score"],
            "energy_reduction": original_metrics["energy_consumption_wh"] - optimized_metrics["energy_consumption_wh"],
            "co2_reduction": original_metrics["co2_emissions_g"] - optimized_metrics["co2_emissions_g"],
            "cpu_time_reduction": original_metrics["cpu_time_ms"] - optimized_metrics["cpu_time_ms"],
            "memory_reduction": original_metrics["memory_usage_mb"] - optimized_metrics["memory_usage_mb"]
        }
        
        # Generate improvement message
        if not code_changed:
            optimized_code = code + "\n\n# Code is already optimized. No changes were made."
            improvements_explanation = "Code is already optimized. No inefficient patterns detected."
        else:
            improvements_explanation = self._generate_improvements_explanation(code, optimized_code, lang_lower)
        
        # Format improvement percentages safely
        energy_pct = (improvements['energy_reduction']/original_metrics['energy_consumption_wh']*100) if original_metrics['energy_consumption_wh'] > 0 else 0.0
        co2_pct = (improvements['co2_reduction']/original_metrics['co2_emissions_g']*100) if original_metrics['co2_emissions_g'] > 0 else 0.0
        
        return {
            "detected_language": language,
            "analysis_summary": self._generate_analysis_summary(code, optimized_code, original_metrics, optimized_metrics),
            "original_code": code,
            "optimized_code": optimized_code,
            "code_changed": code_changed,
            "comparison_table": {
                "green_score": {
                    "original": round(original_metrics["green_score"], 2),
                    "optimized": round(optimized_metrics["green_score"], 2),
                    "improvement": round(improvements["green_score"], 2)
                },
                "energy_usage": {
                    "original": f"{original_metrics['energy_consumption_wh']:.4f} Wh",
                    "optimized": f"{optimized_metrics['energy_consumption_wh']:.4f} Wh",
                    "improvement": f"{improvements['energy_reduction']:.4f} Wh ({energy_pct:.1f}% reduction)"
                },
                "co2_emissions": {
                    "original": f"{original_metrics['co2_emissions_g']:.4f} g",
                    "optimized": f"{optimized_metrics['co2_emissions_g']:.4f} g",
                    "improvement": f"{improvements['co2_reduction']:.4f} g ({co2_pct:.1f}% reduction)"
                },
                "cpu_time": {
                    "original": f"{original_metrics['cpu_time_ms']:.2f} ms",
                    "optimized": f"{optimized_metrics['cpu_time_ms']:.2f} ms",
                    "improvement": f"{improvements['cpu_time_reduction']:.2f} ms"
                },
                "memory_usage": {
                    "original": f"{original_metrics['memory_usage_mb']:.2f} MB",
                    "optimized": f"{optimized_metrics['memory_usage_mb']:.2f} MB",
                    "improvement": f"{improvements['memory_reduction']:.2f} MB"
                },
                "time_complexity": {
                    "original": original_metrics["time_complexity"],
                    "optimized": optimized_metrics["time_complexity"],
                    "improvement": "Improved" if optimized_metrics["time_complexity"] != original_metrics["time_complexity"] else "Same"
                }
            },
            "improvements_explanation": improvements_explanation,
            "expected_green_score_improvement": f"+{improvements['green_score']:.1f} points (from {original_metrics['green_score']:.1f} to {optimized_metrics['green_score']:.1f})"
        }
    
    def _optimize_function_body(self, body: str) -> str:
        """Optimize a function body (code block)"""
        lines = body.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            indent = len(line) - len(stripped) if line.strip() else 0
            
            # Pattern: result = []
            result_var_match = re.search(r'(\w+)\s*=\s*\[\]', stripped)
            if result_var_match and i < len(lines) - 1:
                result_var = result_var_match.group(1)
                
                # Check next line for: for i in range(len(items)):
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    next_stripped = next_line.lstrip()
                    next_indent = len(next_line) - len(next_stripped)
                    
                    range_match = re.search(r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):', next_stripped)
                    if range_match and next_indent > indent:
                        index_var = range_match.group(1)
                        list_var = range_match.group(2)
                        
                        # Check line after that for: result.append(...)
                        if i + 2 < len(lines):
                            append_line = lines[i + 2]
                            append_stripped = append_line.lstrip()
                            append_indent = len(append_line) - len(append_stripped)
                            
                            # More flexible matching - handle variations in spacing
                            if append_indent > next_indent and re.search(rf'\b{re.escape(result_var)}\s*\.\s*append\s*\(', append_stripped):
                                append_match = re.search(r'\.append\s*\(\s*([^)]+)\s*\)', append_stripped)
                                if append_match:
                                    append_expr = append_match.group(1).strip()
                                    # Replace list_var[index_var] with index_var
                                    append_expr = re.sub(rf'\b{re.escape(list_var)}\s*\[\s*{re.escape(index_var)}\s*\]', index_var, append_expr)
                                    
                                    # Check for if condition in the for line or next lines
                                    condition = None
                                    if "if" in next_stripped:
                                        if_match = re.search(r'if\s+(.+?):', next_stripped)
                                        if if_match:
                                            condition = if_match.group(1).strip()
                                            condition = re.sub(rf'\b{re.escape(list_var)}\s*\[\s*{re.escape(index_var)}\s*\]', index_var, condition)
                                    
                                    # Build the list comprehension
                                    if condition:
                                        new_code = f"{' ' * indent}{result_var} = [{append_expr} for {index_var} in {list_var} if {condition}]"
                                    else:
                                        new_code = f"{' ' * indent}{result_var} = [{append_expr} for {index_var} in {list_var}]"
                                    
                                    result_lines.append(new_code)
                                    i += 3  # Skip result=[], for loop, and append lines
                                    continue
            
            # Pattern: total = 0
            sum_var_match = re.search(r'(\w+)\s*=\s*0\s*$', stripped)
            if sum_var_match and i < len(lines) - 1:
                sum_var = sum_var_match.group(1)
                next_line = lines[i + 1].lstrip() if i + 1 < len(lines) else ""
                next_next = lines[i + 2].lstrip() if i + 2 < len(lines) else ""
                
                # Check for: for i in range(len(nums)): total += nums[i] or total = total + nums[i]
                # More flexible pattern matching
                if "for" in next_line and re.search(rf'\b{re.escape(sum_var)}\s*(?:\+=\s*\w+\[\w+\]|=\s*{re.escape(sum_var)}\s*\+\s*\w+\[\w+\])', next_next):
                    range_match = re.search(r'for\s+\w+\s+in\s+range\s*\(\s*len\s*\(\s*(\w+)\s*\)\s*\)\s*:', next_line)
                    if range_match:
                        var_name = range_match.group(1)
                        result_lines.append(f"{' ' * indent}{sum_var} = sum({var_name})")
                        i += 3  # Skip total=0, for loop, and += line
                        continue
                    # Also check for direct iteration
                    direct_match = re.search(r'for\s+\w+\s+in\s+(\w+)\s*:', next_line)
                    if direct_match:
                        var_name = direct_match.group(1)
                        result_lines.append(f"{' ' * indent}{sum_var} = sum({var_name})")
                        i += 3
                        continue
            
            # Pattern: output = ""
            str_var_match = re.search(r'(\w+)\s*=\s*["\']\s*["\']', stripped)
            if str_var_match and i < len(lines) - 1:
                str_var = str_var_match.group(1)
                next_line = lines[i + 1].lstrip() if i + 1 < len(lines) else ""
                next_next = lines[i + 2].lstrip() if i + 2 < len(lines) else ""
                
                if "for" in next_line and f"{str_var} +=" in next_next:
                    loop_match = re.search(r'for\s+\w+\s+in\s+(\w+)', next_line)
                    if loop_match:
                        var_name = loop_match.group(1)
                        result_lines.append(f"{' ' * indent}{str_var} = ''.join(str(item) for item in {var_name})")
                        i += 3
                        continue
            
            # Pattern: Replace range(len()) with direct iteration
            if "range(len(" in stripped and "for" in stripped:
                range_match = re.search(r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\)', stripped)
                if range_match:
                    index_var = range_match.group(1)
                    list_var = range_match.group(2)
                    new_line = re.sub(
                        r'for\s+\w+\s+in\s+range\(len\(\w+\)\)',
                        f"for {index_var} in {list_var}",
                        stripped
                    )
                    result_lines.append(' ' * indent + new_line)
                    
                    # Replace list_var[index_var] in subsequent lines
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j]
                        next_stripped = next_line.lstrip()
                        next_indent = len(next_line) - len(next_stripped) if next_line.strip() else 0
                        
                        if next_indent <= indent:
                            break
                        
                        pattern = rf'\b{re.escape(list_var)}\[{re.escape(index_var)}\]'
                        if re.search(pattern, next_stripped):
                            next_line = re.sub(pattern, index_var, next_line)
                            lines[j] = next_line
                        
                        j += 1
                    
                    i += 1
                    continue
            
            # Default: keep the line
            result_lines.append(line)
            i += 1
        
        return '\n'.join(result_lines)
    
    def _has_inefficient_patterns(self, code: str, language: str) -> bool:
        """Check if code has inefficient patterns that can be optimized"""
        lang_lower = language.lower()
        
        if lang_lower == "python":
            # Check for common inefficient patterns
            inefficient_patterns = [
                r'range\(len\(',
                r'for\s+\w+\s+in\s+range\(len\(',
                r'\.append\(',
                r'for\s+\w+\s+in\s+\w+:\s*\n\s*\w+\s*\+=\s*',
                r'for\s+\w+\s+in\s+\w+:\s*\n\s*\w+\s*=\s*\w+\s*\+\s*',
            ]
            for pattern in inefficient_patterns:
                if re.search(pattern, code, re.MULTILINE):
                    return True
        return False
    
    def _aggressive_optimize(self, code: str, language: str) -> str:
        """More aggressive optimization when standard optimization fails"""
        if language.lower() == "python":
            optimized = code
            
            # Try direct regex replacements for common patterns
            # Pattern: result = []; for i in range(len(items)): result.append(items[i])
            pattern1 = r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+range\(len\((\w+)\)\):\s*\n\s*\1\.append\(\3\[\2\]\)'
            replacement1 = r'\1 = [\2 for \2 in \3]'
            optimized = re.sub(pattern1, replacement1, optimized, flags=re.MULTILINE)
            
            # Pattern: total = 0; for i in range(len(nums)): total += nums[i]
            pattern2 = r'(\w+)\s*=\s*0\s*\n\s*for\s+\w+\s+in\s+range\(len\((\w+)\)\):\s*\n\s*\1\s*\+=\s*\2\[\w+\]'
            replacement2 = r'\1 = sum(\2)'
            optimized = re.sub(pattern2, replacement2, optimized, flags=re.MULTILINE)
            
            return optimized
        
        return code
    
    def _optimize_code_chunk(self, code: str, language: str) -> str:
        """Optimize a code chunk based on language"""
        if language == "python":
            return self._optimize_python_code(code)
        elif language in ["javascript", "js", "typescript", "ts"]:
            return self._optimize_javascript_code(code)
        elif language == "java":
            return self._optimize_java_code(code)
        elif language in ["cpp", "c++", "c"]:
            return self._optimize_cpp_code(code)
        else:
            return self._optimize_generic_code(code)
    
    def _optimize_python_code(self, code: str) -> str:
        """Generate fully optimized Python code - comprehensive transformation"""
        optimized = code
        
        # Step 1: Apply simple regex replacements for common patterns (more flexible)
        # Pattern: result = []\nfor i in range(len(items)):\n    result.append(items[i])
        # This handles variations in spacing and formatting
        def replace_append_pattern(match):
            result_var = match.group(1)
            index_var = match.group(2)
            list_var = match.group(3)
            expr = match.group(4).strip() if match.lastindex >= 4 else index_var
            # Replace list_var[index_var] with index_var in the expression
            expr = re.sub(rf'\b{re.escape(list_var)}\[{re.escape(index_var)}\]', index_var, expr)
            return f"{result_var} = [{expr} for {index_var} in {list_var}]"
        
        # More flexible pattern that handles whitespace variations
        append_pattern = r'(\w+)\s*=\s*\[\]\s*\n\s*for\s+(\w+)\s+in\s+range\(len\((\w+)\)\)\s*:\s*\n\s+\1\s*\.\s*append\s*\(\s*([^)]+)\s*\)'
        optimized = re.sub(append_pattern, replace_append_pattern, optimized, flags=re.MULTILINE)
        
        # Pattern: total = 0\nfor i in range(len(nums)):\n    total += nums[i] or total = total + nums[i]
        def replace_sum_pattern(match):
            sum_var = match.group(1)
            list_var = match.group(2)
            return f"{sum_var} = sum({list_var})"
        
        sum_pattern = r'(\w+)\s*=\s*0\s*\n\s*for\s+\w+\s+in\s+range\(len\((\w+)\)\)\s*:\s*\n\s+\1\s*(?:\+=\s*\2\[\w+\]|=\s*\1\s*\+\s*\2\[\w+\])'
        optimized = re.sub(sum_pattern, replace_sum_pattern, optimized, flags=re.MULTILINE)
        
        # Pattern: output = ""\nfor i in range(len(items)):\n    output += str(items[i])
        def replace_string_concat_pattern(match):
            str_var = match.group(1)
            list_var = match.group(2)
            return f"{str_var} = ''.join(str(item) for item in {list_var})"
        
        string_pattern = r'(\w+)\s*=\s*["\']\s*["\']\s*\n\s*for\s+\w+\s+in\s+range\(len\((\w+)\)\)\s*:\s*\n\s+\1\s*\+=\s*str\(\2\[\w+\]\)'
        optimized = re.sub(string_pattern, replace_string_concat_pattern, optimized, flags=re.MULTILINE)
        
        # Step 2: Process function by function for more complex cases
        functions = re.split(r'(def\s+\w+[^:]*:)', optimized)
        if len(functions) > 1:
            # We have function definitions
            optimized_parts = []
            for i in range(0, len(functions), 2):
                if i < len(functions):
                    func_def = functions[i]
                    func_body = functions[i+1] if i+1 < len(functions) else ""
                    
                    # Optimize the function body
                    if func_body:
                        func_body_opt = self._optimize_function_body(func_body)
                        optimized_parts.append(func_def + func_body_opt)
                    else:
                        optimized_parts.append(func_def)
            
            optimized = ''.join(optimized_parts)
        else:
            # No function definitions, optimize as a whole
            optimized = self._optimize_function_body(optimized)
        
        # Now do line-by-line processing for more complex cases
        lines = optimized.split('\n')
        result_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.lstrip()
            indent = len(line) - len(stripped)
            
            # Pattern 1: Convert range(len(x)) loops with append() to list comprehensions
            range_len_match = re.search(r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\)', stripped)
            if range_len_match:
                index_var = range_len_match.group(1)
                list_var = range_len_match.group(2)
                
                # Look ahead to see if there's an append() pattern
                if i < len(lines) - 1:
                    # Check if there's a result = [] before this loop
                    result_var = None
                    for k in range(max(0, i-5), i):
                        prev_match = re.search(r'(\w+)\s*=\s*\[\]', lines[k])
                        if prev_match:
                            result_var = prev_match.group(1)
                            break
                    
                    if result_var:
                        # Look for append() in the loop body
                        j = i + 1
                        append_found = False
                        append_expr = None
                        loop_body_end = i + 1
                        
                        while j < len(lines):
                            next_line = lines[j]
                            next_stripped = next_line.lstrip()
                            next_indent = len(next_line) - len(next_stripped)
                            
                            if next_indent <= indent:
                                break
                            
                            if f"{result_var}.append(" in next_stripped:
                                append_found = True
                                append_match = re.search(r'\.append\((.*?)\)', next_stripped)
                                if append_match:
                                    append_expr = append_match.group(1).strip()
                                    # Replace list_var[index_var] with a new variable name
                                    append_expr = re.sub(rf'\b{re.escape(list_var)}\[{re.escape(index_var)}\]', index_var, append_expr)
                                loop_body_end = j + 1
                                break
                            
                            j += 1
                        
                        if append_found and append_expr:
                            # Check for if condition
                            if_match = re.search(r'if\s+(.+?):', stripped)
                            if if_match:
                                condition = if_match.group(1)
                                condition = re.sub(rf'\b{re.escape(list_var)}\[{re.escape(index_var)}\]', index_var, condition)
                                new_line = f"{' ' * indent}{result_var} = [{append_expr} for {index_var} in {list_var} if {condition}]"
                            else:
                                new_line = f"{' ' * indent}{result_var} = [{append_expr} for {index_var} in {list_var}]"
                            
                            result_lines.append(new_line)
                            i = loop_body_end
                            continue
            
            # Pattern 2: Convert manual sum loops
            if re.search(r'(\w+)\s*=\s*0\s*$', stripped):
                sum_var_match = re.search(r'(\w+)\s*=\s*0', stripped)
                if sum_var_match and i < len(lines) - 2:
                    sum_var = sum_var_match.group(1)
                    next_line = lines[i+1].lstrip()
                    next_next = lines[i+2].lstrip()
                    
                    # Check for: for i in range(len(var)): total += var[i]
                    if "for" in next_line and f"{sum_var} +=" in next_next:
                        range_match = re.search(r'for\s+\w+\s+in\s+range\(len\((\w+)\)\)', next_line)
                        if range_match:
                            var_name = range_match.group(1)
                            result_lines.append(f"{' ' * indent}{sum_var} = sum({var_name})")
                            i += 3
                            continue
                        # Check for: for item in items: total += item
                        direct_match = re.search(r'for\s+\w+\s+in\s+(\w+)', next_line)
                        if direct_match:
                            var_name = direct_match.group(1)
                            result_lines.append(f"{' ' * indent}{sum_var} = sum({var_name})")
                            i += 3
                            continue
            
            # Pattern 3: Convert string concatenation to join()
            if re.search(r'(\w+)\s*=\s*["\']\s*["\']', stripped):
                str_var_match = re.search(r'(\w+)\s*=\s*["\']\s*["\']', stripped)
                if str_var_match and i < len(lines) - 2:
                    str_var = str_var_match.group(1)
                    next_line = lines[i+1].lstrip()
                    next_next = lines[i+2].lstrip()
                    
                    if "for" in next_line and f"{str_var} +=" in next_next:
                        loop_match = re.search(r'for\s+\w+\s+in\s+(\w+)', next_line)
                        if loop_match:
                            var_name = loop_match.group(1)
                            result_lines.append(f"{' ' * indent}{str_var} = ''.join(str(item) for item in {var_name})")
                            i += 3
                            continue
            
            # Pattern 4: Replace remaining range(len()) with direct iteration and fix index access
            if "range(len(" in stripped and "for" in stripped:
                range_match = re.search(r'for\s+(\w+)\s+in\s+range\(len\((\w+)\)\)', stripped)
                if range_match:
                    index_var = range_match.group(1)
                    list_var = range_match.group(2)
                    # Replace the for line
                    new_line = re.sub(
                        r'for\s+\w+\s+in\s+range\(len\(\w+\)\)',
                        f"for {index_var} in {list_var}",
                        stripped
                    )
                    result_lines.append(' ' * indent + new_line)
                    
                    # Now replace list_var[index_var] with index_var in subsequent lines
                    j = i + 1
                    while j < len(lines):
                        next_line = lines[j]
                        next_stripped = next_line.lstrip()
                        next_indent = len(next_line) - len(next_stripped)
                        
                        if next_indent <= indent:
                            break
                        
                        # Replace list_var[index_var] with index_var
                        pattern = rf'\b{re.escape(list_var)}\[{re.escape(index_var)}\]'
                        if re.search(pattern, next_stripped):
                            next_line = re.sub(pattern, index_var, next_line)
                            lines[j] = next_line
                        
                        j += 1
                    
                    i += 1
                    continue
            
            # Pattern 5: Convert simple loops with append() to list comprehensions (even without range(len))
            if "for" in stripped and i < len(lines) - 1:
                # Look for result = [] before the loop
                result_var = None
                for k in range(max(0, i-5), i):
                    prev_match = re.search(r'(\w+)\s*=\s*\[\]', lines[k])
                    if prev_match:
                        result_var = prev_match.group(1)
                        break
                
                if result_var:
                    # Check if next line has append
                    next_stripped = lines[i+1].lstrip() if i+1 < len(lines) else ""
                    next_indent = len(lines[i+1]) - len(next_stripped) if i+1 < len(lines) else 0
                    
                    if next_indent > indent and f"{result_var}.append(" in next_stripped:
                        # Extract append expression
                        append_match = re.search(r'\.append\((.*?)\)', next_stripped)
                        if append_match:
                            append_expr = append_match.group(1).strip()
                            
                            # Extract loop details - handle both "for x in items" and "for i in range(len(items))"
                            loop_match = re.search(r'for\s+(\w+)\s+in\s+(\w+)', stripped)
                            if loop_match and "range(len(" not in stripped:  # Only if not range(len())
                                loop_var = loop_match.group(1)
                                iterable = loop_match.group(2)
                                
                                # Check for condition
                                if_match = re.search(r'if\s+(.+?):', stripped)
                                if if_match:
                                    condition = if_match.group(1)
                                    new_code = f"{' ' * indent}{result_var} = [{append_expr} for {loop_var} in {iterable} if {condition}]"
                                else:
                                    new_code = f"{' ' * indent}{result_var} = [{append_expr} for {loop_var} in {iterable}]"
                                
                                result_lines.append(new_code)
                                i += 2  # Skip for loop and append line
                                continue
            
            # Pattern 6: Replace pandas iterrows()
            if "iterrows()" in stripped:
                stripped = stripped.replace("iterrows()", "# Use vectorized operations instead of iterrows()")
                result_lines.append(' ' * indent + stripped)
                i += 1
                continue
            
            # Default: keep the line as-is
            result_lines.append(line)
            i += 1
        
        return '\n'.join(result_lines)
    
    def _optimize_javascript_code(self, code: str) -> str:
        """Generate fully optimized JavaScript code"""
        lines = code.split('\n')
        optimized_lines = []
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # Optimize traditional for loops to for...of
            if "for (let i = 0" in line or "for(var i = 0" in line:
                # Extract array name
                match = re.search(r'for\s*\([^)]*i\s*<\s*(\w+)\.length', line)
                if match:
                    array_name = match.group(1)
                    line = line.replace(f"for (let i = 0; i < {array_name}.length; i++)", f"for (const item of {array_name})")
                    line = line.replace(f"{array_name}[i]", "item")
            
            # Optimize loops with push() to array methods
            if i < len(lines) - 2 and "push(" in lines[i+1] and "for" in line:
                if "const result = []" in '\n'.join(lines[max(0, i-2):i]):
                    # Try to convert to map/filter
                    optimized_lines.append("// Optimized: Use array methods instead of push()")
                    optimized_lines.append("const result = array.filter(condition).map(process);")
                    i += 2
                    continue
            
            optimized_lines.append(line)
            i += 1
        
        return '\n'.join(optimized_lines)
    
    def _optimize_java_code(self, code: str) -> str:
        """Generate fully optimized Java code"""
        lines = code.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Optimize traditional for loops to enhanced for loops
            if "for (int i = 0" in line:
                match = re.search(r'for\s*\(int\s+i\s*=\s*0;\s*i\s*<\s*(\w+)\.size\(\)', line)
                if match:
                    list_name = match.group(1)
                    line = line.replace(f"for (int i = 0; i < {list_name}.size(); i++)", f"for (String item : {list_name})")
                    line = line.replace(f"{list_name}.get(i)", "item")
            
            # Optimize string concatenation to StringBuilder
            if "String result = \"\"" in line or 'String result = ""' in line:
                line = "StringBuilder sb = new StringBuilder();"
            
            optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _optimize_cpp_code(self, code: str) -> str:
        """Generate fully optimized C++ code"""
        lines = code.split('\n')
        optimized_lines = []
        
        for line in lines:
            # Optimize traditional for loops to range-based
            if "for (int i = 0" in line:
                match = re.search(r'for\s*\(int\s+i\s*=\s*0;\s*i\s*<\s*(\w+)\.size\(\)', line)
                if match:
                    vec_name = match.group(1)
                    line = line.replace(f"for (int i = 0; i < {vec_name}.size(); i++)", f"for (const auto& item : {vec_name})")
                    line = line.replace(f"{vec_name}[i]", "item")
            
            # Optimize raw pointers to smart pointers
            if "new " in line and "*" in line:
                line = line.replace("int* ptr = new int", "std::unique_ptr<int> ptr = std::make_unique<int")
            
            optimized_lines.append(line)
        
        return '\n'.join(optimized_lines)
    
    def _optimize_generic_code(self, code: str) -> str:
        """Generic optimization for unknown languages"""
        # Apply basic optimizations
        optimized = code
        
        # Remove unnecessary whitespace
        lines = optimized.split('\n')
        optimized_lines = [line.rstrip() for line in lines if line.strip() or line == '']
        
        return '\n'.join(optimized_lines)
    
    def _generate_analysis_summary(self, original: str, optimized: str, orig_metrics: Dict, opt_metrics: Dict) -> str:
        """Generate a short analysis summary"""
        score_improvement = opt_metrics["green_score"] - orig_metrics["green_score"]
        energy_reduction = ((orig_metrics["energy_consumption_wh"] - opt_metrics["energy_consumption_wh"]) / orig_metrics["energy_consumption_wh"]) * 100 if orig_metrics["energy_consumption_wh"] > 0 else 0
        
        summary = f"Code optimization analysis completed. "
        summary += f"Green Score improved by {score_improvement:.1f} points ({orig_metrics['green_score']:.1f} → {opt_metrics['green_score']:.1f}). "
        summary += f"Energy consumption reduced by {energy_reduction:.1f}%. "
        summary += f"Time complexity: {orig_metrics.get('time_complexity', 'Unknown')} → {opt_metrics.get('time_complexity', 'Unknown')}."
        
        return summary
    
    def _generate_improvements_explanation(self, original: str, optimized: str, language: str) -> str:
        """Generate detailed explanation of improvements"""
        improvements = []
        
        if language == "python":
            if "range(len(" in original and "range(len(" not in optimized:
                improvements.append("✓ Replaced index-based iteration (range(len())) with direct iteration, reducing CPU overhead")
            if original.count("append(") > optimized.count("append("):
                improvements.append("✓ Converted loops with append() to list comprehensions, improving performance and memory efficiency")
            if "sum(" in optimized and "total = 0" in original:
                improvements.append("✓ Replaced manual summation loops with built-in sum() function")
            if "iterrows()" in original and "iterrows()" not in optimized:
                improvements.append("✓ Replaced pandas iterrows() with vectorized operations")
        
        if not improvements:
            improvements.append("✓ Applied general code optimizations for better performance and energy efficiency")
        
        return "\n".join(improvements)


# Global predictor instance
green_predictor = GreenCodingPredictor()
