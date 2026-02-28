"""
Unit tests for preprocessing module.
"""
import pytest
import pandas as pd
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.preprocessing import TitanicPreprocessor, preprocess_data


@pytest.fixture
def sample_data():
    """Create sample Titanic data for testing."""
    data = {
        'PassengerId': [1, 2, 3, 4, 5],
        'Survived': [0, 1, 1, 1, 0],
        'Pclass': [3, 1, 3, 1, 3],
        'Name': ['Braund, Mr. Owen Harris', 'Cumings, Mrs. John Bradley',
                 'Heikkinen, Miss. Laina', 'Futrelle, Mrs. Jacques Heath',
                 'Allen, Mr. William Henry'],
        'Sex': ['male', 'female', 'female', 'female', 'male'],
        'Age': [22, 38, 26, 35, 35],
        'SibSp': [1, 1, 0, 1, 0],
        'Parch': [0, 0, 0, 0, 0],
        'Ticket': ['A/5 21171', 'PC 17599', 'STON/O2. 3101282', '113803', '373450'],
        'Fare': [7.25, 71.2833, 7.925, 53.1, 8.05],
        'Cabin': [np.nan, 'C85', np.nan, 'C123', np.nan],
        'Embarked': ['S', 'C', 'S', 'S', 'S']
    }
    return pd.DataFrame(data)


def test_preprocessor_initialization():
    """Test TitanicPreprocessor initialization."""
    preprocessor = TitanicPreprocessor()
    assert preprocessor is not None
    assert preprocessor.label_encoders == {}
    assert preprocessor.scaler is not None


def test_extract_title(sample_data):
    """Test title extraction from names."""
    preprocessor = TitanicPreprocessor()
    
    titles = sample_data['Name'].apply(preprocessor.extract_title)
    assert 'Mr' in titles.values
    assert 'Mrs' in titles.values
    assert 'Miss' in titles.values


def test_create_features(sample_data):
    """Test feature engineering."""
    preprocessor = TitanicPreprocessor()
    df_with_features = preprocessor.create_features(sample_data)
    
    # Check new features exist
    assert 'FamilySize' in df_with_features.columns
    assert 'IsAlone' in df_with_features.columns
    assert 'Title' in df_with_features.columns
    assert 'AgeGroup' in df_with_features.columns
    assert 'FareGroup' in df_with_features.columns
    
    # Check FamilySize calculation
    assert df_with_features.loc[0, 'FamilySize'] == 2  # SibSp=1 + Parch=0 + 1
    assert df_with_features.loc[2, 'FamilySize'] == 1  # SibSp=0 + Parch=0 + 1


def test_fill_missing_values(sample_data):
    """Test missing value imputation."""
    # Add some missing values
    sample_data.loc[0, 'Age'] = np.nan
    sample_data.loc[1, 'Embarked'] = np.nan
    
    preprocessor = TitanicPreprocessor()
    df_filled = preprocessor.fill_missing_values(sample_data)
    
    # Check no missing values in important columns
    assert df_filled['Age'].isna().sum() == 0
    assert df_filled['Embarked'].isna().sum() == 0
    assert 'HasCabin' in df_filled.columns


def test_encode_categorical(sample_data):
    """Test categorical encoding."""
    preprocessor = TitanicPreprocessor()
    
    # Add Title column first
    sample_data = preprocessor.create_features(sample_data)
    
    # Encode
    df_encoded = preprocessor.encode_categorical(sample_data, fit=True)
    
    # Check that Sex is encoded as integers
    assert df_encoded['Sex'].dtype in [np.int32, np.int64]
    assert df_encoded['Embarked'].dtype in [np.int32, np.int64]
    assert df_encoded['Title'].dtype in [np.int32, np.int64]


def test_fit_transform(sample_data):
    """Test complete preprocessing pipeline."""
    preprocessor = TitanicPreprocessor()
    X, y = preprocessor.fit_transform(sample_data)
    
    # Check shapes
    assert X.shape[0] == sample_data.shape[0]
    assert y.shape[0] == sample_data.shape[0]
    
    # Check no missing values in features
    assert X.isna().sum().sum() == 0
    
    # Check target is correct
    assert (y == sample_data['Survived']).all()


def test_transform_consistency(sample_data):
    """Test that transform produces consistent features."""
    preprocessor = TitanicPreprocessor()
    
    # Fit on data
    X_train, y_train = preprocessor.fit_transform(sample_data)
    
    # Transform same data
    X_test, y_test = preprocessor.transform(sample_data, target_col='Survived')
    
    # Should have same columns
    assert list(X_train.columns) == list(X_test.columns)
    assert X_train.shape[1] == X_test.shape[1]


def test_preprocess_data_function():
    """Test the preprocess_data function."""
    # Create larger sample data to avoid stratification issues
    data = {
        'PassengerId': list(range(1, 21)),
        'Survived': [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1],
        'Pclass': [3, 1, 3, 1, 3, 2, 1, 3, 2, 1, 3, 1, 2, 3, 1, 2, 1, 3, 2, 1],
        'Name': [f'Person {i}, {"Mr" if i % 2 == 0 else "Mrs"}. Name' for i in range(1, 21)],
        'Sex': ['male' if i % 2 == 0 else 'female' for i in range(1, 21)],
        'Age': [20 + i for i in range(20)],
        'SibSp': [i % 3 for i in range(20)],
        'Parch': [i % 2 for i in range(20)],
        'Ticket': [f'TICKET{i}' for i in range(20)],
        'Fare': [10 + i * 5 for i in range(20)],
        'Cabin': [np.nan if i % 3 == 0 else f'C{i}' for i in range(20)],
        'Embarked': ['S' if i % 3 == 0 else 'C' if i % 3 == 1 else 'Q' for i in range(20)]
    }
    sample_data = pd.DataFrame(data)
    
    result = preprocess_data(sample_data, val_split=0.2, random_state=42)
    
    # Check all expected keys exist
    assert 'X_train' in result
    assert 'y_train' in result
    assert 'X_val' in result
    assert 'y_val' in result
    assert 'preprocessor' in result
    
    # Check shapes
    assert result['X_train'].shape[0] + result['X_val'].shape[0] == sample_data.shape[0]
    assert result['X_train'].shape[1] == result['X_val'].shape[1]


def test_no_data_leakage():
    """Test that there's no data leakage from train to test."""
    # Create larger sample data to avoid stratification issues
    data = {
        'PassengerId': list(range(1, 21)),
        'Survived': [0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1],
        'Pclass': [3, 1, 3, 1, 3, 2, 1, 3, 2, 1, 3, 1, 2, 3, 1, 2, 1, 3, 2, 1],
        'Name': [f'Person {i}, {"Mr" if i % 2 == 0 else "Mrs"}. Name' for i in range(1, 21)],
        'Sex': ['male' if i % 2 == 0 else 'female' for i in range(1, 21)],
        'Age': [20 + i for i in range(20)],
        'SibSp': [i % 3 for i in range(20)],
        'Parch': [i % 2 for i in range(20)],
        'Ticket': [f'TICKET{i}' for i in range(20)],
        'Fare': [10 + i * 5 for i in range(20)],
        'Cabin': [np.nan if i % 3 == 0 else f'C{i}' for i in range(20)],
        'Embarked': ['S' if i % 3 == 0 else 'C' if i % 3 == 1 else 'Q' for i in range(20)]
    }
    sample_data = pd.DataFrame(data)
    
    result = preprocess_data(sample_data, val_split=0.4, random_state=42)
    
    X_train = result['X_train']
    X_val = result['X_val']
    
    # Check that train and val have different samples (by index)
    train_indices = set(X_train.index)
    val_indices = set(X_val.index)
    
    assert len(train_indices.intersection(val_indices)) == 0
