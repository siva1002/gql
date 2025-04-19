import pandas as pd
from io import BytesIO
class ProcessExcell:
    def __init__(self,file,fields):
        self.file=file
        self.fields=fields
        self.df=self.create_df()
        self.invalid_rows=None
        self.valid_columns=None
    
    def validate(self):
        self.validate_excel_dataframe()
        return self
    
    def validate_excel_dataframe(self):
        self.valid_columns=self.df.columns.to_list() == self.fields
        if not self.valid_columns:
            return 
        def is_invalid(cell):
            return pd.isna(cell) or (isinstance(cell, str) and cell.strip() == '')

        invalid_mask = self.df.map(is_invalid)
        invalid_rows = self.df[invalid_mask.any(axis=1)]
        # Return 1-based row numbers to match Excel-style rows (including header at row 1)
        self.invalid_rows=invalid_rows.index.to_list()
    
    def create_df(self):
        file_data = BytesIO(self.file.read())
        df = pd.read_excel(file_data)
        return df
      