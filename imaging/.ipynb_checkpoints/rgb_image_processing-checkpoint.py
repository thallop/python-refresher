"""
Tutorial: RGB image creation and manipulation (PPM format)
Image representation:
- A list of H rows, each row is a list of L pixels.
- Each pixel is a triplet (r, g, b) with values between 0 and 255.
"""

from math import sqrt


def create_image(height, width, color):
    """Return an image (list of lists) filled with the same RGB color."""
    return [[tuple(color) for _ in range(width)] for _ in range(height)]


def add_rectangle(img, point_bottom, point_top, color):
    """
    Draw a filled rectangle between two opposite corners.
    img: list of lists of (r,g,b)
    point_bottom: (x1, y1)
    point_top: (x2, y2)
    color: (r, g, b)
    """
    height = len(img)
    width = len(img[0])
    x1, y1 = point_bottom
    x2, y2 = point_top

    xmin, xmax = sorted((x1, x2))
    ymin, ymax = sorted((y1, y2))

    for i in range(max(0, ymin), min(height, ymax)):
        for j in range(max(0, xmin), min(width, xmax)):
            img[i][j] = tuple(color)


def add_circle(img, center, radius, color):
    """
    Draw a filled circle in the image.
    center: (x, y)
    radius: int
    color: (r, g, b)
    """
    height = len(img)
    width = len(img[0])
    cx, cy = center

    for i in range(max(0, cy - radius), min(height, cy + radius)):
        for j in range(max(0, cx - radius), min(width, cx + radius)):
            if (i - cy) ** 2 + (j - cx) ** 2 <= radius ** 2:
                img[i][j] = tuple(color)


def save_image(img, filename):
    """Save image (list of lists of RGB) as a PPM ASCII file."""
    if not filename.endswith(".ppm"):
        filename += ".ppm"

    height = len(img)
    width = len(img[0])

    with open(filename, "w", encoding="utf-8") as f:
        f.write("P3\n")
        f.write(f"{width} {height}\n")
        f.write("255\n")
        for row in img:
            for (r, g, b) in row:
                f.write(f"{r} {g} {b}\n")


def read_image(filename):
    """Read a PPM ASCII (P3) image and return it as a list of lists."""
    with open(filename, "r", encoding="utf-8") as f:
        # Magic number
        line = f.readline().strip()
        while line.startswith("#") or not line:
            line = f.readline().strip()
        assert line == "P3", "Only PPM ASCII (P3) supported."

        # Width and height
        line = f.readline().strip()
        while line.startswith("#") or not line:
            line = f.readline().strip()
        width, height = map(int, line.split())

        # Max value
        line = f.readline().strip()
        while line.startswith("#") or not line:
            line = f.readline().strip()
        max_val = int(line)
        assert max_val == 255

        # Pixels
        values = []
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            values.extend(int(x) for x in line.split())

    assert len(values) == width * height * 3, "Pixel count mismatch."

    img = []
    k = 0
    for _ in range(height):
        row = []
        for _ in range(width):
            r, g, b = values[k:k + 3]
            row.append((r, g, b))
            k += 3
        img.append(row)
    return img


def blur_image(img, d):
    """
    Apply a blur of radius d.
    Each pixel becomes the mean color of neighbors within distance <= d.
    """
    height = len(img)
    width = len(img[0])
    new_img = create_image(height, width, (0, 0, 0))

    for i in range(height):
        for j in range(width):
            r_sum = g_sum = b_sum = count = 0
            for di in range(-d, d + 1):
                for dj in range(-d, d + 1):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < height and 0 <= nj < width:
                        dist = sqrt(di ** 2 + dj ** 2)
                        if dist <= d:
                            r, g, b = img[ni][nj]
                            r_sum += r
                            g_sum += g
                            b_sum += b
                            count += 1
            new_img[i][j] = (
                int(r_sum / count),
                int(g_sum / count),
                int(b_sum / count),
            )
    return new_img


def gray_image(img):
    """Convert an RGB image to grayscale."""
    height = len(img)
    width = len(img[0])
    gray_img = create_image(height, width, (0, 0, 0))
    for i in range(height):
        for j in range(width):
            r, g, b = img[i][j]
            gray = int((r + g + b) / 3)
            gray_img[i][j] = (gray, gray, gray)
    return gray_img


# Create a base blue background
img = create_image(300, 300, (31, 119, 180))

# Add shapes
add_circle(img, (115, 115), 30, (255, 127, 14))
add_rectangle(img, (115, 115), (185, 185), (44, 160, 44))

# Save artwork creation
save_image(img, "my_artwork")

# Read ppm image
img = read_image("rose-ringed-parakeet.ppm")

# Blur and gray filters
blurred = blur_image(img, 10)
save_image(blurred, "parakeet-blur")

gray = gray_image(blurred)
save_image(gray, "parakeet-blur-gray")