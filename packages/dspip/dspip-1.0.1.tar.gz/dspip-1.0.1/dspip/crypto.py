"""
DSPIP SDK - Cryptographic Operations
Supports secp256k1 (standard/encrypted modes) and Ed25519 (split-key mode)
"""

import base64
import hashlib
import json
import os
from typing import Literal, Union

import coincurve
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from nacl.signing import SigningKey, VerifyKey
from nacl.public import PrivateKey as X25519PrivateKey, PublicKey as X25519PublicKey, Box
from nacl.exceptions import BadSignatureError

from .types import KeyPair

# ECIES parameters
IV_LENGTH = 12  # 96 bits for GCM
HKDF_INFO = b"DSPIP-ECIES-v1"


def bytes_to_hex(data: bytes) -> str:
    """Convert bytes to hex string."""
    return data.hex()


def hex_to_bytes(hex_str: str) -> bytes:
    """Convert hex string to bytes."""
    return bytes.fromhex(hex_str)


def bytes_to_base64(data: bytes) -> str:
    """Convert bytes to base64 string."""
    return base64.b64encode(data).decode("utf-8")


def base64_to_bytes(b64_str: str) -> bytes:
    """Convert base64 string to bytes."""
    return base64.b64decode(b64_str)


def compute_sha256(data: Union[bytes, str]) -> bytes:
    """Compute SHA-256 hash."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).digest()


def compute_double_sha256(data: Union[bytes, str]) -> bytes:
    """Compute double SHA-256 hash (for checksums)."""
    return compute_sha256(compute_sha256(data))


def generate_random_bytes(length: int) -> bytes:
    """Generate random bytes."""
    return os.urandom(length)


# =============================================================================
# secp256k1 Key Operations
# =============================================================================


def generate_secp256k1_key_pair() -> KeyPair:
    """Generate a secp256k1 key pair (for standard/encrypted modes)."""
    private_key = coincurve.PrivateKey()
    public_key = private_key.public_key

    # Get compressed public key (33 bytes)
    public_key_compressed = public_key.format(compressed=True)
    # Get uncompressed public key (65 bytes)
    public_key_uncompressed = public_key.format(compressed=False)

    return KeyPair(
        private_key=private_key.secret,
        public_key=public_key_compressed,
        private_key_hex=bytes_to_hex(private_key.secret),
        public_key_hex=bytes_to_hex(public_key_compressed),
        public_key_base64=bytes_to_base64(public_key_compressed),
        public_key_uncompressed=public_key_uncompressed,
        public_key_uncompressed_hex=bytes_to_hex(public_key_uncompressed),
    )


def derive_secp256k1_public_key(private_key_hex: str) -> dict[str, Union[bytes, str]]:
    """Derive public key from secp256k1 private key."""
    private_key = coincurve.PrivateKey(hex_to_bytes(private_key_hex))
    public_key = private_key.public_key
    public_key_compressed = public_key.format(compressed=True)
    public_key_uncompressed = public_key.format(compressed=False)

    return {
        "public_key": public_key_compressed,
        "public_key_hex": bytes_to_hex(public_key_compressed),
        "public_key_base64": bytes_to_base64(public_key_compressed),
        "public_key_uncompressed": public_key_uncompressed,
        "public_key_uncompressed_hex": bytes_to_hex(public_key_uncompressed),
    }


def sign_secp256k1(data: Union[bytes, str], private_key_hex: str) -> str:
    """Sign data with secp256k1 private key (ECDSA). Returns DER-encoded signature in hex."""
    hash_bytes = compute_sha256(data)
    private_key = coincurve.PrivateKey(hex_to_bytes(private_key_hex))
    signature = private_key.sign(hash_bytes, hasher=None)  # Already hashed
    return bytes_to_hex(signature)


def verify_secp256k1(
    data: Union[bytes, str], signature_hex: str, public_key_hex: str
) -> bool:
    """Verify secp256k1 signature."""
    try:
        hash_bytes = compute_sha256(data)
        signature = hex_to_bytes(signature_hex)
        public_key = coincurve.PublicKey(hex_to_bytes(public_key_hex))
        return public_key.verify(signature, hash_bytes, hasher=None)
    except Exception:
        return False


def is_valid_secp256k1_private_key(private_key_hex: str) -> bool:
    """Validate that a hex string represents a valid secp256k1 private key."""
    try:
        private_key_bytes = hex_to_bytes(private_key_hex)
        if len(private_key_bytes) != 32:
            return False
        coincurve.PrivateKey(private_key_bytes)
        return True
    except Exception:
        return False


def is_valid_secp256k1_public_key(public_key_hex: str) -> bool:
    """Validate that a hex string represents a valid secp256k1 public key."""
    try:
        public_key_bytes = hex_to_bytes(public_key_hex)
        if len(public_key_bytes) not in (33, 65):
            return False
        coincurve.PublicKey(public_key_bytes)
        return True
    except Exception:
        return False


# =============================================================================
# Ed25519 Key Operations
# =============================================================================


def generate_ed25519_key_pair() -> KeyPair:
    """Generate an Ed25519 key pair (for split-key mode)."""
    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key

    private_key_bytes = bytes(signing_key)
    public_key_bytes = bytes(verify_key)

    return KeyPair(
        private_key=private_key_bytes,
        public_key=public_key_bytes,
        private_key_hex=bytes_to_hex(private_key_bytes),
        public_key_hex=bytes_to_hex(public_key_bytes),
        public_key_base64=bytes_to_base64(public_key_bytes),
    )


def derive_ed25519_public_key(private_key_hex: str) -> dict[str, Union[bytes, str]]:
    """Derive public key from Ed25519 private key."""
    signing_key = SigningKey(hex_to_bytes(private_key_hex))
    verify_key = signing_key.verify_key
    public_key_bytes = bytes(verify_key)

    return {
        "public_key": public_key_bytes,
        "public_key_hex": bytes_to_hex(public_key_bytes),
        "public_key_base64": bytes_to_base64(public_key_bytes),
    }


def sign_ed25519(data: Union[bytes, str], private_key_hex: str) -> str:
    """Sign data with Ed25519 private key."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    signing_key = SigningKey(hex_to_bytes(private_key_hex))
    signed = signing_key.sign(data)
    # Return just the signature (first 64 bytes), not the message
    return bytes_to_hex(signed.signature)


def verify_ed25519(
    data: Union[bytes, str], signature_hex: str, public_key_hex: str
) -> bool:
    """Verify Ed25519 signature."""
    try:
        if isinstance(data, str):
            data = data.encode("utf-8")
        signature = hex_to_bytes(signature_hex)
        verify_key = VerifyKey(hex_to_bytes(public_key_hex))
        verify_key.verify(data, signature)
        return True
    except BadSignatureError:
        return False
    except Exception:
        return False


def is_valid_ed25519_public_key(public_key_hex: str) -> bool:
    """Validate that a hex string represents a valid Ed25519 public key."""
    try:
        public_key_bytes = hex_to_bytes(public_key_hex)
        if len(public_key_bytes) != 32:
            return False
        VerifyKey(public_key_bytes)
        return True
    except Exception:
        return False


# =============================================================================
# Generic Key Operations
# =============================================================================


def generate_key_pair(
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
) -> KeyPair:
    """Generate a key pair for the specified curve."""
    if curve == "ed25519":
        return generate_ed25519_key_pair()
    return generate_secp256k1_key_pair()


def sign(
    data: Union[bytes, str],
    private_key_hex: str,
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
) -> bytes:
    """Sign data with the appropriate algorithm based on curve. Returns signature bytes."""
    if curve == "ed25519":
        return hex_to_bytes(sign_ed25519(data, private_key_hex))
    return hex_to_bytes(sign_secp256k1(data, private_key_hex))


def verify_signature(
    data: Union[bytes, str],
    signature: Union[bytes, str],
    public_key: Union[bytes, str],
    curve: Literal["secp256k1", "ed25519"] = "secp256k1",
) -> bool:
    """Verify signature with the appropriate algorithm based on curve.

    Args:
        data: Message data (bytes or string)
        signature: Signature (bytes, hex string, or base64 string)
        public_key: Public key (bytes, hex string, or base64 string)
        curve: Curve type

    Returns:
        True if valid, False otherwise
    """
    # Convert signature to hex
    if isinstance(signature, bytes):
        signature_hex = bytes_to_hex(signature)
    else:
        signature_hex = signature

    # Convert public key to hex
    if isinstance(public_key, bytes):
        public_key_hex = bytes_to_hex(public_key)
    else:
        # Determine if public_key is base64 or hex
        # Base64 uses A-Z, a-z, 0-9, +, /, = while hex uses only 0-9, a-f, A-F
        # A string is hex if it only contains hex characters
        is_hex = all(c in "0123456789abcdefABCDEF" for c in public_key)
        if is_hex:
            public_key_hex = public_key
        else:
            # Assume base64
            public_key_hex = bytes_to_hex(base64_to_bytes(public_key))

    if curve == "ed25519":
        return verify_ed25519(data, signature_hex, public_key_hex)
    return verify_secp256k1(data, signature_hex, public_key_hex)


# =============================================================================
# ECIES Encryption
# =============================================================================


def _hkdf_derive_keys(shared_secret: bytes) -> tuple[bytes, bytes]:
    """Derive encryption and MAC keys from shared secret using HKDF."""
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=None,
        info=HKDF_INFO,
    )
    derived = hkdf.derive(shared_secret)
    return derived[:32], derived[32:64]


def _compute_shared_secret(
    private_key_bytes: bytes, public_key_bytes: bytes
) -> bytes:
    """Compute ECDH shared secret."""
    private_key = coincurve.PrivateKey(private_key_bytes)
    public_key = coincurve.PublicKey(public_key_bytes)
    # Multiply to get shared point
    shared_point = public_key.multiply(private_key.secret)
    # Get x-coordinate (first 32 bytes after the prefix)
    shared_bytes = shared_point.format(compressed=False)
    x_coord = shared_bytes[1:33]
    # Hash for uniform output
    return compute_sha256(x_coord)


def ecies_encrypt(
    plaintext: Union[str, bytes], recipient_public_key_hex: str
) -> dict[str, str]:
    """
    Encrypt data using ECIES.

    Args:
        plaintext: Data to encrypt (string or bytes)
        recipient_public_key_hex: Recipient's secp256k1 public key in hex

    Returns:
        Dictionary with ephemeralPublicKey, iv, ciphertext, mac (all base64)
    """
    if isinstance(plaintext, str):
        plaintext = plaintext.encode("utf-8")

    # Generate ephemeral key pair
    ephemeral_private = coincurve.PrivateKey()
    ephemeral_public = ephemeral_private.public_key.format(compressed=True)

    # Compute shared secret
    recipient_public = hex_to_bytes(recipient_public_key_hex)
    shared_secret = _compute_shared_secret(ephemeral_private.secret, recipient_public)

    # Derive encryption key
    encryption_key, _ = _hkdf_derive_keys(shared_secret)

    # Generate IV and encrypt with AES-GCM
    iv = generate_random_bytes(IV_LENGTH)
    aesgcm = AESGCM(encryption_key)
    ciphertext_with_tag = aesgcm.encrypt(iv, plaintext, None)

    # Split ciphertext and tag
    ciphertext = ciphertext_with_tag[:-16]
    mac = ciphertext_with_tag[-16:]

    return {
        "ephemeralPublicKey": bytes_to_base64(ephemeral_public),
        "iv": bytes_to_base64(iv),
        "ciphertext": bytes_to_base64(ciphertext),
        "mac": bytes_to_base64(mac),
    }


def ecies_decrypt(ciphertext_data: dict[str, str], recipient_private_key_hex: str) -> str:
    """
    Decrypt ECIES ciphertext.

    Args:
        ciphertext_data: Dictionary with ephemeralPublicKey, iv, ciphertext, mac
        recipient_private_key_hex: Recipient's secp256k1 private key in hex

    Returns:
        Decrypted plaintext as string
    """
    ephemeral_public = base64_to_bytes(ciphertext_data["ephemeralPublicKey"])
    iv = base64_to_bytes(ciphertext_data["iv"])
    ciphertext = base64_to_bytes(ciphertext_data["ciphertext"])
    mac = base64_to_bytes(ciphertext_data["mac"])

    # Compute shared secret
    recipient_private = hex_to_bytes(recipient_private_key_hex)
    shared_secret = _compute_shared_secret(recipient_private, ephemeral_public)

    # Derive encryption key
    encryption_key, _ = _hkdf_derive_keys(shared_secret)

    # Reconstruct ciphertext with tag
    ciphertext_with_tag = ciphertext + mac

    # Decrypt with AES-GCM
    aesgcm = AESGCM(encryption_key)
    plaintext = aesgcm.decrypt(iv, ciphertext_with_tag, None)

    return plaintext.decode("utf-8")


def ecies_encrypt_compact(
    plaintext: Union[str, bytes], recipient_public_key_hex: str
) -> str:
    """
    Encrypt data using ECIES and return as a single base64 string.
    Format: ephemeralPublicKey || iv || ciphertext || mac
    """
    result = ecies_encrypt(plaintext, recipient_public_key_hex)

    ephemeral_pub = base64_to_bytes(result["ephemeralPublicKey"])
    iv = base64_to_bytes(result["iv"])
    ciphertext = base64_to_bytes(result["ciphertext"])
    mac = base64_to_bytes(result["mac"])

    combined = ephemeral_pub + iv + ciphertext + mac
    return bytes_to_base64(combined)


def ecies_decrypt_compact(compact_ciphertext: str, recipient_private_key_hex: str) -> str:
    """Decrypt compact ECIES ciphertext."""
    combined = base64_to_bytes(compact_ciphertext)

    # Parse: [33 bytes pubkey][12 bytes iv][n bytes ciphertext][16 bytes mac]
    ephemeral_public = combined[:33]
    iv = combined[33:45]
    mac = combined[-16:]
    ciphertext = combined[45:-16]

    return ecies_decrypt(
        {
            "ephemeralPublicKey": bytes_to_base64(ephemeral_public),
            "iv": bytes_to_base64(iv),
            "ciphertext": bytes_to_base64(ciphertext),
            "mac": bytes_to_base64(mac),
        },
        recipient_private_key_hex,
    )


def encrypt_for_lmp(
    recipient_data: dict,
    sender_private_key_hex: str,
    lmp_public_key_hex: str,
) -> str:
    """
    Encrypt recipient data for split-key privacy mode shipping.
    Uses X25519 key exchange with Ed25519 keys converted to X25519 (Curve25519).

    Args:
        recipient_data: Dictionary of recipient information to encrypt
        sender_private_key_hex: Sender's Ed25519 private key in hex
        lmp_public_key_hex: LMP's Ed25519 public key in hex

    Returns:
        Base64-encoded encrypted data
    """
    plaintext = json.dumps(recipient_data).encode("utf-8")

    # Generate ephemeral X25519 key pair for this encryption
    ephemeral_private = X25519PrivateKey.generate()
    ephemeral_public = ephemeral_private.public_key

    # Convert LMP's Ed25519 public key to X25519 (Curve25519) public key
    lmp_public_bytes = hex_to_bytes(lmp_public_key_hex)
    lmp_verify_key = VerifyKey(lmp_public_bytes)
    lmp_x25519_public = lmp_verify_key.to_curve25519_public_key()

    # Use NaCl Box for X25519 key exchange and encryption
    box = Box(ephemeral_private, lmp_x25519_public)

    # Derive sender's public key for identity binding
    sender_private = hex_to_bytes(sender_private_key_hex)
    sender_signing_key = SigningKey(sender_private)
    sender_public = bytes(sender_signing_key.verify_key)

    # Encrypt with Box (uses XSalsa20-Poly1305 internally with X25519)
    nonce = generate_random_bytes(24)  # NaCl Box uses 24-byte nonce
    ciphertext = box.encrypt(plaintext, nonce).ciphertext

    # Package: ephemeralPublicKey (32) || senderPublicKey (32) || nonce (24) || ciphertext
    combined = bytes(ephemeral_public) + sender_public + nonce + ciphertext
    return bytes_to_base64(combined)


def decrypt_as_lmp(encrypted_data: str, lmp_private_key_hex: str) -> dict:
    """
    Decrypt recipient data as LMP using X25519 key exchange.

    Args:
        encrypted_data: Base64-encoded encrypted data from encrypt_for_lmp
        lmp_private_key_hex: LMP's Ed25519 private key in hex

    Returns:
        Decrypted recipient data dictionary
    """
    combined = base64_to_bytes(encrypted_data)

    # Parse: ephemeralPublicKey (32) || senderPublicKey (32) || nonce (24) || ciphertext
    ephemeral_public_bytes = combined[:32]
    sender_public = combined[32:64]  # noqa: F841 - kept for potential future identity verification
    nonce = combined[64:88]
    ciphertext = combined[88:]

    # Convert LMP's Ed25519 private key to X25519 (Curve25519) private key
    lmp_private_bytes = hex_to_bytes(lmp_private_key_hex)
    lmp_signing_key = SigningKey(lmp_private_bytes)
    lmp_x25519_private = lmp_signing_key.to_curve25519_private_key()

    # Reconstruct ephemeral public key
    ephemeral_public = X25519PublicKey(ephemeral_public_bytes)

    # Decrypt using NaCl Box
    box = Box(lmp_x25519_private, ephemeral_public)
    plaintext = box.decrypt(ciphertext, nonce)

    return json.loads(plaintext.decode("utf-8"))


def derive_shared_secret(private_key_hex: str, public_key_hex: str) -> bytes:
    """Derive ECDH shared secret between two parties."""
    private_key = hex_to_bytes(private_key_hex)
    public_key = hex_to_bytes(public_key_hex)
    return _compute_shared_secret(private_key, public_key)
