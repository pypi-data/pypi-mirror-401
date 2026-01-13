# naturalpay

Natural Payments SDK

## Installation

```bash
pip install naturalpay
# or
uv add naturalpay
```

## Quick Start

```python
from naturalpay import NaturalClient

client = NaturalClient(api_key="pk_sandbox_xxx")

# Create a payment
payment = await client.payments.create(
    recipient_email="alice@example.com",
    amount=50.00,
    memo="For consulting"
)

print(payment.transfer_id)  # txn_abc123
```

## MCP Server

Run the MCP server for AI agent integrations:

```bash
# Using uvx (recommended)
uvx naturalpay mcp serve

# Or using python module
python -m naturalpay mcp serve

# With SSE transport
uvx naturalpay mcp serve --transport sse --port 8080
```

> **Note:** We recommend `uvx` or `python -m` over global installation to avoid conflicts if you also use the TypeScript SDK (`npx @naturalpay/sdk`).

## Documentation

- [API Reference](https://docs.natural.co)
- [Examples](https://github.com/naturalpay/natural-examples)

## License

MIT
