from enum import Enum

class LayerType(Enum):
    POINT = "point"
    CENTER_POINT = "center_point"
    SQUARE_POINT = "square_point"
    POINT_3D = "point_3d"
    LINE = "line"
    CIRCLE = "circle"
    POLYGON = "polygon"

class Layer:
    def __init__(self, name, layer_type, x=0, y=0, z=0, visible=True, canvas_object_id=None):
        self.name = name
        self.type = layer_type
        self.x = x
        self.y = y
        self.z = z
        self.visible = visible
        self.canvas_object_id = canvas_object_id

    def __repr__(self):
        return f"Layer(name='{self.name}', type={self.type}, visible={self.visible})"

    def draw(self, ax):  # <--- ДОБАВЛЕН ПУСТОЙ МЕТОД draw
        pass


def create_layer(name, layer_type, x=0, y=0, z=0):
    return Layer(name=name, layer_type=layer_type, x=x, y=y, z=z)