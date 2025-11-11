import pytest
import pandas as pd
from pathlib import Path
from src.data_processing.ingestion import load_csv, load_json, load_excel, load_text

# Test with actual sample files
def test_load_csv_success():
    """Test loading real CSV file."""
    df = load_csv('data/circulation_data.csv')

    assert len(df) > 0
    assert 'transaction_id' in df.columns

def test_load_csv_file_not_found():
    """Test error handling when file doesn't exist."""
    with pytest.raises(FileNotFoundError):
        load_csv('data/nonexistent.csv')

def test_load_csv_wrong_extension():
    """Test error handling when file doesn't exist."""
    with pytest.raises(ValueError):
        load_csv('data/circulatiton_data.xlsx')

def test_load_json_success():
    """Test loading real JSON file."""
    df = load_json('data/events_data.json')

    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)

def test_load_json_missing():
    with pytest.raises(FileNotFoundError):
        df = load_json('data/events_data_incorrect.json')

def test_load_excel():
    df = load_excel('data/catalogue.xlsx')
    assert len(df) > 0
    assert isinstance(df, pd.DataFrame)

    df_bad_extension = load_excel('data/catalogue.json')
    assert df_bad_extension is None
    
    df_missing_path = load_excel('data/catalogue_incorrect.xlsx')
    assert df_missing_path is None

def test_load_text():
    df = load_text('data/feedback.txt')
    assert len(df) > 0
    assert isinstance(df, list)

    df_bad_extension = load_excel('data/catalogue.csv')
    assert df_bad_extension is None

    df_missing_path = load_excel('data/catalogue_incorrect.txt')
    assert df_missing_path is None
