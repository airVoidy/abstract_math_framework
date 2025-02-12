import matplotlib
matplotlib.use("TkAgg")  # Ensure TkAgg backend for Matplotlib with Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# Relative import to get LayerType from core module
from abstract_math_framework.core.abstract_math_layer import LayerType

class Visualizer:
    # ... (rest of Visualizer base class code - no changes needed in class logic) ...
    pass

class CartesianVisualizer(Visualizer):
    # ... (rest of CartesianVisualizer class code - no changes needed in class logic) ...
    pass