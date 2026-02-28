"""
Data loader module for Titanic dataset.
"""
import os
import pandas as pd
from pathlib import Path


def get_data_paths():
    """Get paths for data directories."""
    project_root = Path(__file__).parent.parent
    raw_data_path = project_root / 'data' / 'raw'
    processed_data_path = project_root / 'data' / 'processed'
    
    # Create directories if they don't exist
    raw_data_path.mkdir(parents=True, exist_ok=True)
    processed_data_path.mkdir(parents=True, exist_ok=True)
    
    return raw_data_path, processed_data_path


def load_titanic_data(train_path=None, test_path=None):
    """
    Load Titanic train and test datasets.
    
    Args:
        train_path: Path to training data CSV (optional)
        test_path: Path to test data CSV (optional)
    
    Returns:
        tuple: (train_df, test_df)
    """
    raw_data_path, _ = get_data_paths()
    
    # Default paths if not provided
    if train_path is None:
        train_path = raw_data_path / 'train.csv'
    if test_path is None:
        test_path = raw_data_path / 'test.csv'
    
    # Check if files exist
    if not os.path.exists(train_path):
        raise FileNotFoundError(
            f"Training data not found at {train_path}. "
            "Please run scripts/download_data.py first."
        )
    
    # Load data
    train_df = pd.read_csv(train_path)
    
    # Test data might not exist for some scenarios
    test_df = None
    if os.path.exists(test_path):
        test_df = pd.read_csv(test_path)
    
    return train_df, test_df


def save_processed_data(train_df, test_df=None, val_df=None):
    """
    Save processed datasets.
    
    Args:
        train_df: Training dataframe
        test_df: Test dataframe (optional)
        val_df: Validation dataframe (optional)
    """
    _, processed_data_path = get_data_paths()
    
    train_df.to_csv(processed_data_path / 'train_processed.csv', index=False)
    print(f"Saved processed training data: {len(train_df)} rows")
    
    if test_df is not None:
        test_df.to_csv(processed_data_path / 'test_processed.csv', index=False)
        print(f"Saved processed test data: {len(test_df)} rows")
    
    if val_df is not None:
        val_df.to_csv(processed_data_path / 'val_processed.csv', index=False)
        print(f"Saved processed validation data: {len(val_df)} rows")


def load_processed_data():
    """
    Load processed datasets.
    
    Returns:
        tuple: (train_df, test_df, val_df)
    """
    _, processed_data_path = get_data_paths()
    
    train_df = pd.read_csv(processed_data_path / 'train_processed.csv')
    
    test_df = None
    if (processed_data_path / 'test_processed.csv').exists():
        test_df = pd.read_csv(processed_data_path / 'test_processed.csv')
    
    val_df = None
    if (processed_data_path / 'val_processed.csv').exists():
        val_df = pd.read_csv(processed_data_path / 'val_processed.csv')
    
    return train_df, test_df, val_df
