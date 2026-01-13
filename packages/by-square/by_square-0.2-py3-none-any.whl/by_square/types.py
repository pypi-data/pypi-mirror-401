from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import Self
import enum

from by_square.encode import Encodeable
from by_square.serialize import ComplexSerialize, Serializable, SquareReader


def bsqr_field(*args, order: int, **kwargs):
    if not kwargs.get("metadata"):
        kwargs["metadata"] = {}
    kwargs["metadata"]["bsqr_order"] = order
    return field(*args, **kwargs)


class IntegerEnum(Serializable, enum.Enum):
    """Base class for integer-based enums that are serializable to square format."""

    def to_square(self) -> list[str]:
        return [str(self.value)]

    @classmethod
    def from_square(cls, reader: SquareReader) -> Self:
        return cls(int(reader.read()))


class StringEnum(Serializable, enum.StrEnum):
    """Base class for string-based enums that are serializable to square format."""

    def to_square(self) -> list[str]:
        return [str(self.value)]

    @classmethod
    def from_square(cls, reader: SquareReader) -> Self:
        return cls(reader.read())


class PaymentOption(IntegerEnum, enum.Flag):
    """Payment option. Options can be combined."""

    PAYMENT_ORDER = 1
    """Payment order."""
    STANDING_ORDER = 2
    """Standing order, data is filled into StandingOrderExt."""
    DIRECT_DEBIT = 4
    """Direct debit, data is filled into DirectDebitExt."""


class Month(IntegerEnum, enum.Flag):
    """Calendar month."""

    JANUARY = 1
    FEBRUARY = 2
    MARCH = 4
    APRIL = 8
    MAY = 16
    JUNE = 32
    JULY = 64
    AUGUST = 128
    SEPTEMBER = 256
    OCTOBER = 512
    NOVEMBER = 1024
    DECEMBER = 2048


class Periodicity(StringEnum):
    """Periodicity (repetition)."""

    DAILY = "d"
    WEEKLY = "w"
    BIWEEKLY = "b"
    MONTHLY = "m"
    BIMONTHLY = "B"
    QUARTERLY = "q"
    SEMIANNUALLY = "s"
    ANNUALLY = "a"


class DirectDebitScheme(IntegerEnum):
    """Direct debit scheme."""

    SEPA = 0
    """Direct debit corresponds to the SEPA scheme."""
    OTHER = 1
    """Other."""


class DirectDebitType(IntegerEnum):
    """Direct debit type."""

    ONE_OFF = 0
    """One-off direct debit."""
    RECURRENT = 1
    """Recurring direct debit."""


@dataclass
class BankAccount(ComplexSerialize):
    """Bank account in international format."""

    iban: str = bsqr_field(order=1)
    """International bank account number in IBAN format. Example: "SK8209000000000011424060"."""
    bic: str = bsqr_field(order=2, default="")
    """International bank identification code (BIC)."""


@dataclass
class StandingOrderExt(ComplexSerialize):
    """Extension of payment data for standing order setup."""

    periodicity: Periodicity = bsqr_field(order=3)
    """Repetition (periodicity) of the standing order."""
    day: int | None = bsqr_field(order=1, default=None)
    """Day of payment from repetition (Periodicity). Day in month is a number between 1 and 31. Day in week is a number between 1 and 7 (1 = Monday, 2 = Tuesday, ..., 7 = Sunday)."""
    month: Month | None = bsqr_field(order=2, default=None)
    """Months in which the payment should be made."""
    last_date: date | None = bsqr_field(order=4, default=None)
    """Date of the last payment in the standing order."""


@dataclass
class DirectDebitExt(ComplexSerialize):
    """Extension of payment data for direct debit setup and identification."""

    direct_debit_scheme: DirectDebitScheme = bsqr_field(order=1)
    """Direct debit scheme. One of: SEPA, other."""
    direct_debit_type: DirectDebitType = bsqr_field(order=2)
    """Direct debit type. One of: one-off, recurrent."""
    mandate_id: str = bsqr_field(order=6)
    """Mandate identification between creditor and debtor according to SEPA."""
    creditor_id: str = bsqr_field(order=7)
    """Creditor identification according to SEPA."""
    contract_id: str = bsqr_field(order=8)
    """Contract identification between creditor and debtor according to SEPA."""

    variable_symbol: str = bsqr_field(order=3, default="")
    """Variable symbol. Only filled if it differs from the variable symbol in the payment order."""
    specific_symbol: str = bsqr_field(order=4, default="")
    """Specific symbol. Only filled if it differs from the specific symbol in the payment order."""
    originators_reference_information: str = bsqr_field(order=5, default="")
    """Reference information. Only used for the transition period from variable and specific symbols to SEPA direct debit."""
    max_amount: Decimal | None = bsqr_field(order=9, default=None)
    """Maximum direct debit amount."""
    valid_till_date: date | None = bsqr_field(order=10, default=None)
    """Validity date of the direct debit. Direct debit validity expires on this date."""


@dataclass
class Payment(ComplexSerialize):
    """Data for a payment order."""

    payment_options: PaymentOption = bsqr_field(order=1)
    """Payment options can be combined."""
    currency_code: str = bsqr_field(order=3)
    """Payment currency in ISO 4217 format (3 letter abbreviation)."""
    bank_accounts: list[BankAccount] = bsqr_field(order=10)
    """List of bank accounts."""

    amount: Decimal | None = bsqr_field(order=2, default=None)
    """Payment amount. Only positive values are allowed. Can be left blank, for example for a voluntary contribution (donations)."""
    payment_due_date: date | None = bsqr_field(order=4, default=None)
    """Payment due date. Optional. In case of a standing order, indicates the date of the first payment."""
    variable_symbol: str = bsqr_field(order=5, default="")
    """Variable symbol is a maximum 10-digit number. Optional."""
    constant_symbol: str = bsqr_field(order=6, default="")
    """Constant symbol is a 4-digit identification number. Optional."""
    specific_symbol: str = bsqr_field(order=7, default="")
    """Specific symbol is a maximum 10-digit number. Optional."""
    originators_reference_information: str = bsqr_field(order=8, default="")
    """Payer's reference information according to SEPA."""
    payment_note: str = bsqr_field(order=9, default="")
    """Message for the recipient. Payment data based on which the recipient can identify the payment. Recommended maximum 140 Unicode characters."""
    standing_order_ext: list[StandingOrderExt] = bsqr_field(
        order=11, default_factory=list
    )
    """Extension of payment data for standing order setup. Note: List for serialization, but at most 1 element is supported by the standard."""
    direct_debit_ext: list[DirectDebitExt] = bsqr_field(order=12, default_factory=list)
    """Extension of payment data for direct debit setup and identification. Note: List for serialization, but at most 1 element is supported by the standard."""
    beneficiary_name: str = bsqr_field(order=13, default="")
    """Extension with beneficiary name."""
    beneficiary_address_line1: str = bsqr_field(order=14, default="")
    """Extension with beneficiary address."""
    beneficiary_address_line2: str = bsqr_field(order=15, default="")
    """Extension with beneficiary address (second line)."""


@dataclass
class PayQR(Encodeable, ComplexSerialize):
    """Payment QR code document according to the by square standard."""

    BY_SQUARE_TYPE = 0
    VERSION = 0
    DOCUMENT_TYPE = 0

    payments: list[Payment] = bsqr_field(order=2)
    """List of one or more payments in case of a bulk order. The main (preferred) payment is listed first."""
    invoice_id: str = bsqr_field(order=1, default="")
    """Invoice number in case the data is part of an invoice, or identifier for internal issuer needs."""


@dataclass
class Contact(ComplexSerialize):
    """Contact information."""

    name: str = bsqr_field(order=1, default="")
    """Name of the contact person (if different from PartyName). Name of the contact department, for example 'Customer service line'."""
    telephone: str = bsqr_field(order=2, default="")
    """Telephone number. It is recommended to provide it with an international prefix, example '+421900900900'."""
    email: str = bsqr_field(order=3, default="")
    """Email address."""


@dataclass
class PostalAddress(ComplexSerialize):
    """Postal address."""

    street_name: str = bsqr_field(order=1)
    """Street name."""
    city_name: str = bsqr_field(order=3)
    """City (district)."""
    postal_zone: str = bsqr_field(order=4)
    """ZIP: Postal routing number."""

    building_number: str = bsqr_field(order=2, default="")
    """Building orientation number."""
    state: str = bsqr_field(order=5, default="")
    """State within a federation. Not specified for the Slovak Republic."""
    country: str = bsqr_field(order=6, default="")
    """Country in ISO 3166 format (3 letter abbreviation). Example: 'SVK'."""


@dataclass
class SupplierParty(ComplexSerialize):
    """Supplier information."""

    party_name: str = bsqr_field(order=1)
    """Company name for legal entities. First name and surname for individuals."""
    postal_address: PostalAddress = bsqr_field(order=5)
    """Postal address of the supplier's headquarters."""

    company_tax_id: str = bsqr_field(order=2, default="")
    """Tax ID: Tax identification number."""
    company_vat_id: str = bsqr_field(order=3, default="")
    """VAT ID: Identification number for value added tax."""
    company_register_id: str = bsqr_field(order=4, default="")
    """Registration ID: Organization identification number."""
    contact: Contact = bsqr_field(order=6, default_factory=Contact)
    """Supplier contact information."""


@dataclass
class CustomerParty(ComplexSerialize):
    """Customer information."""

    party_name: str = bsqr_field(order=1)
    """Company name for legal entities. First name and surname for individuals."""

    company_tax_id: str = bsqr_field(order=2, default="")
    """Tax ID: Tax identification number."""
    company_vat_id: str = bsqr_field(order=3, default="")
    """VAT ID: Identification number for value added tax."""
    company_register_id: str = bsqr_field(order=4, default="")
    """Registration ID: Organization identification number."""
    party_identification: str = bsqr_field(order=5, default="")
    """Customer identifier in the supplier's accounting system. Used for internal processing purposes."""


@dataclass
class SingleInvoiceLine(ComplexSerialize):
    """Details for a single invoice line item. Used only for a single-line invoice, not for multi-line or header invoices."""

    item_name: str = bsqr_field(order=3)
    """Name and description of the item. Can also be used to store structured information about the item."""
    item_ean_code: str = bsqr_field(order=4)
    """EAN (European Article Number) code of the item."""
    invoiced_quantity: Decimal | None = bsqr_field(order=7)
    """Number of pieces (quantity) of this item."""

    order_line_id: str = bsqr_field(order=1, default="")
    """Order line ID for 1 invoice line item. Specified only if different from the main order number on the invoice."""
    delivery_note_line_id: str = bsqr_field(order=2, default="")
    """Delivery note line ID for 1 invoice line item. Specified only if different from the main delivery note number on the invoice."""
    period_from_date: date | None = bsqr_field(order=5, default=None)
    """Start date of the item billing period."""
    period_to_date: date | None = bsqr_field(order=6, default=None)
    """End date of the item billing period."""


@dataclass
class TaxCategorySummary(ComplexSerialize):
    """Summary of a specific tax rate. At least one tax rate summary must be provided."""

    classified_tax_category: Decimal = bsqr_field(order=1)
    """VAT rate expressed as a percentage on the interval 0 to 1. Example for 20% VAT: '0.2'."""
    tax_exclusive_amount: Decimal = bsqr_field(order=2)
    """Amount without VAT in this tax rate in local currency. Note: If a foreign currency is specified, the amount is in foreign currency."""
    tax_amount: Decimal = bsqr_field(order=3)
    """VAT amount in this tax rate in local currency. Note: If a foreign currency is specified, the amount is in foreign currency."""
    already_claimed_tax_exclusive_amount: Decimal = bsqr_field(order=4)
    """Paid advances without VAT in this tax rate in local currency. Note: If a foreign currency is specified, the amount is in foreign currency."""
    already_claimed_tax_amount: Decimal = bsqr_field(order=5)
    """VAT from paid advances in this tax rate in local currency. Note: If a foreign currency is specified, the amount is in foreign currency."""


@dataclass
class MonetarySummary(ComplexSerialize):
    """Total invoice summary. Sum of summaries of all VAT rates."""

    tax_exclusive_amount: Decimal = bsqr_field(order=1)
    """Amount without VAT of the entire invoice in local currency. Note: If a foreign currency is specified, the amount is in foreign currency."""
    tax_amount: Decimal = bsqr_field(order=2)
    """VAT amount of the entire invoice in local currency. Note: If a foreign currency is specified, the amount is in foreign currency."""


class PaymentMean(IntegerEnum, enum.IntFlag):
    """Form of payment."""

    MONEY_TRANSFER = 1
    """Money transfer to bank account."""
    CASH = 2
    """Cash."""
    CASH_ON_DELIVERY = 4
    """Cash on delivery."""
    CREDIT_CARD = 8
    """Credit card."""
    ADVANCE = 16
    """Advance payment."""
    MUTUAL_OFFSET = 32
    """Mutual offset."""
    OTHER = 64
    """Other, not yet defined form of payment."""


@dataclass
class InvoiceQR(Encodeable, ComplexSerialize):
    """Invoice QR code document according to the by square standard, type: invoice."""

    BY_SQUARE_TYPE = 1
    VERSION = 0
    DOCUMENT_TYPE = 0

    invoice_id: str = bsqr_field(order=1)
    """Invoice number, uniquely identifies the invoice within the company's accounting system."""
    issue_date: date = bsqr_field(order=2)
    """Invoice issue date."""
    local_currency_code: str = bsqr_field(order=6)
    """Local currency in ISO 4217 format (3 letter abbreviation). Example: 'EUR'."""
    supplier_party: SupplierParty = bsqr_field(order=10)
    """Supplier information."""
    customer_party: CustomerParty = bsqr_field(order=11)
    """Customer information."""
    number_of_invoice_lines: int = bsqr_field(order=12)
    """Number of invoice line items. Specified in case of a multi-line invoice. Left blank in case of a single-line invoice. Header invoice means that individual invoice line items are not listed, only a summary of invoiced data. In case of a header invoice, 0 is entered."""
    tax_category_summaries: list[TaxCategorySummary] = bsqr_field(order=15)
    """List of summaries of individual VAT tax rates."""

    tax_point_date: date | None = bsqr_field(order=3, default=None)
    """Date of taxable performance (tax liability), delivery of goods or service."""
    order_id: str = bsqr_field(order=4, default="")
    """Order number. In case the invoice relates to multiple orders, the primary order number is specified. Note: In case of multiple orders, they are listed directly at the line items."""
    delivery_note_id: str = bsqr_field(order=5, default="")
    """Delivery note number. In case the invoice relates to multiple delivery notes, the primary delivery note number is specified. Note: In case of multiple delivery notes, they are listed directly at the line items."""
    foreign_currency_code: str = bsqr_field(order=7, default="")
    """Foreign currency in ISO 4217 format (3 letter abbreviation). Example: 'USD'. If a foreign currency is specified, all amounts on the invoice are listed in the foreign currency."""
    curr_rate: Decimal | None = bsqr_field(order=8, default=None)
    """Foreign currency exchange rate - direct quotation, relative to local currency. Unit of foreign currency = X units of local currency. Use this rate for conversion from foreign currency to local currency."""
    reference_curr_rate: Decimal | None = bsqr_field(order=9, default=None)
    """Foreign currency exchange rate - indirect quotation, relative to local currency. Unit of local currency = X units of foreign currency. This rate should be used for conversion from local currency to foreign currency."""
    invoice_description: str = bsqr_field(order=13, default="")
    """General description of the invoice. Specified in case of multiple items, otherwise must be left blank."""
    single_invoice_line: SingleInvoiceLine = bsqr_field(
        order=14,
        default_factory=lambda: SingleInvoiceLine(
            item_name="", invoiced_quantity=None, item_ean_code=""
        ),
    )
    """Details for a single invoice line item. Specified only in case of a single-line invoice and not filled in case of multi-line and header invoices."""
    monetary_summary: MonetarySummary = bsqr_field(
        order=16, default_factory=lambda: MonetarySummary(Decimal(), Decimal())
    )
    """Total invoice summary. Sum of summaries of all VAT rates."""
    payment_means: PaymentMean | None = bsqr_field(order=17, default=None)
    """Forms of payment. Optional data."""


class ProformaInvoiceQR(InvoiceQR):
    """Invoice QR code document according to the by square standard, type: proforma invoice."""

    DOCUMENT_TYPE = 1


class CreditNoteQR(InvoiceQR):
    """Invoice QR code document according to the by square standard, type: credit note."""

    DOCUMENT_TYPE = 2


class DebitNoteQR(InvoiceQR):
    """Invoice QR code document according to the by square standard, type: debit note."""

    DOCUMENT_TYPE = 3


class AdvanceInvoiceQR(InvoiceQR):
    """Invoice QR code document according to the by square standard, type: advance invoice."""

    DOCUMENT_TYPE = 4
