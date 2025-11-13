"""
Tutorial: PGM edge detection (Sobel-like)
Keeps 3 variables at each step:
- width
- height
- pixels (flattened list, row major)
Works for ASCII PGM (P2).
"""

from math import sqrt


def file_to_list(filename):
    """Read an ASCII PGM (P2) file and return (width, height, pixels)."""
    with open(filename, "r", encoding="utf-8") as f:
        # read magic number
        line = f.readline().strip()
        while line.startswith("#") or line == "":
            line = f.readline().strip()
        assert line == "P2", "Only ASCII PGM (P2) is supported."

        # read width and height
        line = f.readline().strip()
        while line.startswith("#") or line == "":
            line = f.readline().strip()
        parts = line.split()
        if len(parts) == 2:
            width, height = map(int, parts)
        else:
            width = int(parts[0])
            height = int(f.readline().strip())

        # read max gray
        line = f.readline().strip()
        while line.startswith("#") or line == "":
            line = f.readline().strip()
        max_gray = int(line)
        assert max_gray <= 255

        # read pixel values (may be on many lines)
        values = []
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            values.extend(int(x) for x in line.split())

        assert len(values) == width * height, (
            "Pixel count does not match size."
        )

    return width, height, values


def list_to_file(width, height, pixels, filename):
    """Write (width, height, pixels) to an ASCII PGM (P2) file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write("P2\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")
        for val in pixels:
            f.write(f"{val}\n")


def get_pixel(pixels, width, height, i, j):
    """Return pixel value at row i, col j, or 0 if out of bounds."""
    if i < 0 or j < 0 or i >= height or j >= width:
        return 0
    return pixels[i * width + j]


def filter_image(height, width, pixels, grad):
    """Apply a 3x3 mask (grad) to the image and return a new pixel list."""
    result = [0] * (width * height)
    for i in range(height):
        for j in range(width):
            acc = 0
            idx = 0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    val = get_pixel(pixels, width, height, i + di, j + dj)
                    acc += val * grad[idx]
                    idx += 1
            acc = max(0, min(255, acc))
            result[i * width + j] = acc
    return result


# predefined masks (Sobel-like)
GRAD_H = [-1, 0, 1,
          -2, 0, 2,
          -1, 0, 1]

GRAD_V = [-1, -2, -1,
          0, 0, 0,
          1, 2, 1]


def edge_magnitude(width, height, src1, src2):
    """Return sqrt(src1^2 + src2^2) for each pixel."""
    result = []
    for p1, p2 in zip(src1, src2):
        val = int(sqrt(p1 ** 2 + p2 ** 2))
        result.append(min(val, 255))
    return result


def invert(pixels):
    """Invert gray level for each pixel."""
    return [255 - p for p in pixels]


def threshold(pixels, t):
    """If pixel > threshold -> 255 else 0."""
    return [255 if p > t else 0 for p in pixels]


def edge_detection_pipeline(src_filename, dst_prefix="src"):
    """
    Full edge detection pipeline:
    1. load src
    2. apply horizontal gradient -> src1
    3. apply vertical gradient -> src2
    4. combine -> src3
    5. invert -> src4
    6. threshold at 125 -> src5
    All images are saved.
    """
    width, height, pixels = file_to_list(src_filename)

    # 1. horizontal
    src1 = filter_image(height, width, pixels, GRAD_H)
    list_to_file(width, height, src1, f"{dst_prefix}1.pgm")

    # 2. vertical
    src2 = filter_image(height, width, pixels, GRAD_V)
    list_to_file(width, height, src2, f"{dst_prefix}2.pgm")

    # 3. combine
    src3 = edge_magnitude(width, height, src1, src2)
    list_to_file(width, height, src3, f"{dst_prefix}3.pgm")

    # 4. invert
    src4 = invert(src3)
    list_to_file(width, height, src4, f"{dst_prefix}4.pgm")

    # 5. threshold
    src5 = threshold(src4, 125)
    list_to_file(width, height, src5, f"{dst_prefix}5.pgm")


# copy test 
w, h, pix = file_to_list("rose-ringed-parakeet.pgm")
list_to_file(w, h, pix, "rose-ringed-parakeet_copy.pgm")

# full edge detection pipeline
edge_detection_pipeline("rose-ringed-parakeet.pgm")