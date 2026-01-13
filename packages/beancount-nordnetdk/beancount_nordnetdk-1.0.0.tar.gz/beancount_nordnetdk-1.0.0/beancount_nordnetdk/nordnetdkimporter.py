"""Importer for Nordnet CSV files."""

import re
from os import path
from decimal import Decimal
from beancount.core import data, amount
from beancount.core.number import D
from beangulp.importers import csvbase


class NordnetDKImporter(csvbase.Importer):
    """Importer for Nordnet CSV exports.

    CSV Format:
    - Header row present
    - UTF-16 encoding
    - Tab (\t) separated
    - Filename: "transactions-and-notes-export.csv"

    Key columns:
    - Id: 10 digit transaction ID
    - Bogføringsdag: Posting date (yyyy-mm-dd)
    - Handelsdag: Trade date (yyyy-mm-dd)
    - Valørdag: Value date (yyyy-mm-dd)
    - Depot: Account number (8 digits)
    - Transaktionstype: Transaction type
    - Værdipapirer: Security name
    - ISIN: ISIN identifier
    - Antal: Quantity
    - Kurs: Price
    - Beløb: Amount
    - Valuta: Currency
    - Saldo: Account balance
    - Transaktionstekst: Transaction text
    """

    # CSV file settings
    encoding = "utf-16"
    names = True  # Has header row
    header = 0
    footer = 0

    class NordnetDialect(csvbase.csv.Dialect):
        """CSV dialect for Nordnet files."""

        delimiter = "\t"
        quotechar = '"'
        doublequote = True
        skipinitialspace = False
        lineterminator = "\r\n"
        quoting = csvbase.csv.QUOTE_MINIMAL

    dialect = NordnetDialect

    # Column definitions
    # Nordic CSV format uses comma as decimal separator
    _amount_subs = {r"\.": "", r",": "."}

    transaction_id = csvbase.Column("Id")
    date = csvbase.Date("Bogføringsdag", "%Y-%m-%d")
    trade_date = csvbase.Date("Handelsdag", "%Y-%m-%d")
    value_date = csvbase.Date("Valørdag", "%Y-%m-%d")
    depot = csvbase.Column("Depot")
    transaction_type = csvbase.Column("Transaktionstype")
    security = csvbase.Column("Værdipapirer", default="")
    isin = csvbase.Column("ISIN", default="")
    quantity = csvbase.Amount("Antal", subs=_amount_subs)
    price = csvbase.Amount("Kurs", subs=_amount_subs)
    fees = csvbase.Amount("Samlede afgifter", subs=_amount_subs)
    amount = csvbase.Amount("Beløb", subs=_amount_subs)
    # The CSV has multiple "Valuta" columns; use column index 14 (0-based) for the Beløb currency
    currency = csvbase.Column(14)  # Currency column right after Beløb
    balance = csvbase.Amount("Saldo", subs=_amount_subs)
    transaction_text = csvbase.Column("Transaktionstekst", default="")
    brokerage = csvbase.Amount("Kurtage", subs=_amount_subs)
    narration = csvbase.Column("Transaktionstype", default="")

    def __init__(
        self,
        depot_accounts,
        currency="DKK",
        flag="*",
        stock_account=None,
        fees_account=None,
        dividend_account=None,
        tax_account=None,
        interest_account=None,
    ):
        """Initialize the Nordnet importer.

        Args:
            depot_accounts: Dict mapping depot numbers to cash account names
                           (e.g., {"12345678": "Assets:Nordnet:Depot1:Cash"})
            currency: The default currency (default: DKK)
            flag: The default flag for transactions (default: *)
            stock_account: Account for stock positions
            fees_account: Account for brokerage fees
            dividend_account: Account for dividend income
            tax_account: Account for taxes
            interest_account: Account for interest income
        """
        # Validate required parameters
        if not depot_accounts:
            raise ValueError("depot_accounts mapping cannot be empty")

        required_accounts = {
            "stock_account": stock_account,
            "fees_account": fees_account,
            "dividend_account": dividend_account,
            "tax_account": tax_account,
            "interest_account": interest_account,
        }

        missing = [name for name, value in required_accounts.items() if value is None]
        if missing:
            raise ValueError(
                f"Missing required account parameters: {', '.join(missing)}. "
                f"All account parameters must be provided."
            )

        # Pass first depot account to base class or None
        base_account = next(iter(depot_accounts.values())) if depot_accounts else None
        super().__init__(base_account, currency, flag)
        self.depot_accounts = depot_accounts
        self.stock_account = stock_account
        self.fees_account = fees_account
        self.dividend_account = dividend_account
        self.tax_account = tax_account
        self.interest_account = interest_account

    def identify(self, filepath):
        """Identify if a file is a Nordnet CSV export.

        Args:
            filepath: Path to the file to identify

        Returns:
            True if the file is a Nordnet CSV containing transactions for any depot in depot_accounts
        """
        import csv

        # Check if filename matches expected pattern
        filename = path.basename(filepath).lower()
        if "transactions-and-notes-export" not in filename or not filename.endswith(
            ".csv"
        ):
            return False

        # Verify it's actually a Nordnet CSV with the correct structure
        try:
            with open(filepath, encoding="utf-16") as fd:
                reader = csv.DictReader(fd, delimiter="\t")

                # Check if file contains at least one transaction for any of our depots
                for row in reader:
                    depot = row.get("Depot", "").strip()
                    if depot in self.depot_accounts:
                        return True

        except (UnicodeDecodeError, IOError, csv.Error):
            return False

        return False

    def filename(self, filepath):
        """Generate a standardized filename for the imported file.

        Args:
            filepath: Original file path

        Returns:
            Standardized filename
        """
        return "nordnet." + path.basename(filepath)

    def finalize(self, txn, row):
        """Post-process the transaction to handle Nordnet-specific logic.

        This method handles different transaction types and creates
        appropriate postings for each.

        Args:
            txn: The transaction object
            row: The CSV row data

        Returns:
            Modified transaction or None to skip
        """
        if txn is None:
            return None

        trans_type = row.transaction_type.strip()
        postings = list(txn.postings)
        payee = None
        narration = trans_type

        # Get the cash account for this depot from mapping
        if row.depot not in self.depot_accounts:
            # Skip transactions for depots not in our mapping
            return None
        cash_account = self.depot_accounts[row.depot]

        # Build narration
        if row.security:
            narration = f"{trans_type} - {row.security}"
            payee = row.security
        elif row.transaction_text:
            narration = f"{trans_type} - {row.transaction_text}"

        if trans_type == "KØBT":
            # Stock purchase
            # Main posting is already created by csvbase for the cash account
            # We need to add the stock position and fees
            if row.security and row.isin and row.quantity:
                # Add posting for stock position
                stock_amount = amount.Amount(D(str(row.quantity)), row.isin)
                postings.append(
                    data.Posting(
                        self.stock_account, stock_amount, None, None, None, None
                    )
                )

                # Add fees posting if present
                if row.fees and D(str(row.fees)) != 0:
                    fee_amount = amount.Amount(D(str(row.fees)), row.currency)
                    postings.append(
                        data.Posting(
                            self.fees_account, fee_amount, None, None, None, None
                        )
                    )

        elif trans_type == "SOLGT":
            # Stock sale
            if row.security and row.isin and row.quantity:
                # Negative quantity for sale
                stock_amount = amount.Amount(-D(str(row.quantity)), row.isin)
                postings.append(
                    data.Posting(
                        self.stock_account, stock_amount, None, None, None, None
                    )
                )

                # Add fees posting if present
                if row.fees and D(str(row.fees)) != 0:
                    fee_amount = amount.Amount(D(str(row.fees)), row.currency)
                    postings.append(
                        data.Posting(
                            self.fees_account, fee_amount, None, None, None, None
                        )
                    )

        elif trans_type in ["INDBETALING", "INDSÆTTELSE"]:
            # Deposit - check if it's an internal transfer
            internal_match = re.search(r"Internal from (\d+)", row.transaction_text)
            if internal_match:
                # Internal transfer from another depot
                from_depot = internal_match.group(1)
                if from_depot in self.depot_accounts:
                    from_account = self.depot_accounts[from_depot]
                    postings.append(
                        data.Posting(from_account, None, None, None, None, None)
                    )
                # Skip if depot not in mapping - let user set manually
            # Skip external deposits - let user set manually

        elif trans_type == "HÆVNING":
            # Withdrawal - check if it's an internal transfer
            internal_match = re.search(r"Internal to (\d+)", row.transaction_text)
            if internal_match:
                # Internal transfer to another depot - skip this transaction
                # The corresponding INDBETALING will handle both sides
                to_depot = internal_match.group(1)
                if to_depot in self.depot_accounts:
                    # Skip this transaction entirely by returning None
                    return None
            # Skip external withdrawals - let user set manually

        elif trans_type == "UDBYTTE":
            # Dividend income
            postings.append(
                data.Posting(self.dividend_account, None, None, None, None, None)
            )

        elif trans_type == "UDBYTTESKAT":
            # Dividend tax
            postings.append(
                data.Posting(self.tax_account, None, None, None, None, None)
            )

        elif trans_type in ["AFKASTSKAT", "AFKASTSKAT ASK"]:
            # Capital gains tax
            postings.append(
                data.Posting(self.tax_account, None, None, None, None, None)
            )

        elif trans_type == "SKATTEINDBETALING ASK":
            # Tax payment (ASK account)
            internal_match = re.search(r"Internal from (\d+)", row.transaction_text)
            if internal_match:
                from_depot = internal_match.group(1)
                if from_depot in self.depot_accounts:
                    from_account = self.depot_accounts[from_depot]
                    postings.append(
                        data.Posting(from_account, None, None, None, None, None)
                    )
                # Skip if depot not in mapping

        elif trans_type == "KREDITRENTE":
            # Credit interest (interest income)
            postings.append(
                data.Posting(self.interest_account, None, None, None, None, None)
            )

        elif trans_type in ["GEBYR MÅNEDSOPSPARING", "KORR GEBYR MÅNEDSOPSPARING"]:
            # Monthly savings plan fee (or correction)
            postings.append(
                data.Posting(self.fees_account, None, None, None, None, None)
            )

        else:
            # Unknown transaction type - raise exception
            raise ValueError(
                f"Unknown transaction type '{trans_type}' for depot {row.depot} "
                f"on {row.date} (Transaction ID: {row.transaction_id})"
            )

        # Update the main posting to use the correct cash account
        # Also ensure currency is always explicitly set
        if postings:
            main_posting = postings[0]
            # If the posting has an amount, ensure it has a currency
            if main_posting.units and not main_posting.units.currency:
                fixed_amount = amount.Amount(main_posting.units.number, row.currency)
                main_posting = main_posting._replace(units=fixed_amount)
            postings[0] = main_posting._replace(account=cash_account)

        # Reconstruct transaction with updated payee, narration, and postings
        txn = txn._replace(payee=payee, narration=narration, postings=postings)

        return txn
