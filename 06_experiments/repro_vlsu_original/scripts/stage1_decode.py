"""Resource-bounded first-frame decode subprocess. Output contains metadata only."""

import json
from pathlib import Path
import resource
import sys


def main():
    path, mime, byte_limit, pixel_limit, memory, cpu = sys.argv[1:]
    resource.setrlimit(resource.RLIMIT_AS, (int(memory), int(memory)))
    resource.setrlimit(resource.RLIMIT_CPU, (int(cpu), int(cpu) + 1))
    from PIL import Image, UnidentifiedImageError
    from stage0_image_checks import check_image

    try:
        result = check_image(Path(path).read_bytes(), mime, max_bytes=int(byte_limit), max_pixels=int(pixel_limit))
    except ValueError as error:
        result = {"reason": str(error)}
    except UnidentifiedImageError:
        result = {"reason": "unidentified_image"}
    except (Image.DecompressionBombError, Image.DecompressionBombWarning):
        result = {"reason": "image_pixel_limit"}
    except MemoryError:
        result = {"reason": "decode_memory_limit"}
    except (OSError, SyntaxError, EOFError):
        result = {"reason": "image_decode_failed"}
    print(json.dumps(result))


if __name__ == "__main__":
    main()
