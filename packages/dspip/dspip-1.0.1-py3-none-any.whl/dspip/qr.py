"""
DSPIP SDK - QR Code Generation and Parsing
Per Internet-Draft draft-midwestcyber-dspip-02
"""

import io
from typing import Any, Optional

from .payload import decode_payload, parse_qr_data
from .types import DSPIPQRData, PrivacyMode

# QR Code version capacities (alphanumeric mode, error correction L)
QR_CAPACITIES = [
    25,
    47,
    77,
    114,
    154,
    195,
    224,
    279,
    335,
    395,
    468,
    535,
    619,
    667,
    758,
    854,
    938,
    1046,
    1153,
    1249,
    1352,
    1460,
    1588,
    1704,
    1853,
    1990,
    2132,
    2223,
    2369,
    2520,
    2677,
    2840,
    3009,
    3183,
    3351,
    3537,
    3729,
    3927,
    4087,
    4296,
]


def get_optimal_qr_version(data_length: int) -> int:
    """Get the optimal QR code version for a data length.

    Args:
        data_length: Length of data in characters

    Returns:
        QR code version (1-40)

    Raises:
        ValueError: If data is too large for any QR version
    """
    for version, capacity in enumerate(QR_CAPACITIES, 1):
        if data_length <= capacity:
            return version
    raise ValueError(f"Data too large for QR code: {data_length} characters (max: {QR_CAPACITIES[-1]})")


def will_fit_in_qr_code(data: str, max_version: int = 40) -> bool:
    """Check if data will fit in a QR code.

    Args:
        data: Data to encode
        max_version: Maximum QR version to consider

    Returns:
        True if data fits
    """
    try:
        version = get_optimal_qr_version(len(data))
        return version <= max_version
    except ValueError:
        return False


def generate_qr_code_data_url(
    data: str,
    error_correction: str = "L",
    box_size: int = 10,
    border: int = 4,
) -> str:
    """Generate a QR code as a data URL (base64 PNG).

    Args:
        data: Data to encode
        error_correction: Error correction level (L, M, Q, H)
        box_size: Size of each box in pixels
        border: Border size in boxes

    Returns:
        Data URL string (data:image/png;base64,...)
    """
    import base64

    import qrcode
    from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

    error_levels = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=None,  # Auto-detect
        error_correction=error_levels.get(error_correction, ERROR_CORRECT_L),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    b64 = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def generate_qr_code_svg(
    data: str,
    error_correction: str = "L",
    box_size: int = 10,
    border: int = 4,
) -> str:
    """Generate a QR code as SVG string.

    Args:
        data: Data to encode
        error_correction: Error correction level
        box_size: Size of each box in pixels
        border: Border size in boxes

    Returns:
        SVG string
    """
    import qrcode
    import qrcode.image.svg
    from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

    error_levels = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_levels.get(error_correction, ERROR_CORRECT_L),
        box_size=box_size,
        border=border,
        image_factory=qrcode.image.svg.SvgImage,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image()

    buffer = io.BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return buffer.getvalue().decode("utf-8")


def generate_qr_code_terminal(
    data: str,
    error_correction: str = "L",
) -> str:
    """Generate a QR code for terminal display.

    Args:
        data: Data to encode
        error_correction: Error correction level

    Returns:
        String representation for terminal
    """
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

    error_levels = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_levels.get(error_correction, ERROR_CORRECT_L),
        box_size=1,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Generate ASCII representation
    lines = []
    matrix = qr.get_matrix()

    for row in matrix:
        line = ""
        for cell in row:
            line += "██" if cell else "  "
        lines.append(line)

    return "\n".join(lines)


def generate_qr_code_bytes(
    data: str,
    error_correction: str = "L",
    box_size: int = 10,
    border: int = 4,
    format: str = "PNG",
) -> bytes:
    """Generate a QR code as bytes.

    Args:
        data: Data to encode
        error_correction: Error correction level
        box_size: Size of each box in pixels
        border: Border size in boxes
        format: Image format (PNG, JPEG, etc.)

    Returns:
        Image bytes
    """
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

    error_levels = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_levels.get(error_correction, ERROR_CORRECT_L),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)

    return buffer.getvalue()


def save_qr_code_to_file(
    data: str,
    file_path: str,
    error_correction: str = "L",
    box_size: int = 10,
    border: int = 4,
) -> None:
    """Save a QR code to a file.

    Args:
        data: Data to encode
        file_path: Path to save the image
        error_correction: Error correction level
        box_size: Size of each box in pixels
        border: Border size in boxes
    """
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H, ERROR_CORRECT_L, ERROR_CORRECT_M, ERROR_CORRECT_Q

    error_levels = {
        "L": ERROR_CORRECT_L,
        "M": ERROR_CORRECT_M,
        "Q": ERROR_CORRECT_Q,
        "H": ERROR_CORRECT_H,
    }

    qr = qrcode.QRCode(
        version=None,
        error_correction=error_levels.get(error_correction, ERROR_CORRECT_L),
        box_size=box_size,
        border=border,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(file_path)


# QR data parsing utilities


def parse_scanned_data(scanned_data: str) -> DSPIPQRData:
    """Parse scanned QR code data.

    Args:
        scanned_data: Raw scanned data string

    Returns:
        Parsed DSPIPQRData
    """
    return parse_qr_data(scanned_data)


def extract_tracking_info(qr_data: str) -> dict[str, Any]:
    """Extract tracking information from QR data.

    Args:
        qr_data: Raw QR data string

    Returns:
        Dictionary with tracking info
    """
    parsed = parse_qr_data(qr_data)
    payload = decode_payload(parsed.encoded_payload)

    result: dict[str, Any] = {
        "itemId": payload.item_id,
        "type": payload.type,
        "timestamp": payload.timestamp,
        "keyLocator": parsed.key_locator,
    }

    if payload.type_data:
        if payload.type_data.parcel_id:
            result["parcelId"] = payload.type_data.parcel_id
        if payload.type_data.carrier:
            result["carrier"] = payload.type_data.carrier
        if payload.type_data.service:
            result["service"] = payload.type_data.service
        if payload.type_data.privacy_mode:
            result["privacyMode"] = payload.type_data.privacy_mode.value

    return result


def is_privacy_mode(qr_data: str) -> bool:
    """Check if QR data uses a privacy mode.

    Args:
        qr_data: Raw QR data string

    Returns:
        True if using encrypted or split-key mode
    """
    parsed = parse_qr_data(qr_data)
    payload = decode_payload(parsed.encoded_payload)

    if payload.type_data and payload.type_data.privacy_mode:
        return payload.type_data.privacy_mode in (PrivacyMode.ENCRYPTED, PrivacyMode.SPLIT_KEY)

    return payload.subject.encrypted


def requires_decryption(qr_data: str) -> bool:
    """Check if QR data requires decryption.

    Args:
        qr_data: Raw QR data string

    Returns:
        True if decryption is required
    """
    parsed = parse_qr_data(qr_data)
    payload = decode_payload(parsed.encoded_payload)

    return payload.subject.encrypted


def get_public_sender_info(qr_data: str) -> dict[str, Any]:
    """Get publicly visible sender information.

    Args:
        qr_data: Raw QR data string

    Returns:
        Dictionary with sender info
    """
    parsed = parse_qr_data(qr_data)
    payload = decode_payload(parsed.encoded_payload)

    return payload.issuer.to_dict()


def get_recipient_info(qr_data: str) -> Optional[dict[str, Any]]:
    """Get recipient information (if not encrypted).

    Args:
        qr_data: Raw QR data string

    Returns:
        Dictionary with recipient info, or None if encrypted
    """
    parsed = parse_qr_data(qr_data)
    payload = decode_payload(parsed.encoded_payload)

    if payload.subject.encrypted:
        return None

    return payload.subject.to_dict()
