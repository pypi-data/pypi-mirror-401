# x402 XRPL Python SDK

This package provides a small, spec‑aligned SDK for working with x402 payments over XRPL in this repository. It is designed to be reusable by both **buyer clients** (creating `X-PAYMENT` headers) and **seller/resource servers** (verifying and settling via a facilitator).

**Note**: The XRPL `exact` flow in this repo is the **presigned `Payment` tx blob** scheme. The older **escrow-based** implementation has been removed; historical docs remain under `app/docs/xrpl-exact/escrow/`.

For an overview of the scheme and end-to-end flow, see: `app/docs/xrpl-exact/presigned-payment/README.md`.

---

## Install

```bash
pip install x402-xrpl
```

---

## Modules at a Glance

- `x402_xrpl.types`
  - Core x402 types:
    - `PaymentRequirements` – spec‑aligned requirements (string `maxAmountRequired`, `payTo`, `asset`, etc.).
      - XRPL IOU extension: include `extra={"issuer":"r..."}` when `asset != "XRP"`.
    - `PaymentPayload` – outer payment envelope (`x402Version`, `scheme`, `network`, `payload`).
    - `PaymentRequiredResponse` – `{ x402Version, error, accepts: [...] }`.
    - `FacilitatorSupportedResponse`, `PaymentVerifyResponse`, `SettlementResponse` (normalized responses from the facilitator).
- `x402_xrpl.facilitator`
  - HTTP client for x402 facilitators:
    - `FacilitatorClient` (sync).
    - `AsyncFacilitatorClient` (async).
    - `FacilitatorClientOptions`, `FacilitatorWireFormat`.
- `x402_xrpl.client`
  - Client‑side XRPL helper:
    - Presigned payments: `XRPLPresignedPaymentPayer`, `XRPLPresignedPaymentPayerOptions`, `XRPLPresignedPreparedPayment`.
- `x402_xrpl.clients`
  - Buyer-side HTTP helpers (requests-style):
    - `x402_requests`, `X402RequestsSession` – auto-handle 402 → build `X-PAYMENT` → retry.
    - `decode_x_payment_response` – decode `X-PAYMENT-RESPONSE` (base64 JSON).
    - `x402Client.default_payment_requirements_selector` – default requirement selection.
- `x402_xrpl.server`
  - Server‑side FastAPI/Starlette middleware:
    - `RequireX402Options`, `InvoiceStore`, `require_x402(...)`.

---

## Quickstart: Buyer Client (requests-style)

If you want the UX of `x402_requests(...)` (auto-handle 402), use `x402_xrpl.clients.requests`:

```python
import requests
from xrpl.wallet import Wallet

from x402_xrpl.clients.requests import x402_requests
from x402_xrpl.clients.base import decode_x_payment_response

XRPL_RPC = "https://s.altnet.rippletest.net:51234/"
RESOURCE_URL = "http://127.0.0.1:8080/xrpl-demo/resource"

wallet = Wallet.from_seed("…demo seed…")

session: requests.Session = x402_requests(
    wallet,
    rpc_url=XRPL_RPC,
    # Optional filters so most users don't write a custom selector:
    network_filter="xrpl-testnet",
    scheme_filter="exact",
)

resp = session.get(RESOURCE_URL, timeout=180)
print(resp.status_code, resp.text)

if "X-PAYMENT-RESPONSE" in resp.headers:
    settlement = decode_x_payment_response(resp.headers["X-PAYMENT-RESPONSE"])
    print("settled tx:", settlement.get("transaction"))
```

---

## Quickstart: Building a Payment Header on XRPL (Presigned Payment)

Given a 402 response body from `/xrpl-demo/resource`, you can construct `PaymentRequirements` and an `X-PAYMENT` header like this:

```python
import requests
from xrpl.wallet import Wallet

from x402_xrpl.client import XRPLPresignedPaymentPayer, XRPLPresignedPaymentPayerOptions
from x402_xrpl.types import PaymentRequirements

XRPL_RPC = "https://s.altnet.rippletest.net:51234/"
RESOURCE_URL = "http://127.0.0.1:8080/xrpl-demo/resource"

# 1) Fetch payment requirements via HTTP 402
resp = requests.get(RESOURCE_URL, timeout=60)
if resp.status_code != 402:
    resp.raise_for_status()
body = resp.json()
raw_reqs = body.get("paymentRequirements") or (body.get("accepts") or [])[0]
reqs = PaymentRequirements.from_dict(raw_reqs)

# 2) Configure payer with a funded wallet
wallet = Wallet.from_seed("…demo seed…")
payer = XRPLPresignedPaymentPayer(
    XRPLPresignedPaymentPayerOptions(
        wallet=wallet,
        network=reqs.network,  # "xrpl-testnet"
        rpc_url=XRPL_RPC,
        # Default is "both": bind invoiceId via Memos + InvoiceID.
        # invoice_binding="memos" or "invoice_id" are also supported.
    )
)

# 3) Build the presigned Payment tx + X-PAYMENT header
x_payment_header = payer.create_payment_header(reqs)

# 4) Redeem the resource
redeem = requests.get(RESOURCE_URL, headers={"X-PAYMENT": x_payment_header}, timeout=180)
print(redeem.status_code, redeem.json())
```

This flow is essentially what `tests/test_script_xrpl_presigned_flow.py` does end‑to‑end.

**IOU notes** (non-XRP assets):

- Set `reqs.asset` to the currency code (e.g. `"RLUSD"`).
- Provide the issuer as `reqs.extra["issuer"]` (classic address).
- Set `reqs.maxAmountRequired` to the XRPL issued-currency `value` string (e.g. `"1"`, `"1.25"`).

---

## Quickstart: Calling a Facilitator Directly

If you already have:

- An `X-PAYMENT` header value (`payment_header`), and
- A `PaymentRequirements` instance (`reqs`)

you can talk to the XRPL facilitator directly:

```python
from x402_xrpl.facilitator import FacilitatorClient, FacilitatorClientOptions

client = FacilitatorClient(
    FacilitatorClientOptions(
        base_url="http://127.0.0.1:8011",
        wire_format="paymentHeader",  # XRPL facilitator expects paymentHeader
    )
)

# Optional: discover supported scheme/network pairs
supported = client.supported()
for kind in supported.kinds:
    print("facilitator supports:", kind.scheme, kind.network)

# Verify
verify_result = client.verify(
    payment_header=payment_header,
    payment_requirements=reqs,
    x402_version=1,
)
if not verify_result.is_valid:
    raise RuntimeError(f"verify failed: {verify_result.invalid_reason}")

# Settle
settle_result = client.settle(
    payment_header=payment_header,
    payment_requirements=reqs,
    x402_version=1,
)
if not settle_result.success:
    raise RuntimeError(f"settle failed: {settle_result.error_reason}")

print("settled on", settle_result.network, "tx:", settle_result.transaction)
```

For async flows, use `AsyncFacilitatorClient` instead and `await` the same methods.

---

## Quickstart: Protecting a FastAPI Route with `require_x402`

To protect a route (e.g. `/xrpl-demo/resource`) with x402 XRPL payments:

```python
from fastapi import FastAPI

from x402_xrpl.server import RequireX402Options, require_x402

app = FastAPI()

options = RequireX402Options(
    pay_to="rhaDe3NBxgUSLL12N5Sxpii2xy8vSyXNG6",
    max_amount_required="1000000",
    scheme="exact",
    network="xrpl-testnet",
    asset="XRP",
    # For IOUs (asset != "XRP"), also set:
    # issuer="rISSUER...",
    max_timeout_seconds=600,
    resource="demo:xrpl-resource",
    facilitator_url="http://127.0.0.1:8011",
    path="/xrpl-demo/resource",
)

app.middleware("http")(require_x402(options))
```

Behavior:

- First request without `X-PAYMENT`:
  - Returns 402 with a spec‑style `PaymentRequirementsResponse` (`accepts`) plus convenience `paymentRequirements` and `facilitatorBaseUrl`.
- Second request with `X-PAYMENT`:
  - Middleware verifies/settles via the facilitator.
  - On success:
    - Proceeds to the route handler.
    - Copies `X-PAYMENT-RESPONSE` from facilitator → client.

The existing `/xrpl-demo/resource` route in this repo uses this pattern.

---

## Where to Look Next

- `app/docs/xrpl-exact/README.md` – index of XRPL exact approaches in this repo.
- `app/docs/xrpl-exact/presigned-payment/README.md` – presigned-`Payment` approach.
- `app/docs/xrpl-exact/presigned-payment/scheme_exact_xrpl_presigned_payment.md` – scheme spec.
- `app/docs/xrpl-exact/escrow/` – legacy escrow docs only (implementation removed).
- `tests/test_x402_xrpl_sdk.py` – pure unit tests for this package.
- `tests/test_script_xrpl_presigned_flow.py` – full XRPL + facilitator + resource server integration using presigned payments.
