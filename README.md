# x402 & MCP Non-Custodial Crypto Paywall Starter (Python FastAPI + Node.js 18+)

[![PayGate x402 & Checkout Gate](https://github.com/EzequielLech/x402-mcp-paywall-starter/actions/workflows/paygate.yml/badge.svg)](https://github.com/EzequielLech/x402-mcp-paywall-starter/actions/workflows/paygate.yml)
[![GitHub Marketplace](https://img.shields.io/badge/Marketplace-PayGate%20x402%20%26%20Checkout%20Gate-10b981.svg)](https://github.com/marketplace/actions/paygate-x402-crypto-checkout-gate)
[![Protocol: x402 v2](https://img.shields.io/badge/Protocol-x402%20v2-ff6600.svg)](https://chainguard-studio-production.up.railway.app/.well-known/x402.json)
[![Custody: Zero](https://img.shields.io/badge/Custody-0%25%20Direct%20to%20Wallet-10b981.svg)](https://chainguard-studio-production.up.railway.app/paygate)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Click **Use this template** above to launch a production-ready **HTTP 402 (`x402 v2`) API & Model Context Protocol (MCP) Paywall** in Python (`FastAPI`) or Node.js 18+ (`ESM`, zero npm dependencies).

Every payment settles **100% directly from buyer to your self-custody wallet** across **7 networks** (`Base`, `Polygon`, `Arbitrum`, `BNB Chain`, `Ethereum`, `Solana`, and `Bitcoin Taproot`) in `USDC`, `USDT`, `ETH`, `BNB`, `POL`, `SOL`, or `BTC` — with **0% platform cut**, **no Stripe/bank account**, and **no merchant KYC**.

---

## Included Out of the Box

| File | Purpose |
|---|---|
| [`.well-known/x402.json`](.well-known/x402.json) | Validated `x402 v2` machine-payable discovery manifest (`eip155:8453` USDC + PayGate fallback) |
| [`server_fastapi.py`](server_fastapi.py) | Runnable Python FastAPI `402 Payment Required` server with `PAYMENT-REQUIRED` header & live on-chain verification |
| [`server_express.mjs`](server_express.mjs) | Zero-dependency Node.js 18+ HTTP/Express `x402 v2` server & checkout helper |
| [`.mcp.json`](.mcp.json) | Pre-wired MCP Server config for Cursor, Claude Code, Windsurf, and OpenCode (`/paygate/mcp`) |
| [`.github/workflows/paygate.yml`](.github/workflows/paygate.yml) | Automated CI check powered by [`EzequielLech/paygate-usdt@v2.8.1`](https://github.com/marketplace/actions/paygate-x402-crypto-checkout-gate) |

---

## 60-Second Quickstart

### 1. Configure Your Self-Custody Wallet

Set your EVM (`0x...`), Solana, or Bitcoin Taproot (`bc1p...`) payout address:

```bash
export PAYGATE_MERCHANT_WALLET="0xYourSelfCustodyWalletAddress"
export PAYGATE_PRICE_USD="5.00"
export PAYGATE_NETWORK="base"
```

Also update `payTo` in `.well-known/x402.json` and `merchant-wallet` in `.github/workflows/paygate.yml`.

### 2A. Run the Node.js 18+ Paywall Server (Zero Dependencies)

```bash
node server_express.mjs --self-test
node server_express.mjs
```

### 2B. Run the Python FastAPI Paywall Server

```bash
pip install -r requirements.txt
python server_fastapi.py --self-test
python server_fastapi.py
```

### 3. Test the HTTP `402 Payment Required` Flow

```bash
curl -i http://localhost:8000/api/premium-alpha
```

Unpaid callers receive `HTTP/1.1 402 Payment Required`, a Base64-encoded `PAYMENT-REQUIRED` header compatible with autonomous x402 agents, and a 1-Click 7-chain `checkoutUrl` for human buyers. Once settled on-chain, passing `X-PayGate-Invoice: inv_...` unlocks `HTTP 200 OK`.

---

## Embed In-Page Glassmorphic Crypto Checkout on Any Website

Drop two lines into any HTML, Next.js, Astro, or React landing page to open an in-page 7-chain crypto checkout modal:

```html
<script src="https://chainguard-studio-production.up.railway.app/paygate/widget.js" defer></script>
<a href="#" data-paygate data-merchant="0xYourWallet" data-amount="29" data-network="base" data-title="Pro API Access">
  Pay $29 in Crypto (0% Fee)
</a>
```

---

## Production Upgrades & Managed Plans

Self-hosted verification and your **first 3 hosted cloud settlements are 100% free**. Scale up anytime with instant on-chain activation:

- **[Cloud Pro ($9/mo)](https://chainguard-studio-production.up.railway.app/paygate/pay?merchant=0x4Ed4D0750453C027FA8398067d5af980Bcc9B6eD&amount=9&network=base&title=PayGate+Cloud+Pro+30d&issue_pass=1&billing_days=30)** — Unlimited hosted invoices, recurring subscriptions (`customer_ref` + `billing_days`), signed `HMAC-SHA256` webhooks, Telegram VIP auto-kick bot, and 1,000 Pro API calls.
- **[Lifetime White-Label License ($79 One-Time)](https://chainguard-studio-production.up.railway.app/paygate/pay?merchant=0x4Ed4D0750453C027FA8398067d5af980Bcc9B6eD&amount=79&network=base&title=PayGate+Lifetime+White-Label+License&issue_pass=1&billing_days=3650)** — Removes all *"Powered by PayGate"* branding across every hosted checkout page for your merchant wallet forever + 25,000 Master API calls.
- **[Turnkey Done-For-You VIP Bot / SaaS Integration ($99 Deposit)](https://chainguard-studio-production.up.railway.app/paygate#b2b)** — Custom 24-hour deployment for Telegram communities, AI agencies, and SaaS teams.
- **Full SDK & Documentation:** [github.com/EzequielLech/paygate-usdt](https://github.com/EzequielLech/paygate-usdt)
