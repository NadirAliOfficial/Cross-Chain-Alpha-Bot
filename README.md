# Cross-Chain Alpha Bot

A Telegram bot built with Python and aiogram v3 that guides users through selecting trading strategies and blockchain networks via an inline keyboard interface. Supports multi-chain operations including Solana, Ethereum, and BSC.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-Bot-26A5E4?style=flat&logo=telegram&logoColor=white)
![aiogram](https://img.shields.io/badge/aiogram-v3-blue?style=flat)

## Features

- Inline keyboard navigation for strategy and chain selection
- Supports 5 strategies: Sniper, Frontrunning, Sandwich, MEV, Pump.fun
- Multi-chain: Ethereum, BSC, Solana
- FSM-based credential collection (private key or seed phrase)
- Persistent user credential storage (JSON)
- Clean state machine flow — guided step-by-step

## Bot Flow

```
/start
  └─► Select Strategy (Sniper / Frontrunning / Sandwich / MEV / Pump.fun)
        └─► Select Network (ETH / BSC / Solana)
              └─► Enter Private Key or Seed Phrase
                    └─► Bot confirms and activates strategy
```

## Setup

```bash
pip install aiogram python-dotenv
```

Set your bot token in `bot.py`:

```python
TOKEN = "your_telegram_bot_token"
```

Run:

```bash
python bot.py
```

## Files

| File                    | Purpose                                         |
|-------------------------|-------------------------------------------------|
| `bot.py`                | Main bot — FSM states, handlers, strategy flow  |
| `inline.py`             | Inline keyboard definitions                     |
| `user_credentials.json` | Stored user credentials (auto-generated)        |

## Security Note

Credentials entered by users are stored locally in `user_credentials.json`. Never expose this file or deploy without proper encryption in production.

## License

MIT

