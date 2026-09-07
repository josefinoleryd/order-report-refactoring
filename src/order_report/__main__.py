import logging
import sys
from order_report.config import ReportConfig
from order_report.loading import load_order_data
from order_report.processing import (
    aggregate_returns_by_category,
    aggregate_sales_by_category,
    aggregate_sales_by_region,
    calculate_order_values,
    clean_order_data,
    create_overview_metrics
)
from order_report.reporting import save_all_reports
from order_report.validation import validate_order_data

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    """Konfigurerar programmet loggning centralt."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def run_pipeline(config: ReportConfig) -> None:
    """Orkestrerar hela dataflödet från inläsning till export."""
    logger.info("Startar orderrapport med indata: %s", config.input_path)

    raw_data = load_order_data(config.input_path)
    logger.info("Läste in %d rader från datafilen", len(raw_data))

    validate_order_data(raw_data)
    logger.info("Validering genomförd utan anmärkningar.")

    cleaned_data = clean_order_data(raw_data)
    processed_data = calculate_order_values(cleaned_data)

    overview = create_overview_metrics(processed_data)
    sales_by_cat = aggregate_sales_by_category(processed_data)
    sales_by_region = aggregate_sales_by_region(processed_data)
    returns_by_cat = aggregate_returns_by_category(processed_data)

    save_all_reports(
        overview=overview,
        sales_by_category=sales_by_cat,
        sales_by_region=sales_by_region,
        returns_by_category=returns_by_cat,
        config=config
    )
    logger.info("Samtliga rapporter sparade i katalogen: %s", config.output_dir)


def main() -> None:
    """Startpunkt för programmet med specifik felhantering."""
    setup_logging()
    config = ReportConfig()

    try:
        run_pipeline(config)
        logger.info("Körning slutförd!")
    except (FileNotFoundError, ValueError) as err:
        logger.error("Körningen misslyckades: %s", err)
        sys.exit(1)


if __name__ == "__main__":
    main()
