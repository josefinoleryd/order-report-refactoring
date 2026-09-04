from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ReportConfig:
    """Sökvägar som behövs för att skapa rapporterna."""

    # Indatafil och utdatamapp
    input_path: Path = Path("data/orders.csv")
    output_dir: Path = Path("output")

    # Rapportfiler som ska genereras
    overview_path: Path = Path("output/overview.csv")
    sales_by_category_path: Path = Path("output/sales_by_category.csv")
    sales_by_region_path: Path = Path("output/sales_by_region.csv")
    returns_by_category_path: Path = Path("output/returns_by_category.csv")