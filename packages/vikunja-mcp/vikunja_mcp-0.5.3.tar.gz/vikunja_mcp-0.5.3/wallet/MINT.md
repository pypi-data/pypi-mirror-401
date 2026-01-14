# Minting Registration Tokens

## Quick Start

Generate minting instructions:

```bash
# 25 x 1-use tokens
./factumerit/wallet/fw mint 1 25

# 10 x 3-use tokens
./factumerit/wallet/fw mint 3 10

# 5 x 5-use tokens that expire in 30 days
./factumerit/wallet/fw mint 5 5 --expires 30

# Custom named token (for VIPs)
./factumerit/wallet/fw mint 1 1 --token FRIEND2025
```

The `mint` command outputs:
1. Render shell URL
2. Exact command to run
3. Import command to paste output

## Full Workflow Example

```bash
# 1. Generate instructions
./factumerit/wallet/fw mint 1 25

# 2. Open Render shell (URL shown in output)
# 3. Run the command shown
# 4. Copy all output
# 5. Run import command shown, paste, Ctrl+D

# 6. Verify
./factumerit/wallet/fw stats
```

## Using the Wallet

```bash
# See inventory
./factumerit/wallet/fw stats

# Pick a token for someone
./factumerit/wallet/fw pick 1 "Mom"
./factumerit/wallet/fw pick 3 "Book club"

# List available tokens
./factumerit/wallet/fw list
./factumerit/wallet/fw list 1    # Only 1-use tokens

# See who got tokens
./factumerit/wallet/fw given
```

## Options Reference

### fw mint USES [COUNT] [OPTIONS]

| Option | Description |
|--------|-------------|
| `--expires DAYS` | Token expires after N days |
| `--token STRING` | Custom token string (COUNT must be 1) |

### fw add TOKEN USES [OPTIONS]

| Option | Description |
|--------|-------------|
| `--expires DAYS` | Token expires after N days |

### fw import USES [OPTIONS]

| Option | Description |
|--------|-------------|
| `--expires DAYS` | Set expiry date for all imported tokens |

## Token Denominations

| Uses | Typical Use Case |
|------|------------------|
| 1 | Individual beta tester |
| 2 | Couple |
| 3 | Small family |
| 5 | Friend group |
| 10 | Workshop/demo |
