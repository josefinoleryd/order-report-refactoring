import pandas as pd

def clean_order_data(df: pd.DataFrame) -> pd.DataFrame:
    """Rensar och standardiserar kolumnerna i orderdatan."""
    cleaned = df.copy()

    # Standardisera textkolumner
    for col in ["region", "product_category"]:
        cleaned[col] = (
            cleaned[col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

    # Konvertera numeriska kolumner och hantera saknade värden
    cleaned["quantity"] = (
        pd.to_numeric(cleaned["quantity"], errors="coerce")
        .fillna(1)
    )

    cleaned["unit_price"] = pd.to_numeric(
        cleaned["unit_price"], errors="coerce"
    )
    median_price = cleaned["unit_price"].median()
    cleaned["unit_price"] = cleaned["unit_price"].fillna(median_price)

    cleaned["discount"] = (
        pd.to_numeric(cleaned["discount"], errors="coerce")
        .fillna(0.0)
    )

    # Tolka returstatus som booleskt värde
    truthy_values = {"true", "yes", "1", "ja"}
    cleaned["returned"] = (
        cleaned["returned"]
        .fillna("false")
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(truthy_values)
    )

    return cleaned

def calculate_order_values(df: pd.DataFrame) -> pd.DataFrame:
    """Beräknar order_value och discounted_value för varje rad."""
    processed = df.copy()
    processed["order_value"] = processed["quantity"] * processed["unit_price"]
    processed["discounted_value"] = processed["order_value"] * (1 - processed["discount"])

    return processed

def create_overview_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Sammanställer övergripande nyckeltal för hela datasetet."""
    total_sales = round(df["discounted_value"].sum(), 2)
    number_of_orders = df["order_id"].nunique()
    number_of_returns = int(df["returned"].sum())

    return pd.DataFrame(
        {
            "metric": [
                "total_sales",
                "order_count",
                "return_count"
            ],
            "value": [
                total_sales,
                number_of_orders,
                number_of_returns
            ]
        }
    )