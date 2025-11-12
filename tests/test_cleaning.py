"""
Add more tests
"""

# Cleaning tests
import pytest
import pandas as pd
import numpy as np
import pandas.testing as pdt
from src.data_processing.cleaning import (
    remove_duplicates,
    handle_missing_values,
    standardize_dates,
    standardise_isbn
)

# ========================================
# FIXTURES - Reusable test data
# ========================================

@pytest.fixture
def sample_df_with_duplicates():
    """Sample DataFrame with duplicate rows."""
    return pd.DataFrame({
        'id': [1, 2, 2, 3, 3, 3],
        'name': ['Alice', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie'],
        'value': [10, 20, 20, 30, 30, 30]
    })

@pytest.fixture
def sample_df_with_missing():
    """Sample DataFrame with missing values."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4],
        'name': ['Alice', None, 'Charlie', 'David'],
        'value': [10, 20, None, 40]
    })

@pytest.fixture
def sample_df_with_dates():
    """Sample data frame with date column."""
    return pd.DataFrame({
        'id': [1,2,3,4],
        'date': ['2025-10-01', '2025-11-01', '2025-12-01', '2026-01-01']
    })

@pytest.fixture
def sample_with_isbn():
    return pd.DataFrame({
        'id': [1,2,3],
        'isbn': ['978-01-155-42290-0', '978-02-521-1248-7', '978-01-151-5389-2']
    })

# ========================================
# TESTS FOR remove_duplicates()
# ========================================

def test_remove_duplicates_exact(sample_df_with_duplicates):
    """Test duplicate removal using exact DataFrame comparison."""
    result = remove_duplicates(sample_df_with_duplicates, subset=['id'])

    expected = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['Alice', 'Bob', 'Charlie'],
        'value': [10, 20, 30]
    })

    # Reset index for comparison
    result = result.reset_index(drop=True)

    pdt.assert_frame_equal(result, expected)

def test_remove_duplicates_properties(sample_df_with_duplicates):
    """Test duplicate removal using property assertions."""
    result = remove_duplicates(sample_df_with_duplicates, subset=['id'])

    # Test properties instead of exact values
    assert len(result) == 3
    assert result['id'].is_unique
    assert set(result['id']) == {1, 2, 3}

def test_remove_duplicates_no_changes():
    """Test with DataFrame that has no duplicates."""
    df_unique = pd.DataFrame({
        'id': [1, 2, 3],
        'name': ['A', 'B', 'C']
    })

    result = remove_duplicates(df_unique, subset=['id'])

    pdt.assert_frame_equal(result, df_unique)

def test_remove_duplicates_empty():
    """Test with empty DataFrame."""
    empty_df = pd.DataFrame({'id': [], 'name': []})
    result = remove_duplicates(empty_df)

    assert len(result) == 0
    pdt.assert_frame_equal(result, empty_df)

# ========================================
# TESTS FOR handle_missing_values()
# ========================================

def test_handle_missing_drop(sample_df_with_missing):
    """Test dropping rows with missing values."""
    result = handle_missing_values(sample_df_with_missing, strategy='drop')

    # Should only have rows without any NaN
    assert len(result) == 2
    assert result['name'].notna().all()
    assert result['value'].notna().all()

def test_handle_missing_fill(sample_df_with_missing):
    """Test filling missing values."""
    result = handle_missing_values(
        sample_df_with_missing, 
        strategy='fill', 
        fill_value=0
    )

    # Should have all 4 rows
    assert len(result) == 4
    # No missing values
    assert result['name'].notna().all() or (result['name'] == 0).any()
    assert result['value'].notna().all()

def test_handle_missing_invalid_strategy(sample_df_with_missing):
    """Test that invalid strategy raises error."""
    with pytest.raises(ValueError, match="Unknown strategy"):
        handle_missing_values(sample_df_with_missing, strategy='invalid')

# ========================================
# TESTS FOR standardize_dates()
# ========================================

def test_standardize_dates(sample_df_with_dates):
    result = standardize_dates(sample_df_with_dates, date_columns='date')
    dates = [np.datetime64(date) for date in ['2025-10-01', '2025-11-01', '2025-12-01', '2026-01-01']]
    expected = pd.DataFrame({
        'id': [1,2,3,4],
        'date': dates
    })
    pdt.assert_frame_equal(result, expected)

# ========================================
# TESTS FOR standardize_isbn()
# ========================================

def test_standardise_isbn(sample_with_isbn):
    result = standardise_isbn(sample_with_isbn, 'isbn')
    expected = pd.DataFrame({
        'id': [1,2,3],
        'isbn': ['97801155422900', '9780252112487', '9780115153892']

    })