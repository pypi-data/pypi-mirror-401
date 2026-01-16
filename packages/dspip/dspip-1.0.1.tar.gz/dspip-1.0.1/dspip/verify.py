"""
DSPIP SDK - Verification Functions
Per Internet-Draft draft-midwestcyber-dspip-02
"""

import json
from typing import Any, Literal, Optional

from .crypto import (
    base64_to_bytes,
    compute_sha256,
    ecies_decrypt_compact,
    verify_signature,
)
from .dns import check_key_status, parse_dns_record, resolve_dns_record
from .payload import create_signable_content, decode_payload, parse_qr_data
from .types import (
    PROTOCOL_IDENTIFIER,
    DSPIPDNSRecord,
    DSPIPPayload,
    KeyStatus,
    PrivacyMode,
    VerificationError,
    VerificationResult,
    VerificationWarning,
)


def validate_qr_data_structure(qr_data: str) -> list[VerificationError]:
    """Validate the basic structure of QR data.

    Args:
        qr_data: Raw QR data string

    Returns:
        List of validation errors (empty if valid)
    """
    errors: list[VerificationError] = []

    parts = qr_data.split("|")

    if len(parts) < 6:
        errors.append(
            VerificationError(
                code="INVALID_FORMAT",
                message="Invalid QR data format",
                details=f"Expected at least 6 parts, got {len(parts)}",
            )
        )
        return errors

    if parts[0] != PROTOCOL_IDENTIFIER:
        errors.append(
            VerificationError(
                code="INVALID_PROTOCOL",
                message="Invalid protocol identifier",
                details=f"Expected {PROTOCOL_IDENTIFIER}, got {parts[0]}",
            )
        )

    if not parts[3]:  # key_locator
        errors.append(
            VerificationError(
                code="MISSING_KEY_LOCATOR",
                message="Missing key locator",
            )
        )

    if not parts[4]:  # encoded_payload
        errors.append(
            VerificationError(
                code="MISSING_PAYLOAD",
                message="Missing encoded payload",
            )
        )

    if not parts[5]:  # signature
        errors.append(
            VerificationError(
                code="MISSING_SIGNATURE",
                message="Missing signature",
            )
        )

    return errors


def verify_offline(
    qr_data: str,
    public_key_base64: str,
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
) -> VerificationResult:
    """Verify QR data offline with a known public key.

    Args:
        qr_data: Raw QR data string
        public_key_base64: Public key in Base64 format
        curve: Curve type (default: secp256k1)

    Returns:
        VerificationResult
    """
    errors: list[VerificationError] = []
    warnings: list[VerificationWarning] = []

    # Validate structure
    structure_errors = validate_qr_data_structure(qr_data)
    if structure_errors:
        return VerificationResult(valid=False, errors=structure_errors)

    try:
        # Parse QR data
        parsed = parse_qr_data(qr_data)

        # Decode payload
        payload = decode_payload(parsed.encoded_payload)

        # Verify signature
        signable_content = create_signable_content(parsed.key_locator, parsed.encoded_payload)
        signature = base64_to_bytes(parsed.signature)

        # Pass signable content directly - verify_signature() will hash it internally
        is_valid = verify_signature(signable_content, signature, public_key_base64, curve)

        if not is_valid:
            errors.append(
                VerificationError(
                    code="INVALID_SIGNATURE",
                    message="Signature verification failed",
                )
            )
            return VerificationResult(
                valid=False,
                payload=payload,
                key_locator=parsed.key_locator,
                errors=errors,
            )

        return VerificationResult(
            valid=True,
            payload=payload,
            key_locator=parsed.key_locator,
            warnings=warnings,
        )

    except Exception as e:
        errors.append(
            VerificationError(
                code="VERIFICATION_ERROR",
                message="Verification failed",
                details=str(e),
            )
        )
        return VerificationResult(valid=False, errors=errors)


async def verify(
    qr_data: str,
    dns_record: Optional[DSPIPDNSRecord] = None,
) -> VerificationResult:
    """Verify QR data with DNS lookup for public key.

    Args:
        qr_data: Raw QR data string
        dns_record: Optional pre-fetched DNS record

    Returns:
        VerificationResult
    """
    errors: list[VerificationError] = []
    warnings: list[VerificationWarning] = []

    # Validate structure
    structure_errors = validate_qr_data_structure(qr_data)
    if structure_errors:
        return VerificationResult(valid=False, errors=structure_errors)

    try:
        # Parse QR data
        parsed = parse_qr_data(qr_data)

        # Decode payload to check privacy mode and get curve
        payload = decode_payload(parsed.encoded_payload)

        # Determine curve from privacy mode
        curve: Literal["secp256k1", "ed25519"] = "secp256k1"
        if payload.type_data and payload.type_data.privacy_mode == PrivacyMode.SPLIT_KEY:
            curve = "ed25519"

        # Get DNS record
        record = dns_record
        if not record:
            record = await resolve_dns_record(parsed.key_locator)

        if not record:
            errors.append(
                VerificationError(
                    code="DNS_LOOKUP_FAILED",
                    message="Failed to resolve DNS record",
                    details=f"Key locator: {parsed.key_locator}",
                )
            )
            return VerificationResult(
                valid=False,
                payload=payload,
                key_locator=parsed.key_locator,
                errors=errors,
            )

        # Check key status
        key_status = check_key_status(record)
        if not key_status.can_verify:
            errors.append(
                VerificationError(
                    code="KEY_CANNOT_VERIFY",
                    message="Key cannot be used for verification",
                    details=key_status.reason,
                )
            )
            return VerificationResult(
                valid=False,
                payload=payload,
                key_locator=parsed.key_locator,
                key_status=key_status.status,
                errors=errors,
            )

        # Add warning if key is in verify-only mode
        if key_status.status == KeyStatus.VERIFY_ONLY:
            warnings.append(
                VerificationWarning(
                    code="KEY_VERIFY_ONLY",
                    message="Key is in verify-only mode",
                    details="This key can no longer be used for new signatures",
                )
            )

        # Verify signature
        signable_content = create_signable_content(parsed.key_locator, parsed.encoded_payload)
        signature = base64_to_bytes(parsed.signature)

        # Use curve from record if available
        record_curve = record.c if record.c in ("secp256k1", "ed25519") else curve

        # Pass signable content directly - verify_signature() will hash it internally
        is_valid = verify_signature(signable_content, signature, record.p, record_curve)  # type: ignore

        if not is_valid:
            errors.append(
                VerificationError(
                    code="INVALID_SIGNATURE",
                    message="Signature verification failed",
                )
            )
            return VerificationResult(
                valid=False,
                payload=payload,
                key_locator=parsed.key_locator,
                key_status=key_status.status,
                errors=errors,
            )

        return VerificationResult(
            valid=True,
            payload=payload,
            key_locator=parsed.key_locator,
            signed_by=parsed.key_locator,
            key_status=key_status.status,
            warnings=warnings,
        )

    except Exception as e:
        errors.append(
            VerificationError(
                code="VERIFICATION_ERROR",
                message="Verification failed",
                details=str(e),
            )
        )
        return VerificationResult(valid=False, errors=errors)


async def verify_and_decrypt(
    qr_data: str,
    carrier_private_key_hex: str,
    dns_record: Optional[DSPIPDNSRecord] = None,
) -> VerificationResult:
    """Verify QR data and decrypt recipient information.

    Args:
        qr_data: Raw QR data string
        carrier_private_key_hex: Carrier's private key for decryption
        dns_record: Optional pre-fetched DNS record

    Returns:
        VerificationResult with decrypted recipient data
    """
    # First verify the signature
    result = await verify(qr_data, dns_record)

    if not result.valid or not result.payload:
        return result

    # Check if decryption is needed
    if not result.payload.subject.encrypted:
        return result

    try:
        encrypted_data = result.payload.subject.encrypted_data
        if not encrypted_data:
            result.errors.append(
                VerificationError(
                    code="MISSING_ENCRYPTED_DATA",
                    message="Payload is marked encrypted but has no encrypted data",
                )
            )
            return result

        # Decrypt the recipient data
        decrypted_bytes = ecies_decrypt_compact(encrypted_data, carrier_private_key_hex)
        decrypted_data: dict[str, Any] = json.loads(decrypted_bytes.decode("utf-8"))

        result.decrypted_recipient = decrypted_data

    except Exception as e:
        result.errors.append(
            VerificationError(
                code="DECRYPTION_FAILED",
                message="Failed to decrypt recipient data",
                details=str(e),
            )
        )
        result.valid = False

    return result


def verify_record_signature(
    record: DSPIPDNSRecord,
    previous_public_key_base64: Optional[str] = None,
) -> bool:
    """Verify a DNS record's self-signature.

    Args:
        record: The DNS record to verify
        previous_public_key_base64: Previous key's public key for rotation

    Returns:
        True if signature is valid
    """
    if not record.rsig:
        return False

    # Use the public key from the record or the previous key for rotation
    public_key = previous_public_key_base64 or record.p

    # Create content to verify (excluding rsig)
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

    from .dns import format_dns_record

    content = format_dns_record(record_copy)
    content_hash = compute_sha256(content.encode("utf-8"))

    try:
        signature = base64_to_bytes(record.rsig)
        curve: Literal["secp256k1", "ed25519"] = record.c if record.c in ("secp256k1", "ed25519") else "secp256k1"  # type: ignore
        return verify_signature(content_hash, signature, public_key, curve)
    except Exception:
        return False
