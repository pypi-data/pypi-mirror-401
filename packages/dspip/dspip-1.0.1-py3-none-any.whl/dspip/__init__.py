"""
DSPIP SDK - Digital Signing of Physical Items Protocol
Official Python implementation

This SDK provides complete implementation of the DSPIP protocol for
shipping and logistics applications.

Example:
    >>> from dspip import generate_key_pair, create_standard_payload, verify
    >>> keys = generate_key_pair()
    >>> qr_data = create_standard_payload(
    ...     issuer={"name": "Sender", "address": {"country": "US"}},
    ...     recipient={"name": "Recipient", "address": {"country": "US"}},
    ...     item_id="TRACK-001",
    ...     key_locator="warehouse._dspip.example.com",
    ...     sender_private_key_hex=keys.private_key_hex,
    ... )
"""

__version__ = "1.0.0"

# Types
from .types import (
    PROTOCOL_IDENTIFIER,
    PROTOCOL_VERSION,
    DNS_RECORD_VERSION,
    PrivacyMode,
    KeyStatus,
    AuthorityLevel,
    AddressScheme,
    Address,
    EntityInfo,
    EncryptedRecipientData,
    ShipTypeData,
    SubjectInfo,
    DSPIPPayload,
    DSPIPQRData,
    KeyPair,
    DSPIPDNSRecord,
    ParsedAddress,
    VerificationResult,
    VerificationError,
    VerificationWarning,
)

# Crypto
from .crypto import (
    generate_key_pair,
    generate_secp256k1_key_pair,
    generate_ed25519_key_pair,
    derive_secp256k1_public_key,
    derive_ed25519_public_key,
    sign,
    verify_signature,
    sign_secp256k1,
    verify_secp256k1,
    sign_ed25519,
    verify_ed25519,
    compute_sha256,
    bytes_to_hex,
    hex_to_bytes,
    bytes_to_base64,
    base64_to_bytes,
    ecies_encrypt,
    ecies_decrypt,
    ecies_encrypt_compact,
    ecies_decrypt_compact,
    encrypt_for_lmp,
    decrypt_as_lmp,
    derive_shared_secret,
)

# Payload
from .payload import (
    generate_item_id,
    create_standard_payload,
    create_encrypted_payload,
    create_split_key_payload,
    create_shipping_payload,
    sign_payload,
    serialize_qr_data,
    parse_qr_data,
    encode_payload,
    decode_payload,
    create_signable_content,
    calculate_qr_data_size,
)

# DNS
from .dns import (
    create_dns_record,
    format_dns_record,
    parse_dns_record,
    generate_record_signature,
    create_key_lifecycle,
    parse_address_field,
    format_address_field,
    is_plus_code,
    create_plus_code_address,
    create_street_address,
    create_geo_address,
    create_facility_address,
    generate_key_locator,
    parse_key_locator,
    check_key_status,
    resolve_dns_record,
    resolve_public_key,
    MockDNSResolver,
)

# Verification
from .verify import (
    verify,
    verify_and_decrypt,
    verify_offline,
    verify_record_signature,
    validate_qr_data_structure,
)

# QR Code
from .qr import (
    generate_qr_code_data_url,
    generate_qr_code_svg,
    generate_qr_code_terminal,
    generate_qr_code_bytes,
    save_qr_code_to_file,
    will_fit_in_qr_code,
    get_optimal_qr_version,
    parse_scanned_data,
    extract_tracking_info,
    is_privacy_mode,
    requires_decryption,
    get_public_sender_info,
    get_recipient_info,
)

# Revocation (Section 5.5)
from .revocation import (
    # Constants
    REVOCATION_MAX_AGE_SECONDS,
    DEFAULT_BLOOM_FILTER_SIZE,
    DEFAULT_BLOOM_HASH_COUNT,
    # Types
    RevocationEntry,
    BloomFilter,
    RevocationList,
    RevocationCheckResult,
    # Bloom filter operations
    create_bloom_filter,
    bloom_filter_add,
    bloom_filter_check,
    calculate_bloom_filter_size,
    # Revocation list management
    create_revocation_list,
    verify_revocation_list,
    add_revocation_entry,
    prune_revocation_list,
    # Revocation checking
    check_revocation,
    check_revocation_batch,
    # Serialization
    serialize_revocation_list,
    parse_revocation_list,
)

# Delivery Confirmation (Section 5.6, 7.4)
from .delivery import (
    # Constants
    CHALLENGE_NONCE_SIZE,
    CHALLENGE_VALIDITY_SECONDS,
    MAX_TIMESTAMP_DRIFT_SECONDS,
    # Types
    DeliveryChallenge,
    DeliveryResponse,
    DeliveryResponseMetadata,
    DeliveryProof,
    Attestation,
    MultiPartyAttestation,
    # Challenge-response protocol
    create_delivery_challenge,
    verify_challenge,
    is_challenge_valid,
    respond_to_challenge,
    verify_delivery_response,
    verify_delivery_proof,
    # Multi-party attestation
    create_multi_party_attestation,
    add_attestation,
    verify_multi_party_attestation,
    # Serialization
    serialize_delivery_proof,
    parse_delivery_proof,
    serialize_challenge,
    parse_challenge,
    create_compact_challenge,
    parse_compact_challenge,
)

# DNSSEC Validation (Section 8)
from .dnssec import (
    # Constants
    DOH_SERVERS,
    DNS_TYPES,
    DNSSEC_ALGORITHMS,
    DS_DIGEST_TYPES,
    # Types
    DNSKEYRecord,
    DSRecord,
    RRSIGRecord,
    ChainOfTrust,
    DNSSECValidationResult,
    # Key tag calculation
    calculate_key_tag,
    # DS record verification
    compute_ds_digest,
    verify_ds_record,
    # DoH with DNSSEC
    query_doh_with_dnssec,
    fetch_dnskey_records,
    fetch_ds_records,
    # DNSSEC validation
    validate_dnssec,
    clear_dnssec_cache,
    get_dnssec_cache_stats,
    # High-level DSPIP validation
    validate_key_locator_dnssec,
    has_dnssec,
)

# Directory Services (Section 7.2.5)
from .directory import (
    # Constants
    DIRECTORY_BASE_URL,
    MAX_PROVIDERS,
    MAX_COVERAGE_AREAS,
    DIRECTORY_CACHE_TTL,
    # Types
    DelegationScheme,
    ServiceType,
    GeoBounds,
    CoverageArea,
    Provider,
    ProviderLookupResult,
    DirectoryQueryOptions,
    DirectoryClientConfig,
    DiscoveryRecord,
    # Lookup functions
    lookup_providers_by_location,
    lookup_providers_by_postal,
    get_provider,
    # Coverage checking
    is_in_coverage,
    postal_in_coverage,
    # DNS-based discovery
    parse_discovery_record,
    build_selector_from_delegation,
    discover_selectors,
    # Cache management
    clear_provider_cache,
    get_provider_cache_stats,
    # Serialization
    serialize_provider,
    parse_provider,
)

__all__ = [
    # Version
    "__version__",
    # Constants
    "PROTOCOL_IDENTIFIER",
    "PROTOCOL_VERSION",
    "DNS_RECORD_VERSION",
    # Types
    "PrivacyMode",
    "KeyStatus",
    "AuthorityLevel",
    "AddressScheme",
    "Address",
    "EntityInfo",
    "EncryptedRecipientData",
    "ShipTypeData",
    "SubjectInfo",
    "DSPIPPayload",
    "DSPIPQRData",
    "KeyPair",
    "DSPIPDNSRecord",
    "ParsedAddress",
    "VerificationResult",
    "VerificationError",
    "VerificationWarning",
    # Crypto
    "generate_key_pair",
    "generate_secp256k1_key_pair",
    "generate_ed25519_key_pair",
    "derive_secp256k1_public_key",
    "derive_ed25519_public_key",
    "sign",
    "verify_signature",
    "sign_secp256k1",
    "verify_secp256k1",
    "sign_ed25519",
    "verify_ed25519",
    "compute_sha256",
    "bytes_to_hex",
    "hex_to_bytes",
    "bytes_to_base64",
    "base64_to_bytes",
    "ecies_encrypt",
    "ecies_decrypt",
    "ecies_encrypt_compact",
    "ecies_decrypt_compact",
    "encrypt_for_lmp",
    "decrypt_as_lmp",
    "derive_shared_secret",
    # Payload
    "generate_item_id",
    "create_standard_payload",
    "create_encrypted_payload",
    "create_split_key_payload",
    "create_shipping_payload",
    "sign_payload",
    "serialize_qr_data",
    "parse_qr_data",
    "encode_payload",
    "decode_payload",
    "create_signable_content",
    "calculate_qr_data_size",
    # DNS
    "create_dns_record",
    "format_dns_record",
    "parse_dns_record",
    "generate_record_signature",
    "create_key_lifecycle",
    "parse_address_field",
    "format_address_field",
    "is_plus_code",
    "create_plus_code_address",
    "create_street_address",
    "create_geo_address",
    "create_facility_address",
    "generate_key_locator",
    "parse_key_locator",
    "check_key_status",
    "resolve_dns_record",
    "resolve_public_key",
    "MockDNSResolver",
    # Verification
    "verify",
    "verify_and_decrypt",
    "verify_offline",
    "verify_record_signature",
    "validate_qr_data_structure",
    # QR Code
    "generate_qr_code_data_url",
    "generate_qr_code_svg",
    "generate_qr_code_terminal",
    "generate_qr_code_bytes",
    "save_qr_code_to_file",
    "will_fit_in_qr_code",
    "get_optimal_qr_version",
    "parse_scanned_data",
    "extract_tracking_info",
    "is_privacy_mode",
    "requires_decryption",
    "get_public_sender_info",
    "get_recipient_info",
    # Revocation (Section 5.5)
    "REVOCATION_MAX_AGE_SECONDS",
    "DEFAULT_BLOOM_FILTER_SIZE",
    "DEFAULT_BLOOM_HASH_COUNT",
    "RevocationEntry",
    "BloomFilter",
    "RevocationList",
    "RevocationCheckResult",
    "create_bloom_filter",
    "bloom_filter_add",
    "bloom_filter_check",
    "calculate_bloom_filter_size",
    "create_revocation_list",
    "verify_revocation_list",
    "add_revocation_entry",
    "prune_revocation_list",
    "check_revocation",
    "check_revocation_batch",
    "serialize_revocation_list",
    "parse_revocation_list",
    # Delivery Confirmation (Section 5.6, 7.4)
    "CHALLENGE_NONCE_SIZE",
    "CHALLENGE_VALIDITY_SECONDS",
    "MAX_TIMESTAMP_DRIFT_SECONDS",
    "DeliveryChallenge",
    "DeliveryResponse",
    "DeliveryResponseMetadata",
    "DeliveryProof",
    "Attestation",
    "MultiPartyAttestation",
    "create_delivery_challenge",
    "verify_challenge",
    "is_challenge_valid",
    "respond_to_challenge",
    "verify_delivery_response",
    "verify_delivery_proof",
    "create_multi_party_attestation",
    "add_attestation",
    "verify_multi_party_attestation",
    "serialize_delivery_proof",
    "parse_delivery_proof",
    "serialize_challenge",
    "parse_challenge",
    "create_compact_challenge",
    "parse_compact_challenge",
    # DNSSEC Validation (Section 8)
    "DOH_SERVERS",
    "DNS_TYPES",
    "DNSSEC_ALGORITHMS",
    "DS_DIGEST_TYPES",
    "DNSKEYRecord",
    "DSRecord",
    "RRSIGRecord",
    "ChainOfTrust",
    "DNSSECValidationResult",
    "calculate_key_tag",
    "compute_ds_digest",
    "verify_ds_record",
    "query_doh_with_dnssec",
    "fetch_dnskey_records",
    "fetch_ds_records",
    "validate_dnssec",
    "clear_dnssec_cache",
    "get_dnssec_cache_stats",
    "validate_key_locator_dnssec",
    "has_dnssec",
    # Directory Services (Section 7.2.5)
    "DIRECTORY_BASE_URL",
    "MAX_PROVIDERS",
    "MAX_COVERAGE_AREAS",
    "DIRECTORY_CACHE_TTL",
    "DelegationScheme",
    "ServiceType",
    "GeoBounds",
    "CoverageArea",
    "Provider",
    "ProviderLookupResult",
    "DirectoryQueryOptions",
    "DirectoryClientConfig",
    "DiscoveryRecord",
    "lookup_providers_by_location",
    "lookup_providers_by_postal",
    "get_provider",
    "is_in_coverage",
    "postal_in_coverage",
    "parse_discovery_record",
    "build_selector_from_delegation",
    "discover_selectors",
    "clear_provider_cache",
    "get_provider_cache_stats",
    "serialize_provider",
    "parse_provider",
]
