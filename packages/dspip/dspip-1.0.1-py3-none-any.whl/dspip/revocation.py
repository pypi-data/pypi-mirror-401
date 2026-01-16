"""
DSPIP SDK - Revocation List Management
Implements Section 5.5 of the Internet-Draft

Supports:
- JSON revocation lists
- Bloom filter for space-efficient checking
- 180-day auto-pruning
- Signed revocation lists
"""

import json
import math
import time
from dataclasses import dataclass, field
from typing import Any, Optional, Union

import httpx

from .crypto import (
    bytes_to_hex,
    compute_sha256,
    hex_to_bytes,
    sign_secp256k1,
    verify_secp256k1,
)

# =============================================================================
# Constants
# =============================================================================

# Default max age for revocation entries (180 days in seconds)
REVOCATION_MAX_AGE_SECONDS = 180 * 24 * 60 * 60

# Default Bloom filter parameters
DEFAULT_BLOOM_FILTER_SIZE = 1024 * 8  # 1KB = 8192 bits
DEFAULT_BLOOM_HASH_COUNT = 7


# =============================================================================
# Types
# =============================================================================


@dataclass
class RevocationEntry:
    """A single revocation entry."""

    item_id: str
    revoked: int  # Unix timestamp when revoked
    reason: Optional[str] = None
    expires: Optional[int] = None  # Auto-computed based on max_age

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "itemId": self.item_id,
            "revoked": self.revoked,
        }
        if self.reason:
            result["reason"] = self.reason
        if self.expires:
            result["expires"] = self.expires
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RevocationEntry":
        """Create from dictionary."""
        return cls(
            item_id=data["itemId"],
            revoked=data["revoked"],
            reason=data.get("reason"),
            expires=data.get("expires"),
        )


@dataclass
class BloomFilter:
    """Bloom filter structure for space-efficient revocation checking."""

    bits: str  # Bit array as hex string
    size: int  # Size of bit array in bits
    hash_count: int  # Number of hash functions
    item_count: int = 0  # Number of items in filter

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "bits": self.bits,
            "size": self.size,
            "hashCount": self.hash_count,
            "itemCount": self.item_count,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BloomFilter":
        """Create from dictionary."""
        return cls(
            bits=data["bits"],
            size=data["size"],
            hash_count=data["hashCount"],
            item_count=data.get("itemCount", 0),
        )


@dataclass
class RevocationList:
    """Revocation list with optional Bloom filter."""

    version: str
    issuer: str
    ts: int  # Creation timestamp
    max_age: int
    updated: int
    expires: int
    revoked: list[RevocationEntry]
    signature: str
    bloom: Optional[BloomFilter] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "version": self.version,
            "issuer": self.issuer,
            "ts": self.ts,
            "max-age": self.max_age,
            "updated": self.updated,
            "expires": self.expires,
            "revoked": [e.to_dict() for e in self.revoked],
            "signature": self.signature,
        }
        if self.bloom:
            result["bloom"] = self.bloom.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "RevocationList":
        """Create from dictionary."""
        bloom = None
        if "bloom" in data and data["bloom"]:
            bloom = BloomFilter.from_dict(data["bloom"])
        return cls(
            version=data["version"],
            issuer=data["issuer"],
            ts=data["ts"],
            max_age=data["max-age"],
            updated=data["updated"],
            expires=data["expires"],
            revoked=[RevocationEntry.from_dict(e) for e in data["revoked"]],
            signature=data["signature"],
            bloom=bloom,
        )


@dataclass
class RevocationCheckResult:
    """Result of revocation check."""

    revoked: bool
    entry: Optional[RevocationEntry] = None
    used_bloom_filter: bool = False
    signature_verified: bool = False
    error: Optional[str] = None


# =============================================================================
# Bloom Filter Implementation
# =============================================================================


def create_bloom_filter(
    size: int = DEFAULT_BLOOM_FILTER_SIZE,
    hash_count: int = DEFAULT_BLOOM_HASH_COUNT,
) -> BloomFilter:
    """Create an empty Bloom filter."""
    byte_size = (size + 7) // 8
    bits = bytes(byte_size)
    return BloomFilter(
        bits=bytes_to_hex(bits),
        size=size,
        hash_count=hash_count,
        item_count=0,
    )


def _bloom_hashes(item: str, size: int, count: int) -> list[int]:
    """
    Compute multiple hash values for Bloom filter.
    Uses double hashing: h(i) = h1 + i * h2
    """
    hash_bytes = compute_sha256(item)

    # First hash (bytes 0-3)
    h1 = int.from_bytes(hash_bytes[0:4], "big")

    # Second hash (bytes 4-7)
    h2 = int.from_bytes(hash_bytes[4:8], "big")

    hashes = []
    for i in range(count):
        hashes.append(abs((h1 + i * h2) % size))
    return hashes


def bloom_filter_add(filter: BloomFilter, item_id: str) -> BloomFilter:
    """Add an item to a Bloom filter."""
    bits = bytearray(hex_to_bytes(filter.bits))
    hashes = _bloom_hashes(item_id, filter.size, filter.hash_count)

    for hash_val in hashes:
        byte_index = hash_val // 8
        bit_index = hash_val % 8
        bits[byte_index] |= 1 << bit_index

    return BloomFilter(
        bits=bytes_to_hex(bytes(bits)),
        size=filter.size,
        hash_count=filter.hash_count,
        item_count=filter.item_count + 1,
    )


def bloom_filter_check(filter: BloomFilter, item_id: str) -> bool:
    """
    Check if an item might be in a Bloom filter.
    Returns True if possibly present, False if definitely not present.
    """
    bits = hex_to_bytes(filter.bits)
    hashes = _bloom_hashes(item_id, filter.size, filter.hash_count)

    for hash_val in hashes:
        byte_index = hash_val // 8
        bit_index = hash_val % 8
        if (bits[byte_index] & (1 << bit_index)) == 0:
            return False  # Definitely not present
    return True  # Possibly present


def calculate_bloom_filter_size(
    expected_items: int,
    false_positive_rate: float = 0.01,
) -> dict[str, int]:
    """
    Calculate optimal Bloom filter size for expected number of items.

    Args:
        expected_items: Number of items expected
        false_positive_rate: Desired false positive rate (default: 0.01 = 1%)

    Returns:
        Dictionary with 'size' (bits) and 'hash_count'
    """
    # m = -n * ln(p) / (ln(2)^2)
    ln2 = math.log(2)
    size = int(math.ceil((-expected_items * math.log(false_positive_rate)) / (ln2 * ln2)))
    # k = (m/n) * ln(2)
    hash_count = int(math.ceil((size / expected_items) * ln2))
    return {"size": size, "hash_count": min(hash_count, 16)}  # Cap at 16


# =============================================================================
# Revocation List Management
# =============================================================================


def create_revocation_list(
    issuer: str,
    entries: list[dict[str, Any]],
    private_key_hex: str,
    max_age: int = REVOCATION_MAX_AGE_SECONDS,
    include_bloom_filter: bool = True,
    bloom_filter_size: Optional[int] = None,
) -> RevocationList:
    """
    Create a signed revocation list.

    Args:
        issuer: Key locator of the issuer
        entries: List of entries to revoke (dicts with item_id, revoked, reason)
        private_key_hex: Private key to sign the list
        max_age: Max age in seconds (default: 180 days)
        include_bloom_filter: Include Bloom filter for fast checking
        bloom_filter_size: Custom Bloom filter size in bits
    """
    now = int(time.time())
    expires_at = now + max_age

    # Add expiration to entries and filter out already-expired entries
    revoked_entries: list[RevocationEntry] = []
    for entry in entries:
        expires = entry.get("revoked", now) + max_age
        if expires > now:  # Not expired yet
            revoked_entries.append(
                RevocationEntry(
                    item_id=entry["item_id"],
                    revoked=entry.get("revoked", now),
                    reason=entry.get("reason"),
                    expires=expires,
                )
            )

    # Create Bloom filter if requested
    bloom: Optional[BloomFilter] = None
    if include_bloom_filter and revoked_entries:
        if bloom_filter_size:
            params = {"size": bloom_filter_size, "hash_count": DEFAULT_BLOOM_HASH_COUNT}
        else:
            params = calculate_bloom_filter_size(max(len(revoked_entries), 100))

        bloom = create_bloom_filter(params["size"], params["hash_count"])
        for entry in revoked_entries:
            bloom = bloom_filter_add(bloom, entry.item_id)

    # Create the list (without signature first)
    revocation_list = RevocationList(
        version="1.0",
        issuer=issuer,
        ts=now,
        max_age=max_age,
        updated=now,
        expires=expires_at,
        revoked=revoked_entries,
        signature="",
        bloom=bloom,
    )

    # Sign the list
    signable_content = json.dumps(
        {
            "version": revocation_list.version,
            "issuer": revocation_list.issuer,
            "ts": revocation_list.ts,
            "max-age": revocation_list.max_age,
            "updated": revocation_list.updated,
            "expires": revocation_list.expires,
            "revoked": [e.to_dict() for e in revocation_list.revoked],
            "bloom": revocation_list.bloom.to_dict() if revocation_list.bloom else None,
        },
        separators=(",", ":"),
        sort_keys=True,
    )

    revocation_list.signature = sign_secp256k1(signable_content, private_key_hex)

    return revocation_list


def verify_revocation_list(
    revocation_list: RevocationList,
    issuer_public_key_hex: str,
) -> bool:
    """Verify a revocation list signature."""
    signable_content = json.dumps(
        {
            "version": revocation_list.version,
            "issuer": revocation_list.issuer,
            "ts": revocation_list.ts,
            "max-age": revocation_list.max_age,
            "updated": revocation_list.updated,
            "expires": revocation_list.expires,
            "revoked": [e.to_dict() for e in revocation_list.revoked],
            "bloom": revocation_list.bloom.to_dict() if revocation_list.bloom else None,
        },
        separators=(",", ":"),
        sort_keys=True,
    )

    return verify_secp256k1(signable_content, revocation_list.signature, issuer_public_key_hex)


def add_revocation_entry(
    revocation_list: RevocationList,
    entry: dict[str, Any],
    private_key_hex: str,
) -> RevocationList:
    """Add an entry to an existing revocation list."""
    now = int(time.time())
    new_entry = RevocationEntry(
        item_id=entry["item_id"],
        revoked=entry.get("revoked", now),
        reason=entry.get("reason"),
        expires=now + revocation_list.max_age,
    )

    # Add to revoked list
    new_revoked = revocation_list.revoked + [new_entry]

    # Update Bloom filter if present
    new_bloom = revocation_list.bloom
    if new_bloom:
        new_bloom = bloom_filter_add(new_bloom, entry["item_id"])

    # Create updated list
    updated_list = RevocationList(
        version=revocation_list.version,
        issuer=revocation_list.issuer,
        ts=revocation_list.ts,
        max_age=revocation_list.max_age,
        updated=now,
        expires=revocation_list.expires,
        revoked=new_revoked,
        signature="",
        bloom=new_bloom,
    )

    # Re-sign
    signable_content = json.dumps(
        {
            "version": updated_list.version,
            "issuer": updated_list.issuer,
            "ts": updated_list.ts,
            "max-age": updated_list.max_age,
            "updated": updated_list.updated,
            "expires": updated_list.expires,
            "revoked": [e.to_dict() for e in updated_list.revoked],
            "bloom": updated_list.bloom.to_dict() if updated_list.bloom else None,
        },
        separators=(",", ":"),
        sort_keys=True,
    )

    updated_list.signature = sign_secp256k1(signable_content, private_key_hex)

    return updated_list


def prune_revocation_list(
    revocation_list: RevocationList,
    private_key_hex: str,
) -> RevocationList:
    """Prune expired entries from a revocation list."""
    now = int(time.time())

    # Filter out expired entries
    pruned_revoked = [
        entry
        for entry in revocation_list.revoked
        if not entry.expires or entry.expires > now
    ]

    # Rebuild Bloom filter with remaining entries
    new_bloom: Optional[BloomFilter] = None
    if revocation_list.bloom and pruned_revoked:
        params = calculate_bloom_filter_size(max(len(pruned_revoked), 100))
        new_bloom = create_bloom_filter(params["size"], params["hash_count"])
        for entry in pruned_revoked:
            new_bloom = bloom_filter_add(new_bloom, entry.item_id)

    # Create pruned list
    pruned_list = RevocationList(
        version=revocation_list.version,
        issuer=revocation_list.issuer,
        ts=revocation_list.ts,
        max_age=revocation_list.max_age,
        updated=now,
        expires=revocation_list.expires,
        revoked=pruned_revoked,
        signature="",
        bloom=new_bloom,
    )

    # Re-sign
    signable_content = json.dumps(
        {
            "version": pruned_list.version,
            "issuer": pruned_list.issuer,
            "ts": pruned_list.ts,
            "max-age": pruned_list.max_age,
            "updated": pruned_list.updated,
            "expires": pruned_list.expires,
            "revoked": [e.to_dict() for e in pruned_list.revoked],
            "bloom": pruned_list.bloom.to_dict() if pruned_list.bloom else None,
        },
        separators=(",", ":"),
        sort_keys=True,
    )

    pruned_list.signature = sign_secp256k1(signable_content, private_key_hex)

    return pruned_list


# =============================================================================
# Revocation Checking
# =============================================================================


async def check_revocation(
    item_id: str,
    cached_list: Optional[RevocationList] = None,
    fetch_url: Optional[str] = None,
    issuer_public_key_hex: Optional[str] = None,
    skip_verification: bool = False,
) -> RevocationCheckResult:
    """
    Check if an item is revoked.

    Args:
        item_id: Item ID to check
        cached_list: Use cached revocation list
        fetch_url: URL to fetch revocation list from
        issuer_public_key_hex: Public key to verify list signature
        skip_verification: Skip signature verification
    """
    revocation_list = cached_list

    # Fetch list if URL provided
    if fetch_url and not revocation_list:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(fetch_url)
                if response.status_code != 200:
                    return RevocationCheckResult(
                        revoked=False,
                        error=f"Failed to fetch revocation list: {response.status_code}",
                    )
                data = response.json()
                revocation_list = RevocationList.from_dict(data)
        except Exception as e:
            return RevocationCheckResult(
                revoked=False,
                error=f"Network error fetching revocation list: {e}",
            )

    if not revocation_list:
        return RevocationCheckResult(
            revoked=False,
            error="No revocation list available",
        )

    # Verify signature if public key provided
    signature_verified = False
    if issuer_public_key_hex and not skip_verification:
        signature_verified = verify_revocation_list(revocation_list, issuer_public_key_hex)
        if not signature_verified:
            return RevocationCheckResult(
                revoked=False,
                signature_verified=False,
                error="Revocation list signature invalid",
            )

    # Check if list is expired
    now = int(time.time())
    if revocation_list.expires and revocation_list.expires < now:
        return RevocationCheckResult(
            revoked=False,
            signature_verified=signature_verified,
            error="Revocation list expired",
        )

    # Fast path: check Bloom filter first
    used_bloom = False
    if revocation_list.bloom:
        if not bloom_filter_check(revocation_list.bloom, item_id):
            # Definitely not revoked
            return RevocationCheckResult(
                revoked=False,
                used_bloom_filter=True,
                signature_verified=signature_verified,
            )
        used_bloom = True
        # Might be revoked, need to check full list

    # Check full list
    for entry in revocation_list.revoked:
        if entry.item_id == item_id:
            # Check if entry itself is expired
            if entry.expires and entry.expires < now:
                return RevocationCheckResult(
                    revoked=False,
                    used_bloom_filter=used_bloom,
                    signature_verified=signature_verified,
                )
            return RevocationCheckResult(
                revoked=True,
                entry=entry,
                used_bloom_filter=used_bloom,
                signature_verified=signature_verified,
            )

    return RevocationCheckResult(
        revoked=False,
        used_bloom_filter=used_bloom,
        signature_verified=signature_verified,
    )


async def check_revocation_batch(
    item_ids: list[str],
    cached_list: Optional[RevocationList] = None,
    fetch_url: Optional[str] = None,
    issuer_public_key_hex: Optional[str] = None,
    skip_verification: bool = False,
) -> dict[str, RevocationCheckResult]:
    """Check multiple items for revocation efficiently."""
    results: dict[str, RevocationCheckResult] = {}

    revocation_list = cached_list

    # Fetch list if URL provided
    if fetch_url and not revocation_list:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(fetch_url)
                if response.status_code != 200:
                    error = f"Failed to fetch revocation list: {response.status_code}"
                    for item_id in item_ids:
                        results[item_id] = RevocationCheckResult(revoked=False, error=error)
                    return results
                data = response.json()
                revocation_list = RevocationList.from_dict(data)
        except Exception as e:
            error_msg = f"Network error fetching revocation list: {e}"
            for item_id in item_ids:
                results[item_id] = RevocationCheckResult(revoked=False, error=error_msg)
            return results

    if not revocation_list:
        for item_id in item_ids:
            results[item_id] = RevocationCheckResult(
                revoked=False,
                error="No revocation list available",
            )
        return results

    # Verify signature once
    signature_verified = False
    if issuer_public_key_hex and not skip_verification:
        signature_verified = verify_revocation_list(revocation_list, issuer_public_key_hex)
        if not signature_verified:
            for item_id in item_ids:
                results[item_id] = RevocationCheckResult(
                    revoked=False,
                    signature_verified=False,
                    error="Revocation list signature invalid",
                )
            return results

    # Create lookup map for efficiency
    now = int(time.time())
    revoked_map: dict[str, RevocationEntry] = {}
    for entry in revocation_list.revoked:
        if not entry.expires or entry.expires > now:
            revoked_map[entry.item_id] = entry

    has_bloom = revocation_list.bloom is not None

    # Check each item
    for item_id in item_ids:
        # Fast path with Bloom filter
        if has_bloom and not bloom_filter_check(revocation_list.bloom, item_id):  # type: ignore
            results[item_id] = RevocationCheckResult(
                revoked=False,
                used_bloom_filter=True,
                signature_verified=signature_verified,
            )
            continue

        # Check full list
        entry = revoked_map.get(item_id)
        if entry:
            results[item_id] = RevocationCheckResult(
                revoked=True,
                entry=entry,
                used_bloom_filter=has_bloom,
                signature_verified=signature_verified,
            )
        else:
            results[item_id] = RevocationCheckResult(
                revoked=False,
                used_bloom_filter=has_bloom,
                signature_verified=signature_verified,
            )

    return results


# =============================================================================
# Serialization
# =============================================================================


def serialize_revocation_list(revocation_list: RevocationList) -> str:
    """Serialize revocation list to JSON."""
    return json.dumps(revocation_list.to_dict(), indent=2)


def parse_revocation_list(json_str: str) -> RevocationList:
    """Parse revocation list from JSON."""
    data = json.loads(json_str)

    # Validate required fields
    if data.get("version") != "1.0":
        raise ValueError(f"Unsupported revocation list version: {data.get('version')}")
    if not data.get("issuer") or not data.get("signature") or not isinstance(data.get("revoked"), list):
        raise ValueError("Invalid revocation list format")

    return RevocationList.from_dict(data)
