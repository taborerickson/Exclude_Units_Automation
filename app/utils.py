#app/utils.py 

"""  
Helper functions and PandasModel for QTableView

Utility helper functions: 
- PandasModel: maps a pandas.DataFrame to a Qt QAbstractTable for QTableView display 
- safe_filename: helper to clean filenames and append timestamps 
- format_preview: textual preview helper
"""
from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex 
import pandas as pd 
import numpy as np 
from datetime import datetime 
import re 
from pathlib import Path 

class PandasModel(QAbstractTableModel): 
    """   
    Minimal QAbstractTableModel to render a pandas DataFrame in QTableView
    Keeps UI responsive for DataFrames and displays 
    Column headers and values are in a read-only table 
    """
    def __init__(self, data: pd.DataFrame = None, parent=None): 
        super().__init__(parent) 
        # Storing a copy to avoid issues if the original df changes 
        self._data = data.copy() if data is not None else pd.DataFrame() 

    def rowCount(self, parent=QModelIndex()): 
        # Number of rows in the table (df length) 
        return len(self._data.index) 
    
    def columnCount(self, parent=QModelIndex()): 
        # Number of columns in the table (df columns) 
        return len(self._data.columns) 
    
    def data(self, index, role=QModelIndex()): 
        # Provides data for each cell when the view requests is 
        if not index.isValid(): 
            return None 
        if role == Qt.DisplayRole: 
            value = self._data.iat[index.row(), index.column()] 
            # Converts numpy types and NaNs into strings 
            if pd.isna(value): 
                return "" 
            # Converts timestamps to ISO string 
            if isinstance(value, (pd.Timestamp, datetime)): 
                return value.strftime("%Y-%m-%d") 
            return str(value) 
        return None 
    
    def headerData(self, section, orientation, role=Qt.DisplayRole): 
        # Provides header labels for columns and row numbers 
        if role != Qt.DisplayRole: 
            return None 
        if orientation == Qt.Horizontal: 
            # Column headers 
            try: 
                return str(self._data.columns[section]) 
            except Exception: 
                return None 
            
        else: 
            # Row headers (1-based index) 
            return str(section + 1) 
        
    def sort(self, column, order): 
        # If no data --> do nothing 
        if self._data.empty: 
            return 
        if column >= len(self._data.columns): 
            return 
        self.layoutAboutToBeChanged.emit() 
        self._data.sort_values(
            by=self._data.columns[column], 
            ascending=order == Qt.AscendingOrder, 
            inplace=True 
        )
        self.layoutChanged.emit() 

    # def sort(self, column, order): 
    #     # Allows sorting by column index
    #     column_name = self._data.columns[column] 
    #     ascending = order == Qt.AscendingOrder
    #     self.layoutAboutToBeChanged.emit() 
    #     self._data.sort_values(by=column_name, ascending=ascending, inplace=True) 
    #     self._data.reset_index(drop=True, inplace=True) 
    #     self.layoutChanged.emit() 


def safe_filename(original_name: str) -> str: 
    """  
    Creates a safer filename string by removing problem characters 
    Appends a timestamp to avoid overwriting 
    """
    name = Path(original_name).stem 
    # Remvoing non-alphanumeric/underscore/dash characters 
    safe_chars = re.sub(r"[^A-Za-z0-9_\-]", "_", name) 
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    return f"{safe_chars}_{stamp}" 

def format_preview(data: pd.DataFrame, max_rows: int=20) -> str: 
    """  
    Returns a short preview of the DataFrame (limited to 20 rows) 
    """
    if data is None or data.empty: 
        return "No rows flagged." 
    # Showing up to max_rows (including columns) 
    return data.head(max_rows).to_string(index=False) 
