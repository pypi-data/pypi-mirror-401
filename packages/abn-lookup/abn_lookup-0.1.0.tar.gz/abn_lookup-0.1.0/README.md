# abn-lookup

Unofficial Python client for the Australian ABN Lookup API. Provides typed responses, a simple interface, and easy integration for retrieving ABN details in Python applications. Community-driven and lightweight with zero external dependencies.

## Features

- **Zero Dependencies:** Built using Python’s standard library (`urllib`), making it lightweight and easy to install anywhere.
- **Typed Models:** Responses are mapped to Python dataclasses for excellent IDE support and autocompletion.
- **Comprehensive Search:** Supports searching by ABN, ASIC, name, postcode, charity status, and more.
- **Modern Python:** Uses modern Python 3 features and type hinting.

## Installation

```bash
pip install abn-lookup
```

## Usage

You must register for a GUID at:  
http://abr.business.gov.au/Webservices.aspx

### Initialization

```python
from abnlookup import ABNLookupClient

# Initialize client with your GUID
client = ABNLookupClient(guid="YOUR_GUID_HERE")
```

### Search by ABN

Retrieves detailed information for a specific Australian Business Number.

```python
result = client.search_by_abn("51 835 430 479")

print(f"Company: {result.legal_name.name}")
print(f"Status:  {result.abn_status.status_code}")
print(f"Type:    {result.entity_type}")
print(
    f"Address: "
    f"{result.main_business_location.state} "
    f"{result.main_business_location.postcode}"
)

# Check for specific funds (if available)
if result.approved_worker_entitlement_fund:
    print(f"AWEF: {result.approved_worker_entitlement_fund}")
```

### Search by ASIC

Retrieves detailed information using an ASIC number.

```python
result = client.search_by_asic("123 456 789")

print(f"ABN: {result.abn}")
if result.dgr_item_number:
    print(f"DGR Item: {result.dgr_item_number}")
```

### Search by Name

Returns a list of entities matching a name query.

```python
results = client.search_by_name(
    name="Test Company",
    state="NSW",
    postcode="2000",
    min_score=90,
)

for item in results:
    print(f"{item.name} (ABN: {item.abn}) - Score: {item.score}")
```

## Advanced Searches

The library supports several specialised search methods that return lists of matches.

### Search by Postcode

```python
# Get all active ABNs in a specific postcode
results = client.search_by_postcode(postcode="2000")
```

### Search by ABN Status

```python
# Specific status filters
results = client.search_by_abn_status(
    postcode="2000",
    active_only=True,
    gst_registered_only=True,
)
```

### Search by Charity

```python
results = client.search_by_charity(
    state="VIC",
    charity_type_code="ADVANCEMENT OF RELIGION",  # Optional
)
```

### Search by Registration Event

```python
# Find ABNs registered in a specific month and year
results = client.search_by_registration_event(
    month=1,
    year=2024,
    state="QLD",
)
```

## Error Handling

The library uses custom exceptions for predictable error handling.

```python
from abnlookup import (
    ABNLookupClient,
    ABNNotFoundError,
    APIConnectionError,
)

try:
    client.search_by_abn("00 000 000 000")
except ABNNotFoundError:
    print("That ABN does not exist.")
except APIConnectionError:
    print("Could not connect to the ABN Lookup service.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
```

## License

MIT
