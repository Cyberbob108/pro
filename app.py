import streamlit as st
from canvas_engine import init_canvas, get_canvas_result
from layer_manager import LayerManager
from exporter import export_drawing

from undo_stack import UndoStack

if "undo_stack" not in st.session_state:
    st.session_state.undo_stack = UndoStack()


st.set_page_config(page_title="Procreate Clone", layout="wide")
st.title("🖌️ Python Procreate Clone")

# Initialize layer manager
layer_mgr = LayerManager()

# Sidebar tools

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

# Save canvas state to undo stack
if canvas_result.image_data is not None:
    final_arr = (canvas_result.image_data * 255).astype("uint8")
    img = Image.fromarray(final_arr).convert("RGBA")
    st.session_state.undo_stack.push(img)

st.sidebar.header("Tools")
brush_color = st.sidebar.color_picker("Brush Color", "#000000")
brush_size = st.sidebar.slider("Brush Size", 1, 50, 5)
selected_layer = st.sidebar.selectbox("Active Layer", layer_mgr.get_layer_names())
add_layer = st.sidebar.button("➕ Add Layer")

if add_layer:
    layer_mgr.add_layer(f"Layer {len(layer_mgr.layers)+1}")

# Load canvas
canvas_result = init_canvas(brush_color, brush_size)

# Update layer with drawing
layer_mgr.update_layer(selected_layer, canvas_result)

# Show combined result
final_image = layer_mgr.render_all_layers()
st.image(final_image, caption="Your Drawing", use_column_width=True)

# Export
if st.button("📥 Download as PNG"):
    st.markdown(export_drawing(final_image), unsafe_allow_html=True)
