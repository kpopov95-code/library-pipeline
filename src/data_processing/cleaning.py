import pandas as pd
import logging
from typing import List, Optional
import numpy as np

logger = logging.getLogger(__name__)

def remove_duplicates(df, subset=None):
    """Remove duplicate rows from DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame
        subset (list, optional): Columns to consider for duplicates

    Returns:
        pd.DataFrame: DataFrame with duplicates removed

    Example:
        >>> df_clean = remove_duplicates(df, subset=['transaction_id'])
    """
    df = df.copy()  # Work on a copy!

    initial_rows = len(df)
    df = df.drop_duplicates(subset=subset, keep='first')
    removed = initial_rows - len(df)

    if removed > 0:
        logger.info(f"Removed {removed} duplicate rows")

    return df

def handle_missing_values(df, strategy='drop', fill_value=None, columns=None):
    """Handle missing values in DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame
        strategy (str): 'drop', 'fill', or 'forward_fill'
        fill_value: Value to fill if strategy='fill'
        columns (list, optional): Specific columns to handle

    Returns:
        pd.DataFrame: DataFrame with missing values handled

    Example:
        >>> df_clean = handle_missing_values(df, strategy='drop')
        >>> df_filled = handle_missing_values(df, strategy='fill', fill_value=0)
    """
    df = df.copy()

    if columns:
        target_cols = columns
    else:
        target_cols = df.columns

    initial_rows = len(df)

    if strategy == 'drop':
        df = df.dropna(subset=target_cols)
        logger.info(f"Dropped {initial_rows - len(df)} rows with missing values")

    elif strategy == 'fill':
        if fill_value is None:
            raise ValueError("fill_value must be provided when strategy='fill'")
        df[target_cols] = df[target_cols].fillna(fill_value)
        logger.info(f"Filled missing values with {fill_value}")

    elif strategy == 'forward_fill':
        df[target_cols] = df[target_cols].fillna(method='ffill')
        logger.info("Forward filled missing values")

    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    return df

def standardize_dates(df, date_columns, date_format='%Y-%m-%d'):
    """Standardize date columns to consistent format.

    Args:
        df (pd.DataFrame): Input DataFrame
        date_columns (list): Column names containing dates
        date_format (str): Target date format

    Returns:
        pd.DataFrame: DataFrame with standardized dates

    Example:
        >>> df_clean = standardize_dates(df, ['checkout_date', 'return_date'])
    """
    df = df.copy()

    if isinstance(date_columns, str):
        date_columns = [date_columns]
    elif not isinstance(date_columns, list) and not isinstance(date_columns, np.ndarray):
        logger.error(f'date_columns is of type {type(date_columns)}, please enter a list')
        raise ValueError(f'date_columns is of type {type(date_columns)}, please enter a list')

    for col in date_columns:
        if col not in df.columns:
            logger.warning(f"Column {col} not found in DataFrame")
            continue

        try:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
            logger.info(f"Standardized dates in column: {col}")
        except Exception as e:
            logger.error(f"Error standardizing dates in {col}: {e}")
            return

    return df

def standardise_isbn(df, column='ISBN'):
    """Standardize ISBN column to consistent format.
    Removes hyphens from the string entries and returns
    one long number in string format.

    Args:
        df (pd.DataFrame): Input DataFrame
        column (str) (Optional): Column names containing dates

    Returns:
        pd.DataFrame: DataFrame with standardized ISBN values
    """

    df = df.copy()
    if column not in df:
        logger.error(f'WARNING: Column {column} not in the data frame.')
        raise ValueError(f'No column name {column} found in the data frame')
    try:
        df[column] = df[column].astype(str)
        df[column] = df[column].str.replace('-', '')
        logger.info(f'Successfully standardised column {column}')
    except Exception as e:
        error = traceback.format_exc()
        logger.error(f'Error when standardising data:\{error}')
        return

    return df

