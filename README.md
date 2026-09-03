# Transaction Logger Bot

A Discord bot that posts a formatted "Transaction Completed" embed whenever
a staff member logs a completed deal — the same idea as the middleman/escrow
bots used in trading servers, but wired up for your own server.

Run `/logtransaction` and it posts an embed to your transactions channel with:

- Auto-incrementing **Order #** and a cosmetic **Order ID**
- **Category** + **item** description (Roblox, Instagram, or add your own)
- **Payment method**, **amount**, and **currency**
- **Trader rating** (stars)
- **Buyer / seller** (or "Hidden for privacy" if left blank)
- For crypto payments: **blockchain**, **transaction hash**, **confirmations**,
  and a link to view it on a block explorer

## Setup

1. **Create the bot application**
   - [Discord Developer Portal](https://discord.com/developers/applications) → New Application
   - Bot tab → Add Bot → copy the token. No privileged intents needed.

2. **Invite it to your server**
   - OAuth2 → URL Generator → scopes: `bot`, `applications.commands`
   - Bot permissions: `Send Messages`, `Embed Links`
   - Open the generated URL and add it to your server.

3. **Get your IDs**
   - User Settings → Advanced → enable Developer Mode
   - Right-click your server icon → Copy Server ID → `GUILD_ID`
   - Right-click your #transactions channel → Copy Channel ID → `TRANSACTIONS_CHANNEL_ID`
   - Right-click your middleman/staff role → Copy Role ID → `MIDDLEMAN_ROLE_ID`

4. **Configure**
   ```bash
   cp .env.example .env
   ```
   Fill in the values above. Leave `MIDDLEMAN_ROLE_ID` as `0` if anyone with
   access to the command should be able to use it.

5. **Install & run**
   ```bash
   pip install -r requirements.txt
   python bot.py
   ```

With `GUILD_ID` set, slash commands show up in your server almost instantly.
Without it, they sync globally, which can take up to an hour to appear.

## Customizing

- **Payment methods / categories** — edit `PAYMENT_CHOICES` and
  `CATEGORY_CHOICES` near the top of `bot.py`.
- **Explorer links** — add more chains to the `CRYPTO_METHODS` dict.
- **Starting order number** — `START_ORDER_NUMBER` in `.env`.
- **Footer tag** — `SERVER_TAG` in `.env`.

`/logtransaction` is a manual command a staff member runs after verifying a
deal — it doesn't touch real payments or wallets itself, it just posts the
record. Confirmation counts for crypto are entered by whoever runs the
command; wiring up live lookups against a block explorer API is a natural
next step if you want that automated.

## Worth knowing

Real-money trading of Roblox items/currency and buying or selling social
accounts both go against those platforms' terms of service, and middleman
trading servers are a common target for scams — including fake "proof" logs
used to build false trust. That's why `/logtransaction` is gated to your
middleman/staff role by default: only people with that role can post a
confirmation, so it can't be faked by a random member. Worth pairing with
clear rules in your `middleman-info` / `terms-of-service` channels.
