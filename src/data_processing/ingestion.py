"""Data ingestion functions.

TODO: Complete these functions for the library project.
"""

import pandas as pd
import json
import logging
import os
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_csv(filepath):
    """Load CSV file with error handling.
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        DataFrame with loaded data
        
    TODO: Add error handling and logging
    """
    # TODO: Implement this function
    extension = filepath.split('.')[-1]
    if extension != 'csv':
        logger.error(f'Filepath {filepath} is not a .csv file!')
        print(f'Filepath {filepath} is not a .csv file!')
        raise ValueError(f'Filepath {filepath} is not a .csv file!')

    if not os.path.exists(filepath):
        logger.error(f'Filepath {filepath} not found!')
        raise FileNotFoundError(f'Filepath {filepath} not found')

    try:
        data = pd.read_csv(filepath)
        logger.info(f'Successfully loaded {filepath}')
        if data.empty:
            logger.error(f'{filepath} is empty')
            raise ValueError(f'{filepath} is empty')
        return data

    except Exception as e:
        error = traceback.format_exc()
        logger.error(f'Could not load {filepath}:\n{error}')
        print(f'Could not load {filepath}:\n{error}')
        raise
    

def load_json(filepath):
    """Load JSON file and flatten structure.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        DataFrame with flattened data
        
    TODO: Implement JSON loading and flattening
    """
    # TODO: Implement this function
    if not os.path.exists(filepath):
        logger.error(f'Filepath {filepath} not found')
        raise FileNotFoundError(f'Filepath {filepath} not found')
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        
            if isinstance(data, dict) and 'events' in data:
                df = pd.json_normalize(data['events'])
            else:
                df = pd.json_normalize(data)

        logger.info(f'Successfully loaded {filepath}')
        return df
    
    except Exception as e:
        error = traceback.format_exc()
        logger.error(f'Could not load {filepath}:\n{error}')
        raise
    
def load_excel(filepath):
    """Load Excel file with error handling.
    
    Args:
        filepath: Path to xlsx file
        
    Returns:
        DataFrame with loaded data
        
    TODO: Add error handling and logging
    """
    # Check if the extension is correct
    extension = filepath.split('.')[-1]
    if extension != 'xlsx':
        logger.error(f'{filepath} is not an Excel file')
        return None

    # Check if filepath exists
    if not os.path.exists(filepath):
        logger.error(f'Filepath {filepath} not found')
        return None
        # raise FileNotFoundError(f'Filepath {filepath} not found')

    # Load data
    try:
        data = pd.read_excel(filepath, sheet_name='Catalogue')
        # Check if file is empty
        if data.empty:
            logger.error(f'{filepath} is empty')
            return None
        logger.info(f'Successfully loaded {filepath}')
        return data
    # Handle exceptions
    except Exception as e:
        error = traceback.format_exc()
        logger.error(f'Could not load {filepath}:\n{error}')
        return None
  
def load_text(filepath):
    """Load Excel file with error handling.
    
    Args:
        filepath: Path to xlsx file
        
    Returns:
        DataFrame with loaded data
        
    TODO: Add error handling and logging
    """
    # Check if the extension is correct
    extension = filepath.split('.')[-1]
    if extension != 'txt':
        logger.error(f'{filepath} is not a .txt file')
        return None

    # Check if filepath exists
    if not os.path.exists(filepath):
        logger.error(f'Filepath {filepath} not found')
        return None
        raise FileNotFoundError(f'Filepath {filepath} not found')

    try:
        with open(filepath, 'rb') as file:
            data = file.readlines()
        data_cleaned = []
        for line in data:
            data_cleaned.append(line.strip().decode())
        if data_cleaned:
            logger.info(f'Successfully loaded {filepath}')
            return data_cleaned
        else:
            logger.error(f'{filepath} is empty')
            return None

    except Exception as e:
        error = traceback.format_exc()
        logger.error(f'Could not load {filepath}:\n{error}')
        return None


