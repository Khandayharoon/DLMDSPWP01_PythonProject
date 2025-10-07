import pytest
import pandas as pd
from src.base_processor import DataProcessorBase

def test_normalization():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
    base = DataProcessorBase("train", "ideal", "test", "sqlite:///:memory:")
    normalized = base.preprocess_data(df)
    assert round(normalized["A"].mean(), 5) == 0
