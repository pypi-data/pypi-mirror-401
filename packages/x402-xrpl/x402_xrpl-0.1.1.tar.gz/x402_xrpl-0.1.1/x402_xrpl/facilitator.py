from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from typing import Any, Literal, Mapping, Optional

import httpx

from .types import (
    FacilitatorSupportedResponse,
    PaymentPayload,
    PaymentRequirements,
    PaymentVerifyResponse,
    SettlementResponse,
)

FacilitatorWireFormat = Literal["paymentHeader", "paymentPayload"]


@dataclass(frozen=True)
class FacilitatorClientOptions:
    base_url: str
    timeout_seconds: float = 30.0
    wire_format: FacilitatorWireFormat = "paymentHeader"


class FacilitatorClient:
    """
    Synchronous facilitator client (good for scripts/tools).

    For FastAPI middleware, prefer AsyncFacilitatorClient to avoid blocking
    the event loop.
    """

    def __init__(
        self,
        options: FacilitatorClientOptions,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self._options = options
        self._headers = dict(headers or {})

    def _build_verify_body(
        self,
        *,
        payment_header: str,
        payment_requirements: PaymentRequirements,
        x402_version: int,
    ) -> dict[str, Any]:
        if self._options.wire_format == "paymentHeader":
            return {
                "x402Version": x402_version,
                "paymentHeader": payment_header,
                "paymentRequirements": payment_requirements.to_dict(),
            }

        # paymentPayload: decode header into its JSON envelope
        decoded = base64.b64decode(payment_header)
        envelope = json.loads(decoded)
        return {
            "paymentPayload": envelope,
            "paymentRequirements": payment_requirements.to_dict(),
        }

    def _build_settle_body(
        self,
        *,
        payment_header: str,
        payment_requirements: PaymentRequirements,
        x402_version: int,
    ) -> dict[str, Any]:
        body = self._build_verify_body(
            payment_header=payment_header,
            payment_requirements=payment_requirements,
            x402_version=x402_version,
        )
        # XRPL facilitator uses x402Version/paymentHeader/paymentRequirements;
        # generic spec uses the same verify payload for settle, so we can reuse.
        return body

    def supported(self, *, x402_version: int = 1) -> FacilitatorSupportedResponse:
        """
        Calls GET /supported and returns supported (scheme, network) pairs.
        """
        url = self._options.base_url.rstrip("/") + "/supported"
        resp = httpx.get(url, headers=self._headers, timeout=self._options.timeout_seconds)
        resp.raise_for_status()
        data = resp.json()
        return FacilitatorSupportedResponse.from_wire(data)

    def verify(
        self,
        *,
        payment_header: str,
        payment_requirements: PaymentRequirements,
        x402_version: int = 1,
    ) -> PaymentVerifyResponse:
        """
        POST /verify using either:
          - { x402Version, paymentHeader, paymentRequirements }, or
          - { paymentPayload, paymentRequirements } when wire_format="paymentPayload".
        """
        url = self._options.base_url.rstrip("/") + "/verify"
        body = self._build_verify_body(
            payment_header=payment_header,
            payment_requirements=payment_requirements,
            x402_version=x402_version,
        )
        resp = httpx.post(
            url,
            json=body,
            headers=self._headers,
            timeout=self._options.timeout_seconds,
        )
        resp.raise_for_status()
        return PaymentVerifyResponse.from_wire(resp.json())

    def settle(
        self,
        *,
        payment_header: str,
        payment_requirements: PaymentRequirements,
        x402_version: int = 1,
    ) -> SettlementResponse:
        """
        POST /settle.

        For XRPL, the facilitator returns { success, error, txHash, networkId }.
        This method normalizes that into the spec-level SettlementResponse with:
          - success
          - transaction
          - network
          - error_reason
          - payer (if available)
        """
        url = self._options.base_url.rstrip("/") + "/settle"
        body = self._build_settle_body(
            payment_header=payment_header,
            payment_requirements=payment_requirements,
            x402_version=x402_version,
        )
        resp = httpx.post(
            url,
            json=body,
            headers=self._headers,
            timeout=self._options.timeout_seconds,
        )
        resp.raise_for_status()
        return SettlementResponse.from_wire(resp.json())


class AsyncFacilitatorClient:
    """
    Async facilitator client suitable for FastAPI/Starlette middleware.
    """

    def __init__(
        self,
        options: FacilitatorClientOptions,
        *,
        headers: Optional[Mapping[str, str]] = None,
    ) -> None:
        self._options = options
        self._headers = dict(headers or {})
        self._client = httpx.AsyncClient(
            base_url=options.base_url.rstrip("/"),
            headers=self._headers,
            timeout=options.timeout_seconds,
        )

    async def aclose(self) -> None:
        await self._client.aclose()

    async def supported(self, *, x402_version: int = 1) -> FacilitatorSupportedResponse:
        resp = await self._client.get("/supported")
        resp.raise_for_status()
        return FacilitatorSupportedResponse.from_wire(resp.json())

    async def verify(
        self,
        *,
        payment_header: str,
        payment_requirements: PaymentRequirements,
        x402_version: int = 1,
    ) -> PaymentVerifyResponse:
        body = FacilitatorClientOptions(
            base_url=self._options.base_url,
            timeout_seconds=self._options.timeout_seconds,
            wire_format=self._options.wire_format,
        )
        # Reuse the synchronous helper logic via a temporary client instance to
        # avoid duplicating request shaping.
        sync_client = FacilitatorClient(body, headers=self._headers)
        shaped = sync_client._build_verify_body(
            payment_header=payment_header,
            payment_requirements=payment_requirements,
            x402_version=x402_version,
        )
        resp = await self._client.post("/verify", json=shaped)
        resp.raise_for_status()
        return PaymentVerifyResponse.from_wire(resp.json())

    async def settle(
        self,
        *,
        payment_header: str,
        payment_requirements: PaymentRequirements,
        x402_version: int = 1,
    ) -> SettlementResponse:
        sync_opts = FacilitatorClientOptions(
            base_url=self._options.base_url,
            timeout_seconds=self._options.timeout_seconds,
            wire_format=self._options.wire_format,
        )
        sync_client = FacilitatorClient(sync_opts, headers=self._headers)
        shaped = sync_client._build_settle_body(
            payment_header=payment_header,
            payment_requirements=payment_requirements,
            x402_version=x402_version,
        )
        resp = await self._client.post("/settle", json=shaped)
        resp.raise_for_status()
        return SettlementResponse.from_wire(resp.json())


