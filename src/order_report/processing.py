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