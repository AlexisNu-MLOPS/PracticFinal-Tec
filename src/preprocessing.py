"""
Preprocessing module for Titanic dataset.
Includes data cleaning, feature engineering, and transformations.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split


class TitanicPreprocessor:
    """Preprocessing pipeline for Titanic dataset."""
    
    def __init__(self):
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.feature_columns = None
        
    def extract_title(self, name):
        """Extract title from name."""
        if pd.isna(name):
            return 'Unknown'
        title = name.split(',')[1].split('.')[0].strip()
        # Group rare titles
        if title in ['Mlle', 'Ms']:
            return 'Miss'
        elif title == 'Mme':
            return 'Mrs'
        elif title not in ['Mr', 'Miss', 'Mrs', 'Master']:
            return 'Rare'
        return title
    
    def create_features(self, df):
        """
        Create engineered features.
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with new features
        """
        df = df.copy()
        
        # Family size
        df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
        
        # Is alone
        df['IsAlone'] = (df['FamilySize'] == 1).astype(int)
        
        # Title from name
        df['Title'] = df['Name'].apply(self.extract_title)
        
        # Age bins
        df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 35, 60, 100],
                                labels=['Child', 'Teen', 'Adult', 'Middle', 'Senior'])
        
        # Fare bins
        df['FareGroup'] = pd.qcut(df['Fare'], q=4, labels=['Low', 'Medium', 'High', 'VeryHigh'],
                                   duplicates='drop')
        
        return df
    
    def fill_missing_values(self, df):
        """
        Fill missing values with appropriate strategies.
        
        Args:
            df: Input dataframe
            
        Returns:
            DataFrame with filled missing values
        """
        df = df.copy()
        
        # Age: fill with median by Sex and Pclass
        df['Age'] = df.groupby(['Sex', 'Pclass'])['Age'].transform(
            lambda x: x.fillna(x.median())
        )
        
        # If still missing, fill with overall median
        df['Age'] = df['Age'].fillna(df['Age'].median())
        
        # Embarked: fill with mode
        df['Embarked'] = df['Embarked'].fillna(df['Embarked'].mode()[0])
        
        # Fare: fill with median
        df['Fare'] = df['Fare'].fillna(df['Fare'].median())
        
        # Cabin: create binary feature for cabin known/unknown
        df['HasCabin'] = df['Cabin'].notna().astype(int)
        
        return df
    
    def encode_categorical(self, df, fit=True):
        """
        Encode categorical variables.
        
        Args:
            df: Input dataframe
            fit: Whether to fit encoders (True for train, False for test)
            
        Returns:
            DataFrame with encoded categorical variables
        """
        df = df.copy()
        
        categorical_cols = ['Sex', 'Embarked', 'Title']
        
        for col in categorical_cols:
            if col in df.columns:
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    df[col] = self.label_encoders[col].fit_transform(df[col].astype(str))
                else:
                    # Handle unseen categories
                    df[col] = df[col].astype(str)
                    df[col] = df[col].apply(
                        lambda x: x if x in self.label_encoders[col].classes_ 
                        else self.label_encoders[col].classes_[0]
                    )
                    df[col] = self.label_encoders[col].transform(df[col])
        
        # One-hot encode AgeGroup and FareGroup if they exist
        if 'AgeGroup' in df.columns:
            df = pd.get_dummies(df, columns=['AgeGroup'], prefix='AgeGroup', drop_first=True)
        
        if 'FareGroup' in df.columns:
            df = pd.get_dummies(df, columns=['FareGroup'], prefix='FareGroup', drop_first=True)
        
        return df
    
    def select_features(self, df, target_col='Survived'):
        """
        Select relevant features for modeling.
        
        Args:
            df: Input dataframe
            target_col: Name of target column
            
        Returns:
            X (features), y (target)
        """
        # Drop columns not used for modeling
        drop_cols = ['PassengerId', 'Name', 'Ticket', 'Cabin']
        
        # Keep only columns that exist
        drop_cols = [col for col in drop_cols if col in df.columns]
        
        df_features = df.drop(columns=drop_cols, errors='ignore')
        
        # Separate features and target
        if target_col in df_features.columns:
            y = df_features[target_col]
            X = df_features.drop(columns=[target_col])
        else:
            y = None
            X = df_features
        
        return X, y
    
    def scale_features(self, X, fit=True):
        """
        Scale numerical features.
        
        Args:
            X: Feature dataframe
            fit: Whether to fit scaler (True for train, False for test)
            
        Returns:
            Scaled feature dataframe
        """
        numerical_cols = ['Age', 'Fare', 'SibSp', 'Parch', 'FamilySize']
        numerical_cols = [col for col in numerical_cols if col in X.columns]
        
        if len(numerical_cols) > 0:
            if fit:
                X[numerical_cols] = self.scaler.fit_transform(X[numerical_cols])
            else:
                X[numerical_cols] = self.scaler.transform(X[numerical_cols])
        
        return X
    
    def fit_transform(self, df, target_col='Survived'):
        """
        Complete preprocessing pipeline for training data.
        
        Args:
            df: Training dataframe
            target_col: Name of target column
            
        Returns:
            X (features), y (target)
        """
        # Create features first (before filling, as some fills depend on features)
        df = self.create_features(df)
        
        # Fill missing values
        df = self.fill_missing_values(df)
        
        # Encode categorical
        df = self.encode_categorical(df, fit=True)
        
        # Select features
        X, y = self.select_features(df, target_col)
        
        # Store feature columns
        self.feature_columns = X.columns.tolist()
        
        # Scale features
        X = self.scale_features(X, fit=True)
        
        return X, y
    
    def transform(self, df, target_col=None):
        """
        Transform test/validation data using fitted preprocessor.
        
        Args:
            df: Test/validation dataframe
            target_col: Name of target column (optional)
            
        Returns:
            X (features), y (target if available)
        """
        # Create features first (before filling, as some fills depend on features)
        df = self.create_features(df)
        
        # Fill missing values
        df = self.fill_missing_values(df)
        
        # Encode categorical
        df = self.encode_categorical(df, fit=False)
        
        # Select features
        X, y = self.select_features(df, target_col) if target_col else (df, None)
        
        # Align columns with training data
        if self.feature_columns:
            # Add missing columns
            for col in self.feature_columns:
                if col not in X.columns:
                    X[col] = 0
            
            # Remove extra columns and reorder
            X = X[self.feature_columns]
        
        # Scale features
        X = self.scale_features(X, fit=False)
        
        return X, y


def preprocess_data(train_df, test_df=None, val_split=0.2, random_state=42):
    """
    Preprocess Titanic data.
    
    Args:
        train_df: Training dataframe
        test_df: Test dataframe (optional)
        val_split: Validation split ratio
        random_state: Random seed
        
    Returns:
        Dictionary with preprocessed data and preprocessor
    """
    preprocessor = TitanicPreprocessor()
    
    # Split train into train and validation
    if val_split > 0:
        train_data, val_data = train_test_split(
            train_df, test_size=val_split, random_state=random_state, 
            stratify=train_df['Survived'] if 'Survived' in train_df.columns else None
        )
    else:
        train_data = train_df
        val_data = None
    
    # Fit and transform training data
    X_train, y_train = preprocessor.fit_transform(train_data)
    
    # Transform validation data
    X_val, y_val = None, None
    if val_data is not None:
        X_val, y_val = preprocessor.transform(val_data, target_col='Survived')
    
    # Transform test data
    X_test, y_test = None, None
    if test_df is not None:
        target_col = 'Survived' if 'Survived' in test_df.columns else None
        X_test, y_test = preprocessor.transform(test_df, target_col=target_col)
    
    return {
        'X_train': X_train,
        'y_train': y_train,
        'X_val': X_val,
        'y_val': y_val,
        'X_test': X_test,
        'y_test': y_test,
        'preprocessor': preprocessor
    }
