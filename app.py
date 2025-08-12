# app.py

import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Imprint Generator",
    page_icon="🖼️",
    layout="centered",
    initial_sidebar_state="auto"
)

# --- ADVANCED UI/UX STYLING ---
def apply_custom_styling():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lexend+Deca&display=swap');
        
        html, body, [class*="st-"], .st-emotion-cache-16txtl3 {
            font-family: 'Lexend Deca', sans-serif;
        }

        /* Style for all input widgets for high contrast */
        .st-emotion-cache-1j6s6b6, .st-emotion-cache-1x0xh3b {
            background-color: #ECF2FF;
            border-radius: 8px;
        }
        .st-emotion-cache-1j6s6b6 input, .st-emotion-cache-1x0xh3b input {
            color: #040D12 !important;
            -webkit-text-fill-color: #040D12 !important;
        }

        /* Style for the download button */
        .stDownloadButton > button {
            background-color: #00A9FF;
            color: #FFFFFF;
            font-weight: bold;
            border: 2px solid #00A9FF;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            width: 100%;
            transition: all 0.3s ease-in-out;
            box-shadow: 0 4px 15px rgba(0, 169, 255, 0.3);
        }
        .stDownloadButton > button:hover {
            background-color: #FFFFFF;
            color: #00A9FF;
            box-shadow: 0 6px 20px rgba(0, 169, 255, 0.5);
            transform: translateY(-2px);
        }
        </style>
    """, unsafe_allow_html=True)

# Apply the custom styling at the start of the app
apply_custom_styling()

# --- FILE AND CONFIGURATION CONSTANTS ---
POSTER_PATH = "Attending 2025.png"
FONT_PATH = "PhotographSignature.ttf"

# --- CORE IMAGE PROCESSING FUNCTION ---
def create_poster(user_image_file, user_name, photo_scale, photo_pos_x, photo_pos_y, name_font_size):
    poster_template = Image.open(POSTER_PATH).convert("RGBA")
    user_photo = Image.open(user_image_file).convert("RGBA")
    canvas = Image.new("RGBA", poster_template.size)
    
    base_photo_width = 530
    aspect_ratio = user_photo.height / user_photo.width
    new_width = int(base_photo_width * photo_scale)
    new_height = int(new_width * aspect_ratio)
    user_photo = user_photo.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    photo_paste_x = (canvas.width // 2) - (new_width // 2) + photo_pos_x
    photo_paste_y = 455 - (new_height // 2) + photo_pos_y
    
    canvas.paste(user_photo, (photo_paste_x, photo_paste_y))
    canvas.paste(poster_template, (0, 0), poster_template)

    draw = ImageDraw.Draw(canvas)
    try:
        font = ImageFont.truetype(FONT_PATH, name_font_size)
    except IOError:
        st.warning("Custom font not found. Using default.")
        font = ImageFont.load_default(size=60)
    
    # Draw text with fixed position and black color
    draw.text((540, 870), user_name, font=font, fill="#000000", anchor="ms")

    return canvas

# --- STREAMLIT APP LAYOUT ---
st.title("Imprint Generator")
st.write("Create your personalized event poster in seconds.")

# --- SIDEBAR CONTROLS ---
with st.sidebar:
    st.header("1. Your Details")
    user_upload = st.file_uploader("Upload Your Headshot")
    user_name = st.text_input("Enter Your Name", "Your Name")

    st.header("2. Photo Controls")
    photo_scale = st.number_input("Zoom Photo", min_value=0.5, max_value=4.0, value=1.0, step=0.1)
    photo_pos_x = st.number_input("Move Photo Left/Right", min_value=-400, max_value=400, value=150, step=10) # <-- Default value changed
    photo_pos_y = st.number_input("Move Photo Up/Down", min_value=-400, max_value=400, value=0, step=10)

    st.header("3. Name Controls")
    name_font_size = st.number_input("Font Size", min_value=40, max_value=200, value=100, step=5)

# --- MAIN PANEL LOGIC ---
if user_upload and user_name:
    final_poster = create_poster(
        user_image_file=user_upload,
        user_name=user_name,
        photo_scale=photo_scale,
        photo_pos_x=photo_pos_x,
        photo_pos_y=photo_pos_y,
        name_font_size=name_font_size
    )
    
    st.image(final_poster, caption="Looking great! You can now download your poster.", use_container_width=True)
    
    buf = io.BytesIO()
    final_poster.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="📥 Download Poster",
        data=byte_im,
        file_name=f"Imprint_{user_name.replace(' ', '_')}.png",
        mime="image/png"
    )
else:
    st.info("⬅️ Start by uploading your photo and name in the sidebar.")
    st.image(POSTER_PATH, caption="Poster Template", use_container_width=True)
