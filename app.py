import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- CONFIGURATION ---
POSTER_PATH = "Attending 2025.png"
FONT_PATH = "PhotographSignature.ttf"

def create_poster(user_image_file, user_name, photo_scale, photo_pos_x, photo_pos_y, name_font_size):
    """
    Composites the poster by placing the user's photo BEHIND the poster template.
    """
    # Open the poster template and user's photo
    poster_template = Image.open(POSTER_PATH).convert("RGBA")
    user_photo = Image.open(user_image_file).convert("RGBA")

    # Create a new, blank canvas the same size as the poster
    canvas = Image.new("RGBA", poster_template.size)

    # Resize and position the user's photo
    base_photo_width = 530
    aspect_ratio = user_photo.height / user_photo.width
    new_width = int(base_photo_width * photo_scale)
    new_height = int(new_width * aspect_ratio)
    user_photo = user_photo.resize((new_width, new_height))
    
    # Calculate where to place the photo so it appears centered in the hole, then adjust with sliders
    photo_paste_x = (canvas.width // 2) - (new_width // 2) + photo_pos_x
    photo_paste_y = 455 - (new_height // 2) + photo_pos_y
    
    # Paste the user's photo onto the blank canvas FIRST
    canvas.paste(user_photo, (photo_paste_x, photo_paste_y))

    # Paste the poster template ON TOP of the canvas with the user's photo
    # The template's own transparency will act as the mask
    canvas.paste(poster_template, (0, 0), poster_template)

    # Add the user's name on top of everything
    draw = ImageDraw.Draw(canvas)
    
    # Try to load the custom font, but fall back to a default if it fails
    try:
        font = ImageFont.truetype(FONT_PATH, name_font_size)
    except IOError:
        st.warning(f"Could not load custom font at '{FONT_PATH}'. Using a default font.")
        font = ImageFont.load_default(size=60)
    
    # Draw the text with a fixed position, centered horizontally
    draw.text(
        (540, 870),                      # (x, y) position is fixed
        user_name,                       # The text to write
        font=font,                       # The loaded font
        fill=(0, 0, 0, 255),             # Black color
        anchor="ms"                      # Anchor text at middle-top
    )

    return canvas

# --- STREAMLIT APP LAYOUT ---
st.set_page_config(page_title="Poster Generator", layout="centered")
st.title("✨ Custom Poster Generator ✨")
st.write("Upload your photo, add your name, and use the sidebar to adjust.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Edit Your Poster")

user_upload = st.sidebar.file_uploader("1. Upload Your Headshot", type=["jpg", "jpeg", "png"])
user_name = st.sidebar.text_input("2. Enter Your Name", "Your Name")

st.sidebar.header("Photo Controls")
photo_scale = st.sidebar.slider("Zoom Photo", 0.5, 4.0, 1.0, 0.1)
photo_pos_x = st.sidebar.slider("Move Photo Left/Right", -400, 400, 0, 10)
photo_pos_y = st.sidebar.slider("Move Photo Up/Down", -400, 400, 0, 10)

st.sidebar.header("Name Controls")
name_font_size = st.sidebar.slider("Font Size", 40, 200, 100, 5)

# --- MAIN PANEL ---
if user_upload and user_name:
    final_poster = create_poster(
        user_image_file=user_upload,
        user_name=user_name,
        photo_scale=photo_scale,
        photo_pos_x=photo_pos_x,
        photo_pos_y=photo_pos_y,
        name_font_size=name_font_size
    )
    
    st.image(final_poster, caption="Preview of your custom poster", use_column_width=True)
    
    # Prepare image for download
    buf = io.BytesIO()
    final_poster.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    # Add download button
    st.download_button(
        label="📥 Download Custom Poster",
        data=byte_im,
        file_name=f"{user_name.replace(' ', '_')}_poster.png",
        mime="image/png"
    )
else:
    st.info("⬅️ Upload your photo and enter your name in the sidebar to begin!")
    st.image(POSTER_PATH, caption="This is the poster template.")