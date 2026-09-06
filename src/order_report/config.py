from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class ReportConfig:
    """Sökvägar som behövs för att skapa rapporterna."""
    input_path: Path = Path("data/orders.csv")
    output_dir: Path = Path("output")

    @property
    def overview_path(self) -> Path:
        return self.output_dir / "overview.csv"

    @property
    def sales_by_category_path(self) -> Path:
        return self.output_dir / "sales_by_category.csv"

    @property
    def sales_by_region_path(self) -> Path:
        return self.output_dir / "sales_by_region.csv"

    @property
    def returns_by_category_path(self) -> Path:
        return self.output_dir / "returns_by_category.csv"