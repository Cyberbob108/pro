import streamlit as st
from canvas_engine import init_canvas
from layer_manager import LayerManager
from exporter import export_drawing
from undo_stack import UndoStack
from PIL import Image
import numpy as np

# ---- Initialize ----
st.set_page_config(page_title="Procreate Clone", layout="wide")
st.title("🖌️ Python Procreate Clone")

# ---- Session State for Undo Stack ----
if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = UndoStack()

# ---- Layer Manager ----
layer_mgr = LayerManager()

# ---- Sidebar ----
st.sidebar.header("🎨 Tool Settings")
brush_color = st.sidebar.color_picker("Brush Color", "#000000")
brush_size = st.sidebar.slider("Brush Size", 1, 50, 5)
selected_layer = st.sidebar.selectbox("Active Layer", layer_mgr.get_layer_names())

if st.sidebar.button("➕ Add Layer"):
    layer_mgr.add_layer(f"Layer {len(layer_mgr.layers) + 1}")

# ---- Canvas ----
canvas_result = init_canvas(brush_color, brush_size)

# ---- Save Drawing to Layer + Push to Undo Stack ----
if canvas_result and canvas_result.image_data is not None:
    final_arr = (canvas_result.image_data * 255).astype("uint8")
    img = Image.fromarray(final_arr).convert("RGBA")

    layer_mgr.update_layer(selected_layer, canvas_result.image_data)
    st.session_state.undo_stack.push(img)

# ---- Undo / Redo Buttons ----
col1, col2 = st.columns(2)
with col1:
    if st.button("⏪ Undo"):
        result = st.session_state.undo_stack.undo()
        if result:
            st.image(result, caption="Undo Result", use_column_width=True)

with col2:
    if st.button("⏩ Redo"):
        result = st.session_state.undo_stack.redo()
        if result:
            st.image(result, caption="Redo Result", use_column_width=True)

# ---- Final Combined Output ----
final_image = layer_mgr.render_all_layers()
st.image(final_image, caption="Your Drawing", use_column_width=True)

# ---- Export ----
if st.button("📥 Download as PNG"):
    st.markdown(export_drawing(final_image), unsafe_allow_html=True)
