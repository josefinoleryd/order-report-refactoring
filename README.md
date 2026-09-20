# Individuell inlämningsuppgift – Refaktorera ett Pythonprogram för orderrapportering

Det här projektet är en refaktorering av ett befintligt skript som bearbetar orderdata från en e-handel och genererar rapporter över försäljning och returer. 

Målet har varit att ta ett program där all kod låg i en enda fil och dela upp det i moduler med tydliga ansvarsområden, centraliserad logging, defensiv validering, typannoteringar och automatiserade enhetstester. Beräkningsresultaten och nyckeltalen i rapporterna är helt bevarade mot originalet.

## Installation och hur man kör

### Förutsättningar
* Python-version: `>=3.10` (utvecklat och testat på Python 3.13)

### Installation
1. Klona repot från GitHub:
   ```bash
   git clone https://github.com/josefinoleryd/order-report-refactoring.git
   cd order-report-refactoring
   ```
2. Skapa och aktivera en virtuell miljö:
    ```bash
    python -m venv .venv
    # På Windows:
    .venv\Scripts\activate
    # På macOS/Linux:
    source .venv/bin/activate
    ```
3. Installera projektet som ett redigerbart paket inklusive testberoenden:
    ```bash
    pip install -e ".[test]"
    ```

### Så kör du programmet 

Starta pipelinen från projektets rotkatalog:

```bash
python -m order_report
```

Programmet läser in data från ```data/orders.csv```, validerar strukturen, tvättar och standardiserar fält, beräknar ordervärden och sparar fyra CSV-rapporter i katalogen ```output/```.

### Så kör du testerna

Kör samtliga enhetstester med pytest:

```bash
pytest -v
```

## Projektstruktur

```
order-report-refactoring/
├── data/
│   └── orders.csv               # Indata med råa orderrader
├── output/                      # Genererade CSV-rapporter
├── output_baseline/             # Ursprungliga rapporter sparade som facit för jämförelse
├── src/
│   └── order_report/
│       ├── __init__.py          # Paketmarkör
│       ├── __main__.py          # Startpunkt för terminalkörning, orkestrering och central logging
│       ├── config.py            # ReportConfig (dataclass för sökvägar)
│       ├── loading.py           # Inläsning av CSV med felhantering
│       ├── processing.py        # Ren datatvätt, rapportering av avvikelser och beräkningar
│       ├── reporting.py         # Skrivning av rapporter till disk (skapar mappar vid behov)
│       └── validation.py        # Strukturell schemavalidering av obligatoriska kolumner
├── tests/
│   ├── test_loading.py          # Tester för filinläsning och felaktiga sökvägar
│   ├── test_processing.py       # Tester för datatvätt, immutabilitet och aggregeringslogik
│   ├── test_reporting.py        # Tester för rapportgenerering med tmp_path
│   └── test_validation.py       # Tester för saknade kolumner och tomma filer
├── code_review.md               # Granskning av originalkoden (observation, konsekvens, förslag)
├── legacy_order_report.py       # Ursprungligt skript före refaktorering
├── pyproject.toml               # Projektkonfiguration, byggsystem och beroenden
└── README.md                    # Projekt- och körinstruktioner
```

## Teknikstack och beroenden 

- Programmeringsspråk: Python
- Datahantering och aggregering: pandas
- Testramverk: pytest
- Byggsystem: setuptools 
- Versionshantering: Git och GitHub