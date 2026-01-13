<div align="center">
  <h1>by-square</h1>
  <p>Encoder and decoder of "by square" QR codes (PAY by square, INVOICE by square)</p>
</div>

`by-square` is a Python library for encoding and decoding "by square" QR codes as
used in the Slovak banking and invoicing ecosystem. The library implements the
PAY by square and INVOICE by square standards for payment and invoice data.

This implementation follows the official [by square schema](https://bsqr.co/schema/)
and [specifications](https://www.sbaonline.sk/wp-content/uploads/2020/03/pay-by-square-specifications-1_1_0.pdf).

## Installation

```bash
pip install by-square
```

## PAY by square

Create a payment QR code:

```python
from datetime import date
from decimal import Decimal
from by_square import PayQR, Payment, PaymentOption, BankAccount

payment = Payment(
    payment_options=PaymentOption.PAYMENT_ORDER,
    amount=Decimal("34.50"),
    currency_code="EUR",
    bank_accounts=[BankAccount(iban="SK7700000000000000000000", bic="FIOZSKBAXXX")],
    variable_symbol="102",
    payment_due_date=date(2026, 1, 9),
    payment_note="Payment for services",
)

pay_qr = PayQR(payments=[payment])
encoded = pay_qr.encode()
print(encoded)
```

Decode a payment QR code:

```python
from by_square import PayQR

decoded = PayQR.decode(encoded)
print(decoded.payments[0].amount)
```

Or use the universal decoder that automatically detects the document type:

```python
from by_square import decode_universal

decoded = decode_universal(encoded)
print(decoded.payments[0].amount)
```

## INVOICE by square

Create an invoice QR code:

```python
from datetime import date
from decimal import Decimal
from by_square import (
    InvoiceQR, SupplierParty, CustomerParty, PostalAddress,
    Contact, TaxCategorySummary, PaymentMean
)

invoice = InvoiceQR(
    invoice_id="2025001",
    issue_date=date(2026, 1, 10),
    tax_point_date=date(2026, 1, 10),
    local_currency_code="EUR",
    supplier_party=SupplierParty(
        party_name="Supplier, s.r.o.",
        company_tax_id="0000000000",
        company_vat_id="SK0000000000",
        postal_address=PostalAddress(
            street_name="Address",
            building_number="10",
            city_name="Bratislava",
            postal_zone="800 00",
            country="SVK",
        ),
        contact=Contact(
            name="Ján Mrva",
            telephone="+421900000000",
            email="info@example.com",
        ),
    ),
    customer_party=CustomerParty(
        party_name="Customer s.r.o.",
        company_tax_id="0000000000",
    ),
    tax_category_summaries=[
        TaxCategorySummary(
            classified_tax_category=Decimal("0.2"),
            tax_exclusive_amount=Decimal("1000"),
            tax_amount=Decimal("200"),
            already_claimed_tax_exclusive_amount=Decimal(),
            already_claimed_tax_amount=Decimal(),
        )
    ],
    number_of_invoice_lines=0,
    payment_means=PaymentMean.MONEY_TRANSFER,
)

encoded = invoice.encode()
print(encoded)
```

Decode an invoice QR code:

```python
from by_square import InvoiceQR

decoded = InvoiceQR.decode(encoded)
print(decoded.invoice_id)
```

Or use the universal decoder that automatically detects the document type:

```python
from by_square import decode_universal

decoded = decode_universal(encoded)
print(decoded.invoice_id)
```

Supported invoice types:

- `InvoiceQR` - Standard invoice
- `ProformaInvoiceQR` - Proforma invoice
- `CreditNoteQR` - Credit note
- `DebitNoteQR` - Debit note
- `AdvanceInvoiceQR` - Advance invoice

## Implementation notes

### InvoiceItems

The by square specification defines a InvoiceItems document type, however these were
not seen in the wild, and as I don't have any examples available, these were not
implemented in the library.

### Data validation

This library focuses solely on encoding and decoding "by square" codes. Validation
of the contained data (such as IBAN checksums, VAT number formats, date ranges, etc.)
is out of scope.

### Optional complex types

The by square specification defines some complex types as optional (minOccurs="0").
According to the spec, these should be preceded by a count indicator (0 or 1) in
the serialized sequence.

To simplify the serialization semantics, this library represents optional complex
types as lists:

- Use an empty list `[]` to omit the type (equivalent to count=0)
- Use a single-element list `[instance]` to include the type (equivalent to count=1)

**Important**: The specification allows at most one instance of optional complex
types. While this library technically allows multiple items in these lists,
generated encodings with more than one element will not be accepted by other
implementations.

Examples of optional complex types:

- `Payment.standing_order_ext` - Standing order extension
- `Payment.direct_debit_ext` - Direct debit extension

## by square quirks

The by square standard contains several inconsistencies and edge cases that differ
from the written specification:

### INVOICE by square encoding of optional types

While the specification describes how optional complex types should be encoded with
a 0/1 count indicator, real-world INVOICE by square codes omit this entirely.
Instead, optional types are simply included with all fields left empty.

### MonetarySummary field

The INVOICE by square schema defines a `MonetarySummary` field for invoice totals.
However, in practice, no real QR codes have been observed containing meaningful
data in this field. The totals are typically derived from `TaxCategorySummary`
items instead.

If you encounter a QR code with actual MonetarySummary data, please report it as
it would help improve interoperability testing.
