"""
DSPIP SDK - Payload Creation and Signing
Per Internet-Draft draft-midwestcyber-dspip-02
"""

import base64
import json
import time
import uuid
from typing import Any, Literal, Optional

from .crypto import (
    bytes_to_base64,
    ecies_encrypt_compact,
    encrypt_for_lmp,
    sign,
)
from .types import (
    PROTOCOL_IDENTIFIER,
    PROTOCOL_VERSION,
    Address,
    DSPIPPayload,
    DSPIPQRData,
    EncryptedRecipientData,
    EntityInfo,
    PrivacyMode,
    ShipTypeData,
    SubjectInfo,
)


def generate_item_id(prefix: str = "PKG") -> str:
    """Generate a unique item ID.

    Args:
        prefix: Prefix for the ID (default: "PKG")

    Returns:
        Unique item ID string
    """
    unique_part = uuid.uuid4().hex[:12].upper()
    return f"{prefix}-{unique_part}"


def encode_payload(payload: DSPIPPayload) -> str:
    """Encode a payload to Base64.

    Args:
        payload: The payload to encode

    Returns:
        Base64-encoded payload string
    """
    payload_dict = payload.to_dict()
    json_str = json.dumps(payload_dict, separators=(",", ":"), sort_keys=True)
    return base64.b64encode(json_str.encode("utf-8")).decode("ascii")


def decode_payload(encoded: str) -> DSPIPPayload:
    """Decode a Base64-encoded payload.

    Args:
        encoded: Base64-encoded payload string

    Returns:
        Decoded DSPIPPayload
    """
    json_str = base64.b64decode(encoded).decode("utf-8")
    data = json.loads(json_str)
    return DSPIPPayload.from_dict(data)


def create_signable_content(key_locator: str, encoded_payload: str) -> str:
    """Create the content to be signed per Section 6.2.

    Args:
        key_locator: The key locator string
        encoded_payload: Base64-encoded payload

    Returns:
        Content string to be signed
    """
    return f"{key_locator}|{encoded_payload}"


def sign_payload(
    key_locator: str,
    encoded_payload: str,
    private_key_hex: str,
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
) -> str:
    """Sign an encoded payload.

    Args:
        key_locator: The key locator string
        encoded_payload: Base64-encoded payload
        private_key_hex: Private key in hex format
        curve: Curve to use (default: secp256k1)

    Returns:
        Base64-encoded signature
    """
    signable_content = create_signable_content(key_locator, encoded_payload)
    # Pass the signable content directly - sign() will hash it internally
    signature = sign(signable_content, private_key_hex, curve)
    return bytes_to_base64(signature)


def serialize_qr_data(qr_data: DSPIPQRData) -> str:
    """Serialize QR data to string format per Section 4.4.

    Args:
        qr_data: The QR data to serialize

    Returns:
        Serialized QR data string
    """
    parts = [
        qr_data.protocol,
        qr_data.version,
        qr_data.type,
        qr_data.key_locator,
        qr_data.encoded_payload,
        qr_data.signature,
    ]

    if qr_data.private_message:
        parts.append(qr_data.private_message)

    return "|".join(parts)


def parse_qr_data(data: str) -> DSPIPQRData:
    """Parse QR data from string format.

    Args:
        data: Serialized QR data string

    Returns:
        Parsed DSPIPQRData

    Raises:
        ValueError: If the data format is invalid
    """
    parts = data.split("|")

    if len(parts) < 6:
        raise ValueError(f"Invalid QR data format: expected at least 6 parts, got {len(parts)}")

    if parts[0] != PROTOCOL_IDENTIFIER:
        raise ValueError(f"Invalid protocol identifier: {parts[0]}")

    return DSPIPQRData(
        protocol=parts[0],
        version=parts[1],
        type=parts[2],  # type: ignore
        key_locator=parts[3],
        encoded_payload=parts[4],
        signature=parts[5],
        private_message=parts[6] if len(parts) > 6 else None,
    )


def calculate_qr_data_size(qr_data: str) -> int:
    """Calculate the size of QR data in bytes.

    Args:
        qr_data: Serialized QR data string

    Returns:
        Size in bytes
    """
    return len(qr_data.encode("utf-8"))


def create_standard_payload(
    issuer: dict[str, Any],
    recipient: dict[str, Any],
    item_id: str,
    key_locator: str,
    sender_private_key_hex: str,
    message: Optional[str] = None,
    type_data: Optional[dict[str, Any]] = None,
    expiration_days: Optional[int] = None,
) -> str:
    """Create a standard (non-encrypted) shipping payload.

    Args:
        issuer: Issuer information dict
        recipient: Recipient information dict
        item_id: Unique item identifier
        key_locator: DNS key locator
        sender_private_key_hex: Sender's private key in hex
        message: Optional message
        type_data: Optional SHIP type data
        expiration_days: Days until expiration

    Returns:
        Serialized QR data string
    """
    timestamp = int(time.time())
    expiration_date = None
    if expiration_days:
        expiration_date = timestamp + (expiration_days * 24 * 60 * 60)

    # Build issuer entity
    issuer_entity = EntityInfo.from_dict(issuer)

    # Build subject (recipient) entity
    subject = SubjectInfo.from_dict(recipient)

    # Build type data
    ship_type_data = None
    if type_data:
        ship_type_data = ShipTypeData.from_dict(type_data)
    else:
        ship_type_data = ShipTypeData(privacy_mode=PrivacyMode.STANDARD)

    # Create payload
    payload = DSPIPPayload(
        type="SHIP",
        issuer=issuer_entity,
        subject=subject,
        item_id=item_id,
        timestamp=timestamp,
        expiration_date=expiration_date,
        message=message,
        type_data=ship_type_data,
    )

    # Encode and sign
    encoded_payload = encode_payload(payload)
    signature = sign_payload(key_locator, encoded_payload, sender_private_key_hex)

    # Create QR data
    qr_data = DSPIPQRData(
        protocol=PROTOCOL_IDENTIFIER,
        version=PROTOCOL_VERSION,
        type="SHIP",
        key_locator=key_locator,
        encoded_payload=encoded_payload,
        signature=signature,
    )

    return serialize_qr_data(qr_data)


def create_encrypted_payload(
    issuer: dict[str, Any],
    recipient: dict[str, Any],
    item_id: str,
    key_locator: str,
    sender_private_key_hex: str,
    carrier_public_key_hex: str,
    lmp_address: Optional[str] = None,
    delivery_instructions: Optional[str] = None,
    message: Optional[str] = None,
    type_data: Optional[dict[str, Any]] = None,
    expiration_days: Optional[int] = None,
) -> str:
    """Create an encrypted privacy mode payload.

    Args:
        issuer: Issuer information dict
        recipient: Recipient information dict (will be encrypted)
        item_id: Unique item identifier
        key_locator: DNS key locator
        sender_private_key_hex: Sender's private key in hex
        carrier_public_key_hex: Carrier's public key for encryption
        lmp_address: Last-mile provider address (for routing)
        delivery_instructions: Optional delivery instructions
        message: Optional message
        type_data: Optional SHIP type data
        expiration_days: Days until expiration

    Returns:
        Serialized QR data string
    """
    timestamp = int(time.time())
    expiration_date = None
    if expiration_days:
        expiration_date = timestamp + (expiration_days * 24 * 60 * 60)

    # Build issuer entity
    issuer_entity = EntityInfo.from_dict(issuer)

    # Build recipient data for encryption
    recipient_address = Address.from_dict(recipient.get("address", {}))
    encrypted_recipient_data = EncryptedRecipientData(
        recipient_name=recipient.get("name", ""),
        address=recipient_address,
        delivery_instructions=delivery_instructions,
    )

    # Encrypt recipient data using ECIES
    encrypted_data = ecies_encrypt_compact(
        json.dumps(encrypted_recipient_data.to_dict()).encode("utf-8"),
        carrier_public_key_hex,
    )

    # Build subject with encrypted data
    subject = SubjectInfo(
        encrypted=True,
        encrypted_data=encrypted_data,
        lmp_address=lmp_address,
    )

    # Build type data
    ship_type_data = ShipTypeData.from_dict(type_data) if type_data else ShipTypeData()
    ship_type_data.privacy_mode = PrivacyMode.ENCRYPTED

    # Create payload
    payload = DSPIPPayload(
        type="SHIP",
        issuer=issuer_entity,
        subject=subject,
        item_id=item_id,
        timestamp=timestamp,
        expiration_date=expiration_date,
        message=message,
        type_data=ship_type_data,
    )

    # Encode and sign
    encoded_payload = encode_payload(payload)
    signature = sign_payload(key_locator, encoded_payload, sender_private_key_hex)

    # Create QR data
    qr_data = DSPIPQRData(
        protocol=PROTOCOL_IDENTIFIER,
        version=PROTOCOL_VERSION,
        type="SHIP",
        key_locator=key_locator,
        encoded_payload=encoded_payload,
        signature=signature,
    )

    return serialize_qr_data(qr_data)


def create_split_key_payload(
    issuer: dict[str, Any],
    recipient: dict[str, Any],
    item_id: str,
    key_locator: str,
    sender_private_key_hex: str,
    lmp_public_key_hex: str,
    lmp_address: Optional[str] = None,
    delivery_instructions: Optional[str] = None,
    message: Optional[str] = None,
    type_data: Optional[dict[str, Any]] = None,
    expiration_days: Optional[int] = None,
) -> str:
    """Create a split-key privacy mode payload.

    In split-key mode, the recipient data is encrypted for the LMP
    using Ed25519/X25519 key agreement.

    Args:
        issuer: Issuer information dict
        recipient: Recipient information dict (will be encrypted for LMP)
        item_id: Unique item identifier
        key_locator: DNS key locator
        sender_private_key_hex: Sender's Ed25519 private key in hex
        lmp_public_key_hex: LMP's Ed25519 public key in hex
        lmp_address: Last-mile provider address (for routing)
        delivery_instructions: Optional delivery instructions
        message: Optional message
        type_data: Optional SHIP type data
        expiration_days: Days until expiration

    Returns:
        Serialized QR data string
    """
    timestamp = int(time.time())
    expiration_date = None
    if expiration_days:
        expiration_date = timestamp + (expiration_days * 24 * 60 * 60)

    # Build issuer entity
    issuer_entity = EntityInfo.from_dict(issuer)

    # Build recipient data for LMP encryption
    recipient_data = {
        "recipientName": recipient.get("name", ""),
        "address": recipient.get("address", {}),
    }
    if delivery_instructions:
        recipient_data["deliveryInstructions"] = delivery_instructions

    # Encrypt recipient data for LMP
    encrypted_data = encrypt_for_lmp(
        recipient_data,
        sender_private_key_hex,
        lmp_public_key_hex,
    )

    # Build subject with encrypted data
    subject = SubjectInfo(
        encrypted=True,
        encrypted_data=encrypted_data,
        lmp_address=lmp_address,
        last_mile_provider=type_data.get("lastMileProvider") if type_data else None,
    )

    # Build type data
    ship_type_data = ShipTypeData.from_dict(type_data) if type_data else ShipTypeData()
    ship_type_data.privacy_mode = PrivacyMode.SPLIT_KEY

    # Create payload
    payload = DSPIPPayload(
        type="SHIP",
        issuer=issuer_entity,
        subject=subject,
        item_id=item_id,
        timestamp=timestamp,
        expiration_date=expiration_date,
        message=message,
        type_data=ship_type_data,
    )

    # Encode and sign (using Ed25519 for split-key mode)
    encoded_payload = encode_payload(payload)
    signature = sign_payload(key_locator, encoded_payload, sender_private_key_hex, "ed25519")

    # Create QR data
    qr_data = DSPIPQRData(
        protocol=PROTOCOL_IDENTIFIER,
        version=PROTOCOL_VERSION,
        type="SHIP",
        key_locator=key_locator,
        encoded_payload=encoded_payload,
        signature=signature,
    )

    return serialize_qr_data(qr_data)


def create_shipping_payload(
    issuer: dict[str, Any],
    recipient: dict[str, Any],
    item_id: str,
    key_locator: str,
    sender_private_key_hex: str,
    privacy_mode: PrivacyMode = PrivacyMode.STANDARD,
    carrier_public_key_hex: Optional[str] = None,
    lmp_public_key_hex: Optional[str] = None,
    lmp_address: Optional[str] = None,
    delivery_instructions: Optional[str] = None,
    message: Optional[str] = None,
    type_data: Optional[dict[str, Any]] = None,
    expiration_days: Optional[int] = None,
) -> str:
    """Create a shipping payload with the specified privacy mode.

    This is a convenience function that delegates to the appropriate
    payload creation function based on privacy mode.

    Args:
        issuer: Issuer information dict
        recipient: Recipient information dict
        item_id: Unique item identifier
        key_locator: DNS key locator
        sender_private_key_hex: Sender's private key in hex
        privacy_mode: Privacy mode to use
        carrier_public_key_hex: Carrier's public key (for encrypted mode)
        lmp_public_key_hex: LMP's public key (for split-key mode)
        lmp_address: Last-mile provider address
        delivery_instructions: Optional delivery instructions
        message: Optional message
        type_data: Optional SHIP type data
        expiration_days: Days until expiration

    Returns:
        Serialized QR data string
    """
    if privacy_mode == PrivacyMode.STANDARD:
        return create_standard_payload(
            issuer=issuer,
            recipient=recipient,
            item_id=item_id,
            key_locator=key_locator,
            sender_private_key_hex=sender_private_key_hex,
            message=message,
            type_data=type_data,
            expiration_days=expiration_days,
        )
    elif privacy_mode == PrivacyMode.ENCRYPTED:
        if not carrier_public_key_hex:
            raise ValueError("carrier_public_key_hex required for encrypted mode")
        return create_encrypted_payload(
            issuer=issuer,
            recipient=recipient,
            item_id=item_id,
            key_locator=key_locator,
            sender_private_key_hex=sender_private_key_hex,
            carrier_public_key_hex=carrier_public_key_hex,
            lmp_address=lmp_address,
            delivery_instructions=delivery_instructions,
            message=message,
            type_data=type_data,
            expiration_days=expiration_days,
        )
    elif privacy_mode == PrivacyMode.SPLIT_KEY:
        if not lmp_public_key_hex:
            raise ValueError("lmp_public_key_hex required for split-key mode")
        return create_split_key_payload(
            issuer=issuer,
            recipient=recipient,
            item_id=item_id,
            key_locator=key_locator,
            sender_private_key_hex=sender_private_key_hex,
            lmp_public_key_hex=lmp_public_key_hex,
            lmp_address=lmp_address,
            delivery_instructions=delivery_instructions,
            message=message,
            type_data=type_data,
            expiration_days=expiration_days,
        )
    else:
        raise ValueError(f"Unknown privacy mode: {privacy_mode}")
