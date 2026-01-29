# SecParse SDK

Python SDK for SecParse - Query and subscribe to SEC EDGAR filing data via GraphQL.

## Features

- Simple and intuitive API
- Support for GraphQL queries
- WebSocket-based subscriptions for real-time data
- Async/await support
- Built-in API key authentication
- Type-safe error handling

## Installation

```bash
pip install secparse
```

## Quick Start

### Queries

Query SEC filing data using GraphQL:

```python
import asyncio
from secparse import SecParseClient

async def main():
    async with SecParseClient(api_key="your-api-key") as client:
        # Query for Assets facts from Apple Inc. (CIK: 63908)
        result = await client.query("""
            query {
              Fact(
                where: {
                  Concept: {name: {_eq: "Assets"}, namespace: {_eq: "us-gaap"}}
                  isSuperseded: {_eq: false}
                  Submission: {filerCik: {_eq: "63908"}}
                  FactSegments_aggregate: {count: {predicate: {_eq: 0}}}
                }
                order_by: {effectiveDate: asc}
              ) {
                effectiveDate
                Submission {
                  Filer {
                    name
                    cik
                  }
                  type
                  accessionNumber
                }
                valueNumber
                measure
              }
            }
        """)
        print(result)

asyncio.run(main())
```

### Queries with Variables

Use variables for dynamic queries:

```python
import asyncio
from secparse import SecParseClient

async def main():
    async with SecParseClient(api_key="your-api-key") as client:
        result = await client.query(
            """
            query GetFactsByCik($cik: String!, $conceptName: String!) {
              Fact(
                where: {
                  Concept: {name: {_eq: $conceptName}, namespace: {_eq: "us-gaap"}}
                  isSuperseded: {_eq: false}
                  Submission: {filerCik: {_eq: $cik}}
                }
                limit: 10
                order_by: {effectiveDate: desc}
              ) {
                effectiveDate
                valueNumber
                Submission {
                  Filer {
                    name
                    cik
                  }
                }
              }
            }
            """,
            variables={
                "cik": "63908",  # Apple Inc.
                "conceptName": "Assets"
            }
        )
        print(result)

asyncio.run(main())
```

### Subscriptions

Subscribe to real-time SEC filing updates:

```python
import asyncio
from secparse import SecParseClient

async def main():
    client = SecParseClient(api_key="your-api-key")

    try:
        # Subscribe to new submissions from Apple Inc.
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

### Subscriptions with Variables

```python
import asyncio
from secparse import SecParseClient

async def main():
    client = SecParseClient(api_key="your-api-key")

    try:
        async for data in client.subscribe(
            """
            subscription GetSubmissions($cik: String!) {
              Submission(where: {Filer: {cik: {_eq: $cik}}}) {
                accessionNumber
                acceptedDate
                type
                Filer {
                  name
                  cik
                }
              }
            }
            """,
            variables={"cik": "63908"}
        ):
            print(f"New submission: {data}")
    finally:
        await client.close()

asyncio.run(main())
```

## Configuration

### Default Endpoints

By default, the client connects to:
- Queries: `https://secparse.com/api/graphql`
- Subscriptions: `wss://secparse.com/api/graphql/ws`

### Custom Endpoints

```python
from secparse import SecParseClient

client = SecParseClient(
    api_key="your-api-key",
    url="https://custom.secparse.com/api/graphql",
    ws_url="wss://custom.secparse.com/api/graphql/ws"
)
```

### Additional Headers

```python
client = SecParseClient(
    api_key="your-api-key",
    headers={
        "X-Custom-Header": "value"
    }
)
```

### Custom Timeout

```python
client = SecParseClient(
    api_key="your-api-key",
    timeout=60.0  # 60 seconds
)
```

## Error Handling

```python
from secparse import SecParseClient, SecParseRequestError, SecParseConnectionError

async def main():
    client = SecParseClient(api_key="your-api-key")

    try:
        result = await client.query("""
            query {
              Fact(limit: 10) {
                effectiveDate
                valueNumber
              }
            }
        """)
    except SecParseRequestError as e:
        print(f"Request error: {e}")
        print(f"GraphQL errors: {e.errors}")
        print(f"Status code: {e.status_code}")
    except SecParseConnectionError as e:
        print(f"Connection failed: {e}")
    finally:
        await client.close()
```

## Common Query Examples

### Get Company Facts

```python
query {
  Fact(
    where: {
      Concept: {name: {_eq: "Assets"}, namespace: {_eq: "us-gaap"}}
      Submission: {filerCik: {_eq: "63908"}}
      isSuperseded: {_eq: false}
    }
    order_by: {effectiveDate: desc}
    limit: 5
  ) {
    effectiveDate
    valueNumber
    measure
    Submission {
      Filer {
        name
        cik
      }
      type
      acceptedDate
    }
  }
}
```

### Get Submission Details

```python
query {
  Submission(
    where: {filerCik: {_eq: "63908"}}
    order_by: {acceptedDate: desc}
    limit: 10
  ) {
    accessionNumber
    acceptedDate
    type
    Filer {
      name
      cik
    }
  }
}
```

## Publishing to PyPI

### 1. Install build tools

```bash
pip install build twine
```

### 2. Update package metadata

Edit [pyproject.toml](pyproject.toml):
- Update `version` when releasing
- Add your name and email in `authors`
- Update URLs to your repository

### 3. Build the package

```bash
python -m build
```

### 4. Upload to PyPI

Test on TestPyPI first:

```bash
python -m twine upload --repository testpypi dist/*
```

Then upload to PyPI:

```bash
python -m twine upload dist/*
```

### 5. Install your published package

```bash
pip install secparse
```

## Development

### Install development dependencies

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Format code

```bash
black secparse
```

### Type checking

```bash
mypy secparse
```

## Requirements

- Python 3.8+
- httpx >= 0.24.0
- websockets >= 11.0

## API Key

Get your SecParse API key from [secparse.com](http://secparse.com).

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Resources

- [SecParse Website](http://secparse.com)
- [SEC EDGAR Database](https://www.sec.gov/edgar)
- [US-GAAP Taxonomy](https://www.fasb.org/xbrl)
