import pandas as pd
import pytest
from order_report.processing import (
    clean_order_data, 
    calculate_order_values,
    create_overview_metrics,
    aggregate_sales_by_category,
    aggregate_sales_by_region
)

def test_clean_order_data_cleans_and_imputes_correctly():
    raw_data = pd.DataFrame(
        {
            "region": [" north ", None],
            "product_category": ["books", "TOYS "],
            "quantity": ["2", None],
            "unit_price": [10.0, None],
            "discount": [0.1, None],
            "returned": ["Ja", "no"]
        }
    )

    result = clean_order_data(raw_data)

    # Kontrollera textformatering
    assert result.loc[0, "region"] == "North"
    assert result.loc[1, "region"] == "Unknown"
    assert result.loc[1, "product_category"] == "Toys"

    # Kontrollera numeriska värden & defaults/median
    assert result.loc[1, "quantity"] == 1
    assert result.loc[1, "unit_price"] == pytest.approx(10.0)
    assert result.loc[1, "discount"] == pytest.approx(0.0)

    # Kontrollera boolesk flagga
    assert bool(result.loc[0, "returned"]) is True
    assert bool(result.loc[1, "returned"]) is False

def test_calculate_order_values():
    sample_data = pd.DataFrame(
        {
            "quantity": [2, 1],
            "unit_price": [100.0, 50.0],
            "discount": [0.1, 0.0]
        }
    )

    result = calculate_order_values(sample_data)

    assert result.loc[0, "order_value"] == pytest.approx(200.0)
    assert result.loc[0, "discounted_value"] == pytest.approx(180.0)

    assert result.loc[1, "order_value"] == pytest.approx(50.0)
    assert result.loc[1, "discounted_value"] == pytest.approx(50.0)

def test_create_overview_metrics():
    sample_data = pd.DataFrame(
        {
            "order_id": ["0-100", "0-100", "0-101"],
            "discounted_value": [100.50, 49.50, 50.00],
            "returned": [True, False, True]
        }
    )

    overview = create_overview_metrics(sample_data)

    assert list(overview.columns) == ["metric", "value"]

    metrics = dict(zip(overview["metric"], overview["value"]))
    assert metrics["total_sales"] == pytest.approx(200.00)
    assert metrics["order_count"] == 2
    assert metrics["return_count"] == 2

@pytest.fixture
def sales_sample_data():
    """Gemensam testdata för både kategori- och regiontester."""
    return pd.DataFrame(
        {
            "product_category": ["Books", "Books", "Toys"],
            "region": ["North", "North", "South"],
            "order_id": ["0-1", "0-1", "0-2"],
            "discounted_value": [50.0, 50.0, 200.0],
            "returned": [True, False, False]
        }
    )

def test_aggregate_sales_by_category(sales_sample_data):
    result = aggregate_sales_by_category(sales_sample_data)

    assert result.loc[0, "product_category"] == "Toys"
    assert result.loc[0, "order_count"] == 1
    assert result.loc[0, "total_sales"] == pytest.approx(200.0)
    assert result.loc[0, "returns"] == 0
    assert result.loc[0, "return_rate"] == pytest.approx(0.0)

    assert result.loc[1, "product_category"] == "Books"
    assert result.loc[1, "order_count"] == 1
    assert result.loc[1, "total_sales"] == pytest.approx(100.0)
    assert result.loc[1, "returns"] == 1
    assert result.loc[1, "return_rate"] == pytest.approx(1.0)

def test_aggregate_sales_by_region(sales_sample_data):
    result = aggregate_sales_by_region(sales_sample_data)

    assert result.loc[0, "region"] == "South"
    assert result.loc[0, "order_count"] == 1
    assert result.loc[0, "total_sales"] == pytest.approx(200.0)
    assert result.loc[0, "returns"] == 0
    assert result.loc[0, "return_rate"] == pytest.approx(0.0)

    assert result.loc[1, "region"] == "North"
    assert result.loc[1, "order_count"] == 1
    assert result.loc[1, "total_sales"] == pytest.approx(100.0)
    assert result.loc[1, "returns"] == 1
    assert result.loc[1, "return_rate"] == pytest.approx(1.0)