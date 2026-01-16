"""
DSPIP SDK - Core Type Definitions
Per Internet-Draft draft-midwestcyber-dspip-02
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Literal, Optional

# Protocol constants
PROTOCOL_IDENTIFIER = "DSPIP"
PROTOCOL_VERSION = "1.0"
DNS_RECORD_VERSION = "DSPIP1"


class PrivacyMode(str, Enum):
    """Privacy modes for shipping."""

    STANDARD = "standard"
    ENCRYPTED = "encrypted"
    SPLIT_KEY = "split-key"


class KeyStatus(str, Enum):
    """Key status values per Section 5.4.2."""

    ACTIVE = "active"
    VERIFY_ONLY = "verify-only"
    REVOKED = "revoked"


class AuthorityLevel(str, Enum):
    """Authority levels for keys."""

    ENTERPRISE = "enterprise"
    ORGANIZATION = "organization"
    GOVERNMENT = "government"
    PERSONAL = "personal"


class AddressScheme(str, Enum):
    """Address scheme types per Section 5.2.1."""

    PLUS = "plus"
    STREET = "street"
    GEO = "geo"
    FACILITY = "facility"


class DeliveryConfirmationMethod(str, Enum):
    """Delivery confirmation methods."""

    SIGNATURE = "signature"
    PHOTO = "photo"
    CRYPTOGRAPHIC = "cryptographic"


@dataclass
class Address:
    """Physical address structure."""

    country: str  # ISO 3166-1 alpha-2 REQUIRED
    street1: Optional[str] = None
    street2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, excluding None values."""
        result: dict[str, Any] = {"country": self.country}
        if self.street1:
            result["street1"] = self.street1
        if self.street2:
            result["street2"] = self.street2
        if self.city:
            result["city"] = self.city
        if self.state:
            result["state"] = self.state
        if self.postal_code:
            result["postalCode"] = self.postal_code
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Address":
        """Create from dictionary."""
        return cls(
            country=data.get("country", ""),
            street1=data.get("street1"),
            street2=data.get("street2"),
            city=data.get("city"),
            state=data.get("state"),
            postal_code=data.get("postalCode"),
        )


@dataclass
class EntityInfo:
    """Entity information - sender or recipient per Section 4.1."""

    name: Optional[str] = None
    organization: Optional[str] = None
    address: Optional[Address] = None
    email: Optional[str] = None
    public_key_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {}
        if self.name:
            result["name"] = self.name
        if self.organization:
            result["organization"] = self.organization
        if self.address:
            result["address"] = self.address.to_dict()
        if self.email:
            result["email"] = self.email
        if self.public_key_id:
            result["publicKeyId"] = self.public_key_id
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EntityInfo":
        """Create from dictionary."""
        address = None
        if "address" in data and data["address"]:
            address = Address.from_dict(data["address"])
        return cls(
            name=data.get("name"),
            organization=data.get("organization"),
            address=address,
            email=data.get("email"),
            public_key_id=data.get("publicKeyId"),
        )


@dataclass
class EncryptedRecipientData:
    """Recipient information that gets encrypted in privacy modes."""

    recipient_name: str
    address: Address
    delivery_instructions: Optional[str] = None
    authorized_receivers: Optional[list[str]] = None
    internal_routing: Optional[str] = None
    proof_of_delivery: Optional[dict[str, str]] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "recipientName": self.recipient_name,
            "address": self.address.to_dict(),
        }
        if self.delivery_instructions:
            result["deliveryInstructions"] = self.delivery_instructions
        if self.authorized_receivers:
            result["authorizedReceivers"] = self.authorized_receivers
        if self.internal_routing:
            result["internalRouting"] = self.internal_routing
        if self.proof_of_delivery:
            result["proofOfDelivery"] = self.proof_of_delivery
        return result


@dataclass
class Dimensions:
    """Package dimensions."""

    length: float
    width: float
    height: float
    unit: Literal["cm", "in"] = "cm"


@dataclass
class CustomsInfo:
    """Customs information for international shipping."""

    contents: str
    value: float
    origin_country: str
    destination_country: str
    hs_code: Optional[str] = None


@dataclass
class DeliveryConfirmation:
    """Delivery confirmation configuration."""

    required: bool
    method: DeliveryConfirmationMethod
    callback_url: Optional[str] = None
    callback_auth: Optional[str] = None
    public_key: Optional[str] = None


@dataclass
class ShipTypeData:
    """SHIP type payload data per Section 4.2."""

    parcel_id: Optional[str] = None
    carrier: Optional[str] = None
    carrier_key_locator: Optional[str] = None
    service: Optional[str] = None
    weight: Optional[float] = None
    dimensions: Optional[Dimensions] = None
    declared_value: Optional[float] = None
    customs_info: Optional[CustomsInfo] = None
    privacy_mode: Optional[PrivacyMode] = None
    last_mile_provider: Optional[str] = None
    encrypted_recipient: Optional[str] = None
    authentication_profile: Optional[str] = None
    public_key_location: Optional[str] = None
    label_serial: Optional[str] = None
    delivery_confirmation: Optional[DeliveryConfirmation] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {}
        if self.parcel_id:
            result["parcelId"] = self.parcel_id
        if self.carrier:
            result["carrier"] = self.carrier
        if self.carrier_key_locator:
            result["carrierKeyLocator"] = self.carrier_key_locator
        if self.service:
            result["service"] = self.service
        if self.weight is not None:
            result["weight"] = self.weight
        if self.privacy_mode:
            result["privacyMode"] = self.privacy_mode.value
        if self.last_mile_provider:
            result["lastMileProvider"] = self.last_mile_provider
        if self.encrypted_recipient:
            result["encryptedRecipient"] = self.encrypted_recipient
        if self.authentication_profile:
            result["authenticationProfile"] = self.authentication_profile
        if self.public_key_location:
            result["publicKeyLocation"] = self.public_key_location
        if self.label_serial:
            result["labelSerial"] = self.label_serial
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ShipTypeData":
        """Create from dictionary."""
        privacy_mode = None
        if "privacyMode" in data:
            privacy_mode = PrivacyMode(data["privacyMode"])
        return cls(
            parcel_id=data.get("parcelId"),
            carrier=data.get("carrier"),
            carrier_key_locator=data.get("carrierKeyLocator"),
            service=data.get("service"),
            weight=data.get("weight"),
            privacy_mode=privacy_mode,
            last_mile_provider=data.get("lastMileProvider"),
            encrypted_recipient=data.get("encryptedRecipient"),
            authentication_profile=data.get("authenticationProfile"),
            public_key_location=data.get("publicKeyLocation"),
            label_serial=data.get("labelSerial"),
        )


@dataclass
class SubjectInfo(EntityInfo):
    """Subject information in payload. In privacy modes, may contain encrypted data."""

    last_mile_provider: Optional[str] = None
    encrypted: bool = False
    encrypted_data: Optional[str] = None
    lmp_address: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result = super().to_dict()
        if self.last_mile_provider:
            result["lastMileProvider"] = self.last_mile_provider
        if self.encrypted:
            result["encrypted"] = self.encrypted
        if self.encrypted_data:
            result["encryptedData"] = self.encrypted_data
        if self.lmp_address:
            result["lmpAddress"] = self.lmp_address
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SubjectInfo":
        """Create from dictionary."""
        address = None
        if "address" in data and data["address"]:
            address = Address.from_dict(data["address"])
        return cls(
            name=data.get("name"),
            organization=data.get("organization"),
            address=address,
            email=data.get("email"),
            public_key_id=data.get("publicKeyId"),
            last_mile_provider=data.get("lastMileProvider"),
            encrypted=data.get("encrypted", False),
            encrypted_data=data.get("encryptedData"),
            lmp_address=data.get("lmpAddress"),
        )


@dataclass
class DSPIPPayload:
    """The main DSPIP payload structure per Section 4.1."""

    type: Literal["SHIP"]
    issuer: EntityInfo
    subject: SubjectInfo
    item_id: str
    timestamp: int
    expiration_date: Optional[int] = None
    message: Optional[str] = None
    type_data: Optional[ShipTypeData] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        result: dict[str, Any] = {
            "type": self.type,
            "issuer": self.issuer.to_dict(),
            "subject": self.subject.to_dict(),
            "itemId": self.item_id,
            "timestamp": self.timestamp,
        }
        if self.expiration_date:
            result["expirationDate"] = self.expiration_date
        if self.message:
            result["message"] = self.message
        if self.type_data:
            result["typeData"] = self.type_data.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "DSPIPPayload":
        """Create from dictionary."""
        type_data = None
        if "typeData" in data and data["typeData"]:
            type_data = ShipTypeData.from_dict(data["typeData"])
        return cls(
            type=data.get("type", "SHIP"),
            issuer=EntityInfo.from_dict(data.get("issuer", {})),
            subject=SubjectInfo.from_dict(data.get("subject", {})),
            item_id=data.get("itemId", ""),
            timestamp=data.get("timestamp", 0),
            expiration_date=data.get("expirationDate"),
            message=data.get("message"),
            type_data=type_data,
        )


@dataclass
class DSPIPQRData:
    """Complete QR code data structure per Section 4.4."""

    protocol: str
    version: str
    type: Literal["SHIP"]
    key_locator: str
    encoded_payload: str
    signature: str
    private_message: Optional[str] = None


@dataclass
class KeyPair:
    """Key pair structure."""

    private_key: bytes
    public_key: bytes
    private_key_hex: str
    public_key_hex: str
    public_key_base64: str
    public_key_uncompressed: Optional[bytes] = None
    public_key_uncompressed_hex: Optional[str] = None


@dataclass
class DSPIPDNSRecord:
    """DNS TXT record format per Section 5.2."""

    v: str  # Version (DSPIP1)
    k: str  # Key type (ec)
    c: str  # Curve (secp256k1 or ed25519)
    p: str  # Public key (Base64)
    t: Optional[int] = None  # Creation timestamp
    exp: Optional[int] = None  # Signing expiration
    exp_v: Optional[int] = None  # Verification expiration
    s: Optional[KeyStatus] = None  # Status
    seq: Optional[int] = None  # Sequence number
    rsig: Optional[str] = None  # Record signature
    n: Optional[str] = None  # Notes (percent-encoded)
    types: Optional[str] = None  # Supported types
    auth: Optional[AuthorityLevel] = None  # Authority level
    address: Optional[str] = None  # Facility address
    coverage: Optional[str] = None  # Covered zip codes


@dataclass
class ParsedAddress:
    """Parsed address field result."""

    scheme: AddressScheme
    value: str
    raw: str


@dataclass
class VerificationError:
    """Verification error."""

    code: str
    message: str
    details: Optional[str] = None


@dataclass
class VerificationWarning:
    """Verification warning."""

    code: str
    message: str
    details: Optional[str] = None


@dataclass
class VerificationResult:
    """Verification result."""

    valid: bool
    payload: Optional[DSPIPPayload] = None
    key_locator: Optional[str] = None
    signed_by: Optional[str] = None
    key_status: Optional[KeyStatus] = None
    errors: list[VerificationError] = field(default_factory=list)
    warnings: list[VerificationWarning] = field(default_factory=list)
    decrypted_recipient: Optional[dict[str, Any]] = None


@dataclass
class KeyStatusResult:
    """Result of checking key status."""

    can_sign: bool
    can_verify: bool
    status: KeyStatus
    reason: Optional[str] = None


# ============================================================================
# Key Revocation Types (Section 5.5 - Key Revocation)
# ============================================================================

KeyRevocationReason = Literal["compromised", "retired", "superseded", "suspended"]


@dataclass
class KeyRevocationRecord:
    """Key revocation record from DNS TXT record at _revoked-key._dspip.<domain>."""

    v: str
    type: str
    selector: str
    revoked: int
    reason: KeyRevocationReason
    replacement: Optional[str] = None


@dataclass
class KeyRevocationListEntry:
    """Entry in a bulk key revocation list."""

    selector: str
    revoked: int
    reason: KeyRevocationReason
    replacement: Optional[str] = None


@dataclass
class KeyRevocationList:
    """Bulk key revocation list format."""

    version: str
    domain: str
    updated: int
    revoked_keys: list["KeyRevocationListEntry"]
    signature: str
