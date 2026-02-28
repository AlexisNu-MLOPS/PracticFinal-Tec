"""
Script to download Titanic dataset.
"""
import os
import pandas as pd
import ssl
import urllib.request
from pathlib import Path


def download_titanic_data():
    """Download Titanic dataset from seaborn (reliable source)."""
    
    # Get data directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    raw_data_path = project_root / 'data' / 'raw'
    raw_data_path.mkdir(parents=True, exist_ok=True)
    
    print("Downloading Titanic dataset...")
    
    train_path = raw_data_path / 'train.csv'
    
    if train_path.exists():
        print(f"✓ Dataset already exists, skipping download...")
    else:
        try:
            # Try using seaborn's built-in dataset
            print("Attempting to download from seaborn datasets...")
            import seaborn as sns
            df = sns.load_dataset('titanic')
            
            # Normalize column names to match Kaggle Titanic format
            column_mapping = {
                'survived': 'Survived',
                'pclass': 'Pclass',
                'sex': 'Sex',
                'age': 'Age',
                'sibsp': 'SibSp',
                'parch': 'Parch',
                'fare': 'Fare',
                'embarked': 'Embarked',
                'class': 'Pclass',  # seaborn also has 'class' which is duplicate
                'who': 'Who',
                'adult_male': 'Adult_male',
                'deck': 'Deck',
                'embark_town': 'Embark_town',
                'alive': 'Alive',
                'alone': 'Alone'
            }
            
            #Rename columns using mapping (only if they exist)
            df = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
            
            # Convert Pclass values from strings to numbers if needed
            if 'Pclass' in df.columns:
                pclass_map = {'First': 1, 'Second': 2, 'Third': 3, 1: 1, 2: 2, 3: 3}
                df['Pclass'] = df['Pclass'].map(lambda x: pclass_map.get(x, x))
                df['Pclass'] = df['Pclass'].astype(int)
            
            # Convert Sex to standard capitalized format if needed
            if 'Sex' in df.columns:
                df['Sex'] = df['Sex'].str.capitalize()
            
            # Convert Embarked to single letter code if needed
            if 'Embarked' in df.columns:
                embarked_map = {'Southampton': 'S', 'Cherbourg': 'C', 'Queenstown': 'Q', 
                                'S': 'S', 'C': 'C', 'Q': 'Q'}
                df['Embarked'] = df['Embarked'].map(lambda x: embarked_map.get(x, x) if pd.notna(x) else x)
            
            # Keep only the columns needed for Kaggle Titanic compatibility
            # PassengerId will be created as index, Name and Ticket need special handling
            required_cols = ['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']
            optional_cols = ['Who', 'Deck', 'Embark_town', 'Alive', 'Alone', 'Adult_male']
            
            # Create PassengerId if it doesn't exist
            if'PassengerId' not in df.columns:
                df.insert(0, 'PassengerId', range(1, len(df) + 1))
            
            # Create dummy Name and Ticket columns if they don't exist
            if 'Name' not in df.columns:
                df['Name'] = df.apply(lambda row: f"{row.get('Who', 'Unknown')}, {'Mr' if row.get('Sex') == 'male' else 'Mrs'}. Passenger {row.get('PassengerId', 0)}", axis=1)
            
            if 'Ticket' not in df.columns:
                df['Ticket'] = df['PassengerId'].apply(lambda x: f"TICKET{x:05d}")
            
            if 'Cabin' not in df.columns:
                # Use 'deck' if available, otherwise NaN
                if 'Deck' in df.columns:
                    df['Cabin'] = df['Deck'].apply(lambda x: f"{x}01" if pd.notna(x) else pd.NA)
                else:
                    df['Cabin'] = pd.NA
            
            # Select only Kaggle-compatible columns (remove seaborn-specific columns)
            kaggle_columns = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age',
                             'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
            
            # Keep only the columns that exist in our dataframe
            available_kaggle_cols = [col for col in kaggle_columns if col in df.columns]
            df = df[available_kaggle_cols]
            
            df.to_csv(train_path, index=False)
            print(f"✓ Downloaded dataset using seaborn and normalized column names")
            print(f"  Columns kept: {list(df.columns)}")
        except Exception as e:
            print(f"⚠ Could not download via seaborn: {e}")
            
            # Fallback: try direct download with SSL context
            try:
                print("Attempting direct download...")
                # Create SSL context that doesn't verify certificates
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                
                url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
                
                with urllib.request.urlopen(url, context=ssl_context) as response:
                    data = response.read()
                    with open(train_path, 'wb') as f:
                        f.write(data)
                print(f"✓ Downloaded dataset directly")
            except Exception as e2:
                print(f"✗ Error during direct download: {e2}")
                print("\n⚠ Could not download dataset automatically.")
                print("Please download manually from: https://www.kaggle.com/c/titanic/data")
                return False
    
    # Verify downloaded data
    if train_path.exists():
        df = pd.read_csv(train_path)
        print(f"\n✓ Dataset loaded successfully!")
        print(f"  Shape: {df.shape}")
        print(f"  Columns: {list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head())
        
        # Create a test set from the training data for demonstration
        # In a real scenario, you'd have a separate test set
        print("\nCreating test set from training data...")
        train_df = df.sample(frac=0.8, random_state=42)
        test_df = df.drop(train_df.index)
        
        train_df.to_csv(raw_data_path / 'train.csv', index=False)
        test_df.to_csv(raw_data_path / 'test.csv', index=False)
        
        print(f"✓ Train set: {train_df.shape[0]} rows")
        print(f"✓ Test set: {test_df.shape[0]} rows")
    else:
        print("\n✗ Failed to download dataset")
        return False
    
    print("\n✓ Data download complete!")
    return True


if __name__ == '__main__':
    download_titanic_data()
