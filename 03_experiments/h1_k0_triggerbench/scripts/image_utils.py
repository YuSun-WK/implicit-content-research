"""Resolve and validate the frozen TriggerBench image bytes."""
import hashlib
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def image_path(row, side, image_root):
    if side not in ('safe', 'unsafe'):
        raise ValueError(f'invalid image side: {side}')
    relative = Path(row[f'{side}_hf_path'])
    if relative.is_absolute() or '..' in relative.parts:
        raise ValueError(f'unsafe HF image path: {relative}')
    path = Path(image_root) / relative
    if not path.is_file():
        raise FileNotFoundError(f'cached image missing: {path}')
    return path


def load_image(row, side, image_root):
    path = image_path(row, side, image_root)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    expected = row[f'{side}_sha256'].lower()
    if digest != expected:
        raise ValueError(f'SHA256 mismatch for {path}: expected {expected}, got {digest}')
    try:
        with Image.open(path) as source:
            source.load()
            return source.convert('RGB')
    except (OSError, ValueError, UnidentifiedImageError) as exc:
        raise ValueError(f'image decode failed: {path}') from exc
