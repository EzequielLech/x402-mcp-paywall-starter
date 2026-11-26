// Zero-Dependency Node.js 18+ x402 v2 & MCP Tool Paywall Starter
// Settles USDT, USDC, ETH, BNB, POL, SOL & BTC directly to your self-custody wallet.
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const MERCHANT_WALLET = process.env.PAYGATE_MERCHANT_WALLET || "0x4Ed4D0750453C027FA8398067d5af980Bcc9B6eD";
const PAYGATE_API_BASE = process.env.PAYGATE_API_BASE || "https://chainguard-studio-production.up.railway.app";
const PRICE_USD = Number(process.env.PAYGATE_PRICE_USD || "1.00");
const NETWORK = process.env.PAYGATE_NETWORK || "base";

export function buildCheckoutUrl(amountUsd = PRICE_USD, title = "x402 Node API Unlock") {
  const params = new URLSearchParams({
    merchant: MERCHANT_WALLET,
    amount: amountUsd.toFixed(2),
    network: NETWORK,
    title,
  });
  return `${PAYGATE_API_BASE}/paygate/pay?${params.toString()}`;
}

export function buildX402Challenge(resource = "/api/premium-alpha") {
  return {
    x402Version: 2,
    error: "Payment Required",
    checkoutUrl: buildCheckoutUrl(),
    accepts: [
      {
        scheme: "exact",
        network: "eip155:8453",
        asset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
        maxAmountRequired: String(Math.round(PRICE_USD * 1_000_000)),
        resource,
        payTo: MERCHANT_WALLET,
      },
    ],
  };
}

async function verifyPaidInvoice(invoiceId) {
  const clean = String(invoiceId || "").trim();
  if (!clean.startsWith("inv_")) return false;
  try {
    const res = await fetch(`${PAYGATE_API_BASE}/api/v1/paygate/invoices/${encodeURIComponent(clean)}`);
    if (!res.ok) return false;
    const data = await res.json();
    const inv = data.invoice || data;
    return (
      String(inv.status || "").toLowerCase() === "paid" &&
      String(inv.merchant_wallet || "").toLowerCase() === MERCHANT_WALLET.toLowerCase() &&
      Number(inv.amount_usd || 0) >= PRICE_USD
    );
  } catch {
    return false;
  }
}

if (process.argv.includes("--self-test")) {
  const manifest = JSON.parse(fs.readFileSync(path.join(__dirname, ".well-known", "x402.json"), "utf8"));
  if (manifest.x402Version !== 2) throw new Error("Expected x402Version 2");
  const ch = buildX402Challenge();
  if (!ch.checkoutUrl.includes("/paygate/pay?")) throw new Error("Missing checkoutUrl");
  console.log("OK: Node.js x402 & MCP paywall starter self-test passed.");
  process.exit(0);
}

const port = Number(process.env.PORT || 3000);
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url || "/", `http://localhost:${port}`);
  if (url.pathname === "/.well-known/x402.json") {
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(fs.readFileSync(path.join(__dirname, ".well-known", "x402.json"), "utf8"));
    return;
  }
  if (url.pathname === "/api/premium-alpha") {
    const invId = req.headers["x-paygate-invoice"] || "";
    if (await verifyPaidInvoice(invId)) {
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ unlocked: true, invoiceId: invId, alpha: "DIRECT_WALLET_SETTLEMENT_VERIFIED" }));
      return;
    }
    const challenge = buildX402Challenge("/api/premium-alpha");
    const b64 = Buffer.from(JSON.stringify(challenge), "utf8").toString("base64");
    res.writeHead(402, { "Content-Type": "application/json", "PAYMENT-REQUIRED": b64 });
    res.end(JSON.stringify(challenge));
    return;
  }
  res.writeHead(200, { "Content-Type": "application/json" });
  res.end(JSON.stringify({ ok: true, checkoutUrl: buildCheckoutUrl(), protectedEndpoint: "/api/premium-alpha" }));
});

server.listen(port, () => {
  console.log(`x402 & PayGate starter listening on http://localhost:${port}`);
});
