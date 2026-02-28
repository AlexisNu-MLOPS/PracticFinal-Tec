"""
Unit tests for model module.
"""
import pytest
import numpy as np
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.model import create_model, save_model, load_model
from sklearn.datasets import make_classification


@pytest.fixture
def sample_classification_data():
    """Create sample classification data."""
    X, y = make_classification(n_samples=100, n_features=10, n_classes=2, random_state=42)
    return X, y


def test_create_random_forest():
    """Test Random Forest model creation."""
    model = create_model('random_forest')
    assert model is not None
    assert hasattr(model, 'fit')
    assert hasattr(model, 'predict')


def test_create_logistic_regression():
    """Test Logistic Regression model creation."""
    model = create_model('logistic_regression')
    assert model is not None
    assert hasattr(model, 'fit')
    assert hasattr(model, 'predict')


def test_create_gradient_boosting():
    """Test Gradient Boosting model creation."""
    model = create_model('gradient_boosting')
    assert model is not None
    assert hasattr(model, 'fit')
    assert hasattr(model, 'predict')


def test_invalid_model_type():
    """Test that invalid model type raises error."""
    with pytest.raises(ValueError):
        create_model('invalid_model')


def test_model_training(sample_classification_data):
    """Test that model can be trained."""
    X, y = sample_classification_data
    model = create_model('random_forest', n_estimators=10, random_state=42)
    
    # Train model
    model.fit(X, y)
    
    # Make predictions
    predictions = model.predict(X)
    
    assert len(predictions) == len(y)
    assert all(p in [0, 1] for p in predictions)


def test_model_predict_proba(sample_classification_data):
    """Test that model can predict probabilities."""
    X, y = sample_classification_data
    model = create_model('random_forest', n_estimators=10, random_state=42)
    
    model.fit(X, y)
    probabilities = model.predict_proba(X)
    
    assert probabilities.shape == (len(y), 2)
    assert np.allclose(probabilities.sum(axis=1), 1.0)


def test_save_and_load_model(sample_classification_data, tmp_path):
    """Test model saving and loading."""
    X, y = sample_classification_data
    
    # Train model
    model = create_model('random_forest', n_estimators=10, random_state=42)
    model.fit(X, y)
    
    # Get predictions before saving
    pred_before = model.predict(X[:5])
    
    # Save model to temporary directory
    # Temporarily change model path
    from src import model as model_module
    original_get_model_path = model_module.get_model_path
    model_module.get_model_path = lambda: tmp_path
    
    try:
        # Save model
        filepath = save_model(model, 'test_model.pkl')
        assert filepath.exists()
        
        # Load model
        loaded_model = load_model('test_model.pkl')
        
        # Get predictions after loading
        pred_after = loaded_model.predict(X[:5])
        
        # Predictions should be the same
        assert np.array_equal(pred_before, pred_after)
    finally:
        # Restore original function
        model_module.get_model_path = original_get_model_path


def test_model_with_custom_params():
    """Test model creation with custom parameters."""
    model = create_model('random_forest', n_estimators=50, max_depth=5)
    assert model.n_estimators == 50
    assert model.max_depth == 5


def test_model_feature_importance(sample_classification_data):
    """Test that tree-based models have feature importance."""
    X, y = sample_classification_data
    
    model = create_model('random_forest', n_estimators=10, random_state=42)
    model.fit(X, y)
    
    assert hasattr(model, 'feature_importances_')
    assert len(model.feature_importances_) == X.shape[1]
    assert all(imp >= 0 for imp in model.feature_importances_)
