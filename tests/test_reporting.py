from pathlib import Path
import pandas as pd
from order_report.config import ReportConfig
from order_report.reporting import save_all_reports, save_report


def test_save_report_creates_directory_and_file(tmp_path: Path):
    target_file = tmp_path / "nested_dir" / "report.csv"
    data = pd.DataFrame({"col_a": [1, 2], "col_b": ["x", "y"]})

    save_report(data, target_file)

    assert target_file.exists()
    loaded_data = pd.read_csv(target_file)
    assert len(loaded_data) == 2
    assert list(loaded_data.columns) == ["col_a", "col_b"]


def test_save_all_reports_generates_all_four_files(tmp_path: Path):
    test_config = ReportConfig(output_dir=tmp_path / "reports")
    dummy_df = pd.DataFrame({"sample": [1]})

    save_all_reports(
        overview=dummy_df,
        sales_by_category=dummy_df,
        sales_by_region=dummy_df,
        returns_by_category=dummy_df,
        config=test_config,
    )

    assert test_config.overview_path.exists()
    assert test_config.sales_by_category_path.exists()
    assert test_config.sales_by_region_path.exists()
    assert test_config.returns_by_category_path.exists()