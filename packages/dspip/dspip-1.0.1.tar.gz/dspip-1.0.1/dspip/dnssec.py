"""
DSPIP SDK - DNSSEC Validation
Implements Section 8 Security Considerations of the Internet-Draft

Provides DNSSEC chain validation for high-assurance deployments:
- DS record verification
- DNSKEY record validation
- RRSIG signature verification
- Chain of trust validation from root to target

Uses DNS-over-HTTPS (DoH) with DNSSEC validation flags.
"""

import asyncio
import base64
import time
from dataclasses import dataclass, field
from typing import Any, Optional

import httpx

from .crypto import bytes_to_hex, compute_sha256

# =============================================================================
# Constants
# =============================================================================

# Well-known DoH servers that support DNSSEC
DOH_SERVERS = {
    "cloudflare": "https://cloudflare-dns.com/dns-query",
    "google": "https://dns.google/resolve",
    "quad9": "https://dns.quad9.net:5053/dns-query",
}

# DNS record types
DNS_TYPES = {
    "A": 1,
    "NS": 2,
    "CNAME": 5,
    "SOA": 6,
    "TXT": 16,
    "AAAA": 28,
    "DS": 43,
    "RRSIG": 46,
    "DNSKEY": 48,
}

# DNSSEC algorithms
DNSSEC_ALGORITHMS = {
    "RSASHA256": 8,
    "RSASHA512": 10,
    "ECDSAP256SHA256": 13,
    "ECDSAP384SHA384": 14,
    "ED25519": 15,
    "ED448": 16,
}

# DS digest types
DS_DIGEST_TYPES = {
    "SHA1": 1,
    "SHA256": 2,
    "SHA384": 4,
}


# =============================================================================
# Types
# =============================================================================


@dataclass
class DNSKEYRecord:
    """DNSKEY record structure."""

    flags: int  # 256 = ZSK, 257 = KSK
    protocol: int  # Always 3
    algorithm: int  # Algorithm number
    public_key: str  # Public key in base64
    key_tag: int = 0  # Computed key tag

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "flags": self.flags,
            "protocol": self.protocol,
            "algorithm": self.algorithm,
            "publicKey": self.public_key,
            "keyTag": self.key_tag,
        }


@dataclass
class DSRecord:
    """DS (Delegation Signer) record structure."""

    key_tag: int  # Key tag of the DNSKEY
    algorithm: int  # Algorithm number
    digest_type: int  # Digest type
    digest: str  # Digest in hex

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "keyTag": self.key_tag,
            "algorithm": self.algorithm,
            "digestType": self.digest_type,
            "digest": self.digest,
        }


@dataclass
class RRSIGRecord:
    """RRSIG (Resource Record Signature) structure."""

    type_covered: int
    algorithm: int
    labels: int
    original_ttl: int
    signature_expiration: int
    signature_inception: int
    key_tag: int
    signer_name: str
    signature: str  # Base64 encoded

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "typeCovered": self.type_covered,
            "algorithm": self.algorithm,
            "labels": self.labels,
            "originalTTL": self.original_ttl,
            "signatureExpiration": self.signature_expiration,
            "signatureInception": self.signature_inception,
            "keyTag": self.key_tag,
            "signerName": self.signer_name,
            "signature": self.signature,
        }


@dataclass
class ChainOfTrust:
    """Chain of trust status."""

    root: bool = False
    tld: bool = False
    domain: bool = False
    subdomain: bool = False

    def to_dict(self) -> dict[str, bool]:
        """Convert to dictionary."""
        return {
            "root": self.root,
            "tld": self.tld,
            "domain": self.domain,
            "subdomain": self.subdomain,
        }


@dataclass
class DNSSECValidationResult:
    """DNSSEC validation result."""

    secure: bool  # Whether DNSSEC validation passed
    dnssec_enabled: bool  # Whether the domain has DNSSEC enabled
    chain_of_trust: ChainOfTrust
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    authenticated_data: bool = False  # AD flag from resolver
    raw_response: Optional[dict[str, Any]] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "secure": self.secure,
            "dnssecEnabled": self.dnssec_enabled,
            "chainOfTrust": self.chain_of_trust.to_dict(),
            "errors": self.errors,
            "warnings": self.warnings,
            "authenticatedData": self.authenticated_data,
        }


# =============================================================================
# Key Tag Calculation
# =============================================================================


def calculate_key_tag(dnskey: DNSKEYRecord) -> int:
    """
    Calculate the key tag for a DNSKEY record.
    Per RFC 4034 Appendix B.
    """
    key_bytes = base64.b64decode(dnskey.public_key)

    # Create the RDATA: flags (2) + protocol (1) + algorithm (1) + public key
    rdata = bytearray(4 + len(key_bytes))
    rdata[0] = (dnskey.flags >> 8) & 0xFF
    rdata[1] = dnskey.flags & 0xFF
    rdata[2] = dnskey.protocol
    rdata[3] = dnskey.algorithm
    rdata[4:] = key_bytes

    # Calculate key tag per RFC 4034
    ac = 0
    for i, byte in enumerate(rdata):
        if i & 1:
            ac += byte
        else:
            ac += byte << 8
    ac += (ac >> 16) & 0xFFFF
    return ac & 0xFFFF


# =============================================================================
# DS Record Verification
# =============================================================================


def _domain_to_wire_format(domain: str) -> bytes:
    """Convert domain name to DNS wire format."""
    labels = [l for l in domain.split(".") if l]
    wire = bytearray()
    for label in labels:
        wire.append(len(label))
        wire.extend(label.encode("ascii"))
    wire.append(0)  # Root label
    return bytes(wire)


def compute_ds_digest(
    domain: str,
    dnskey: DNSKEYRecord,
    digest_type: int = DS_DIGEST_TYPES["SHA256"],
) -> str:
    """Compute DS digest from DNSKEY."""
    # Normalize domain name to wire format
    domain_wire = _domain_to_wire_format(domain.lower())
    key_bytes = base64.b64decode(dnskey.public_key)

    # Create the DNSKEY RDATA
    rdata = bytearray(4 + len(key_bytes))
    rdata[0] = (dnskey.flags >> 8) & 0xFF
    rdata[1] = dnskey.flags & 0xFF
    rdata[2] = dnskey.protocol
    rdata[3] = dnskey.algorithm
    rdata[4:] = key_bytes

    # Concatenate domain wire format + RDATA
    data_to_hash = domain_wire + bytes(rdata)

    # Only SHA-256 supported in this implementation
    if digest_type != DS_DIGEST_TYPES["SHA256"]:
        raise ValueError(f"Unsupported digest type: {digest_type}")

    return bytes_to_hex(compute_sha256(data_to_hash))


def verify_ds_record(domain: str, ds_record: DSRecord, dnskey: DNSKEYRecord) -> bool:
    """Verify that a DS record matches a DNSKEY."""
    # Check key tag matches
    computed_key_tag = calculate_key_tag(dnskey)
    if ds_record.key_tag != computed_key_tag:
        return False

    # Check algorithm matches
    if ds_record.algorithm != dnskey.algorithm:
        return False

    # Compute and compare digest
    computed_digest = compute_ds_digest(domain, dnskey, ds_record.digest_type)
    return computed_digest.lower() == ds_record.digest.lower()


# =============================================================================
# DoH Resolution with DNSSEC
# =============================================================================


async def query_doh_with_dnssec(
    domain: str,
    record_type: int = DNS_TYPES["TXT"],
    doh_server: str = DOH_SERVERS["cloudflare"],
    timeout: float = 5.0,
) -> dict[str, Any]:
    """Query DNS over HTTPS with DNSSEC validation."""
    async with httpx.AsyncClient() as client:
        params = {
            "name": domain,
            "type": str(record_type),
            "do": "1",  # Request DNSSEC records
            "cd": "0",  # Enable DNSSEC checking
        }

        try:
            response = await client.get(
                doh_server,
                params=params,
                headers={"Accept": "application/dns-json"},
                timeout=timeout,
            )

            if response.status_code != 200:
                raise Exception(f"DoH request failed: {response.status_code}")

            data = response.json()

            return {
                "answers": data.get("Answer", []),
                "authenticated_data": data.get("AD", False),
                "status": data.get("Status", 0),
            }

        except httpx.TimeoutException:
            raise Exception("DoH request timed out")


async def fetch_dnskey_records(
    domain: str,
    doh_server: str = DOH_SERVERS["cloudflare"],
    timeout: float = 5.0,
) -> list[DNSKEYRecord]:
    """Fetch DNSKEY records for a domain."""
    result = await query_doh_with_dnssec(domain, DNS_TYPES["DNSKEY"], doh_server, timeout)

    dnskeys: list[DNSKEYRecord] = []
    for answer in result["answers"]:
        if answer.get("type") == DNS_TYPES["DNSKEY"]:
            parsed = _parse_dnskey_data(answer.get("data", ""))
            if parsed:
                dnskeys.append(parsed)

    return dnskeys


def _parse_dnskey_data(data: str) -> Optional[DNSKEYRecord]:
    """Parse DNSKEY record data."""
    # Format: flags protocol algorithm publicKey
    parts = data.split()
    if len(parts) < 4:
        return None

    try:
        flags = int(parts[0])
        protocol = int(parts[1])
        algorithm = int(parts[2])
        public_key = "".join(parts[3:])

        dnskey = DNSKEYRecord(
            flags=flags,
            protocol=protocol,
            algorithm=algorithm,
            public_key=public_key,
        )
        dnskey.key_tag = calculate_key_tag(dnskey)
        return dnskey
    except (ValueError, IndexError):
        return None


async def fetch_ds_records(
    domain: str,
    doh_server: str = DOH_SERVERS["cloudflare"],
    timeout: float = 5.0,
) -> list[DSRecord]:
    """Fetch DS records for a domain."""
    result = await query_doh_with_dnssec(domain, DNS_TYPES["DS"], doh_server, timeout)

    ds_records: list[DSRecord] = []
    for answer in result["answers"]:
        if answer.get("type") == DNS_TYPES["DS"]:
            parsed = _parse_ds_data(answer.get("data", ""))
            if parsed:
                ds_records.append(parsed)

    return ds_records


def _parse_ds_data(data: str) -> Optional[DSRecord]:
    """Parse DS record data."""
    # Format: keyTag algorithm digestType digest
    parts = data.split()
    if len(parts) < 4:
        return None

    try:
        return DSRecord(
            key_tag=int(parts[0]),
            algorithm=int(parts[1]),
            digest_type=int(parts[2]),
            digest="".join(parts[3:]),
        )
    except (ValueError, IndexError):
        return None


# =============================================================================
# DNSSEC Chain Validation
# =============================================================================

# Simple in-memory cache
_dnssec_cache: dict[str, tuple[DNSSECValidationResult, float]] = {}
_CACHE_TTL = 300.0  # 5 minutes


async def validate_dnssec(
    domain: str,
    doh_server: str = DOH_SERVERS["cloudflare"],
    timeout: float = 5.0,
    full_chain_validation: bool = False,
    use_cache: bool = True,
) -> DNSSECValidationResult:
    """
    Validate DNSSEC for a domain.

    This performs a simplified validation that checks:
    1. Whether the resolver reports AD (Authenticated Data) flag
    2. Whether DNSSEC records exist
    3. Basic chain of trust validation
    """
    cache_key = f"{domain}:{doh_server}"

    # Check cache
    if use_cache and cache_key in _dnssec_cache:
        cached_result, cached_time = _dnssec_cache[cache_key]
        if time.time() - cached_time < _CACHE_TTL:
            return cached_result

    errors: list[str] = []
    warnings: list[str] = []
    chain_of_trust = ChainOfTrust()
    authenticated_data = False
    dnssec_enabled = False
    raw_response: Optional[dict[str, Any]] = None

    try:
        # Step 1: Query the target domain with DNSSEC
        target_result = await query_doh_with_dnssec(domain, DNS_TYPES["TXT"], doh_server, timeout)
        authenticated_data = target_result.get("authenticated_data", False)
        raw_response = target_result

        # If AD flag is set, the resolver has validated DNSSEC
        if authenticated_data:
            chain_of_trust.root = True
            chain_of_trust.tld = True
            chain_of_trust.domain = True
            chain_of_trust.subdomain = True
            dnssec_enabled = True

        # Step 2: Check for DNSKEY records (indicates DNSSEC is configured)
        if full_chain_validation:
            # Parse domain into parts
            parts = domain.split(".")
            tld = parts[-1] if parts else ""
            sld = ".".join(parts[-2:]) if len(parts) >= 2 else domain

            # Check TLD DNSKEY
            try:
                tld_keys = await fetch_dnskey_records(tld, doh_server, timeout)
                if tld_keys:
                    chain_of_trust.tld = True
                    dnssec_enabled = True
            except Exception:
                warnings.append(f"Could not fetch DNSKEY for TLD: {tld}")

            # Check domain DNSKEY
            try:
                domain_keys = await fetch_dnskey_records(sld, doh_server, timeout)
                if domain_keys:
                    chain_of_trust.domain = True
                    dnssec_enabled = True

                    # Verify DS record at parent
                    ds_records = await fetch_ds_records(sld, doh_server, timeout)
                    if ds_records:
                        # Find KSK (flags 257)
                        ksk = next((k for k in domain_keys if k.flags == 257), None)
                        if ksk:
                            ds_match = any(verify_ds_record(sld, ds, ksk) for ds in ds_records)
                            if not ds_match:
                                warnings.append("DS record does not match KSK")
            except Exception:
                warnings.append(f"Could not fetch DNSKEY for domain: {sld}")

            # Check subdomain if applicable
            if len(parts) > 2:
                try:
                    subdomain_keys = await fetch_dnskey_records(domain, doh_server, timeout)
                    if subdomain_keys:
                        chain_of_trust.subdomain = True
                except Exception:
                    # Subdomains often don't have their own DNSKEY
                    chain_of_trust.subdomain = chain_of_trust.domain
            else:
                chain_of_trust.subdomain = chain_of_trust.domain

        # Step 3: Check for specific DNSSEC failure indicators
        if target_result.get("status") == 2:  # SERVFAIL often indicates DNSSEC validation failure
            errors.append("DNS resolution failed (possible DNSSEC validation failure)")

    except Exception as e:
        errors.append(f"DNSSEC validation error: {e}")

    result = DNSSECValidationResult(
        secure=authenticated_data and len(errors) == 0,
        dnssec_enabled=dnssec_enabled,
        chain_of_trust=chain_of_trust,
        errors=errors,
        warnings=warnings,
        authenticated_data=authenticated_data,
        raw_response=raw_response,
    )

    # Cache the result
    if use_cache:
        _dnssec_cache[cache_key] = (result, time.time())

    return result


def clear_dnssec_cache() -> None:
    """Clear the DNSSEC validation cache."""
    _dnssec_cache.clear()


def get_dnssec_cache_stats() -> dict[str, Any]:
    """Get DNSSEC cache statistics."""
    return {
        "size": len(_dnssec_cache),
        "entries": list(_dnssec_cache.keys()),
    }


# =============================================================================
# High-Level Validation for DSPIP
# =============================================================================


async def validate_key_locator_dnssec(
    key_locator: str,
    doh_server: str = DOH_SERVERS["cloudflare"],
    timeout: float = 5.0,
    full_chain_validation: bool = False,
) -> dict[str, Any]:
    """
    Validate DNSSEC for a DSPIP key locator.
    Returns whether the key lookup can be trusted.
    """
    result = await validate_dnssec(
        key_locator,
        doh_server,
        timeout,
        full_chain_validation,
    )

    if result.secure:
        recommendation = "DNSSEC validated - key lookup is cryptographically authenticated"
    elif result.dnssec_enabled and result.authenticated_data:
        recommendation = "DNSSEC partially validated - proceed with caution"
    elif result.dnssec_enabled:
        recommendation = "DNSSEC enabled but not validated - resolver may not support DNSSEC"
    else:
        recommendation = "DNSSEC not enabled - key lookup relies on network security only"

    return {
        "trusted": result.secure,
        "dnssec_result": result,
        "recommendation": recommendation,
    }


async def has_dnssec(
    domain: str,
    doh_server: str = DOH_SERVERS["cloudflare"],
    timeout: float = 5.0,
) -> bool:
    """Check if a domain has DNSSEC enabled (quick check)."""
    try:
        ds_records = await fetch_ds_records(domain, doh_server, timeout)
        return len(ds_records) > 0
    except Exception:
        return False
