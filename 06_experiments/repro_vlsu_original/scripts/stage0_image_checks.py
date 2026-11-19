"""Pure CPU validation for the Stage 1 design. No DNS or HTTP is performed here."""

from hashlib import sha256
from io import BytesIO
from ipaddress import ip_address
from urllib.parse import urlsplit
import warnings

from PIL import Image


def check_target(url, resolved_addresses):
    """Validate a URL and its supplied DNS results before a pinned connection."""
    if any(character.isspace() or ord(character) < 32 or character == "\\" for character in url):
        raise ValueError("invalid_url_characters")
    target = urlsplit(url)
    if target.scheme not in {"http", "https"} or not target.hostname or target.username is not None:
        raise ValueError("invalid_url")
    if target.port not in {None, 443 if target.scheme == "https" else 80}:
        raise ValueError("unsupported_port")
    host = target.hostname.rstrip(".").lower()
    if host == "localhost" or host.endswith(".localhost") or "%" in host:
        raise ValueError("local_hostname")
    try:
        literal = ip_address(host)
    except ValueError:
        literal = None
    # Check literal URLs directly, even if the caller supplied different DNS answers.
    addresses = [literal] if literal is not None else [ip_address(addr) for addr in resolved_addresses]
    if not addresses:
        raise ValueError("missing_dns_answer")
    for address in addresses:
        if address.version == 6:
            if address.sixtofour is not None or address.teredo is not None:
                raise ValueError("transition_address")
            address = address.ipv4_mapped or address
        if (not address.is_global or address.is_multicast or address.is_reserved
                or getattr(address, "is_site_local", False)):
            raise ValueError("non_public_address")
    return host, tuple(str(address) for address in addresses)


def check_image(raw, content_type, *, max_bytes, max_pixels):
    """Verify container and decode the first frame for Stage 1 coverage accounting."""
    if not raw or len(raw) > max_bytes:
        raise ValueError("image_byte_limit")
    mime = content_type.partition(";")[0].strip().lower()
    if not mime.startswith("image/"):
        raise ValueError("unsupported_content_type")
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        with Image.open(BytesIO(raw)) as image:
            if image.width * image.height > max_pixels:
                raise ValueError("image_pixel_limit")
            format_name = image.format
            if mime != Image.MIME.get(format_name):
                raise ValueError("image_mime_mismatch")
            image.verify()
        with Image.open(BytesIO(raw)) as image:
            image.load()
            return {
                "sha256": sha256(raw).hexdigest(), "bytes": len(raw),
                "format": format_name, "width": image.width, "height": image.height,
                "animated": getattr(image, "is_animated", False),
            }
