import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
import yaml

# Relative import to get Visualizer base class from sibling visualizers directory
from ...visualizers.visualizers import Visualizer
    

class YAMLVisualizer(Visualizer):
    # ... (rest of YAMLVisualizer class code - no changes needed in class logic) ...
    pass