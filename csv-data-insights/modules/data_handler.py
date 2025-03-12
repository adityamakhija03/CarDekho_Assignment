import pandas as pd

class DataHandler:
    def __init__(self):
        self.df = None
    
    def load_csv(self, file_path):
        """Load and validate a CSV file"""
        try:
            if not file_path:
                return False, "⚠️ No file uploaded!", []
            
            self.df = pd.read_csv(file_path)
            
            if self.df.empty:
                return False, "⚠️ Uploaded CSV is empty!", []
            
            column_list = self.df.columns.tolist()
            return True, f"✅ CSV Loaded Successfully! Columns: {', '.join(column_list)}", column_list
        except Exception as e:
            return False, f"❌ Error loading CSV: {str(e)}", []
    
    def get_dataframe(self):
        """Return the loaded dataframe"""
        return self.df
    
    def get_sample_json(self, rows=50):
        """Convert sample data to JSON format"""
        if self.df is not None:
            return self.df.head(rows).to_json(orient="records")
        return None
