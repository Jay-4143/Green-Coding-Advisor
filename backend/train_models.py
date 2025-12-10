#!/usr/bin/env python
"""
Script to train ML models for Green Coding Advisor
Run this from the backend directory: python train_models.py
"""
import sys
import os
from pathlib import Path

# Add the backend directory to the path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

try:
    from app.ml_training import GreenCodingModelTrainer
    
    print("=" * 60)
    print("Green Coding Advisor - ML Model Training")
    print("=" * 60)
    print()
    
    # Create trainer instance
    trainer = GreenCodingModelTrainer()
    
    # Train all models
    models = trainer.train_all_models()
    
    print()
    print("=" * 60)
    print("Training Complete!")
    print("=" * 60)
    models_path = backend_dir / "app" / "models"
    print(f"Models saved to: {models_path}")
    print()
    print("Trained models:")
    for model_name in models.keys():
        model_file = models_path / f"{model_name}_model.pkl"
        if model_file.exists():
            size = model_file.stat().st_size / 1024  # Size in KB
            print(f"  ✓ {model_name} ({size:.1f} KB)")
        else:
            print(f"  ✓ {model_name} (saved)")
    print()
    
except ImportError as e:
    print(f"ERROR: Failed to import required modules: {e}")
    print("\nPlease ensure all dependencies are installed:")
    print("  pip install torch transformers scikit-learn numpy pandas joblib")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Training failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

