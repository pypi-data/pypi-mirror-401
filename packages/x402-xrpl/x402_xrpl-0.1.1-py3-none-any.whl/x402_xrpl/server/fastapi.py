from __future__ import annotations

import base64
import json
import uuid
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Mapping, Optional, Protocol, Sequence

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from x402_xrpl.facilitator import AsyncFacilitatorClient, FacilitatorClientOptions
from x402_xrpl.types import PaymentRequirements, PaymentRequiredResponse

XRPLNetworkId = str


class InvoiceStore(Protocol):
    """
    Minimal persistence contract to bind an issued invoice to its PaymentRequirements.
    (Use Redis/DB in production; memory store is fine for dev.)
    """

    async def put(
        self,
        invoice_id: str,
        reqs: Sequence[PaymentRequirements],
        *,
        ttl_seconds: int,
    ) -> None: ...

    async def get(self, invoice_id: str) -> Optional[Sequence[PaymentRequirements]]: ...

    async def consume(self, invoice_id: str) -> None: ...


@dataclass(frozen=True)
class RequireX402PaymentOption:
    """
    One accepted payment option for an x402-protected resource.

    XRPL notes:
      - For IOUs (asset != "XRP"), issuer MUST be provided (or via extra["issuer"]).
      - max_amount_required is a string:
          - XRP: drops string
          - IOU: issued-currency "value" string
    """

    asset: str
    max_amount_required: str
    issuer: Optional[str] = None
    extra: Optional[Mapping[str, Any]] = None


@dataclass(frozen=True)
class RequireX402Options:
    # required pricing fields (x402 PaymentRequirements)
    pay_to: str
    max_amount_required: str  # XRP: drops string; IOUs: XRPL issued-currency "value" string
    scheme: str = "exact"
    network: XRPLNetworkId = "xrpl-testnet"
    asset: str = "XRP"
    issuer: Optional[str] = None  # required for XRPL IOU assets (non-XRP)
    max_timeout_seconds: int = 600

    # resource metadata (recommended by spec)
    resource: Optional[str] = None  # default: request.url
    description: str = ""
    mime_type: str = "application/json"
    output_schema: Optional[dict[str, Any]] = None
    extra: Optional[Mapping[str, Any]] = None
    payment_options: Optional[Sequence[RequireX402PaymentOption]] = None

    # where to settle/verify
    facilitator: Optional[AsyncFacilitatorClient] = None
    facilitator_url: Optional[str] = None  # convenience constructor
    facilitator_headers: Optional[Mapping[str, str]] = None

    # routing
    path: Optional[str | Sequence[str]] = None  # protect all if None

    # invoice binding
    invoice_store: Optional[InvoiceStore] = None
    invoice_ttl_seconds: int = 900
    invoice_id_factory: Optional[Callable[[], str]] = None

    # settlement strategy
    settle: bool = True  # verify only if False (still spec-compatible)


class _InMemoryInvoiceStore:
    def __init__(self) -> None:
        self._data: dict[str, Sequence[PaymentRequirements]] = {}

    async def put(
        self,
        invoice_id: str,
        reqs: Sequence[PaymentRequirements],
        *,
        ttl_seconds: int,  # noqa: ARG002
    ) -> None:
        self._data[invoice_id] = reqs

    async def get(self, invoice_id: str) -> Optional[Sequence[PaymentRequirements]]:
        return self._data.get(invoice_id)

    async def consume(self, invoice_id: str) -> None:
        self._data.pop(invoice_id, None)


def _normalize_paths(path: Optional[str | Sequence[str]]) -> Optional[set[str]]:
    if path is None:
        return None
    if isinstance(path, str):
        return {path}
    return set(path)


def require_x402(
    options: RequireX402Options,
) -> Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]:
    """
    FastAPI/Starlette middleware implementing the x402 flow:
      - If no X-PAYMENT: returns 402 Payment Required with {x402Version, accepts, error}.
      - If X-PAYMENT present: calls facilitator /verify (and /settle if enabled).
      - On success: forwards request to handler and sets X-PAYMENT-RESPONSE header
        containing base64-encoded Settlement Response JSON.
    """

    protected_paths = _normalize_paths(options.path)
    invoice_store: InvoiceStore = options.invoice_store or _InMemoryInvoiceStore()

    if options.facilitator is not None:
        facilitator = options.facilitator
    elif options.facilitator_url is not None:
        facilitator = AsyncFacilitatorClient(
            FacilitatorClientOptions(
                base_url=options.facilitator_url,
                wire_format="paymentHeader",
            ),
            headers=options.facilitator_headers,
        )
    else:
        raise ValueError("RequireX402Options.facilitator or facilitator_url must be provided")

    async def middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        # Pass through CORS preflight requests so CORSMiddleware can handle them
        if request.method == "OPTIONS":
            return await call_next(request)
        if protected_paths is not None and request.url.path not in protected_paths:
            return await call_next(request)

        x_payment = request.headers.get("X-PAYMENT")
        if not x_payment:
            invoice_id = options.invoice_id_factory() if options.invoice_id_factory else uuid.uuid4().hex.upper()

            option_specs = options.payment_options
            if not option_specs:
                option_specs = [
                    RequireX402PaymentOption(
                        asset=options.asset,
                        max_amount_required=options.max_amount_required,
                        issuer=options.issuer,
                        extra=options.extra,
                    )
                ]

            reqs: list[PaymentRequirements] = []
            for opt in option_specs:
                extra: dict[str, Any] | None = dict(options.extra) if options.extra else None
                if opt.extra:
                    extra = dict(extra or {})
                    extra.update(opt.extra)

                issuer = opt.issuer or options.issuer
                if issuer:
                    extra = dict(extra or {})
                    extra["issuer"] = issuer

                reqs.append(
                    PaymentRequirements(
                        scheme=options.scheme,
                        network=options.network,
                        max_amount_required=opt.max_amount_required,
                        asset=opt.asset,
                        pay_to=options.pay_to,
                        resource=options.resource or str(request.url),
                        description=options.description,
                        max_timeout_seconds=options.max_timeout_seconds,
                        mime_type=options.mime_type,
                        output_schema=options.output_schema or {},
                        extra=extra,
                        invoice_id=invoice_id,
                    )
                )

            await invoice_store.put(invoice_id, reqs, ttl_seconds=options.invoice_ttl_seconds)

            body = PaymentRequiredResponse(
                x402_version=1,
                error="X-PAYMENT header is required",
                accepts=reqs,
            ).to_dict()
            # Include invoiceId alongside the advertised requires for easier client UX
            # and expose a convenience top-level paymentRequirements field plus
            # facilitatorBaseUrl for backwards compatibility with existing clients.
            first = body["accepts"][0]
            first["invoiceId"] = invoice_id
            body["paymentRequirements"] = first
            if options.facilitator_url:
                body["facilitatorBaseUrl"] = options.facilitator_url
            return JSONResponse(status_code=402, content=body)

        # Decode envelope so we can recover invoice_id for lookup
        try:
            decoded = json.loads(base64.b64decode(x_payment))
        except Exception as exc:  # pragma: no cover - defensive
            return JSONResponse(
                status_code=400,
                content={"error": f"invalid_x_payment_header:{exc}"},
            )

        payload = decoded.get("payload") or {}
        invoice_id = payload.get("invoice_id")
        if not invoice_id:
            return JSONResponse(status_code=400, content={"error": "missing_invoice_id"})

        stored = await invoice_store.get(invoice_id)
        if not stored:
            return JSONResponse(status_code=400, content={"error": "unknown_invoice_id"})

        stored_reqs = list(stored)
        selected_req: PaymentRequirements | None = None
        invalid_reasons: list[dict[str, Any]] = []

        for req in stored_reqs:
            verify_body = {
                "x402Version": decoded.get("x402Version", 1),
                "paymentHeader": x_payment,
                "paymentRequirements": req.to_dict(),
            }

            verify_resp = await facilitator._client.post("/verify", json=verify_body)  # type: ignore[attr-defined]
            if verify_resp.status_code != 200:
                try:
                    verify_payload = verify_resp.json()
                except Exception:  # pragma: no cover - defensive
                    verify_payload = {"raw": verify_resp.text}
                # Treat any non-200 from the facilitator as a verification failure
                # from the client's perspective and surface details in the body.
                return JSONResponse(
                    status_code=402,
                    content={
                        "error": f"verify_http_error:{verify_resp.status_code}",
                        "details": verify_payload,
                    },
                )

            verify_json = verify_resp.json()
            if verify_json.get("isValid"):
                selected_req = req
                break

            invalid_reasons.append(
                {
                    "asset": req.asset,
                    "issuer": (req.extra or {}).get("issuer") if isinstance(req.extra, dict) else None,
                    "invalidReason": verify_json.get("invalidReason"),
                }
            )

        if not selected_req:
            return JSONResponse(
                status_code=402,
                content={
                    "error": "verify_failed",
                    "invalidReasons": invalid_reasons,
                },
            )

        if options.settle:
            settle_body = {
                "x402Version": decoded.get("x402Version", 1),
                "paymentHeader": x_payment,
                "paymentRequirements": selected_req.to_dict(),
            }
            settle_resp = await facilitator._client.post("/settle", json=settle_body)  # type: ignore[attr-defined]
            if settle_resp.status_code != 200:
                try:
                    settle_payload = settle_resp.json()
                except Exception:  # pragma: no cover - defensive
                    settle_payload = {"raw": settle_resp.text}
                return JSONResponse(
                    status_code=502,
                    content={
                        "error": f"settle_http_error:{settle_resp.status_code}",
                        "details": settle_payload,
                    },
                )
            settle_json = settle_resp.json()
            if not settle_json.get("success"):
                return JSONResponse(
                    status_code=500,
                    content={"error": f"settle_failed:{settle_json.get('error')}"},
                )

            await invoice_store.consume(invoice_id)

            inner_response = await call_next(request)
            if "X-PAYMENT-RESPONSE" in settle_resp.headers:
                inner_response.headers["X-PAYMENT-RESPONSE"] = settle_resp.headers["X-PAYMENT-RESPONSE"]
            return inner_response

        # verify-only mode: forward on success without calling /settle
        return await call_next(request)

    return middleware


def require_payment(
    *,
    path: Optional[str | Sequence[str]] = None,
    price: str | int,
    pay_to_address: str,
    network: XRPLNetworkId = "xrpl-testnet",
    facilitator_url: str | None = None,
    facilitator: AsyncFacilitatorClient | None = None,
    facilitator_headers: Mapping[str, str] | None = None,
    asset: str = "XRP",
    issuer: str | None = None,
    scheme: str = "exact",
    max_timeout_seconds: int = 600,
    resource: str | None = None,
    description: str = "",
    mime_type: str = "application/json",
    output_schema: Mapping[str, Any] | None = None,
    extra: Mapping[str, Any] | None = None,
    payment_options: Sequence[RequireX402PaymentOption] | None = None,
    invoice_store: InvoiceStore | None = None,
    invoice_ttl_seconds: int = 900,
    invoice_id_factory: Callable[[], str] | None = None,
    settle: bool = True,
) -> Callable[[Request, Callable[[Request], Awaitable[Response]]], Awaitable[Response]]:
    """
    Ergonomic wrapper around require_x402(...) using XRPL-style inputs.

    Notes:
      - `path` is currently exact-match only (no wildcards/globs).
      - `price` is:
          - XRP: drops string/int (1 XRP = 1_000_000 drops)
          - IOU: issued-currency value string (e.g. "1", "1.25")
      - For IOUs (asset != "XRP"), `issuer` must be provided (or via extra["issuer"]).
    """
    options = RequireX402Options(
        pay_to=pay_to_address,
        max_amount_required=str(price),
        scheme=scheme,
        network=network,
        asset=asset,
        issuer=issuer,
        max_timeout_seconds=max_timeout_seconds,
        resource=resource,
        description=description,
        mime_type=mime_type,
        output_schema=dict(output_schema) if output_schema is not None else None,
        extra=extra,
        payment_options=payment_options,
        facilitator=facilitator,
        facilitator_url=facilitator_url,
        facilitator_headers=facilitator_headers,
        path=path,
        invoice_store=invoice_store,
        invoice_ttl_seconds=invoice_ttl_seconds,
        invoice_id_factory=invoice_id_factory,
        settle=settle,
    )
    return require_x402(options)
