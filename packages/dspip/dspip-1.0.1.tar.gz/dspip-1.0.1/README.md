# DSPIP Python SDK

Official Python implementation of the Digital Signing of Physical Items Protocol (DSPIP) per [Internet-Draft draft-midwestcyber-dspip-02](https://datatracker.ietf.org/doc/draft-midwestcyber-dspip/).

[![PyPI version](https://badge.fury.io/py/dspip.svg)](https://pypi.org/project/dspip/)
[![Python Support](https://img.shields.io/pypi/pyversions/dspip.svg)](https://pypi.org/project/dspip/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

⚠️ **BETA VERSION**: This is a pre-release implementation of the DSPIP protocol, 
currently under review by the IETF. The API may change based on feedback.

## Overview

DSPIP provides cryptographic authentication for physical items using digitally 
signed QR codes, with a focus on shipping and logistics applications.

## Installation

```bash
pip install dspip
```

Or install from source:

```bash
git clone https://github.com/MidwestCyberLLC/dspip-python.git
cd dspip-python
pip install -e .
```

## Quick Start

```python
from dspip import (
    generate_key_pair,
    create_standard_payload,
    verify_offline,
    generate_qr_code_data_url,
)

# Generate a key pair
keys = generate_key_pair()
print(f"Public Key: {keys.public_key_base64}")

# Create a shipping label
qr_data = create_standard_payload(
    issuer={"name": "Acme Corp", "address": {"country": "US"}},
    recipient={"name": "John Doe", "address": {"country": "US", "city": "New York"}},
    item_id="PKG-001",
    key_locator="warehouse._dspip.example.com",
    sender_private_key_hex=keys.private_key_hex,
)

# Generate QR code
qr_image = generate_qr_code_data_url(qr_data)

# Verify offline
result = verify_offline(qr_data, keys.public_key_base64)
print(f"Valid: {result.valid}")
```

## Features

### Key Generation

```python
from dspip import (
    generate_key_pair,
    generate_secp256k1_key_pair,
    generate_ed25519_key_pair,
)

# Generate secp256k1 key pair (default for standard/encrypted mode)
secp_keys = generate_secp256k1_key_pair()

# Generate Ed25519 key pair (for split-key mode)
ed_keys = generate_ed25519_key_pair()

# Auto-detect based on curve parameter
keys = generate_key_pair("ed25519")
```

### Privacy Modes

DSPIP supports three privacy modes:

#### Standard Mode
Recipient information is visible to all parties.

```python
from dspip import create_standard_payload

qr_data = create_standard_payload(
    issuer={"name": "Sender", "address": {"country": "US"}},
    recipient={"name": "Recipient", "address": {"country": "US"}},
    item_id="PKG-001",
    key_locator="warehouse._dspip.example.com",
    sender_private_key_hex=keys.private_key_hex,
)
```

#### Encrypted Mode
Recipient information is encrypted for the carrier.

```python
from dspip import create_encrypted_payload

qr_data = create_encrypted_payload(
    issuer={"name": "Sender", "address": {"country": "US"}},
    recipient={"name": "Recipient", "address": {"country": "US"}},
    item_id="PKG-001",
    key_locator="warehouse._dspip.example.com",
    sender_private_key_hex=sender_keys.private_key_hex,
    carrier_public_key_hex=carrier_keys.public_key_hex,
    lmp_address="plus:87G8Q2JM+HV",
)
```

#### Split-Key Mode
Recipient information is encrypted for the last-mile provider using Ed25519/X25519.

```python
from dspip import create_split_key_payload, generate_ed25519_key_pair

sender_keys = generate_ed25519_key_pair()
lmp_keys = generate_ed25519_key_pair()

qr_data = create_split_key_payload(
    issuer={"name": "Sender", "address": {"country": "US"}},
    recipient={"name": "Recipient", "address": {"country": "US"}},
    item_id="PKG-001",
    key_locator="warehouse._dspip.example.com",
    sender_private_key_hex=sender_keys.private_key_hex,
    lmp_public_key_hex=lmp_keys.public_key_hex,
    lmp_address="plus:87G8Q2JM+HV",
)
```

### DNS Records

```python
from dspip import (
    create_dns_record,
    format_dns_record,
    parse_dns_record,
    create_key_lifecycle,
)

# Create a DNS record
record = create_dns_record(
    public_key_base64=keys.public_key_base64,
    curve="secp256k1",
)

# Format for DNS TXT record
txt_record = format_dns_record(record)
# v=DSPIP1; k=ec; c=secp256k1; p=...

# Create with lifecycle management
record = create_key_lifecycle(
    public_key_base64=keys.public_key_base64,
    private_key_hex=keys.private_key_hex,
    signing_days=365,
    verification_grace_days=90,
)
```

### Address Schemes

```python
from dspip import (
    create_plus_code_address,
    create_street_address,
    create_geo_address,
    create_facility_address,
    parse_address_field,
)

# Plus Code (Google Open Location Code)
addr = create_plus_code_address("87G8Q2JM+HV")

# Street address (percent-encoded)
addr = create_street_address("123 Main St, New York, NY 10001")

# Geo coordinates (RFC 5870)
addr = create_geo_address(40.7128, -74.0060, uncertainty=10)

# Facility identifier
addr = create_facility_address("NYC-SORT-01")

# Parse any address format
parsed = parse_address_field("plus:87G8Q2JM+HV")
print(f"Scheme: {parsed.scheme}, Value: {parsed.value}")
```

### Verification

```python
import asyncio
from dspip import verify, verify_offline, verify_and_decrypt

# Offline verification with known public key
result = verify_offline(qr_data, public_key_base64)

# Online verification with DNS lookup
async def verify_label():
    result = await verify(qr_data)
    if result.valid:
        print(f"Verified! Signed by: {result.signed_by}")
    else:
        for error in result.errors:
            print(f"Error: {error.message}")

asyncio.run(verify_label())

# Verify and decrypt (for encrypted mode)
async def verify_and_decrypt_label():
    result = await verify_and_decrypt(qr_data, carrier_private_key_hex)
    if result.valid and result.decrypted_recipient:
        print(f"Recipient: {result.decrypted_recipient['recipientName']}")

asyncio.run(verify_and_decrypt_label())
```

### QR Code Generation

```python
from dspip import (
    generate_qr_code_data_url,
    generate_qr_code_svg,
    generate_qr_code_terminal,
    save_qr_code_to_file,
    will_fit_in_qr_code,
)

# Generate as data URL (for HTML img src)
data_url = generate_qr_code_data_url(qr_data)

# Generate as SVG
svg = generate_qr_code_svg(qr_data)

# Generate for terminal display
terminal = generate_qr_code_terminal(qr_data)
print(terminal)

# Save to file
save_qr_code_to_file(qr_data, "label.png")

# Check if data fits in QR code
if will_fit_in_qr_code(qr_data):
    print("Data fits in QR code")
```

## API Reference

### Types

- `KeyPair` - Key pair with hex and base64 formats
- `DSPIPPayload` - Main payload structure
- `DSPIPQRData` - QR code data structure
- `DSPIPDNSRecord` - DNS TXT record structure
- `VerificationResult` - Verification result with errors/warnings
- `PrivacyMode` - Enum: STANDARD, ENCRYPTED, SPLIT_KEY
- `KeyStatus` - Enum: ACTIVE, VERIFY_ONLY, REVOKED
- `AddressScheme` - Enum: PLUS, STREET, GEO, FACILITY

### Crypto Functions

- `generate_key_pair(curve)` - Generate key pair
- `sign(message_hash, private_key_hex, curve)` - Sign message
- `verify_signature(message_hash, signature, public_key, curve)` - Verify signature
- `ecies_encrypt(plaintext, public_key_hex)` - ECIES encryption
- `ecies_decrypt(ciphertext, private_key_hex)` - ECIES decryption
- `encrypt_for_lmp(data, sender_private_key, lmp_public_key)` - Split-key encryption
- `decrypt_as_lmp(encrypted, sender_public_key, lmp_private_key)` - Split-key decryption

### Payload Functions

- `create_standard_payload(...)` - Create standard mode payload
- `create_encrypted_payload(...)` - Create encrypted mode payload
- `create_split_key_payload(...)` - Create split-key mode payload
- `encode_payload(payload)` - Encode payload to Base64
- `decode_payload(encoded)` - Decode payload from Base64
- `serialize_qr_data(qr_data)` - Serialize to QR string
- `parse_qr_data(data)` - Parse QR string

### DNS Functions

- `create_dns_record(...)` - Create DNS record structure
- `format_dns_record(record)` - Format as TXT record string
- `parse_dns_record(txt)` - Parse TXT record string
- `resolve_dns_record(key_locator)` - Resolve via DNS-over-HTTPS
- `check_key_status(record)` - Check if key can sign/verify

### Verification Functions

- `verify(qr_data)` - Verify with DNS lookup
- `verify_offline(qr_data, public_key)` - Verify with known key
- `verify_and_decrypt(qr_data, private_key)` - Verify and decrypt

### QR Functions

- `generate_qr_code_data_url(data)` - Generate as data URL
- `generate_qr_code_svg(data)` - Generate as SVG
- `generate_qr_code_terminal(data)` - Generate for terminal
- `save_qr_code_to_file(data, path)` - Save to file
- `will_fit_in_qr_code(data)` - Check if data fits

## Revocation Lists

Revocation lists allow revoking item IDs (e.g., for lost, stolen, or damaged packages):

```python
import asyncio
from dspip import (
    create_revocation_list,
    check_revocation,
    verify_revocation_list,
    calculate_bloom_filter_size,
)

# Create a signed revocation list with Bloom filter
revocation_list = create_revocation_list(
    issuer="warehouse._dspip.acme.com",
    entries=[
        {"item_id": "TRACK-001", "revoked": int(time.time()), "reason": "lost"},
        {"item_id": "TRACK-002", "revoked": int(time.time()), "reason": "stolen"},
    ],
    private_key_hex=sender_keys.private_key_hex,
    include_bloom_filter=True,
)

# Verify the list signature
is_valid = verify_revocation_list(revocation_list, sender_keys.public_key_hex)

# Check if an item is revoked
async def check():
    result = await check_revocation(
        "TRACK-001",
        cached_list=revocation_list,
        issuer_public_key_hex=sender_keys.public_key_hex,
    )
    print(f"Revoked: {result.revoked}")  # True
    print(f"Reason: {result.entry.reason}")  # 'lost'

asyncio.run(check())

# Calculate optimal Bloom filter size
params = calculate_bloom_filter_size(10000, 0.01)  # 10k items, 1% false positive
print(f"Size: {params['size']} bits, Hash count: {params['hash_count']}")
```

## Delivery Confirmation

Cryptographic proof of delivery using challenge-response protocol:

```python
from dspip import (
    create_delivery_challenge,
    respond_to_challenge,
    verify_delivery_response,
    create_multi_party_attestation,
    add_attestation,
)

# Step 1: Carrier creates challenge
challenge = create_delivery_challenge(
    item_id="TRACK-2025-001",
    carrier_key_locator="driver._dspip.usps.gov",
    carrier_private_key_hex=carrier_keys.private_key_hex,
)

# Step 2: Recipient signs the challenge
response = respond_to_challenge(
    challenge=challenge,
    recipient_private_key_hex=recipient_keys.private_key_hex,
    recipient_public_key_hex=recipient_keys.public_key_hex,
    metadata={
        "recipient_name": "Bob Jones",
        "location": "41.2565,-95.9345",
    },
)

# Step 3: Carrier verifies and creates proof
proof = verify_delivery_response(
    challenge=challenge,
    response=response,
    carrier_private_key_hex=carrier_keys.private_key_hex,
)

print(f"Delivery verified: {proof.valid}")
print(f"Proof hash: {proof.proof_hash}")  # For blockchain recording

# Multi-party attestation for high-value deliveries
attestation = create_multi_party_attestation(proof, required_attestations=3)
attestation = add_attestation(attestation, "carrier", "carrier", carrier_keys.private_key_hex)
attestation = add_attestation(attestation, "recipient", "recipient", recipient_keys.private_key_hex)
attestation = add_attestation(attestation, "witness", "witness", witness_keys.private_key_hex)

print(f"Complete: {attestation.complete}")  # True (3/3 attestations)
```

## DNSSEC Validation

Validate the chain of trust from DNS root to key locator:

```python
import asyncio
from dspip import (
    validate_dnssec,
    validate_key_locator_dnssec,
    has_dnssec,
)

async def check_dnssec():
    # Quick check: does domain have DNSSEC?
    dnssec_enabled = await has_dnssec("example.com")
    print(f"DNSSEC enabled: {dnssec_enabled}")

    # Full validation for a key locator
    result = await validate_key_locator_dnssec(
        "warehouse._dspip.example.com",
        full_chain_validation=True,
    )
    print(f"Trusted: {result['trusted']}")
    print(f"Recommendation: {result['recommendation']}")
    # "DNSSEC validated - key lookup is cryptographically authenticated"
    # OR "DNSSEC not enabled - key lookup relies on network security only"

    # Detailed validation result
    dnssec_result = await validate_dnssec("cloudflare.com")
    print(f"Chain of trust: {dnssec_result.chain_of_trust.to_dict()}")
    # {'root': True, 'tld': True, 'domain': True, 'subdomain': True}

asyncio.run(check_dnssec())
```

## Dependencies

- `coincurve` - secp256k1 operations
- `pynacl` - Ed25519/X25519 operations
- `cryptography` - AES-GCM encryption
- `qrcode[pil]` - QR code generation
- `httpx` - Async HTTP for DNS resolution

## License

MIT License - see LICENSE file for details.
