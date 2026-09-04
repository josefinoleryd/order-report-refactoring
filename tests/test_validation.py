import pandas as pd
import pytest
from order_report.validation import validate_order_data 

VALID_DATA = {
    "order_id": [1],
    "order_date": ["2026-01-01"],
    "customer_id": [10],
    "region": ["North"],
    "product_category": ["Electronics"],
    "quantity": [2],
    "unit_price": [100.0],
    "discount": [0.0],
    "returned": [False]
}

def test_validate_order_data_success():
    """Giltig data ska passera utan fel."""
    df = pd.DataFrame(VALID_DATA)
    result = validate_order_data(df)
    assert result.equals(df)


EMPTY_DF = pd.DataFrame()
MISSING_COLS_DF = pd.DataFrame({"order_id": [1], "quantity": [2]})

@pytest.mark.parametrize(
    "invalid_df, expected_error_msg",
    [
        (EMPTY_DF, "Indata är tom."),
        (MISSING_COLS_DF, "Saknade kolumner:"),
    ],
)

def test_validate_order_data_errors(invalid_df, expected_error_msg):
    """Både tom DataFrame och saknade kolumner ska kasta ValueError."""
    with pytest.raises(ValueError, match=expected_error_msg):
        validate_order_data(invalid_df)