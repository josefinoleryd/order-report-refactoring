import pandas as pd

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "customer_id",
    "region",
    "product_category",
    "quantity",
    "unit_price",
    "discount",
    "returned"
}

def validate_order_data(df: pd.DataFrame) -> pd.DataFrame:
    """Validerar att indata innehåller nödvändiga kolumner och inte är tom."""
    if df.empty:
        raise ValueError("Indata är tom.")

    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Saknade kolumner: {missing}")

    return df