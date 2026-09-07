from pathlib import Path
import pandas as pd
from order_report.config import ReportConfig

def save_report(df: pd.DataFrame, file_path: Path) -> None:
    """Sparar en DataFrame till angiven CSV-fil och skapar målmappen om den saknas."""
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=False)


def save_all_reports(
        overview: pd.DataFrame,
        sales_by_category: pd.DataFrame,
        sales_by_region: pd.DataFrame,
        returns_by_category: pd.DataFrame,
        config: ReportConfig
) -> None:
    """Sparar samtliga fyra rapporter till de sökvägar som anges i konfigurationen."""
    save_report(overview, config.overview_path)
    save_report(sales_by_category, config.sales_by_category_path)
    save_report(sales_by_region, config.sales_by_region_path)
    save_report(returns_by_category, config.returns_by_category_path)