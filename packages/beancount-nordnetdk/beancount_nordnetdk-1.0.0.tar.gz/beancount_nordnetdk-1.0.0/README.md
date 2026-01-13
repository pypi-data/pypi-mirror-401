# Beancount Nordnet DK Importer

`beancount-nordnetdk` provides an importer for converting CSV exports of [Nordnet](https://www.nordnet.dk) transaction summaries to the [Beancount](http://furius.ca/beancount/) format.

## Installation

```sh
$ pip install beancount-nordnetdk
```

In case you prefer installing from the Github repository, please note that `main` is the development branch so `stable` is what you should be installing from.

## Usage

If you're not familiar with how to import external data into Beancount, please read [this guide](https://beancount.github.io/docs/importing_external_data.html) first.

### Beancount 3.x

Beancount 3.x has replaced the `config.py` file based workflow in favor of having a script based workflow, as per the [changes documented here](https://docs.google.com/document/d/1O42HgYQBQEna6YpobTqszSgTGnbRX7RdjmzR2xumfjs/edit#heading=h.hjzt0c6v8pfs). The `beangulp` examples suggest using a Python script based on `beangulp.Ingest`. Here's an example of how that might work:

Add an `import.py` script in your project root with the following contents:

```python
from beancount_nordnetdk import NordnetDKImporter
from beangulp import Ingest

importers = (
    NordnetDKImporter(
        depot_accounts={
            "12345678": "Assets:Nordnet:Account1",
            "23456789": "Assets:Nordnet:Account2",
            "34567890": "Assets:Nordnet:Account3",
        },
        currency="DKK",
        stock_account="Assets:Nordnet:Stocks",
        fees_account="Expenses:Investments:Fees",
        dividend_account="Income:Investments:Dividends",
        tax_account="Expenses:Investments:Tax",
        interest_account="Income:Investments:Interest",
    ),
)

if __name__ == "__main__":
    ingest = Ingest(importers)
    ingest()
```

... and run it directly using `python import.py extract`.

### Beancount 2.x

Adjust your [config file](https://beancount.github.io/docs/importing_external_data.html#configuration) to include `NordnetDKImporter`.

Add the following to your `config.py`:

```python
from beancount_nordnetdk import NordnetDKImporter

CONFIG = [
    NordnetDKImporter(
        depot_accounts={
            "12345678": "Assets:Nordnet:Account1",
            "23456789": "Assets:Nordnet:Account2",
        },
        currency="DKK",
        stock_account="Assets:Nordnet:Stocks",
        fees_account="Expenses:Investments:Fees",
        dividend_account="Income:Investments:Dividends",
        tax_account="Expenses:Investments:Tax",
        interest_account="Income:Investments:Interest",
    ),
]
```

Once this is in place, you should be able to run `bean-extract` on the command line to extract the transactions and pipe all of them into your Beancount file.

```sh
$ bean-extract /path/to/config.py transactions-and-notes-export.csv >> you.beancount
```

## CSV Format

The importer expects Nordnet CSV exports with the following characteristics:

- **Filename**: `transactions-and-notes-export.csv`
- **Encoding**: UTF-16
- **Separator**: Tab (`\t`)
- **Header row**: Present

### Key columns:

- **Id** - 10 digit transaction ID
- **Bogføringsdag** - Posting date (yyyy-mm-dd)
- **Handelsdag** - Trade date (yyyy-mm-dd)
- **Valørdag** - Value date (yyyy-mm-dd)
- **Depot** - Account number (8 digits)
- **Transaktionstype** - Transaction type
- **Værdipapirer** - Security name
- **ISIN** - ISIN identifier
- **Antal** - Quantity
- **Kurs** - Price
- **Samlede afgifter** - Total fees
- **Beløb** - Amount
- **Valuta** - Currency
- **Saldo** - Account balance
- **Transaktionstekst** - Transaction text
- **Kurtage** - Brokerage

## Contributing

Contributions are most welcome!

Please make sure you have Python 3.11+ and [uv](https://docs.astral.sh/uv/) installed.

1. Clone the repository: `git clone https://github.com/joandrsn/beancount-nordnetdk`
2. Install the packages required for development: `uv sync --dev`
3. That's basically it. You should now be able to run the test suite: `uv run pytest`.