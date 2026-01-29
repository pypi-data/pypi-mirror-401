# SecParse SDK

Python SDK for SecParse - Query and subscribe to SEC EDGAR filing data via GraphQL.

## Installation

```bash
pip install secparse
```

## API Key

Get your API key at https://secparse.com

## Quick Start

### Basic Query

```python
import asyncio
from secparse import SecParseClient

async def main():
    async with SecParseClient(api_key="your-api-key") as client:
        result = await client.query("""
            query {
              Fact(
                where: {
                  Concept: {name: {_eq: "Assets"}, namespace: {_eq: "us-gaap"}}
                  Submission: {filerCik: {_eq: "63908"}}
                }
                limit: 5
              ) {
                effectiveDate
                valueNumber
                Submission {
                  Filer { name }
                }
              }
            }
        """)
        print(result)

asyncio.run(main())
```

### Real-time Subscriptions

```python
import asyncio
from secparse import SecParseClient

async def main():
    client = SecParseClient(api_key="your-api-key")

    try:
        async for data in client.subscribe("""
            subscription {
              Submission(where: {Filer: {cik: {_eq: "63908"}}}) {
                accessionNumber
                acceptedDate
              }
            }
        """):
            print(f"New submission: {data}")
    finally:
        await client.close()

asyncio.run(main())
```

## License

MIT
