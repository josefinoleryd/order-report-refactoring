import logging
import pandas as pd

logger = logging.getLogger(__name__)


def clean_order_data(df: pd.DataFrame) -> pd.DataFrame:
    """Rensar och standardiserar kolumnerna i orderdatan samt rapporterar avvikelser."""
    cleaned = df.copy()

    # 1. Kontrollera och standardisera textkolumner
    for col in ["region", "product_category"]:
        missing_text = cleaned[col].isna().sum()
        if missing_text > 0:
            logger.warning("Upptäckte %d saknade värden i '%s'. Ersätts med 'Unknown'.", missing_text, col)

        cleaned[col] = (
            cleaned[col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
            .str.title()
        )

    # 2. Konvertera och rapportera numeriska kolumner
    # Quantity
    raw_quantity = pd.to_numeric(cleaned["quantity"], errors="coerce")
    missing_qty = raw_quantity.isna().sum()
    if missing_qty > 0:
        logger.warning("Upptäckte %d ogiltiga eller saknade värden i 'quantity'. Ersätts med 1.", missing_qty)
    
    negative_qty = (raw_quantity < 0).sum()
    if negative_qty > 0:
        logger.warning("Upptäckte %d rader med orimligt/negativt värde i 'quantity'.", negative_qty)
    
    cleaned["quantity"] = raw_quantity.fillna(1)
    
    # Unit price
    raw_price = pd.to_numeric(cleaned["unit_price"], errors="coerce")
    missing_price = raw_price.isna().sum()
    median_price = raw_price.median()
    
    if missing_price > 0:
        logger.warning(
            "Upptäckte %d ogiltiga eller saknade värden i 'unit_price'. Ersätts med median (%.2f).",
            missing_price,
            median_price,
        )
    
    negative_price = (raw_price < 0).sum()
    if negative_price > 0:
        logger.warning("Upptäckte %d rader med orimligt/negativt värde i 'unit_price'.", negative_price)
    
    cleaned["unit_price"] = raw_price.fillna(median_price)
    
    # Discount
    raw_discount = pd.to_numeric(cleaned["discount"], errors="coerce")
    missing_discount = raw_discount.isna().sum()
    if missing_discount > 0:
        logger.warning("Upptäckte %d ogiltiga eller saknade värden i 'discount'. Ersätts med 0.0.", missing_discount)
    
    invalid_discount_range = ((raw_discount < 0) | (raw_discount > 1)).sum()
    if invalid_discount_range > 0:
        logger.warning("Upptäckte %d rader med orimlig rabattsats (utanför intervallet 0.0 till 1.0).", invalid_discount_range)
    
    cleaned["discount"] = raw_discount.fillna(0.0)
    
    # 3. Tolka returstatus som booleskt värde
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

def aggregate_sales_by_dimension(df: pd.DataFrame, group_by_col: str) -> pd.DataFrame:
    """Aggregerar försäljning, unika ordrar och returgrad per vald kolumn."""
    summary = (
        df.groupby(group_by_col, as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            total_sales=("discounted_value", "sum"),
            returns=("returned", "sum")
        )
    )

    summary["total_sales"] = summary["total_sales"].round(2)
    summary["return_rate"] = (summary["returns"] / summary["order_count"]).round(3)

    return summary.sort_values("total_sales", ascending=False).reset_index(drop=True)

def aggregate_sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return aggregate_sales_by_dimension(df, group_by_col="product_category")

def aggregate_sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    return aggregate_sales_by_dimension(df, group_by_col="region")

def aggregate_returns_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregerar antal ordrar, returer och returgrad per produktkategori."""
    summary = (
        df.groupby("product_category", as_index=False)
        .agg(
            order_count=("order_id", "nunique"),
            returns=("returned", "sum")
        )
    )

    summary["return_rate"] = (summary["returns"] / summary["order_count"]).round(3)

    return summary.sort_values("return_rate", ascending=False).reset_index(drop=True)