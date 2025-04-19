import streamlit as st
from canvas_engine import init_canvas, get_canvas_result
from layer_manager import LayerManager
from exporter import export_drawing

st.set_page_config(page_title="Procreate Clone", layout="wide")
st.title("🖌️ Python Procreate Clone")

# Initialize layer manager
layer_mgr = LayerManager()

# Sidebar tools
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
