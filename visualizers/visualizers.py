import matplotlib
matplotlib.use("TkAgg")  # Ensure TkAgg backend for Matplotlib with Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import abstract_math_framework


class Visualizer():
    def __init__(self, name=None):
        pass

class CartesianVisualizer(Visualizer):
    def __init__(self, parameters=None):
        self.visualizers = {} # Dictionary to store loaded visualizers, key=name, value=Visualizer object
        self.active_visualizer_name = None # Name of the currently active visualizer
        self.active_visualizer = None # Instance of the currently active visualizer
        self.parameters = None
    # ... (rest of CartesianVisualizer class code - no changes needed in class logic) ...
    pass

class VisualizerManager: # Class to manage visualizers
    def __init__(self):
        self.visualizers = {} # Dictionary to store loaded visualizers, key=name, value=Visualizer object
        self.active_visualizer_name = None # Name of the currently active visualizer
        self.active_visualizer = None # Instance of the currently active visualizer

    def load_visualizers_from_config(self, visualizer_configs): # Load visualizers from YAML config
        for vis_name, vis_config in visualizer_configs.items():
            vis_type = vis_config.get('type')
            vis_params = vis_config.get('parameters', {})
            if vis_type:
                visualizer = create_visualizer(vis_type, vis_name, vis_params) # Use factory function
                if visualizer:
                    self.visualizers[vis_name] = visualizer
                    print(f"DEBUG: VisualizerManager loaded visualizer: '{vis_name}' of type '{vis_type}'")
                else:
                    print(f"DEBUG: VisualizerManager could not create visualizer: '{vis_name}' of type '{vis_type}'")

    def set_active_visualizer(self, visualizer_instance):
        if isinstance(visualizer_instance, Visualizer):
            self.active_visualizer = visualizer_instance
            self.active_visualizer_name = visualizer_instance.name
            print(f"DEBUG: VisualizerManager set active visualizer to: '{self.active_visualizer_name}'")
        else:
            print("DEBUG: VisualizerManager - set_active_visualizer - instance is not a Visualizer subclass.")
            return False
        return True

    def get_active_visualizer(self):
        return self.active_visualizer