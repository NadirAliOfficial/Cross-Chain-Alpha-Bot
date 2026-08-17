# Cross-Chain Alpha Bot

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Web3](https://img.shields.io/badge/Web3.py-6.x-F16822?style=flat)](https://web3py.readthedocs.io/)
[![aiogram](https://img.shields.io/badge/aiogram-v3-blue?style=flat)](https://docs.aiogram.dev/)
[![License](https://img.shields.io/github/license/NadirAliOfficial/Cross-Chain-Alpha-Bot)](LICENSE)
[![Release](https://img.shields.io/github/v/release/NadirAliOfficial/Cross-Chain-Alpha-Bot)](https://github.com/NadirAliOfficial/Cross-Chain-Alpha-Bot/releases)

A multi-chain trading bot with a Telegram interface. Monitors DEX price feeds across Ethereum, BSC, and Solana for arbitrage opportunities, executes gas-optimized swaps via Uniswap V2/V3 and Curve Finance, and enforces per-session risk limits. Strategy selection and chain configuration are handled through an inline Telegram keyboard.

---

## Architecture

```
Telegram Bot (aiogram v3)
    │
    ├── Strategy Selector (inline keyboard)
    │   └── Sniper / Frontrunning / Sandwich / MEV / Arbitrage
    │
    ├── Chain Selector
    │   └── Ethereum / BSC / Solana
    │
    └── Credential Collection (FSM)
            │
            ▼
    Signal Engine (WebSocket price feeds)
    ├── Mempool watcher — monitors pending txns > $50k
    ├── DEX price scanner — Uniswap V2, V3, Curve
    └── Arbitrage detector — cross-DEX spread calculation
            │
            ▼
    Gas Optimizer
    ├── EIP-1559 gas pricing (maxFeePerGas / maxPriorityFeePerGas)
    ├── Gas cost vs profit check (skip if gas > 8% of expected profit)
    └── Dynamic base fee polling every 30s
            │
            ▼
    Execution Engine (Web3.py)
    ├── Route selection: Uniswap V3 vs V2 vs Curve (best price)
    ├── Slippage protection: 0.3% max
    └── Nonce manager (prevents race conditions)
            │
            ▼
    Risk Manager
    ├── Per-session max loss limit (default: 2% of wallet)
    └── Auto-halt on limit breach
```

---

## Features

- **Multi-DEX routing** — compares Uniswap V2, V3, and Curve Finance; executes on best price
- **Mempool monitoring** — detects large pending swaps (>$50k) and pre-positions ahead of price impact
- **Gas optimization** — EIP-1559 native, skips trades where gas > 8% of expected profit
- **Fast scan cycle** — arbitrage scanner runs every 0.4s via WebSocket (vs 2s polling previously)
- **Slippage protection** — 0.3% max on all non-stable pairs
- **Session risk limit** — auto-halts all trading if cumulative session loss exceeds threshold
- **Nonce race prevention** — nonce manager serializes transactions within the same block
- **Telegram interface** — full strategy and chain selection via inline keyboard, no CLI needed
- **Multi-chain support** — Ethereum, BSC, Solana in a single bot

---

## Setup

### 1. Install dependencies

```bash
pip install aiogram web3 python-dotenv aiohttp
```

### 2. Configure environment

```bash
export TELEGRAM_TOKEN=your_bot_token
export ETH_RPC=https://mainnet.infura.io/v3/YOUR_KEY
export BSC_RPC=https://bsc-dataseed.binance.org/
export SOLANA_RPC=https://api.mainnet-beta.solana.com
export MAX_SESSION_LOSS_PCT=2.0
export MAX_GAS_PCT=8.0
```

### 3. Run

```bash
python bot.py
```

---

## Supported Strategies

| Strategy | Description |
|---|---|
| **Arbitrage** | Cross-DEX price difference trades (Uniswap V2/V3/Curve) |
| **Sniper** | New token launch sniping on DEX pair creation |
| **Frontrunning** | Pre-position ahead of detected large pending swaps |
| **Sandwich** | Sandwich attack on large pending slippage txns |
| **MEV** | General maximal extractable value via flashbots bundle |

---

## Risk Controls

| Control | Default | Description |
|---|---|---|
| Max session loss | 2% of wallet | Auto-halt when breached |
| Max gas cost | 8% of profit | Skip trade if gas exceeds this |
| Max slippage | 0.3% | Hard limit on all swaps |
| Retry backoff | 3x exponential | For RPC timeouts (Arbitrum) |

---

## Project Structure

```
Cross-Chain-Alpha-Bot/
├── bot.py              # Telegram bot — FSM states, inline keyboard, strategy dispatch
├── inline.py           # Keyboard definitions
├── scanner.py          # Price feed scanner — Uniswap V2/V3/Curve
├── mempool.py          # Mempool watcher for large pending swaps
├── executor.py         # Web3 transaction builder and gas optimizer
├── risk.py             # Session loss tracking and auto-halt
├── nonce.py            # Nonce manager for concurrent tx prevention
└── README.md
```

---

## Developer

Built by **Nadir Ali Khan** — [TEAM NAK](https://github.com/NadirAliOfficial) | [Telegram](https://t.me/NAKBlockDev)
