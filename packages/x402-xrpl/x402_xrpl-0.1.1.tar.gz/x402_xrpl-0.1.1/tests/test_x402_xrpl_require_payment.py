from fastapi import FastAPI
from starlette.testclient import TestClient

from x402_xrpl.server import require_payment


def test_require_payment_returns_402_with_payment_requirements():
    app = FastAPI()

    app.middleware("http")(
        require_payment(
            path="/weather",
            price="1000",
            pay_to_address="rPAYTO",
            network="xrpl-testnet",
            facilitator_url="http://example.com",
            resource="demo:weather",
            invoice_id_factory=lambda: "INV123",
        )
    )

    @app.get("/weather")
    def weather():
        return {"ok": True}

    client = TestClient(app)
    resp = client.get("/weather")

    assert resp.status_code == 402
    body = resp.json()

    assert body["x402Version"] == 1
    assert body["paymentRequirements"]["payTo"] == "rPAYTO"
    assert body["paymentRequirements"]["maxAmountRequired"] == "1000"
    assert body["paymentRequirements"]["asset"] == "XRP"
    assert body["paymentRequirements"]["invoiceId"] == "INV123"
    assert body["facilitatorBaseUrl"] == "http://example.com"

