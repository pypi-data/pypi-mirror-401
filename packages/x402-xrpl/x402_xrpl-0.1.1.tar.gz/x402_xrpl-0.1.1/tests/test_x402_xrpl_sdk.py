import base64
import json

from x402_xrpl.types import (
    FacilitatorSupportedResponse,
    PaymentRequiredResponse,
    PaymentRequirements,
    PaymentVerifyResponse,
    SettlementResponse,
)


def test_payment_requirements_roundtrip():
    wire = {
        "scheme": "exact",
        "network": "xrpl-testnet",
        "maxAmountRequired": "1000000",
        "asset": "XRP",
        "payTo": "rPAYTO",
        "resource": "https://api.example.com/resource",
        "description": "Demo resource",
        "mimeType": "application/json",
        "outputSchema": {"type": "object"},
        "maxTimeoutSeconds": 600,
        "extra": {"foo": "bar"},
        "invoiceId": "INV123",
    }
    req = PaymentRequirements.from_dict(wire)

    assert req.scheme == "exact"
    assert req.network == "xrpl-testnet"
    assert req.max_amount_required == "1000000"
    assert req.asset == "XRP"
    assert req.pay_to == "rPAYTO"
    assert req.invoice_id == "INV123"

    back = req.to_dict()
    assert back == wire


def test_payment_requirements_from_dict_accepts_currency_and_issuer_aliases():
    wire = {
        "scheme": "exact",
        "network": "xrpl-testnet",
        "maxAmountRequired": "1.5",
        "currency": "RLUSD",
        "issuer": "rISSUER",
        "payTo": "rPAYTO",
        "resource": "demo:xrpl-resource",
        "description": "Demo IOU resource",
        "maxTimeoutSeconds": 600,
        "invoiceId": "INV123",
    }

    req = PaymentRequirements.from_dict(wire)

    assert req.asset == "RLUSD"
    assert req.extra is not None
    assert req.extra.get("issuer") == "rISSUER"

    back = req.to_dict()
    assert back["asset"] == "RLUSD"
    assert back["extra"]["issuer"] == "rISSUER"


def test_payment_required_response_to_dict():
    req = PaymentRequirements(
        scheme="exact",
        network="xrpl-testnet",
        max_amount_required="42",
        asset="XRP",
        pay_to="rPAYTO",
        resource="demo:xrpl",
        description="desc",
        max_timeout_seconds=60,
        mime_type="application/json",
        output_schema={"type": "object"},
        extra=None,
        invoice_id="INV-XYZ",
    )
    resp = PaymentRequiredResponse(x402_version=1, error="X-PAYMENT header is required", accepts=[req])
    wire = resp.to_dict()

    assert wire["x402Version"] == 1
    assert wire["error"] == "X-PAYMENT header is required"
    assert len(wire["accepts"]) == 1
    accepts0 = wire["accepts"][0]
    assert accepts0["maxAmountRequired"] == "42"
    assert accepts0["payTo"] == "rPAYTO"
    assert accepts0["invoiceId"] == "INV-XYZ"


def test_facilitator_supported_response_from_wire_kinds_and_supported():
    # Generic x402 spec style
    data_kinds = {
        "kinds": [
            {"x402Version": 1, "scheme": "exact", "network": "base-sepolia"},
            {"x402Version": 1, "scheme": "exact", "network": "xrpl-testnet"},
        ]
    }
    resp_kinds = FacilitatorSupportedResponse.from_wire(data_kinds)
    assert len(resp_kinds.kinds) == 2
    assert resp_kinds.kinds[0].scheme == "exact"
    assert resp_kinds.kinds[1].network == "xrpl-testnet"

    # XRPL facilitator style
    data_supported = {
        "supported": [
            {"scheme": "exact", "network": "xrpl-testnet"},
        ]
    }
    resp_supported = FacilitatorSupportedResponse.from_wire(data_supported)
    assert len(resp_supported.kinds) == 1
    kind = resp_supported.kinds[0]
    assert kind.scheme == "exact"
    assert kind.network == "xrpl-testnet"
    assert kind.x402_version == 1


def test_payment_verify_response_from_wire():
    data = {"isValid": True, "invalidReason": None, "payer": "0xPAYER"}
    resp = PaymentVerifyResponse.from_wire(data)
    assert resp.is_valid is True
    assert resp.invalid_reason is None
    assert resp.payer == "0xPAYER"


def test_settlement_response_from_wire_spec_shape():
    data = {
        "success": True,
        "transaction": "0xabc",
        "network": "base-sepolia",
        "payer": "0xPAYER",
        "errorReason": None,
    }
    resp = SettlementResponse.from_wire(data)
    assert resp.success is True
    assert resp.transaction == "0xabc"
    assert resp.network == "base-sepolia"
    assert resp.payer == "0xPAYER"
    assert resp.error_reason is None


def test_settlement_response_from_wire_xrpl_shape():
    data = {
        "success": False,
        "error": "verify_failed:auth_out_of_window",
        "txHash": "ABC123",
        "networkId": "xrpl-testnet",
    }
    resp = SettlementResponse.from_wire(data)
    assert resp.success is False
    assert resp.transaction == "ABC123"
    assert resp.network == "xrpl-testnet"
    assert resp.error_reason == "verify_failed:auth_out_of_window"


def test_payment_payload_encoding_matches_header_envelope_shape():
    req = PaymentRequirements(
        scheme="exact",
        network="xrpl-testnet",
        max_amount_required="1000000",
        asset="XRP",
        pay_to="rPAYTO",
        resource="demo:xrpl-resource",
        description="demo",
        max_timeout_seconds=600,
        mime_type="application/json",
        output_schema=None,
        extra=None,
        invoice_id="INV123",
    )
    payload = {
        "signed_tx_blob": "DEADBEEF",
        "invoice_id": "INV123",
    }
    env = {
        "x402Version": "1",
        "scheme": req.scheme,
        "network": req.network,
        "payload": payload,
    }
    header = base64.b64encode(
        json.dumps(env, separators=(",", ":"), sort_keys=True).encode("utf-8")
    ).decode("utf-8")

    # Ensure the header decodes back to the same envelope
    decoded = json.loads(base64.b64decode(header))
    assert decoded["x402Version"] == "1"
    assert decoded["scheme"] == "exact"
    assert decoded["network"] == "xrpl-testnet"
    assert decoded["payload"]["signed_tx_blob"] == "DEADBEEF"
