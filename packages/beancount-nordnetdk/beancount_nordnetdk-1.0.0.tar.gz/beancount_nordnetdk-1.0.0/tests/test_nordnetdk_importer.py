"""Tests for NordnetDKImporter."""

import datetime
from decimal import Decimal
from pathlib import Path
import pytest
from beancount.core import data
from beancount_nordnetdk import NordnetDKImporter


@pytest.fixture
def importer():
    """Create a NordnetDKImporter instance for testing."""
    return NordnetDKImporter(
        depot_accounts={
            "11111111": "Assets:Nordnet:Depot1",
            "22222222": "Assets:Nordnet:Depot2",
            "33333333": "Assets:Nordnet:ASK",
        },
        currency="DKK",
        stock_account="Assets:Nordnet:Stocks",
        fees_account="Expenses:Investments:Fees",
        dividend_account="Income:Investments:Dividends",
        tax_account="Expenses:Investments:Tax",
        interest_account="Income:Investments:Interest",
    )


@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a sample Nordnet CSV file for testing."""
    csv_content = (
        "Id\tBogføringsdag\tHandelsdag\tValørdag\tDepot\tTransaktionstype\t"
        "Værdipapirer\tISIN\tAntal\tKurs\tRente\tSamlede afgifter\tValuta\t"
        "Beløb\tValuta\tIndkøbsværdi\tValuta\tResultat\tValuta\tTotalt antal\t"
        "Saldo\tVekslingskurs\tTransaktionstekst\tMakuleringsdato\tNotanummer\t"
        "Verifikationsnummer\tKurtage\tValuta\tMiddelkurs\tOprindelig rente\n"
        "1000000001\t2026-01-08\t2026-01-08\t2026-01-12\t11111111\tKØBT\t"
        "Acme Global Stocks Fund\tXX0000000001\t13\t190,9498\t0\t0\tDKK\t"
        "-2.482,35\tDKK\t2.482,35\tDKK\t0\tDKK\t2835\t1.877,03\t\t\t\t"
        "9000000001\t9000000001\t0\tDKK\t\t\n"
        "1000000002\t2026-01-05\t2026-01-05\t2026-01-05\t11111111\tINDBETALING\t"
        "\t\t\t\t\t\t\t2.500\tDKK\t\t\t\t\t\t4.359,38\t\t"
        "FROM BANK\t\t\t9000000002\t\t\t\t\n"
        "1000000003\t2026-01-02\t2026-01-02\t2026-01-02\t22222222\tINDBETALING\t"
        "\t\t\t\t\t\t\t9.900\tDKK\t\t\t\t\t\t9.930,22\t\t"
        "Internal from 11111111\t\t\t9000000003\t\t\t\t\n"
        "1000000004\t2026-01-02\t2026-01-02\t2026-01-02\t11111111\tHÆVNING\t"
        "\t\t\t\t\t\t\t-9.900\tDKK\t\t\t\t\t\t1.859,38\t\t"
        "Internal to 22222222\t\t\t9000000004\t\t\t\t\n"
    )
    csv_file = tmp_path / "transactions-and-notes-export.csv"
    csv_file.write_text(csv_content, encoding="utf-16")
    return csv_file


class TestNordnetDKImporterInit:
    """Test NordnetDKImporter initialization."""

    def test_init_with_valid_parameters(self):
        """Test that importer initializes with valid parameters."""
        importer = NordnetDKImporter(
            depot_accounts={"12345678": "Assets:Nordnet:Account"},
            stock_account="Assets:Stocks",
            fees_account="Expenses:Fees",
            dividend_account="Income:Dividends",
            tax_account="Expenses:Tax",
            interest_account="Income:Interest",
        )
        assert importer.depot_accounts == {"12345678": "Assets:Nordnet:Account"}
        assert importer.stock_account == "Assets:Stocks"
        assert importer.currency == "DKK"

    def test_init_without_depot_accounts_raises_error(self):
        """Test that initialization without depot_accounts raises ValueError."""
        with pytest.raises(ValueError, match="depot_accounts mapping cannot be empty"):
            NordnetDKImporter(
                depot_accounts={},
                stock_account="Assets:Stocks",
                fees_account="Expenses:Fees",
                dividend_account="Income:Dividends",
                tax_account="Expenses:Tax",
                interest_account="Income:Interest",
            )

    def test_init_missing_required_account_raises_error(self):
        """Test that initialization without required accounts raises ValueError."""
        with pytest.raises(ValueError, match="Missing required account parameters"):
            NordnetDKImporter(
                depot_accounts={"12345678": "Assets:Nordnet:Account"},
                stock_account="Assets:Stocks",
                fees_account="Expenses:Fees",
                # Missing dividend_account, tax_account, interest_account
            )


class TestNordnetDKImporterIdentify:
    """Test file identification."""

    def test_identify_valid_nordnet_file(self, importer, sample_csv_file):
        """Test that a valid Nordnet CSV file is identified."""
        assert importer.identify(sample_csv_file) is True

    def test_identify_wrong_filename(self, importer, tmp_path):
        """Test that a file with wrong name is not identified."""
        wrong_file = tmp_path / "wrong-name.csv"
        wrong_file.write_text("some,data", encoding="utf-16")
        assert importer.identify(wrong_file) is False

    def test_identify_no_matching_depot(self, tmp_path):
        """Test that file with no matching depot is not identified."""
        importer = NordnetDKImporter(
            depot_accounts={"99999999": "Assets:Other"},
            stock_account="Assets:Stocks",
            fees_account="Expenses:Fees",
            dividend_account="Income:Dividends",
            tax_account="Expenses:Tax",
            interest_account="Income:Interest",
        )
        csv_content = (
            "Id\tBogføringsdag\tHandelsdag\tValørdag\tDepot\tTransaktionstype\t"
            "Værdipapirer\tISIN\tAntal\tKurs\tRente\tSamlede afgifter\tValuta\t"
            "Beløb\tValuta\tIndkøbsværdi\tValuta\tResultat\tValuta\tTotalt antal\t"
            "Saldo\tVekslingskurs\tTransaktionstekst\tMakuleringsdato\tNotanummer\t"
            "Verifikationsnummer\tKurtage\tValuta\tMiddelkurs\tOprindelig rente\n"
            "1000000500\t2026-01-01\t2026-01-01\t2026-01-01\t88888888\tINDBETALING\t"
            "\t\t\t\t\t\t\t1.000\tDKK\t\t\t\t\t\t1.000\t\t\t\t\t\t\t\t\t\t\n"
        )
        csv_file = tmp_path / "transactions-and-notes-export.csv"
        csv_file.write_text(csv_content, encoding="utf-16")
        assert importer.identify(csv_file) is False


class TestNordnetDKImporterFilename:
    """Test filename generation."""

    def test_filename(self, importer):
        """Test that filename is properly generated."""
        result = importer.filename("/path/to/transactions-and-notes-export.csv")
        assert result == "nordnet.transactions-and-notes-export.csv"


class TestNordnetDKImporterExtract:
    """Test transaction extraction."""

    def test_extract_stock_purchase(self, importer, sample_csv_file):
        """Test extraction of stock purchase transaction."""
        entries = importer.extract(sample_csv_file, [])
        
        # Find the KØBT transaction
        transactions = [e for e in entries if isinstance(e, data.Transaction)]
        stock_tx = [t for t in transactions if "KØBT" in t.narration][0]
        
        assert stock_tx.date == datetime.date(2026, 1, 8)
        assert stock_tx.payee == "Acme Global Stocks Fund"
        assert len(stock_tx.postings) == 2
        
        # Check cash posting
        assert stock_tx.postings[0].account == "Assets:Nordnet:Depot1"
        assert stock_tx.postings[0].units.number == Decimal("-2482.35")
        assert stock_tx.postings[0].units.currency == "DKK"
        
        # Check stock posting
        assert stock_tx.postings[1].account == "Assets:Nordnet:Stocks"
        assert stock_tx.postings[1].units.number == Decimal("13")
        assert stock_tx.postings[1].units.currency == "XX0000000001"

    def test_extract_deposit(self, importer, sample_csv_file):
        """Test extraction of deposit transaction."""
        entries = importer.extract(sample_csv_file, [])
        
        transactions = [e for e in entries if isinstance(e, data.Transaction)]
        deposit_tx = [t for t in transactions if "FROM BANK" in t.narration][0]
        
        assert deposit_tx.date == datetime.date(2026, 1, 5)
        assert len(deposit_tx.postings) == 1
        assert deposit_tx.postings[0].account == "Assets:Nordnet:Depot1"
        assert deposit_tx.postings[0].units.number == Decimal("2500")

    def test_extract_internal_transfer(self, importer, sample_csv_file):
        """Test that internal transfers are handled correctly."""
        entries = importer.extract(sample_csv_file, [])
        
        transactions = [e for e in entries if isinstance(e, data.Transaction)]
        
        # Should have INDBETALING but not HÆVNING (withdrawal is skipped)
        internal_deposits = [t for t in transactions if "Internal from" in t.narration]
        internal_withdrawals = [t for t in transactions if "Internal to" in t.narration]
        
        assert len(internal_deposits) == 1
        assert len(internal_withdrawals) == 0
        
        # Check the deposit side has both accounts
        transfer_tx = internal_deposits[0]
        assert len(transfer_tx.postings) == 2
        assert transfer_tx.postings[0].account == "Assets:Nordnet:Depot2"
        assert transfer_tx.postings[1].account == "Assets:Nordnet:Depot1"

    def test_extract_balance_assertions(self, importer, sample_csv_file):
        """Test that balance assertions are created per account."""
        entries = importer.extract(sample_csv_file, [])
        
        balances = [e for e in entries if isinstance(e, data.Balance)]
        
        # Should have at least one balance assertion
        assert len(balances) >= 1
        
        # Check that balance is for the correct account
        accounts_with_balances = {b.account for b in balances}
        assert "Assets:Nordnet:Depot1" in accounts_with_balances


class TestNordnetDKImporterTransactionTypes:
    """Test different transaction types."""

    def test_unknown_transaction_type_raises_error(self, importer, tmp_path):
        """Test that unknown transaction types raise ValueError."""
        csv_content = (
            "Id\tBogføringsdag\tHandelsdag\tValørdag\tDepot\tTransaktionstype\t"
            "Værdipapirer\tISIN\tAntal\tKurs\tRente\tSamlede afgifter\tValuta\t"
            "Beløb\tValuta\tIndkøbsværdi\tValuta\tResultat\tValuta\tTotalt antal\t"
            "Saldo\tVekslingskurs\tTransaktionstekst\tMakuleringsdato\tNotanummer\t"
            "Verifikationsnummer\tKurtage\tValuta\tMiddelkurs\tOprindelig rente\n"
            "1000000999\t2026-01-01\t2026-01-01\t2026-01-01\t11111111\tUNKNOWN_TYPE\t"
            "\t\t\t\t\t\t\t1.000\tDKK\t\t\t\t\t\t1.000\t\t\t\t\t\t\t\t\t\t\n"
        )
        csv_file = tmp_path / "transactions-and-notes-export.csv"
        csv_file.write_text(csv_content, encoding="utf-16")
        
        with pytest.raises(ValueError, match="Unknown transaction type 'UNKNOWN_TYPE'"):
            importer.extract(csv_file, [])

    def test_dividend_transaction(self, importer, tmp_path):
        """Test extraction of dividend transaction."""
        csv_content = (
            "Id\tBogføringsdag\tHandelsdag\tValørdag\tDepot\tTransaktionstype\t"
            "Værdipapirer\tISIN\tAntal\tKurs\tRente\tSamlede afgifter\tValuta\t"
            "Beløb\tValuta\tIndkøbsværdi\tValuta\tResultat\tValuta\tTotalt antal\t"
            "Saldo\tVekslingskurs\tTransaktionstekst\tMakuleringsdato\tNotanummer\t"
            "Verifikationsnummer\tKurtage\tValuta\tMiddelkurs\tOprindelig rente\n"
            "1000000100\t2026-01-01\t2026-01-01\t2026-01-01\t11111111\tUDBYTTE\t"
            "Fictional Company Stock\tXX0000000099\t100\t\t\t\t\t500\tDKK\t\t\t\t\t\t"
            "5.000\t\t\t\t\t\t\t\t\t\t\n"
        )
        csv_file = tmp_path / "transactions-and-notes-export.csv"
        csv_file.write_text(csv_content, encoding="utf-16")
        
        entries = importer.extract(csv_file, [])
        transactions = [e for e in entries if isinstance(e, data.Transaction)]
        
        assert len(transactions) == 1
        tx = transactions[0]
        assert len(tx.postings) == 2
        assert tx.postings[0].account == "Assets:Nordnet:Depot1"
        assert tx.postings[1].account == "Income:Investments:Dividends"

    def test_tax_transaction(self, importer, tmp_path):
        """Test extraction of tax transaction."""
        csv_content = (
            "Id\tBogføringsdag\tHandelsdag\tValørdag\tDepot\tTransaktionstype\t"
            "Værdipapirer\tISIN\tAntal\tKurs\tRente\tSamlede afgifter\tValuta\t"
            "Beløb\tValuta\tIndkøbsværdi\tValuta\tResultat\tValuta\tTotalt antal\t"
            "Saldo\tVekslingskurs\tTransaktionstekst\tMakuleringsdato\tNotanummer\t"
            "Verifikationsnummer\tKurtage\tValuta\tMiddelkurs\tOprindelig rente\n"
            "1000000200\t2026-01-01\t2026-01-01\t2026-01-01\t11111111\tUDBYTTESKAT\t"
            "\t\t\t\t\t\t\t-150\tDKK\t\t\t\t\t\t4.850\t\t\t\t\t\t\t\t\t\t\n"
        )
        csv_file = tmp_path / "transactions-and-notes-export.csv"
        csv_file.write_text(csv_content, encoding="utf-16")
        
        entries = importer.extract(csv_file, [])
        transactions = [e for e in entries if isinstance(e, data.Transaction)]
        
        assert len(transactions) == 1
        tx = transactions[0]
        assert len(tx.postings) == 2
        assert tx.postings[0].account == "Assets:Nordnet:Depot1"
        assert tx.postings[1].account == "Expenses:Investments:Tax"

    def test_fee_transaction(self, importer, tmp_path):
        """Test extraction of fee transaction."""
        csv_content = (
            "Id\tBogføringsdag\tHandelsdag\tValørdag\tDepot\tTransaktionstype\t"
            "Værdipapirer\tISIN\tAntal\tKurs\tRente\tSamlede afgifter\tValuta\t"
            "Beløb\tValuta\tIndkøbsværdi\tValuta\tResultat\tValuta\tTotalt antal\t"
            "Saldo\tVekslingskurs\tTransaktionstekst\tMakuleringsdato\tNotanummer\t"
            "Verifikationsnummer\tKurtage\tValuta\tMiddelkurs\tOprindelig rente\n"
            "1000000300\t2026-01-01\t2026-01-01\t2026-01-01\t11111111\tGEBYR MÅNEDSOPSPARING\t"
            "\t\t\t\t\t\t\t-10\tDKK\t\t\t\t\t\t4.990\t\t"
            "Monthly fee\t\t\t\t\t\t\t\t\n"
        )
        csv_file = tmp_path / "transactions-and-notes-export.csv"
        csv_file.write_text(csv_content, encoding="utf-16")
        
        entries = importer.extract(csv_file, [])
        transactions = [e for e in entries if isinstance(e, data.Transaction)]
        
        assert len(transactions) == 1
        tx = transactions[0]
        assert len(tx.postings) == 2
        assert tx.postings[0].account == "Assets:Nordnet:Depot1"
        assert tx.postings[1].account == "Expenses:Investments:Fees"
