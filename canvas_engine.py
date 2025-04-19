from streamlit_drawable_canvas import st_canvas

def init_canvas(stroke_color, stroke_width):
    return st_canvas(
        fill_color="rgba(255, 255, 255, 0)",  # Transparent fill
        stroke_color=stroke_color,
        stroke_width=stroke_width,
        background_color="#ffffff",
        width=1200,
        height=600,
        drawing_mode="freedraw",
        key="canvas"
    )

def get_canvas_result(canvas_result):
    return canvas_result.image_data if canvas_result else None
