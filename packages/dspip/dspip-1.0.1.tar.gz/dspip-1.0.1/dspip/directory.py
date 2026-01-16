"""
Directory Services for DSPIP

Implements Section 7.2.5 of the Internet-Draft:
- Last Mile Provider (LMP) lookup by location
- Provider registration and discovery
- Coverage area queries

Supports delegation schemes:
- geo: Geographic (lat/long bounding boxes)
- postal: Postal codes
- region: Administrative regions
- list: Explicit selector lists
- service: Service type-based routing
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Dict, Any, Callable, Tuple
import time
import json
import re
import hashlib

from .types import AuthorityLevel


# ============================================================================
# Constants
# ============================================================================

DIRECTORY_BASE_URL = "https://directory.dspip.io/v1"
MAX_PROVIDERS = 16
MAX_COVERAGE_AREAS = 32
CACHE_TTL_SECONDS = 3600  # 1 hour
DIRECTORY_CACHE_TTL = CACHE_TTL_SECONDS  # Alias for external use


# ============================================================================
# Types
# ============================================================================

class DelegationScheme(Enum):
    """Delegation scheme per Section 5.3"""
    GEO = "geo"           # Geographic (lat/long bounding boxes)
    POSTAL = "postal"     # Postal codes
    REGION = "region"     # Administrative regions
    LIST = "list"         # Explicit selector lists
    SERVICE = "service"   # Service type-based routing


class ServiceType(Enum):
    """Provider service type"""
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    RURAL = "rural"
    EXPRESS = "express"


@dataclass
class GeoBounds:
    """Geographic bounding box"""
    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float

    def contains(self, lat: float, lon: float) -> bool:
        """Check if a point is within the bounds"""
        return (self.min_lat <= lat <= self.max_lat and
                self.min_lon <= lon <= self.max_lon)


@dataclass
class CoverageArea:
    """Coverage area definition"""
    scheme: DelegationScheme
    geo_bounds: Optional[GeoBounds] = None
    postal_codes: Optional[List[str]] = None
    regions: Optional[List[str]] = None
    service_type: Optional[ServiceType] = None
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        result = {"scheme": self.scheme.value, "description": self.description}
        if self.geo_bounds:
            result["geoBounds"] = {
                "minLat": self.geo_bounds.min_lat,
                "maxLat": self.geo_bounds.max_lat,
                "minLon": self.geo_bounds.min_lon,
                "maxLon": self.geo_bounds.max_lon,
            }
        if self.postal_codes:
            result["postalCodes"] = self.postal_codes
        if self.regions:
            result["regions"] = self.regions
        if self.service_type:
            result["serviceType"] = self.service_type.value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CoverageArea":
        geo_bounds = None
        if "geoBounds" in data:
            gb = data["geoBounds"]
            geo_bounds = GeoBounds(
                min_lat=gb["minLat"],
                max_lat=gb["maxLat"],
                min_lon=gb["minLon"],
                max_lon=gb["maxLon"],
            )
        return cls(
            scheme=DelegationScheme(data["scheme"]),
            geo_bounds=geo_bounds,
            postal_codes=data.get("postalCodes"),
            regions=data.get("regions"),
            service_type=ServiceType(data["serviceType"]) if data.get("serviceType") else None,
            description=data.get("description", ""),
        )


@dataclass
class Provider:
    """Last Mile Provider (LMP) information"""
    name: str
    key_locator: str
    public_key_hex: str
    authority: AuthorityLevel = AuthorityLevel.ENTERPRISE
    coverage: List[CoverageArea] = field(default_factory=list)
    contact_email: str = ""
    contact_phone: str = ""
    website: str = ""
    registered_at: int = 0
    expires_at: int = 0
    active: bool = True
    services: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "keyLocator": self.key_locator,
            "publicKey": self.public_key_hex,
            "authority": self.authority.value if isinstance(self.authority, AuthorityLevel) else self.authority,
            "coverage": [c.to_dict() for c in self.coverage],
            "contactEmail": self.contact_email,
            "contactPhone": self.contact_phone,
            "website": self.website,
            "registeredAt": self.registered_at,
            "expiresAt": self.expires_at,
            "active": self.active,
            "services": self.services,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Provider":
        authority = data.get("authority", "enterprise")
        if isinstance(authority, str):
            authority = AuthorityLevel(authority)
        return cls(
            name=data.get("name", ""),
            key_locator=data.get("keyLocator", ""),
            public_key_hex=data.get("publicKey", ""),
            authority=authority,
            coverage=[CoverageArea.from_dict(c) for c in data.get("coverage", [])],
            contact_email=data.get("contactEmail", ""),
            contact_phone=data.get("contactPhone", ""),
            website=data.get("website", ""),
            registered_at=data.get("registeredAt", 0),
            expires_at=data.get("expiresAt", 0),
            active=data.get("active", True),
            services=data.get("services", []),
        )


@dataclass
class ProviderLookupResult:
    """Provider lookup result"""
    providers: List[Provider]
    queried_at: int
    query_location: str
    from_cache: bool = False


@dataclass
class DirectoryQueryOptions:
    """Directory query options"""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None  # ISO 3166-1 alpha-2
    service_type: Optional[ServiceType] = None
    min_authority: Optional[AuthorityLevel] = None
    use_cache: bool = True
    cache_ttl_seconds: int = CACHE_TTL_SECONDS


@dataclass
class DiscoveryRecord:
    """Discovery record per Section 5.3"""
    version: str
    record_type: str  # "discovery"
    selectors: List[str]
    delegation: DelegationScheme
    pattern: Optional[str] = None
    coverage: Optional[str] = None


# ============================================================================
# HTTP Client Type
# ============================================================================

HttpGetCallback = Callable[[str], Tuple[str, int]]  # (url) -> (response, status)
HttpPostCallback = Callable[[str, str, str], Tuple[str, int]]  # (url, body, content_type) -> (response, status)


@dataclass
class DirectoryClientConfig:
    """Directory service client configuration"""
    base_url: str = DIRECTORY_BASE_URL
    http_get: Optional[HttpGetCallback] = None
    http_post: Optional[HttpPostCallback] = None
    timeout_seconds: int = 10
    verify_ssl: bool = True


# ============================================================================
# Cache
# ============================================================================

class ProviderCache:
    """Simple provider cache with TTL"""

    def __init__(self):
        self._cache: Dict[str, Tuple[ProviderLookupResult, int]] = {}
        self._hits = 0
        self._misses = 0

    def get(self, key: str, ttl: int) -> Optional[ProviderLookupResult]:
        if key in self._cache:
            result, timestamp = self._cache[key]
            if time.time() - timestamp < ttl:
                self._hits += 1
                return ProviderLookupResult(
                    providers=result.providers,
                    queried_at=result.queried_at,
                    query_location=result.query_location,
                    from_cache=True,
                )
        self._misses += 1
        return None

    def set(self, key: str, result: ProviderLookupResult):
        self._cache[key] = (result, int(time.time()))

    def clear(self):
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def stats(self) -> Dict[str, int]:
        return {
            "size": len(self._cache),
            "hits": self._hits,
            "misses": self._misses,
        }


_provider_cache = ProviderCache()


def clear_provider_cache():
    """Clear the provider cache"""
    _provider_cache.clear()


def get_provider_cache_stats() -> Dict[str, int]:
    """Get provider cache statistics"""
    return _provider_cache.stats()


# ============================================================================
# Directory Service Functions
# ============================================================================

def lookup_providers_by_location(
    latitude: float,
    longitude: float,
    options: Optional[DirectoryQueryOptions] = None,
    config: Optional[DirectoryClientConfig] = None,
) -> ProviderLookupResult:
    """
    Lookup providers by geographic location.

    Args:
        latitude: Latitude
        longitude: Longitude
        options: Query options
        config: Client configuration

    Returns:
        ProviderLookupResult with matching providers
    """
    options = options or DirectoryQueryOptions()
    config = config or DirectoryClientConfig()

    cache_key = f"geo:{latitude:.4f},{longitude:.4f}"
    if options.use_cache:
        cached = _provider_cache.get(cache_key, options.cache_ttl_seconds)
        if cached:
            return cached

    # Build URL
    url = f"{config.base_url}/providers?lat={latitude}&lon={longitude}"
    if options.service_type:
        url += f"&service={options.service_type.value}"
    if options.min_authority:
        url += f"&minAuthority={options.min_authority.value}"

    # Make request
    providers = []
    if config.http_get:
        response, status = config.http_get(url)
        if status == 200:
            data = json.loads(response)
            providers = [Provider.from_dict(p) for p in data.get("providers", [])]

    result = ProviderLookupResult(
        providers=providers[:MAX_PROVIDERS],
        queried_at=int(time.time() * 1000),
        query_location=f"{latitude},{longitude}",
        from_cache=False,
    )

    if options.use_cache:
        _provider_cache.set(cache_key, result)

    return result


def lookup_providers_by_postal(
    postal_code: str,
    country_code: str,
    options: Optional[DirectoryQueryOptions] = None,
    config: Optional[DirectoryClientConfig] = None,
) -> ProviderLookupResult:
    """
    Lookup providers by postal code.

    Args:
        postal_code: Postal/ZIP code
        country_code: ISO 3166-1 alpha-2 country code (e.g., "US")
        options: Query options
        config: Client configuration

    Returns:
        ProviderLookupResult with matching providers
    """
    options = options or DirectoryQueryOptions()
    config = config or DirectoryClientConfig()

    cache_key = f"postal:{country_code}:{postal_code}"
    if options.use_cache:
        cached = _provider_cache.get(cache_key, options.cache_ttl_seconds)
        if cached:
            return cached

    # Build URL
    url = f"{config.base_url}/providers?zip={postal_code}&country={country_code}"
    if options.service_type:
        url += f"&service={options.service_type.value}"
    if options.min_authority:
        url += f"&minAuthority={options.min_authority.value}"

    # Make request
    providers = []
    if config.http_get:
        response, status = config.http_get(url)
        if status == 200:
            data = json.loads(response)
            providers = [Provider.from_dict(p) for p in data.get("providers", [])]

    result = ProviderLookupResult(
        providers=providers[:MAX_PROVIDERS],
        queried_at=int(time.time() * 1000),
        query_location=f"{country_code}:{postal_code}",
        from_cache=False,
    )

    if options.use_cache:
        _provider_cache.set(cache_key, result)

    return result


def get_provider(
    key_locator: str,
    config: Optional[DirectoryClientConfig] = None,
) -> Optional[Provider]:
    """
    Get provider by key locator.

    Args:
        key_locator: Provider's key locator
        config: Client configuration

    Returns:
        Provider if found, None otherwise
    """
    config = config or DirectoryClientConfig()

    url = f"{config.base_url}/provider/{key_locator}"

    if config.http_get:
        response, status = config.http_get(url)
        if status == 200:
            data = json.loads(response)
            return Provider.from_dict(data)

    return None


def register_provider(
    name: str,
    public_key_hex: str,
    private_key_hex: str,
    authority: AuthorityLevel,
    coverage: List[CoverageArea],
    contact_email: str = "",
    contact_phone: str = "",
    website: str = "",
    config: Optional[DirectoryClientConfig] = None,
) -> Optional[str]:
    """
    Register a new provider.

    Args:
        name: Provider name
        public_key_hex: Public key in hex
        private_key_hex: Private key for authentication (signs the registration)
        authority: Authority level
        coverage: Coverage areas
        contact_email: Contact email
        contact_phone: Contact phone
        website: Website URL
        config: Client configuration

    Returns:
        Assigned key locator if successful, None otherwise
    """
    config = config or DirectoryClientConfig()

    # Build registration payload
    timestamp = int(time.time() * 1000)
    payload = {
        "name": name,
        "publicKey": public_key_hex,
        "authority": authority.value,
        "coverage": [c.to_dict() for c in coverage],
        "contactEmail": contact_email,
        "contactPhone": contact_phone,
        "website": website,
        "timestamp": timestamp,
    }

    # Sign with private key (signature over JSON string)
    payload_str = json.dumps(payload, sort_keys=True)
    signature = hashlib.sha256(payload_str.encode() + bytes.fromhex(private_key_hex)).hexdigest()
    payload["signature"] = signature

    url = f"{config.base_url}/providers"

    if config.http_post:
        response, status = config.http_post(url, json.dumps(payload), "application/json")
        if status == 201 or status == 200:
            data = json.loads(response)
            return data.get("keyLocator")

    return None


# ============================================================================
# Coverage Checking
# ============================================================================

def is_in_coverage(latitude: float, longitude: float, coverage: CoverageArea) -> bool:
    """
    Check if a location is within a coverage area.

    Args:
        latitude: Latitude to check
        longitude: Longitude to check
        coverage: Coverage area definition

    Returns:
        True if location is within coverage
    """
    if coverage.scheme == DelegationScheme.GEO and coverage.geo_bounds:
        return coverage.geo_bounds.contains(latitude, longitude)
    return False


def postal_in_coverage(postal_code: str, coverage: CoverageArea) -> bool:
    """
    Check if a postal code is within a coverage area.

    Args:
        postal_code: Postal code to check
        coverage: Coverage area definition

    Returns:
        True if postal code is within coverage
    """
    if coverage.scheme == DelegationScheme.POSTAL and coverage.postal_codes:
        # Check exact match or prefix match
        for code in coverage.postal_codes:
            if code.endswith("-"):
                # Range like "68101-68199" or prefix like "681"
                if postal_code.startswith(code.rstrip("-")):
                    return True
            elif "-" in code:
                # Range like "68101-68199"
                parts = code.split("-")
                if len(parts) == 2:
                    try:
                        start = int(parts[0])
                        end = int(parts[1])
                        postal_int = int(postal_code)
                        if start <= postal_int <= end:
                            return True
                    except ValueError:
                        pass
            elif postal_code == code:
                return True
    return False


# ============================================================================
# DNS-Based Discovery (Offline/Embedded)
# ============================================================================

def parse_discovery_record(txt_record: str) -> Optional[DiscoveryRecord]:
    """
    Parse discovery record from DNS TXT.

    Per Section 5.3.2, discovery records contain delegation information.

    Args:
        txt_record: TXT record string

    Returns:
        DiscoveryRecord if valid, None otherwise
    """
    fields = {}
    for part in txt_record.split(";"):
        part = part.strip()
        if "=" in part:
            key, value = part.split("=", 1)
            fields[key.strip()] = value.strip()

    if fields.get("v") != "DSPIP1" or fields.get("type") != "discovery":
        return None

    selectors = []
    if "selectors" in fields:
        selectors = [s.strip() for s in fields["selectors"].split(",")]

    delegation = DelegationScheme.LIST
    if "delegation" in fields:
        try:
            delegation = DelegationScheme(fields["delegation"])
        except ValueError:
            pass

    return DiscoveryRecord(
        version=fields.get("v", "DSPIP1"),
        record_type="discovery",
        selectors=selectors,
        delegation=delegation,
        pattern=fields.get("pattern"),
        coverage=fields.get("coverage"),
    )


def build_selector_from_delegation(
    base_domain: str,
    scheme: DelegationScheme,
    value: str,
) -> str:
    """
    Build selector from discovery delegation.

    Args:
        base_domain: Base domain (e.g., "example.com")
        scheme: Delegation scheme
        value: Delegation value (e.g., postal code, region name)

    Returns:
        Full selector (e.g., "68101._dspip.example.com")
    """
    # Clean up base domain
    base = base_domain.replace("_dspip.", "")

    if scheme == DelegationScheme.POSTAL:
        return f"{value}._dspip.{base}"
    elif scheme == DelegationScheme.GEO:
        # Use geohash or simplified coordinates
        return f"{value}._dspip.{base}"
    elif scheme == DelegationScheme.REGION:
        return f"{value.lower().replace(' ', '-')}._dspip.{base}"
    elif scheme == DelegationScheme.SERVICE:
        return f"{value.lower()}._dspip.{base}"
    else:
        # LIST scheme - value is the selector itself
        return f"{value}._dspip.{base}"


def discover_selectors(
    domain: str,
    discovery_record: DiscoveryRecord,
) -> List[str]:
    """
    Discover available selectors for a domain.

    Args:
        domain: Base domain
        discovery_record: Parsed discovery record

    Returns:
        List of available selectors
    """
    if discovery_record.delegation == DelegationScheme.LIST:
        return [
            build_selector_from_delegation(domain, DelegationScheme.LIST, s)
            for s in discovery_record.selectors
        ]
    return []


# ============================================================================
# Utility Functions
# ============================================================================

def serialize_provider(provider: Provider) -> str:
    """Serialize provider to JSON string"""
    return json.dumps(provider.to_dict(), indent=2)


def parse_provider(json_str: str) -> Provider:
    """Parse provider from JSON string"""
    return Provider.from_dict(json.loads(json_str))
