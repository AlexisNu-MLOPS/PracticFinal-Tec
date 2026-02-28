"""
Run complete ML pipeline: preprocessing -> training -> evaluation
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.train import train_model
from src.evaluate import evaluate_model


def main():
    """Run complete pipeline."""
    print("\n" + "=" * 60)
    print(" " * 15 + "TITANIC ML PIPELINE")
    print("=" * 60 + "\n")
    
    # Step 1: Train model
    print("STEP 1: TRAINING MODEL")
    print("-" * 60)
    metrics = train_model(model_type='random_forest', val_split=0.2, cv_folds=5)
    
    print("\n\n")
    
    # Step 2: Evaluate model
    print("STEP 2: EVALUATING MODEL")
    print("-" * 60)
    results = evaluate_model(
        model_filename='titanic_model_random_forest.pkl',
        use_test=True
    )
    
    print("\n\n" + "=" * 60)
    print(" " * 20 + "PIPELINE COMPLETE!")
    print("=" * 60)
    print("\n📊 Check the 'reports/' directory for detailed results and visualizations")
    print("🤖 Trained model saved in 'models/' directory\n")


if __name__ == '__main__':
    main()
