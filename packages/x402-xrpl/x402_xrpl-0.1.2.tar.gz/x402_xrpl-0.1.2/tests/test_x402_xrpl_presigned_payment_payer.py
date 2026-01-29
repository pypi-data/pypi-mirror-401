import base64
import hashlib
import json

from x402_xrpl.client.presigned_payment_payer import (
    build_payment_header_for_signed_blob,
    invoice_id_to_invoice_id_field,
    invoice_id_to_memo_hex,
)
from x402_xrpl.types import PaymentRequirements


def test_presigned_invoice_memo_hex_roundtrip():
    invoice_id = "INV-123"
    memo_hex = invoice_id_to_memo_hex(invoice_id)
    assert bytes.fromhex(memo_hex).decode("utf-8") == invoice_id


def test_presigned_invoice_id_field_is_sha256_upper_hex():
    invoice_id = "INV-123"
    expected = hashlib.sha256(invoice_id.encode("utf-8")).hexdigest().upper()
    assert invoice_id_to_invoice_id_field(invoice_id) == expected


def test_presigned_payment_header_envelope_shape():
    req = PaymentRequirements(
        scheme="exact",
        network="xrpl:1",
        amount="1000000",
        asset="XRP",
        pay_to="rPAYTO",
        max_timeout_seconds=600,
        extra={"invoiceId": "INV-123"},
    )

    header = build_payment_header_for_signed_blob(
        req=req,
        signed_tx_blob="DEADBEEF",
        invoice_id=req.invoice_id() or "INV-123",
    )

    decoded = json.loads(base64.b64decode(header))
    assert decoded["x402Version"] == 2
    assert decoded["accepted"]["scheme"] == "exact"
    assert decoded["accepted"]["network"] == "xrpl:1"
    assert decoded["payload"]["signedTxBlob"] == "DEADBEEF"
    assert decoded["payload"]["invoiceId"] == "INV-123"

