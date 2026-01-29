import hashlib

from xrpl.models.transactions import Memo, Payment
from xrpl.transaction import sign
from xrpl.wallet import Wallet

from app.services.xrpl_x402_presigned_payment_facilitator import (
    PaymentRequirements as FacilitatorPaymentRequirements,
    X402Envelope,
    verify_logic,
)


SENDER_SEED = "sEd7M69Yu4Kz8JkunvshAzrPwwdQYQL"
RECEIVER_SEED = "sEd73youjTvFdc6koXuxMac5ppmse6e"


def _memo_hex(invoice_id: str) -> str:
    return invoice_id.encode("utf-8").hex().upper()


def _invoice_id_field(invoice_id: str) -> str:
    return hashlib.sha256(invoice_id.encode("utf-8")).hexdigest().upper()


def _to_currency_hex(code: str) -> str:
    if len(code) == 40:
        try:
            bytes.fromhex(code)
            return code.upper()
        except ValueError:
            pass
    if len(code) <= 3:
        return code.upper()
    raw = code.encode("utf-8")
    if len(raw) > 20:
        raise ValueError("Currency code too long (max 20 bytes).")
    return raw.hex().upper().ljust(40, "0")


def _sign_payment_blob(
    *,
    sender: Wallet,
    destination: str,
    amount_drops: int,
    invoice_id: str,
    include_memo: bool = True,
    include_invoice_id_field: bool = False,
    last_ledger_sequence: int | None = 10,
    fee_drops: str = "12",
    flags: int | None = None,
    send_max: object | None = None,
) -> str:
    memos = [Memo(memo_data=_memo_hex(invoice_id))] if include_memo else None
    invoice_id_val = _invoice_id_field(invoice_id) if include_invoice_id_field else None

    tx_kwargs: dict = {
        "account": sender.classic_address,
        "destination": destination,
        "amount": str(int(amount_drops)),
        "sequence": 1,
        "fee": fee_drops,
        "memos": memos,
        "invoice_id": invoice_id_val,
        "flags": flags,
        "send_max": send_max,
    }
    if last_ledger_sequence is not None:
        tx_kwargs["last_ledger_sequence"] = last_ledger_sequence

    tx = Payment(**tx_kwargs)
    signed = sign(tx, sender)
    return signed.blob()


def _sign_payment_blob_iou(
    *,
    sender: Wallet,
    destination: str,
    currency: str,
    issuer: str,
    value: str,
    invoice_id: str,
    include_memo: bool = True,
    include_invoice_id_field: bool = False,
    last_ledger_sequence: int | None = 10,
    fee_drops: str = "12",
    flags: int | None = None,
    send_max: object | None = None,
) -> str:
    memos = [Memo(memo_data=_memo_hex(invoice_id))] if include_memo else None
    invoice_id_val = _invoice_id_field(invoice_id) if include_invoice_id_field else None

    tx_kwargs: dict = {
        "account": sender.classic_address,
        "destination": destination,
        "amount": {"currency": _to_currency_hex(currency), "issuer": issuer, "value": value},
        "sequence": 1,
        "fee": fee_drops,
        "memos": memos,
        "invoice_id": invoice_id_val,
        "flags": flags,
        "send_max": send_max,
    }
    if last_ledger_sequence is not None:
        tx_kwargs["last_ledger_sequence"] = last_ledger_sequence

    tx = Payment(**tx_kwargs)
    signed = sign(tx, sender)
    return signed.blob()


def test_verify_valid_memos_binding():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=100,
        invoice_id=invoice_id,
        include_memo=True,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, payer = verify_logic(envelope, req)
    assert ok is True
    assert reason is None
    assert payer == sender.classic_address


def test_verify_valid_invoice_id_field_binding():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=100,
        invoice_id=invoice_id,
        include_memo=False,
        include_invoice_id_field=True,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, payer = verify_logic(envelope, req)
    assert ok is True
    assert reason is None
    assert payer == sender.classic_address


def test_verify_rejects_invalid_tx_blob():
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": "NOTHEX", "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "invalid_tx_blob"
    assert payer is None


def test_verify_rejects_missing_last_ledger_sequence():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=100,
        invoice_id=invoice_id,
        include_memo=True,
        last_ledger_sequence=None,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "missing_last_ledger_sequence"


def test_verify_rejects_invoice_binding_missing():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=100,
        invoice_id=invoice_id,
        include_memo=False,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "invoice_binding_missing"


def test_verify_rejects_invoice_binding_mismatch():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    expected_invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=100,
        invoice_id="INV-OTHER",
        include_memo=True,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": expected_invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=expected_invoice_id,
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "invoice_binding_mismatch"


def test_verify_rejects_amount_mismatch():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=200,
        invoice_id=invoice_id,
        include_memo=True,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "amount_mismatch"


def test_verify_rejects_sendmax():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=100,
        invoice_id=invoice_id,
        include_memo=True,
        last_ledger_sequence=10,
        send_max={"currency": "USD", "issuer": sender.classic_address, "value": "100"},
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "unsupported_payment_features"


def test_verify_rejects_fee_too_high():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-123"

    blob = _sign_payment_blob(
        sender=sender,
        destination=receiver.classic_address,
        amount_drops=100,
        invoice_id=invoice_id,
        include_memo=True,
        last_ledger_sequence=10,
        fee_drops="5001",
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="100",
        scheme="exact",
        network="xrpl-testnet",
        asset="XRP",
        invoiceId=invoice_id,
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "fee_too_high"


def test_verify_valid_iou_memos_binding():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-IOU-123"

    issuer = sender.classic_address
    blob = _sign_payment_blob_iou(
        sender=sender,
        destination=receiver.classic_address,
        currency="RLUSD",
        issuer=issuer,
        value="1",
        invoice_id=invoice_id,
        include_memo=True,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="1.0",
        scheme="exact",
        network="xrpl-testnet",
        asset="RLUSD",
        invoiceId=invoice_id,
        extra={"issuer": issuer},
    )

    ok, reason, payer = verify_logic(envelope, req)
    assert ok is True
    assert reason is None
    assert payer == sender.classic_address


def test_verify_rejects_iou_missing_issuer_in_requirements():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-IOU-123"

    blob = _sign_payment_blob_iou(
        sender=sender,
        destination=receiver.classic_address,
        currency="RLUSD",
        issuer=sender.classic_address,
        value="1",
        invoice_id=invoice_id,
        include_memo=True,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="1",
        scheme="exact",
        network="xrpl-testnet",
        asset="RLUSD",
        invoiceId=invoice_id,
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "missing_issuer"


def test_verify_rejects_iou_currency_mismatch():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-IOU-123"

    issuer = sender.classic_address
    blob = _sign_payment_blob_iou(
        sender=sender,
        destination=receiver.classic_address,
        currency="RLUSD",
        issuer=issuer,
        value="1",
        invoice_id=invoice_id,
        include_memo=True,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="1",
        scheme="exact",
        network="xrpl-testnet",
        asset="USD",
        invoiceId=invoice_id,
        extra={"issuer": issuer},
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "currency_mismatch"


def test_verify_rejects_iou_issuer_mismatch():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-IOU-123"

    blob = _sign_payment_blob_iou(
        sender=sender,
        destination=receiver.classic_address,
        currency="RLUSD",
        issuer=sender.classic_address,
        value="1",
        invoice_id=invoice_id,
        include_memo=True,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="1",
        scheme="exact",
        network="xrpl-testnet",
        asset="RLUSD",
        invoiceId=invoice_id,
        extra={"issuer": receiver.classic_address},
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "issuer_mismatch"


def test_verify_rejects_iou_amount_mismatch():
    sender = Wallet.from_seed(SENDER_SEED)
    receiver = Wallet.from_seed(RECEIVER_SEED)
    invoice_id = "INV-IOU-123"

    issuer = sender.classic_address
    blob = _sign_payment_blob_iou(
        sender=sender,
        destination=receiver.classic_address,
        currency="RLUSD",
        issuer=issuer,
        value="2",
        invoice_id=invoice_id,
        include_memo=True,
        include_invoice_id_field=False,
        last_ledger_sequence=10,
    )

    envelope = X402Envelope(
        x402Version="1",
        scheme="exact",
        network="xrpl-testnet",
        payload={"signed_tx_blob": blob, "invoice_id": invoice_id},
    )
    req = FacilitatorPaymentRequirements(
        payTo=receiver.classic_address,
        maxAmountRequired="1",
        scheme="exact",
        network="xrpl-testnet",
        asset="RLUSD",
        invoiceId=invoice_id,
        extra={"issuer": issuer},
    )

    ok, reason, _payer = verify_logic(envelope, req)
    assert ok is False
    assert reason == "amount_mismatch"
