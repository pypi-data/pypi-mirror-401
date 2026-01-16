"""
DSPIP SDK - DNS Record Utilities
Per Internet-Draft draft-midwestcyber-dspip-02
"""

import re
import time
from typing import Any, Literal, Optional
from urllib.parse import quote, unquote

import httpx

from .crypto import bytes_to_base64, compute_sha256, sign
from .types import (
    DNS_RECORD_VERSION,
    AddressScheme,
    AuthorityLevel,
    DSPIPDNSRecord,
    KeyStatus,
    KeyStatusResult,
    ParsedAddress,
)


def create_dns_record(
    public_key_base64: str,
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
    status: KeyStatus = KeyStatus.ACTIVE,
    creation_timestamp: Optional[int] = None,
    signing_expiration: Optional[int] = None,
    verification_expiration: Optional[int] = None,
    sequence: Optional[int] = None,
    notes: Optional[str] = None,
    types: Optional[str] = None,
    authority: Optional[AuthorityLevel] = None,
    address: Optional[str] = None,
    coverage: Optional[str] = None,
) -> DSPIPDNSRecord:
    """Create a DNS record structure.

    Args:
        public_key_base64: Public key in Base64 format
        curve: Curve type (secp256k1 or ed25519)
        status: Key status
        creation_timestamp: Key creation timestamp
        signing_expiration: When signing expires
        verification_expiration: When verification expires
        sequence: Sequence number for updates
        notes: Optional notes (will be percent-encoded)
        types: Supported types (e.g., "SHIP")
        authority: Authority level
        address: Facility address
        coverage: Covered zip codes

    Returns:
        DSPIPDNSRecord structure
    """
    return DSPIPDNSRecord(
        v=DNS_RECORD_VERSION,
        k="ec",
        c=curve,
        p=public_key_base64,
        t=creation_timestamp,
        exp=signing_expiration,
        exp_v=verification_expiration,
        s=status,
        seq=sequence,
        n=notes,
        types=types,
        auth=authority,
        address=address,
        coverage=coverage,
    )


def format_dns_record(record: DSPIPDNSRecord) -> str:
    """Format a DNS record to TXT record string.

    Args:
        record: The DNS record to format

    Returns:
        Formatted TXT record string
    """
    parts = [
        f"v={record.v}",
        f"k={record.k}",
        f"c={record.c}",
        f"p={record.p}",
    ]

    if record.t is not None:
        parts.append(f"t={record.t}")
    if record.exp is not None:
        parts.append(f"exp={record.exp}")
    if record.exp_v is not None:
        parts.append(f"exp-v={record.exp_v}")
    if record.s is not None:
        parts.append(f"s={record.s.value}")
    if record.seq is not None:
        parts.append(f"seq={record.seq}")
    if record.rsig is not None:
        parts.append(f"rsig={record.rsig}")
    if record.n is not None:
        parts.append(f"n={quote(record.n)}")
    if record.types is not None:
        parts.append(f"types={record.types}")
    if record.auth is not None:
        parts.append(f"auth={record.auth.value}")
    if record.address is not None:
        parts.append(f"address={record.address}")
    if record.coverage is not None:
        parts.append(f"coverage={record.coverage}")

    return "; ".join(parts)


def parse_dns_record(txt_record: str) -> DSPIPDNSRecord:
    """Parse a DNS TXT record string to DSPIPDNSRecord.

    Args:
        txt_record: The TXT record string

    Returns:
        Parsed DSPIPDNSRecord

    Raises:
        ValueError: If the record format is invalid
    """
    # Parse key=value pairs
    pairs: dict[str, str] = {}
    for part in txt_record.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            pairs[key.strip()] = value.strip()

    # Validate required fields
    if pairs.get("v") != DNS_RECORD_VERSION:
        raise ValueError(f"Invalid or missing version: {pairs.get('v')}")
    if "p" not in pairs:
        raise ValueError("Missing public key (p)")

    # Parse optional fields
    status = None
    if "s" in pairs:
        status = KeyStatus(pairs["s"])

    auth = None
    if "auth" in pairs:
        auth = AuthorityLevel(pairs["auth"])

    return DSPIPDNSRecord(
        v=pairs["v"],
        k=pairs.get("k", "ec"),
        c=pairs.get("c", "secp256k1"),
        p=pairs["p"],
        t=int(pairs["t"]) if "t" in pairs else None,
        exp=int(pairs["exp"]) if "exp" in pairs else None,
        exp_v=int(pairs["exp-v"]) if "exp-v" in pairs else None,
        s=status,
        seq=int(pairs["seq"]) if "seq" in pairs else None,
        rsig=pairs.get("rsig"),
        n=unquote(pairs["n"]) if "n" in pairs else None,
        types=pairs.get("types"),
        auth=auth,
        address=pairs.get("address"),
        coverage=pairs.get("coverage"),
    )


def generate_record_signature(
    record: DSPIPDNSRecord,
    private_key_hex: str,
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
) -> str:
    """Generate a signature for a DNS record.

    Args:
        record: The record to sign
        private_key_hex: Private key in hex format
        curve: Curve to use for signing

    Returns:
        Base64-encoded signature
    """
    # Create content to sign (excluding rsig)
    record_copy = DSPIPDNSRecord(
        v=record.v,
        k=record.k,
        c=record.c,
        p=record.p,
        t=record.t,
        exp=record.exp,
        exp_v=record.exp_v,
        s=record.s,
        seq=record.seq,
        n=record.n,
        types=record.types,
        auth=record.auth,
        address=record.address,
        coverage=record.coverage,
    )
    content = format_dns_record(record_copy)
    content_hash = compute_sha256(content.encode("utf-8"))
    signature = sign(content_hash, private_key_hex, curve)
    return bytes_to_base64(signature)


def create_key_lifecycle(
    public_key_base64: str,
    private_key_hex: str,
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
    signing_days: int = 365,
    verification_grace_days: int = 90,
    notes: Optional[str] = None,
    authority: Optional[AuthorityLevel] = None,
    address: Optional[str] = None,
    coverage: Optional[str] = None,
) -> DSPIPDNSRecord:
    """Create a DNS record with proper lifecycle management.

    Args:
        public_key_base64: Public key in Base64
        private_key_hex: Private key for signing the record
        curve: Curve type
        signing_days: Days until signing expiration
        verification_grace_days: Additional days for verification after signing expires
        notes: Optional notes
        authority: Authority level
        address: Facility address
        coverage: Covered zip codes

    Returns:
        DSPIPDNSRecord with lifecycle fields and signature
    """
    now = int(time.time())
    signing_exp = now + (signing_days * 24 * 60 * 60)
    verification_exp = signing_exp + (verification_grace_days * 24 * 60 * 60)

    record = create_dns_record(
        public_key_base64=public_key_base64,
        curve=curve,
        status=KeyStatus.ACTIVE,
        creation_timestamp=now,
        signing_expiration=signing_exp,
        verification_expiration=verification_exp,
        sequence=1,
        notes=notes,
        types="SHIP",
        authority=authority,
        address=address,
        coverage=coverage,
    )

    # Sign the record
    record.rsig = generate_record_signature(record, private_key_hex, curve)

    return record


# Address field parsing per Section 5.2.1


def is_plus_code(value: str) -> bool:
    """Check if a value is a valid Plus Code.

    Args:
        value: String to check

    Returns:
        True if valid Plus Code format
    """
    # Plus codes are 8+ alphanumeric chars, can have + after first 8
    pattern = r"^[23456789CFGHJMPQRVWX]{8,}\+?[23456789CFGHJMPQRVWX]*$"
    return bool(re.match(pattern, value.upper()))


def parse_address_field(address: str) -> ParsedAddress:
    """Parse an address field value.

    Args:
        address: Address field string

    Returns:
        ParsedAddress with scheme and value

    Raises:
        ValueError: If address format is invalid
    """
    # Check for scheme prefix
    if address.startswith("plus:"):
        return ParsedAddress(
            scheme=AddressScheme.PLUS,
            value=address[5:],
            raw=address,
        )
    elif address.startswith("street:"):
        return ParsedAddress(
            scheme=AddressScheme.STREET,
            value=unquote(address[7:]),
            raw=address,
        )
    elif address.startswith("geo:"):
        return ParsedAddress(
            scheme=AddressScheme.GEO,
            value=address[4:],
            raw=address,
        )
    elif address.startswith("facility:"):
        return ParsedAddress(
            scheme=AddressScheme.FACILITY,
            value=address[9:],
            raw=address,
        )
    else:
        # Default: check if it's a Plus Code
        if is_plus_code(address):
            return ParsedAddress(
                scheme=AddressScheme.PLUS,
                value=address,
                raw=address,
            )
        else:
            raise ValueError(f"Unknown address format: {address}")


def format_address_field(scheme: AddressScheme, value: str) -> str:
    """Format an address field value.

    Args:
        scheme: Address scheme
        value: Address value

    Returns:
        Formatted address string
    """
    if scheme == AddressScheme.PLUS:
        return f"plus:{value}"
    elif scheme == AddressScheme.STREET:
        return f"street:{quote(value)}"
    elif scheme == AddressScheme.GEO:
        return f"geo:{value}"
    elif scheme == AddressScheme.FACILITY:
        return f"facility:{value}"
    else:
        raise ValueError(f"Unknown address scheme: {scheme}")


def create_plus_code_address(plus_code: str) -> str:
    """Create a Plus Code address field.

    Args:
        plus_code: Plus Code value

    Returns:
        Formatted address string
    """
    return format_address_field(AddressScheme.PLUS, plus_code)


def create_street_address(street: str) -> str:
    """Create a street address field.

    Args:
        street: Street address

    Returns:
        Formatted address string (percent-encoded)
    """
    return format_address_field(AddressScheme.STREET, street)


def create_geo_address(latitude: float, longitude: float, uncertainty: Optional[float] = None) -> str:
    """Create a geo address field per RFC 5870.

    Args:
        latitude: Latitude (-90 to 90)
        longitude: Longitude (-180 to 180)
        uncertainty: Optional uncertainty in meters

    Returns:
        Formatted geo address string
    """
    value = f"{latitude},{longitude}"
    if uncertainty is not None:
        value += f";u={uncertainty}"
    return format_address_field(AddressScheme.GEO, value)


def create_facility_address(facility_id: str) -> str:
    """Create a facility address field.

    Args:
        facility_id: Facility identifier

    Returns:
        Formatted facility address string
    """
    return format_address_field(AddressScheme.FACILITY, facility_id)


# Key locator utilities


def generate_key_locator(
    selector: str,
    domain: str,
    subdomain: str = "_dspip",
) -> str:
    """Generate a key locator string.

    Args:
        selector: Key selector (e.g., "warehouse1")
        domain: Domain name
        subdomain: DSPIP subdomain (default: "_dspip")

    Returns:
        Key locator string
    """
    return f"{selector}.{subdomain}.{domain}"


def parse_key_locator(key_locator: str) -> dict[str, str]:
    """Parse a key locator string.

    Args:
        key_locator: Key locator string

    Returns:
        Dict with selector, subdomain, and domain
    """
    parts = key_locator.split(".")

    if len(parts) < 3:
        raise ValueError(f"Invalid key locator format: {key_locator}")

    # Find _dspip subdomain
    dspip_index = -1
    for i, part in enumerate(parts):
        if part == "_dspip":
            dspip_index = i
            break

    if dspip_index == -1:
        # Assume format: selector.domain.tld
        return {
            "selector": parts[0],
            "subdomain": "_dspip",
            "domain": ".".join(parts[1:]),
        }

    return {
        "selector": ".".join(parts[:dspip_index]),
        "subdomain": "_dspip",
        "domain": ".".join(parts[dspip_index + 1 :]),
    }


def check_key_status(record: DSPIPDNSRecord) -> KeyStatusResult:
    """Check if a key can be used for signing or verification.

    Args:
        record: The DNS record to check

    Returns:
        KeyStatusResult with can_sign, can_verify, and reason
    """
    now = int(time.time())
    status = record.s or KeyStatus.ACTIVE

    # Check explicit status
    if status == KeyStatus.REVOKED:
        return KeyStatusResult(
            can_sign=False,
            can_verify=False,
            status=status,
            reason="Key has been revoked",
        )

    if status == KeyStatus.VERIFY_ONLY:
        return KeyStatusResult(
            can_sign=False,
            can_verify=True,
            status=status,
            reason="Key is verify-only",
        )

    # Check signing expiration
    if record.exp and now > record.exp:
        # Signing expired, check verification expiration
        if record.exp_v and now > record.exp_v:
            return KeyStatusResult(
                can_sign=False,
                can_verify=False,
                status=KeyStatus.REVOKED,
                reason="Key has expired for both signing and verification",
            )
        return KeyStatusResult(
            can_sign=False,
            can_verify=True,
            status=KeyStatus.VERIFY_ONLY,
            reason="Key has expired for signing but can still verify",
        )

    return KeyStatusResult(
        can_sign=True,
        can_verify=True,
        status=status,
        reason=None,
    )


# DNS resolution


class MockDNSResolver:
    """Mock DNS resolver for testing."""

    def __init__(self) -> None:
        self._records: dict[str, str] = {}

    def add_record(self, key_locator: str, txt_record: str) -> None:
        """Add a mock DNS record."""
        self._records[key_locator] = txt_record

    def resolve(self, key_locator: str) -> Optional[str]:
        """Resolve a key locator to TXT record."""
        return self._records.get(key_locator)


# Global mock resolver for testing
_mock_resolver: Optional[MockDNSResolver] = None


def set_mock_resolver(resolver: Optional[MockDNSResolver]) -> None:
    """Set a mock DNS resolver for testing."""
    global _mock_resolver
    _mock_resolver = resolver


async def resolve_dns_record(
    key_locator: str,
    dns_servers: Optional[list[str]] = None,
    timeout: float = 5.0,
) -> Optional[DSPIPDNSRecord]:
    """Resolve a DNS TXT record using DNS-over-HTTPS.

    Args:
        key_locator: The key locator to resolve
        dns_servers: List of DoH servers (default: Cloudflare and Google)
        timeout: Request timeout in seconds

    Returns:
        Parsed DSPIPDNSRecord or None if not found
    """
    global _mock_resolver

    # Check mock resolver first
    if _mock_resolver:
        txt = _mock_resolver.resolve(key_locator)
        if txt:
            return parse_dns_record(txt)
        return None

    if dns_servers is None:
        dns_servers = [
            "https://cloudflare-dns.com/dns-query",
            "https://dns.google/resolve",
        ]

    async with httpx.AsyncClient(timeout=timeout) as client:
        for server in dns_servers:
            try:
                response = await client.get(
                    server,
                    params={"name": key_locator, "type": "TXT"},
                    headers={"Accept": "application/dns-json"},
                )

                if response.status_code != 200:
                    continue

                data: dict[str, Any] = response.json()

                if "Answer" not in data:
                    continue

                for answer in data["Answer"]:
                    if answer.get("type") == 16:  # TXT record
                        txt_data = answer.get("data", "")
                        # Remove quotes if present
                        if txt_data.startswith('"') and txt_data.endswith('"'):
                            txt_data = txt_data[1:-1]
                        # Check if it's a DSPIP record
                        if txt_data.startswith("v=DSPIP"):
                            return parse_dns_record(txt_data)

            except Exception:
                continue

    return None


async def resolve_public_key(
    key_locator: str,
    dns_servers: Optional[list[str]] = None,
    timeout: float = 5.0,
) -> Optional[tuple[str, str]]:
    """Resolve a public key from DNS.

    Args:
        key_locator: The key locator to resolve
        dns_servers: List of DoH servers
        timeout: Request timeout

    Returns:
        Tuple of (public_key_base64, curve) or None if not found
    """
    record = await resolve_dns_record(key_locator, dns_servers, timeout)
    if record:
        return (record.p, record.c)
    return None
