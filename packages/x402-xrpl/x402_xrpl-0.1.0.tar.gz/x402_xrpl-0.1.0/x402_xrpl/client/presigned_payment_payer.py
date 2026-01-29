from __future__ import annotations

import base64
import hashlib
import json
from dataclasses import dataclass
from typing import Literal, Mapping, Optional

from xrpl.clients import JsonRpcClient
from xrpl.models.amounts import IssuedCurrencyAmount
from xrpl.models.transactions import Memo, Payment
from xrpl.transaction import autofill, sign
from xrpl.wallet import Wallet

from x402_xrpl.types import PaymentPayload, PaymentRequirements

InvoiceBindingMode = Literal["memos", "invoice_id", "both"]
XRPLNetworkId = Literal["xrpl-testnet", "xrpl-mainnet"]


def invoice_id_to_memo_hex(invoice_id: str) -> str:
    """
    Encode an invoice id as UTF-8 and return uppercase hex suitable for MemoData.
    """
    return invoice_id.encode("utf-8").hex().upper()


def invoice_id_to_invoice_id_field(invoice_id: str) -> str:
    """
    Encode an invoice id into the XRPL Payment.InvoiceID field as SHA-256(invoice_id).
    """
    return hashlib.sha256(invoice_id.encode("utf-8")).hexdigest().upper()


def build_payment_header_for_signed_blob(
    *,
    req: PaymentRequirements,
    signed_tx_blob: str,
    invoice_id: str,
) -> str:
    """
    Build the base64 JSON envelope for the X-PAYMENT header.
    """
    payment_payload = PaymentPayload(
        x402_version="1",
        scheme=req.scheme,
        network=req.network,
        payload={"signed_tx_blob": signed_tx_blob, "invoice_id": invoice_id},
    )
    return base64.b64encode(
        json.dumps(payment_payload.to_dict(), separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).decode("utf-8")


@dataclass(frozen=True)
class XRPLPresignedPaymentPayerOptions:
    wallet: Wallet
    network: XRPLNetworkId
    rpc_url: str
    invoice_binding: InvoiceBindingMode = "both"


@dataclass(frozen=True)
class XRPLPresignedPreparedPayment:
    payment_payload: PaymentPayload
    payment_header: str
    signed_tx_blob: str
    invoice_id: str


class XRPLPresignedPaymentPayer:
    """
    Client-side helper that:
      - validates PaymentRequirements for XRPL exact presigned payments
      - builds an XRPL Payment transaction (XRP + direct IOU v1)
      - binds invoiceId into the tx (Memos and/or InvoiceID)
      - autofills + signs to a tx blob (hex)
      - returns X-PAYMENT header value (base64 JSON PaymentPayload)
    """

    def __init__(
        self,
        options: XRPLPresignedPaymentPayerOptions,
        *,
        client: Optional[JsonRpcClient] = None,
    ) -> None:
        self._options = options
        self._client = client or JsonRpcClient(options.rpc_url)

    def supports(self, req: PaymentRequirements) -> bool:
        if req.scheme != "exact":
            return False
        if req.network not in ("xrpl-testnet", "xrpl-mainnet"):
            return False
        asset = str(req.asset or "XRP")
        if asset.upper() == "XRP":
            return True
        return _issuer_from_payment_req(req) is not None

    def prepare_payment(
        self,
        req: PaymentRequirements,
        *,
        invoice_id: Optional[str] = None,
    ) -> XRPLPresignedPreparedPayment:
        if not self.supports(req):
            raise ValueError("PaymentRequirements not supported by XRPLPresignedPaymentPayer")

        inv = invoice_id or req.invoice_id
        if not inv:
            raise ValueError("invoice_id is required (expected PaymentRequirements.invoiceId)")

        memo_list: list[Memo] | None = None
        invoice_id_field: str | None = None

        if self._options.invoice_binding in ("memos", "both"):
            memo_list = [Memo(memo_data=invoice_id_to_memo_hex(inv))]

        if self._options.invoice_binding in ("invoice_id", "both"):
            invoice_id_field = invoice_id_to_invoice_id_field(inv)

        asset = str(req.asset or "XRP")
        if asset.upper() == "XRP":
            amount: str | IssuedCurrencyAmount = str(int(req.max_amount_required))
        else:
            issuer = _issuer_from_payment_req(req)
            if not issuer:
                raise ValueError('issuer is required for IOU payments (expected PaymentRequirements.extra["issuer"])')
            amount = IssuedCurrencyAmount(
                currency=to_currency_hex(asset),
                issuer=issuer,
                value=str(req.max_amount_required),
            )

        payment_tx = Payment(
            account=self._options.wallet.classic_address,
            destination=req.pay_to,
            amount=amount,
            memos=memo_list,
            invoice_id=invoice_id_field,
        )

        filled = autofill(payment_tx, self._client)
        signed = sign(filled, self._options.wallet)
        signed_blob = signed.blob()

        payment_payload = PaymentPayload(
            x402_version="1",
            scheme=req.scheme,
            network=req.network,
            payload={"signed_tx_blob": signed_blob, "invoice_id": inv},
        )
        header = base64.b64encode(
            json.dumps(payment_payload.to_dict(), separators=(",", ":"), sort_keys=True).encode("utf-8")
        ).decode("utf-8")

        return XRPLPresignedPreparedPayment(
            payment_payload=payment_payload,
            payment_header=header,
            signed_tx_blob=signed_blob,
            invoice_id=inv,
        )

    def create_payment_header(
        self,
        req: PaymentRequirements,
        *,
        invoice_id: Optional[str] = None,
    ) -> str:
        return self.prepare_payment(req, invoice_id=invoice_id).payment_header


def _issuer_from_payment_req(req: PaymentRequirements) -> Optional[str]:
    extra = req.extra
    if not isinstance(extra, Mapping):
        return None
    issuer = extra.get("issuer")
    if not isinstance(issuer, str) or not issuer:
        return None
    return issuer


def to_currency_hex(code: str) -> str:
    """
    Convert currency codes longer than 3 chars into XRPL 160-bit currency hex.

    - "USD" stays "USD"
    - "RLUSD" -> "524C555344000000000000000000000000000000"
    - 40-char hex is passed through as-is (uppercased)
    """
    code = code.strip()
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
