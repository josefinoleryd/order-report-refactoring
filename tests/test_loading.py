from pathlib import Path
import pandas as pd
import pytest
from order_report.loading import load_order_data


def test_load_order_data_success(tmp_path: Path):
    test_file = tmp_path / "orders_test.csv"
    test_file.write_text("order_id,quantity\n0-1,2\n0,1\n", encoding="utf-8")

    df = load_order_data(test_file)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["order_id", "quantity"]


def test_load_order_data_file_not_found(tmp_path: Path):
    missing_file = tmp_path / "saknas.csv"

    with pytest.raises(FileNotFoundError, match="Filen kunde inte hittas"):
        load_order_data(missing_file)