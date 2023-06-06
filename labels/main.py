from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

DEBUG_BORDER = True  # Set to False to hide label borders


def create_labels() -> None:
    """Create labels for the Jacksonville Presbyterian Church Disabilities Ministry."""

    # Dimensions
    top_margin, _ = 0.5 * inch, 0.5 * inch
    left_margin, _ = 0.156 * inch, 0.156 * inch
    center_margin = 0.188 * inch
    label_width, label_height = 4 * inch, 3.33 * inch
    _, page_height = letter  # Default letter paper size
    image_filename = "jpc_dm_logo.png"
    image_scale_factor = 0.4  # Scale image to 40% of original size

    # Open image file
    im = Image.open(image_filename)
    width, height = im.size
    new_width, new_height = (
        width * image_scale_factor,
        height * image_scale_factor,
    )  # calculate new size
    im = im.resize((int(new_width), int(new_height)))  # resize image
    im.save("resized_" + image_filename)

    # Create canvas
    output_filename = "labels_debug.pdf" if DEBUG_BORDER else "labels.pdf"
    c = canvas.Canvas(output_filename, pagesize=letter)

    # Starting position for first label (top left corner)
    x, y = left_margin, page_height - top_margin - label_height

    for i in range(6):  # 6 labels
        # Draw image, centered and slightly nudged up
        image_x = x + (label_width - new_width) / 2
        image_y = (
            y + (label_height - new_height) / 2 + 0.1 * inch + 20
        )  # nudge up by 20 pixels
        c.drawInlineImage("resized_" + image_filename, image_x, image_y)

        # Add text in Helvetica under the image
        c.setFont("Helvetica", 16)  # Decrease font size to 16
        c.drawCentredString(
            x + label_width / 2,
            y + label_height / 2 - new_height / 2 - 0.2 * inch + 20,
            "Jacksonville Presbyterian Church",
        )  # nudge up by 20 pixels
        c.drawCentredString(
            x + label_width / 2,
            y + label_height / 2 - new_height / 2 - 0.5 * inch + 20,
            "Disabilities Ministry",
        )  # nudge up by 20 pixels and add more leading

        # Draw border for debugging
        if DEBUG_BORDER:
            c.rect(x, y, label_width, label_height)

        # Calculate position for next label
        if i % 2 != 0:  # Move to next row after every two labels
            y -= label_height
            x = left_margin
        else:  # Move to next column
            x += label_width + center_margin

    c.save()


if __name__ == "__main__":
    create_labels()
