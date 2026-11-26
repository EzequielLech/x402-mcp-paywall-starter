"""
Zero-Custody x402 v2 & 7-Chain PayGate Checkout Starter (Python / FastAPI).
Settles 100% directly to your self-custody wallet across Base, Polygon, Arbitrum,
BSC, Ethereum, Solana, and Bitcoin Taproot with 0% platform cut.
"""
from __future__ import annotations

import base64
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

MERCHANT_WALLET = os.environ.get("PAYGATE_MERCHANT_WALLET", "0x4Ed4D0750453C027FA8398067d5af980Bcc9B6eD")
PAYGATE_API_BASE = os.environ.get("PAYGATE_API_BASE", "https://chainguard-studio-production.up.railway.app")
PRICE_USD = float(os.environ.get("PAYGATE_PRICE_USD", "1.00"))
DEFAULT_NETWORK = os.environ.get("PAYGATE_NETWORK", "base")

MANIFEST_PATH = Path(__file__).resolve().parent / ".well-known" / "x402.json"


def build_checkout_url(amount_usd: float = PRICE_USD, title: str = "x402 API Unlock") -> str:
    params = urllib.parse.urlencode(
        {
            "merchant": MERCHANT_WALLET,
            "amount": f"{amount_usd:.2f}",
            "network": DEFAULT_NETWORK,
            "title": title,
        }
    )
    return f"{PAYGATE_API_BASE}/paygate/pay?{params}"


def build_x402_challenge(resource: str = "/api/premium-alpha") -> dict:
    units = str(int(round(PRICE_USD * 1_000_000)))
    return {
        "x402Version": 2,
        "error": "Payment Required",
        "checkoutUrl": build_checkout_url(),
        "accepts": [
            {
                "scheme": "exact",
                "network": "eip155:8453",
                "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
                "maxAmountRequired": units,
                "resource": resource,
                "payTo": MERCHANT_WALLET,
                "description": f"Pay ${PRICE_USD:.2f} USDC/USDT directly to merchant wallet (0% cut).",
            }
        ],
    }


def verify_paid_invoice(invoice_id: str) -> bool:
    clean = (invoice_id or "").strip()
    if not clean.startswith("inv_"):
        return False
    url = f"{PAYGATE_API_BASE}/api/v1/paygate/invoices/{urllib.parse.quote(clean)}"
    req = urllib.request.Request(url, headers={"User-Agent": "x402PaywallStarter/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        inv = payload.get("invoice") or payload
        return (
            str(inv.get("status") or "").lower() == "paid"
            and str(inv.get("merchant_wallet") or "").lower() == MERCHANT_WALLET.lower()
            and float(inv.get("amount_usd") or 0.0) >= PRICE_USD
        )
    except Exception:
        return False


def create_fastapi_app():
    from fastapi import FastAPI, Header
    from fastapi.responses import JSONResponse

    app = FastAPI(title="x402 & MCP Non-Custodial Paywall Starter", version="1.0.0")

    @app.get("/")
    def index():
        return {
            "service": "x402 & MCP Non-Custodial Paywall Starter",
            "merchant_wallet": MERCHANT_WALLET,
            "checkout_url": build_checkout_url(),
            "protected_endpoint": "/api/premium-alpha",
            "manifest": "/.well-known/x402.json",
        }

    @app.get("/.well-known/x402.json")
    def x402_manifest():
        return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

    @app.get("/api/premium-alpha")
    def premium_alpha(x_paygate_invoice: str = Header(default="")):
        if verify_paid_invoice(x_paygate_invoice):
            return {
                "unlocked": True,
                "invoice_id": x_paygate_invoice,
                "alpha": {
                    "signal": "BASE_LIQUIDITY_EXPANSION",
                    "settlement": "100% Non-Custodial Direct-to-Wallet",
                },
            }
        challenge = build_x402_challenge("/api/premium-alpha")
        b64_header = base64.b64encode(json.dumps(challenge).encode("utf-8")).decode("ascii")
        return JSONResponse(
            status_code=402,
            content=challenge,
            headers={"PAYMENT-REQUIRED": b64_header},
        )

    return app


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        manifest_data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        assert manifest_data["x402Version"] == 2
        ch = build_x402_challenge()
        assert ch["x402Version"] == 2 and "/paygate/pay?" in ch["checkoutUrl"]
        print("OK: Python x402 starter self-test passed.")
        sys.exit(0)

    import uvicorn

    uvicorn.run(create_fastapi_app(), host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
