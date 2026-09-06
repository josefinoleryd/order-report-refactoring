import pandas as pd
from order_report.processing import clean_order_data

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
    assert result.loc[1, "unit_price"] == 10.0  # Medianen av [10.0] är 10.0
    assert result.loc[1, "discount"] == 0.0

    # Kontrollera boolesk flagga
    assert result.loc[0, "returned"] is True or result.loc[0, "returned"] == True
    assert result.loc[1, "returned"] is False or result.loc[1, "returned"] == False