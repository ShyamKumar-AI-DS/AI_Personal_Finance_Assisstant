import pandas as pd
import numpy as np
import os

class DataLoader:
    def __init__(self):
        pass

    def load_file(self, filepath):
        """
        Loads data from CSV or Excel file.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        _, ext = os.path.splitext(filepath)
        ext = ext.lower()

        try:
            if ext == '.csv':
                df = pd.read_csv(filepath)
            elif ext in ['.xlsx', '.xls']:
                df = pd.read_excel(filepath)
            else:
                raise ValueError(f"Unsupported file extension: {ext}")
            return df
        except Exception as e:
            raise RuntimeError(f"Error loading file {filepath}: {e}")

    def clean_column_names(self, df):
        """
        Standardizes column names: lowercase, strip, replace spaces with underscores.
        """
        df.columns = df.columns.astype(str).str.strip().str.lower().str.replace(' ', '_')
        return df

    def remove_duplicates(self, df):
        """
        Removes duplicate rows.
        """
        return df.drop_duplicates()

    def parse_dates(self, df, date_col='date'):
        """
        Parses the specified date column to datetime objects.
        """
        if date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        return df

    def standardize_amounts(self, df, amount_col='amount'):
        """
        Ensures amount column is numeric and adds a normalized column.
        """
        if amount_col in df.columns:
            # Ensure numeric, coercing errors to NaN
            df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce')
            
            # Drop/fill NaNs if needed? For now we keep them or let user decide.
            # Normalization (Min-Max scaling) as per notebook logic
            min_val = df[amount_col].min()
            max_val = df[amount_col].max()
            
            if max_val != min_val:
                df[f'{amount_col}_normalized'] = (df[amount_col] - min_val) / (max_val - min_val)
            else:
                df[f'{amount_col}_normalized'] = 0.0
                
        return df

    def df_shape(self,df):
        return df.shape

    def run_pipeline(self, filepath, date_col='date', amount_col='amount'):
        """
        Runs the full loading and cleaning pipeline.
        """
        print(f"Loading {filepath}...")
        df = self.load_file(filepath)
        
        print("Cleaning column names...")
        df = self.clean_column_names(df)
        
        print("Removing duplicates...")
        df = self.remove_duplicates(df)
        
        # After cleaning columns, the passed date_col/amount_col might need to match the new schema
        # Usually user passes 'Date' but after cleaning it becomes 'date'. 
        # We handle this by checking if the snake_case version exists if original doesn't.
        
        target_date_col = date_col.strip().lower().replace(' ', '_')
        target_amount_col = amount_col.strip().lower().replace(' ', '_')

        print(f"Parsing dates (column: {target_date_col})...")
        df = self.parse_dates(df, date_col=target_date_col)
        
        print(f"Standardizing amounts (column: {target_amount_col})...")
        df = self.standardize_amounts(df, amount_col=target_amount_col)
        
        return df

if __name__ == "__main__":
    # Example usage
    loader = DataLoader()
    
    # Construct path relative to this script file to work regardless of CWD
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "../Datasets/Personal_Finance_Data_2023.csv")
    
    # Verify file exists before running
    if os.path.exists(dataset_path):
        df = loader.run_pipeline(dataset_path)
        print(df.head())
        print(loader.df_shape(df))
    else:
        print(f"Example file not found at: {dataset_path}")
