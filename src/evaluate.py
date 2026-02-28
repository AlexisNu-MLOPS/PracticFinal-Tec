"""
Evaluation script for Titanic survival prediction model.
"""
import sys
import json
import argparse
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve
)

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import load_titanic_data
from src.preprocessing import preprocess_data
from src.model import load_model


def plot_confusion_matrix(y_true, y_pred, save_path):
    """Plot and save confusion matrix."""
    cm = confusion_matrix(y_true, y_pred)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Confusion matrix saved to: {save_path}")


def plot_roc_curve(y_true, y_proba, save_path):
    """Plot and save ROC curve."""
    fpr, tpr, _ = roc_curve(y_true, y_proba)
    roc_auc = roc_auc_score(y_true, y_proba)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ ROC curve saved to: {save_path}")


def plot_feature_importance(feature_importance, save_path, top_n=15):
    """Plot and save feature importance."""
    # Sort features by importance
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    top_features = sorted_features[:top_n]
    
    features, importances = zip(*top_features)
    
    plt.figure(figsize=(10, 6))
    plt.barh(range(len(features)), importances, color='steelblue')
    plt.yticks(range(len(features)), features)
    plt.xlabel('Importance')
    plt.title(f'Top {top_n} Feature Importances')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"   ✓ Feature importance plot saved to: {save_path}")


def evaluate_model(model_filename='titanic_model_random_forest.pkl', use_test=True):
    """
    Evaluate trained Titanic survival prediction model.
    
    Args:
        model_filename: Name of model file to load
        use_test: Whether to evaluate on test set (True) or validation set (False)
        
    Returns:
        Dictionary with evaluation results
    """
    print("=" * 50)
    print("TITANIC SURVIVAL PREDICTION - EVALUATION")
    print("=" * 50)
    
    # Load model
    print("\n1. Loading model...")
    model = load_model(model_filename)
    
    # Load data
    print("\n2. Loading data...")
    train_df, test_df = load_titanic_data()
    
    # Preprocess data
    print("\n3. Preprocessing data...")
    processed = preprocess_data(train_df, test_df, val_split=0.2)
    
    # Select evaluation set
    if use_test and processed['X_test'] is not None and processed['y_test'] is not None:
        X_eval = processed['X_test']
        y_eval = processed['y_test']
        eval_set_name = 'Test'
    elif processed['X_val'] is not None and processed['y_val'] is not None:
        X_eval = processed['X_val']
        y_eval = processed['y_val']
        eval_set_name = 'Validation'
    else:
        raise ValueError("No evaluation data available")
    
    print(f"   ✓ Evaluating on {eval_set_name} set: {X_eval.shape}")
    
    # Make predictions
    print("\n4. Making predictions...")
    y_pred = model.predict(X_eval)
    y_proba = model.predict_proba(X_eval)[:, 1] if hasattr(model, 'predict_proba') else None
    print("   ✓ Predictions generated")
    
    # Calculate metrics
    print("\n5. Calculating metrics...")
    accuracy = accuracy_score(y_eval, y_pred)
    precision = precision_score(y_eval, y_pred)
    recall = recall_score(y_eval, y_pred)
    f1 = f1_score(y_eval, y_pred)
    
    print(f"\n   Accuracy:  {accuracy:.4f}")
    print(f"   Precision: {precision:.4f}")
    print(f"   Recall:    {recall:.4f}")
    print(f"   F1-Score:  {f1:.4f}")
    
    if y_proba is not None:
        roc_auc = roc_auc_score(y_eval, y_proba)
        print(f"   ROC-AUC:   {roc_auc:.4f}")
    else:
        roc_auc = None
    
    # Classification report
    print("\n6. Classification Report:")
    print(classification_report(y_eval, y_pred, target_names=['Not Survived', 'Survived']))
    
    # Create reports directory
    project_root = Path(__file__).parent.parent
    reports_path = project_root / 'reports'
    reports_path.mkdir(parents=True, exist_ok=True)
    
    # Plot confusion matrix
    print("\n7. Generating visualizations...")
    plot_confusion_matrix(y_eval, y_pred, reports_path / 'confusion_matrix.png')
    
    # Plot ROC curve
    if y_proba is not None:
        plot_roc_curve(y_eval, y_proba, reports_path / 'roc_curve.png')
    
    # Plot feature importance
    if hasattr(model, 'feature_importances_'):
        feature_importance = dict(zip(X_eval.columns, model.feature_importances_))
        plot_feature_importance(feature_importance, reports_path / 'feature_importance.png')
    
    # Save detailed results
    results = {
        'model_filename': model_filename,
        'evaluation_set': eval_set_name,
        'n_samples': int(len(y_eval)),
        'n_features': int(X_eval.shape[1]),
        'metrics': {
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'roc_auc': float(roc_auc) if roc_auc else None
        },
        'confusion_matrix': confusion_matrix(y_eval, y_pred).tolist(),
        'classification_report': classification_report(y_eval, y_pred, output_dict=True)
    }
    
    results_file = reports_path / 'evaluation_results.json'
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n8. Results saved to: {results_file}")
    
    print("\n" + "=" * 50)
    print("EVALUATION COMPLETE!")
    print("=" * 50)
    
    return results


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Evaluate Titanic survival prediction model')
    parser.add_argument('--model', type=str, default='titanic_model_random_forest.pkl',
                        help='Model filename to evaluate')
    parser.add_argument('--use-test', action='store_true',
                        help='Use test set instead of validation set')
    
    args = parser.parse_args()
    
    evaluate_model(
        model_filename=args.model,
        use_test=args.use_test
    )
