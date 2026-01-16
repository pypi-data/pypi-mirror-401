"""
DSPIP SDK - Delivery Confirmation Protocol
Implements Section 5.6 and 7.4 of the Internet-Draft

Provides cryptographic proof of delivery through challenge-response protocol:
1. Carrier generates nonce (challenge)
2. Recipient signs: sign(nonce || itemId || timestamp)
3. Carrier verifies signature
4. Proof stored for audit

Also supports multi-party attestation for high-value deliveries.
"""

import base64
import json
import time
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from .crypto import (
    bytes_to_hex,
    compute_sha256,
    generate_random_bytes,
    sign_secp256k1,
    verify_secp256k1,
)

# =============================================================================
# Constants
# =============================================================================

# Challenge nonce size in bytes
CHALLENGE_NONCE_SIZE = 32

# Default challenge validity period (5 minutes)
CHALLENGE_VALIDITY_SECONDS = 300

# Maximum timestamp drift allowed (30 seconds)
MAX_TIMESTAMP_DRIFT_SECONDS = 30


# =============================================================================
# Types
# =============================================================================


@dataclass
class DeliveryChallenge:
    """Delivery challenge created by carrier."""

    id: str  # Unique challenge ID
    nonce: str  # Random nonce (32 bytes, hex-encoded)
    item_id: str  # Item being delivered
    carrier_key_locator: str  # Carrier's key locator
    created_at: int  # Timestamp when challenge was created
    expires_at: int  # Timestamp when challenge expires
    carrier_signature: Optional[str] = None  # Optional carrier signature

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "id": self.id,
            "nonce": self.nonce,
            "itemId": self.item_id,
            "carrierKeyLocator": self.carrier_key_locator,
            "createdAt": self.created_at,
            "expiresAt": self.expires_at,
        }
        if self.carrier_signature:
            result["carrierSignature"] = self.carrier_signature
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeliveryChallenge":
        """Create from dictionary."""
        return cls(
            id=data["id"],
            nonce=data["nonce"],
            item_id=data["itemId"],
            carrier_key_locator=data["carrierKeyLocator"],
            created_at=data["createdAt"],
            expires_at=data["expiresAt"],
            carrier_signature=data.get("carrierSignature"),
        )


@dataclass
class DeliveryResponseMetadata:
    """Optional metadata for delivery response."""

    recipient_name: Optional[str] = None
    location: Optional[str] = None  # GPS coordinates
    photo_proof: Optional[str] = None  # Base64 encoded
    notes: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {}
        if self.recipient_name:
            result["recipientName"] = self.recipient_name
        if self.location:
            result["location"] = self.location
        if self.photo_proof:
            result["photoProof"] = self.photo_proof
        if self.notes:
            result["notes"] = self.notes
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeliveryResponseMetadata":
        """Create from dictionary."""
        return cls(
            recipient_name=data.get("recipientName"),
            location=data.get("location"),
            photo_proof=data.get("photoProof"),
            notes=data.get("notes"),
        )


@dataclass
class DeliveryResponse:
    """Delivery response from recipient."""

    challenge_id: str  # Challenge ID being responded to
    nonce: str  # Original nonce from challenge
    item_id: str  # Item ID
    timestamp: int  # Response timestamp
    signature: str  # Recipient's signature
    recipient_public_key_hex: str  # Recipient's public key
    metadata: Optional[DeliveryResponseMetadata] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "challengeId": self.challenge_id,
            "nonce": self.nonce,
            "itemId": self.item_id,
            "timestamp": self.timestamp,
            "signature": self.signature,
            "recipientPublicKeyHex": self.recipient_public_key_hex,
        }
        if self.metadata:
            result["metadata"] = self.metadata.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeliveryResponse":
        """Create from dictionary."""
        metadata = None
        if "metadata" in data and data["metadata"]:
            metadata = DeliveryResponseMetadata.from_dict(data["metadata"])
        return cls(
            challenge_id=data["challengeId"],
            nonce=data["nonce"],
            item_id=data["itemId"],
            timestamp=data["timestamp"],
            signature=data["signature"],
            recipient_public_key_hex=data["recipientPublicKeyHex"],
            metadata=metadata,
        )


@dataclass
class DeliveryProof:
    """Verified delivery proof."""

    valid: bool
    challenge: DeliveryChallenge
    response: DeliveryResponse
    verified_at: int
    proof_hash: str  # Hash of the complete proof (for blockchain recording)
    errors: list[str] = field(default_factory=list)
    carrier_attestation: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "valid": self.valid,
            "challenge": self.challenge.to_dict(),
            "response": self.response.to_dict(),
            "verifiedAt": self.verified_at,
            "proofHash": self.proof_hash,
            "errors": self.errors,
        }
        if self.carrier_attestation:
            result["carrierAttestation"] = self.carrier_attestation
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DeliveryProof":
        """Create from dictionary."""
        return cls(
            valid=data["valid"],
            challenge=DeliveryChallenge.from_dict(data["challenge"]),
            response=DeliveryResponse.from_dict(data["response"]),
            verified_at=data["verifiedAt"],
            proof_hash=data["proofHash"],
            errors=data.get("errors", []),
            carrier_attestation=data.get("carrierAttestation"),
        )


@dataclass
class Attestation:
    """Single attestation from a party."""

    party: str  # Party identifier (key locator)
    role: Literal["carrier", "witness", "recipient", "sender"]
    signature: str
    timestamp: int

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "party": self.party,
            "role": self.role,
            "signature": self.signature,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Attestation":
        """Create from dictionary."""
        return cls(
            party=data["party"],
            role=data["role"],
            signature=data["signature"],
            timestamp=data["timestamp"],
        )


@dataclass
class MultiPartyAttestation:
    """Multi-party attestation for high-value deliveries."""

    proof_hash: str
    item_id: str
    attestations: list[Attestation]
    required_attestations: int
    complete: bool

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "proofHash": self.proof_hash,
            "itemId": self.item_id,
            "attestations": [a.to_dict() for a in self.attestations],
            "requiredAttestations": self.required_attestations,
            "complete": self.complete,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MultiPartyAttestation":
        """Create from dictionary."""
        return cls(
            proof_hash=data["proofHash"],
            item_id=data["itemId"],
            attestations=[Attestation.from_dict(a) for a in data["attestations"]],
            required_attestations=data["requiredAttestations"],
            complete=data["complete"],
        )


# =============================================================================
# Challenge-Response Protocol
# =============================================================================


def _generate_challenge_id() -> str:
    """Generate a unique challenge ID."""
    random_bytes = generate_random_bytes(16)
    timestamp = int(time.time())
    timestamp_b36 = ""
    while timestamp > 0:
        timestamp_b36 = "0123456789abcdefghijklmnopqrstuvwxyz"[timestamp % 36] + timestamp_b36
        timestamp //= 36
    return f"DC-{timestamp_b36}-{bytes_to_hex(random_bytes)[:8]}"


def create_delivery_challenge(
    item_id: str,
    carrier_key_locator: str,
    carrier_private_key_hex: Optional[str] = None,
    validity_seconds: int = CHALLENGE_VALIDITY_SECONDS,
) -> DeliveryChallenge:
    """
    Create a delivery challenge (Step 1: Carrier generates nonce).

    Args:
        item_id: Item being delivered
        carrier_key_locator: Carrier's key locator
        carrier_private_key_hex: Private key for signing challenge (optional)
        validity_seconds: How long the challenge is valid
    """
    nonce = bytes_to_hex(generate_random_bytes(CHALLENGE_NONCE_SIZE))
    now = int(time.time())

    challenge = DeliveryChallenge(
        id=_generate_challenge_id(),
        nonce=nonce,
        item_id=item_id,
        carrier_key_locator=carrier_key_locator,
        created_at=now,
        expires_at=now + validity_seconds,
    )

    # Optionally sign the challenge
    if carrier_private_key_hex:
        challenge_data = f"{challenge.id}|{challenge.nonce}|{challenge.item_id}|{challenge.created_at}|{challenge.expires_at}"
        challenge.carrier_signature = sign_secp256k1(challenge_data, carrier_private_key_hex)

    return challenge


def verify_challenge(
    challenge: DeliveryChallenge,
    carrier_public_key_hex: str,
) -> bool:
    """Verify a carrier-signed challenge."""
    if not challenge.carrier_signature:
        return True  # Unsigned challenges are valid (signing is optional)

    challenge_data = f"{challenge.id}|{challenge.nonce}|{challenge.item_id}|{challenge.created_at}|{challenge.expires_at}"
    return verify_secp256k1(challenge_data, challenge.carrier_signature, carrier_public_key_hex)


def is_challenge_valid(challenge: DeliveryChallenge) -> bool:
    """Check if a challenge is still valid (not expired)."""
    now = int(time.time())
    return now < challenge.expires_at


def respond_to_challenge(
    challenge: DeliveryChallenge,
    recipient_private_key_hex: str,
    recipient_public_key_hex: str,
    metadata: Optional[dict[str, Any]] = None,
) -> DeliveryResponse:
    """
    Respond to a delivery challenge (Step 2: Recipient signs).

    Args:
        challenge: The challenge to respond to
        recipient_private_key_hex: Recipient's private key
        recipient_public_key_hex: Recipient's public key
        metadata: Optional metadata (recipient name, location, etc.)
    """
    if not is_challenge_valid(challenge):
        raise ValueError("Challenge has expired")

    timestamp = int(time.time())

    # Create signable content: nonce || itemId || timestamp
    signable_content = f"{challenge.nonce}|{challenge.item_id}|{timestamp}"
    signature = sign_secp256k1(signable_content, recipient_private_key_hex)

    response_metadata = None
    if metadata:
        response_metadata = DeliveryResponseMetadata(
            recipient_name=metadata.get("recipient_name"),
            location=metadata.get("location"),
            photo_proof=metadata.get("photo_proof"),
            notes=metadata.get("notes"),
        )

    return DeliveryResponse(
        challenge_id=challenge.id,
        nonce=challenge.nonce,
        item_id=challenge.item_id,
        timestamp=timestamp,
        signature=signature,
        recipient_public_key_hex=recipient_public_key_hex,
        metadata=response_metadata,
    )


def verify_delivery_response(
    challenge: DeliveryChallenge,
    response: DeliveryResponse,
    carrier_private_key_hex: Optional[str] = None,
) -> DeliveryProof:
    """
    Verify a delivery response (Step 3: Carrier verifies).

    Args:
        challenge: The original challenge
        response: The response to verify
        carrier_private_key_hex: Private key for attestation (optional)
    """
    errors: list[str] = []
    now = int(time.time())

    # Verify challenge ID matches
    if response.challenge_id != challenge.id:
        errors.append("Challenge ID mismatch")

    # Verify nonce matches
    if response.nonce != challenge.nonce:
        errors.append("Nonce mismatch")

    # Verify item ID matches
    if response.item_id != challenge.item_id:
        errors.append("Item ID mismatch")

    # Verify timestamp is reasonable
    if response.timestamp < challenge.created_at:
        errors.append("Response timestamp before challenge creation")
    if response.timestamp > now + MAX_TIMESTAMP_DRIFT_SECONDS:
        errors.append("Response timestamp too far in future")

    # Verify the signature
    signable_content = f"{response.nonce}|{response.item_id}|{response.timestamp}"
    signature_valid = verify_secp256k1(
        signable_content,
        response.signature,
        response.recipient_public_key_hex,
    )

    if not signature_valid:
        errors.append("Invalid recipient signature")

    # Create proof hash
    proof_data = json.dumps(
        {
            "challenge": {
                "id": challenge.id,
                "nonce": challenge.nonce,
                "itemId": challenge.item_id,
                "carrierKeyLocator": challenge.carrier_key_locator,
                "createdAt": challenge.created_at,
            },
            "response": {
                "timestamp": response.timestamp,
                "signature": response.signature,
                "recipientPublicKeyHex": response.recipient_public_key_hex,
            },
        },
        separators=(",", ":"),
        sort_keys=True,
    )
    proof_hash = bytes_to_hex(compute_sha256(proof_data))

    # Create carrier attestation if private key provided
    carrier_attestation = None
    if carrier_private_key_hex and not errors:
        attestation_data = f"DELIVERY_CONFIRMED|{proof_hash}|{now}"
        carrier_attestation = sign_secp256k1(attestation_data, carrier_private_key_hex)

    return DeliveryProof(
        valid=len(errors) == 0,
        challenge=challenge,
        response=response,
        verified_at=now,
        proof_hash=proof_hash,
        errors=errors,
        carrier_attestation=carrier_attestation,
    )


def verify_delivery_proof(
    proof: DeliveryProof,
    carrier_public_key_hex: Optional[str] = None,
) -> bool:
    """Verify a delivery proof (for auditing)."""
    # Re-verify the response signature
    signable_content = f"{proof.response.nonce}|{proof.response.item_id}|{proof.response.timestamp}"
    response_valid = verify_secp256k1(
        signable_content,
        proof.response.signature,
        proof.response.recipient_public_key_hex,
    )

    if not response_valid:
        return False

    # Verify carrier attestation if present
    if proof.carrier_attestation and carrier_public_key_hex:
        attestation_data = f"DELIVERY_CONFIRMED|{proof.proof_hash}|{proof.verified_at}"
        attestation_valid = verify_secp256k1(
            attestation_data,
            proof.carrier_attestation,
            carrier_public_key_hex,
        )
        if not attestation_valid:
            return False

    return True


# =============================================================================
# Multi-Party Attestation
# =============================================================================


def create_multi_party_attestation(
    proof: DeliveryProof,
    required_attestations: int = 2,
) -> MultiPartyAttestation:
    """Create a multi-party attestation for high-value deliveries."""
    return MultiPartyAttestation(
        proof_hash=proof.proof_hash,
        item_id=proof.challenge.item_id,
        attestations=[],
        required_attestations=required_attestations,
        complete=False,
    )


def add_attestation(
    attestation: MultiPartyAttestation,
    party: str,
    role: Literal["carrier", "witness", "recipient", "sender"],
    private_key_hex: str,
) -> MultiPartyAttestation:
    """Add an attestation to a multi-party proof."""
    timestamp = int(time.time())
    signable_content = f"ATTEST|{attestation.proof_hash}|{party}|{role}|{timestamp}"
    signature = sign_secp256k1(signable_content, private_key_hex)

    new_attestation = Attestation(
        party=party,
        role=role,
        signature=signature,
        timestamp=timestamp,
    )

    new_attestations = attestation.attestations + [new_attestation]

    return MultiPartyAttestation(
        proof_hash=attestation.proof_hash,
        item_id=attestation.item_id,
        attestations=new_attestations,
        required_attestations=attestation.required_attestations,
        complete=len(new_attestations) >= attestation.required_attestations,
    )


def verify_multi_party_attestation(
    attestation: MultiPartyAttestation,
    public_keys: dict[str, str],  # party -> public_key_hex
) -> dict[str, Any]:
    """Verify all attestations in a multi-party proof."""
    errors: list[str] = []
    verified_count = 0

    for att in attestation.attestations:
        public_key_hex = public_keys.get(att.party)
        if not public_key_hex:
            errors.append(f"No public key for party: {att.party}")
            continue

        signable_content = f"ATTEST|{attestation.proof_hash}|{att.party}|{att.role}|{att.timestamp}"
        if verify_secp256k1(signable_content, att.signature, public_key_hex):
            verified_count += 1
        else:
            errors.append(f"Invalid attestation from: {att.party}")

    return {
        "valid": verified_count >= attestation.required_attestations and len(errors) == 0,
        "verified_count": verified_count,
        "errors": errors,
    }


# =============================================================================
# Serialization
# =============================================================================


def serialize_delivery_proof(proof: DeliveryProof) -> str:
    """Serialize a delivery proof for storage or transmission."""
    return json.dumps(proof.to_dict())


def parse_delivery_proof(json_str: str) -> DeliveryProof:
    """Parse a serialized delivery proof."""
    data = json.loads(json_str)

    # Validate required fields
    if "challenge" not in data or "response" not in data or "proofHash" not in data:
        raise ValueError("Invalid delivery proof format")

    return DeliveryProof.from_dict(data)


def serialize_challenge(challenge: DeliveryChallenge) -> str:
    """Serialize a challenge for QR code or transmission."""
    json_str = json.dumps(challenge.to_dict())
    return base64.b64encode(json_str.encode()).decode()


def parse_challenge(encoded: str) -> DeliveryChallenge:
    """Parse a serialized challenge."""
    json_str = base64.b64decode(encoded).decode()
    data = json.loads(json_str)

    # Validate required fields
    if "id" not in data or "nonce" not in data or "itemId" not in data:
        raise ValueError("Invalid challenge format")

    return DeliveryChallenge.from_dict(data)


def create_compact_challenge(challenge: DeliveryChallenge) -> str:
    """
    Create a compact challenge for QR code display.
    Format: DC|nonce|itemId|expiresAt|signature
    """
    # Convert expires_at to base36
    expires_b36 = ""
    num = challenge.expires_at
    while num > 0:
        expires_b36 = "0123456789abcdefghijklmnopqrstuvwxyz"[num % 36] + expires_b36
        num //= 36

    parts = ["DC", challenge.nonce, challenge.item_id, expires_b36]
    if challenge.carrier_signature:
        parts.append(challenge.carrier_signature)
    return "|".join(parts)


def parse_compact_challenge(compact: str, carrier_key_locator: str) -> DeliveryChallenge:
    """Parse a compact challenge."""
    parts = compact.split("|")
    if len(parts) < 4 or parts[0] != "DC":
        raise ValueError("Invalid compact challenge format")

    # Parse base36 expires_at
    expires_at = 0
    for char in parts[3]:
        expires_at = expires_at * 36 + "0123456789abcdefghijklmnopqrstuvwxyz".index(char)

    return DeliveryChallenge(
        id=_generate_challenge_id(),  # Generate new ID
        nonce=parts[1],
        item_id=parts[2],
        carrier_key_locator=carrier_key_locator,
        created_at=int(time.time()),
        expires_at=expires_at,
        carrier_signature=parts[4] if len(parts) > 4 else None,
    )
