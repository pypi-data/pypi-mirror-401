from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, MutableMapping, Optional, Sequence


@dataclass(frozen=True)
class PaymentRequirements:
    """
    Core x402 PaymentRequirements (spec-level shape).

    All amounts are strings (uint256-as-string in atomic units).

    XRPL extension (optional):
      - For XRPL IOU payments (non-XRP), the issuer address SHOULD be provided as:
          extra = {"issuer": "<classic address>"}
        because on XRPL an issued currency is uniquely identified by (currency, issuer).
    """

    scheme: str
    network: str
    max_amount_required: str
    asset: str
    pay_to: str
    resource: str
    description: str
    max_timeout_seconds: int
    mime_type: str | None = None
    output_schema: Mapping[str, Any] | None = None
    extra: Mapping[str, Any] | None = None
    # XRPL / implementation-specific extension: invoice identifier
    invoice_id: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert to wire-format dict using spec field names (camelCase / exact keys).
        """
        data: dict[str, Any] = {
            "scheme": self.scheme,
            "network": self.network,
            "maxAmountRequired": self.max_amount_required,
            "asset": self.asset,
            "payTo": self.pay_to,
            "resource": self.resource,
            "description": self.description,
            "maxTimeoutSeconds": self.max_timeout_seconds,
        }
        if self.mime_type is not None:
            data["mimeType"] = self.mime_type
        if self.output_schema is not None:
            data["outputSchema"] = dict(self.output_schema)
        if self.extra is not None:
            data["extra"] = dict(self.extra)
        if self.invoice_id is not None:
            # XRPL-specific extension – optional but widely used in this repo.
            data["invoiceId"] = self.invoice_id
        return data

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "PaymentRequirements":
        """
        Construct from a wire-format dict (e.g., from a 402 or facilitator API).
        """
        # Some clients use "currency" instead of "asset" (XRPL terminology).
        asset = data.get("asset")
        if asset is None:
            asset = data.get("currency")

        extra = data.get("extra")
        # Convenience: accept top-level "issuer" and normalize into extra["issuer"].
        issuer = data.get("issuer")
        if issuer is not None:
            if extra is None:
                extra = {"issuer": issuer}
            elif isinstance(extra, Mapping) and "issuer" not in extra:
                merged: MutableMapping[str, Any] = dict(extra)
                merged["issuer"] = issuer
                extra = merged

        return cls(
            scheme=str(data["scheme"]),
            network=str(data["network"]),
            max_amount_required=str(data["maxAmountRequired"]),
            asset=str(asset) if asset is not None else str(data["asset"]),
            pay_to=str(data["payTo"]),
            resource=str(data["resource"]),
            description=str(data.get("description", "")),
            max_timeout_seconds=int(data["maxTimeoutSeconds"]),
            mime_type=data.get("mimeType"),
            output_schema=data.get("outputSchema"),
            extra=extra,
            invoice_id=data.get("invoiceId"),
        )


@dataclass(frozen=True)
class PaymentPayload:
    """
    x402 PaymentPayload (outer envelope, not base64-encoded).

    Note: The XRPL facilitator currently models `x402Version` as a string
    field in its internal X402Envelope, so this type stores the version
    as a string and serializes it accordingly, even though the spec treats
    it as a number.
    """

    x402_version: str
    scheme: str
    network: str
    payload: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "x402Version": self.x402_version,
            "scheme": self.scheme,
            "network": self.network,
            "payload": dict(self.payload),
        }


@dataclass(frozen=True)
class PaymentRequiredResponse:
    """
    HTTP 402 Payment Requirements response body.
    """

    x402_version: int
    error: str
    accepts: Sequence[PaymentRequirements]

    def to_dict(self) -> dict[str, Any]:
        return {
            "x402Version": self.x402_version,
            "error": self.error,
            "accepts": [req.to_dict() for req in self.accepts],
        }


@dataclass(frozen=True)
class FacilitatorKind:
    """
    Supported (scheme, network) pair with x402 version.
    """

    x402_version: int
    scheme: str
    network: str


@dataclass(frozen=True)
class FacilitatorSupportedResponse:
    """
    Normalized /supported response.

    Some facilitators return {"kinds":[...]}, others (like the XRPL facilitator)
    return {"supported":[{"scheme": "...", "network":"..."}]}.
    This type normalizes both into a single representation.
    """

    kinds: Sequence[FacilitatorKind]

    @classmethod
    def from_wire(cls, data: Mapping[str, Any]) -> "FacilitatorSupportedResponse":
        kinds_raw: Sequence[Mapping[str, Any]]
        if "kinds" in data:
            kinds_raw = data["kinds"]
        elif "supported" in data:
            kinds_raw = data["supported"]
        else:
            kinds_raw = []

        kinds: list[FacilitatorKind] = []
        for item in kinds_raw:
            x_version = item.get("x402Version", 1)
            kinds.append(
                FacilitatorKind(
                    x402_version=int(x_version),
                    scheme=str(item["scheme"]),
                    network=str(item["network"]),
                )
            )
        return cls(kinds=kinds)


@dataclass(frozen=True)
class PaymentVerifyResponse:
    """
    Normalized facilitator /verify response.
    """

    is_valid: bool
    invalid_reason: str | None = None
    payer: str | None = None

    @classmethod
    def from_wire(cls, data: Mapping[str, Any]) -> "PaymentVerifyResponse":
        return cls(
            is_valid=bool(data.get("isValid")),
            invalid_reason=data.get("invalidReason"),
            payer=data.get("payer"),
        )


@dataclass(frozen=True)
class SettlementResponse:
    """
    Normalized settlement response per the x402 spec.

    Spec fields:
      - success (bool)
      - errorReason (optional string)
      - transaction (string hash, empty if failed)
      - network (string)
      - payer (string)

    The XRPL facilitator uses {success, error, txHash, networkId};
    this SDK maps that shape into the spec fields.
    """

    success: bool
    transaction: str
    network: str
    payer: str | None = None
    error_reason: str | None = None

    @classmethod
    def from_wire(cls, data: Mapping[str, Any]) -> "SettlementResponse":
        # Generic x402 spec-style names
        if "transaction" in data or "errorReason" in data:
            return cls(
                success=bool(data.get("success")),
                transaction=str(data.get("transaction", "")),
                network=str(data.get("network", "")),
                payer=data.get("payer"),
                error_reason=data.get("errorReason"),
            )

        # XRPL facilitator shape: {success, error, txHash, networkId}
        tx_hash = str(data.get("txHash", "") or "")
        net = str(data.get("networkId", "") or data.get("network", ""))
        err = data.get("error")
        return cls(
            success=bool(data.get("success")),
            transaction=tx_hash,
            network=net,
            payer=data.get("payer"),  # usually not present for XRPL
            error_reason=err,
        )
