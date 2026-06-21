!pip install gradio pillow -q

import gradio as gr
from PIL import Image
import os

def compress_image(image, compression):
    if image is None:
        return None, "", None

    temp_original = "original_temp.jpg"
    image.save(temp_original, quality=100)

    original_size = os.path.getsize(temp_original) / 1024
    original_width, original_height = image.size

    scale = (100 - compression) / 100

    new_width = max(1, int(original_width * scale))
    new_height = max(1, int(original_height * scale))

    compressed_img = image.resize(
        (new_width, new_height),
        Image.LANCZOS
    )

    output_file = "compressed_image.jpg"

    compressed_img.save(
        output_file,
        quality=max(5, 100 - compression)
    )

    compressed_size = os.path.getsize(output_file) / 1024

    info = f"""
📷 ORIGINAL IMAGE

Size: {original_size:.2f} KB
Dimensions: {original_width} × {original_height}

🗜 COMPRESSED IMAGE

Size: {compressed_size:.2f} KB
Dimensions: {new_width} × {new_height}

📉 Compression Applied: {compression}%
"""

    return compressed_img, info, output_file


demo = gr.Interface(
    fn=compress_image,
    inputs=[
        gr.Image(type="pil", label="Upload Image"),
        gr.Slider(
            minimum=0,
            maximum=100,
            value=50,
            step=1,
            label="Compression Percentage"
        )
    ],
    outputs=[
        gr.Image(label="Compressed Preview"),
        gr.Textbox(label="Image Details"),
        gr.File(label="Download Compressed Image")
    ],
    title="Image Compression Tool",
    description="Upload an image, select compression percentage, and download the compressed image."
)

demo.launch(share=True)
