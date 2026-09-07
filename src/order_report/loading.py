from pathlib import Path
import pandas as pd 


def load_order_data(file_path: Path | str) -> pd.DataFrame:
    """Läser in orderdata från en CSV-fil.
    
    Kastar FileNotFoundError om filen inte existerar.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Filen kunde inte hittas på sökvägen: {path}")

    return pd.read_csv(path)
