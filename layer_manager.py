from PIL import Image
import numpy as np

class Layer:
    def __init__(self, name, width=1200, height=600):
        self.name = name
        self.image = Image.new("RGBA", (width, height), (0, 0, 0, 0))

class LayerManager:
    def __init__(self):
        self.layers = [Layer("Background")]   
    
    def add_layer(self, name):
        self.layers.append(Layer(name))

    def get_layer_names(self):
        return [layer.name for layer in self.layers]

    def update_layer(self, name, new_image_data):
        for layer in self.layers:
            if layer.name == name and new_image_data is not None:
                arr = (new_image_data * 255).astype("uint8")
                layer.image = Image.fromarray(arr).convert("RGBA")

    def render_all_layers(self):
        base = self.layers[0].image.copy()
        for layer in self.layers[1:]:
            base = Image.alpha_composite(base, layer.image)
        return base
