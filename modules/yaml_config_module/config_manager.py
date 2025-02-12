import yaml
from tkinter import filedialog
import os

loaded_yaml_configs = []  # Global to store raw loaded YAML configs


def load_yaml_config():
    global loaded_yaml_configs  # Declare as global to modify it
    file_paths = filedialog.askopenfilenames(filetypes=[("YAML files", "*.yaml *.yml")])  # askopenfilenames (plural)
    if file_paths:  # file_paths is now a tuple of paths
        yaml_configs = []  # List to store configurations from each file
        for file_path in file_paths:  # Iterate through selected file paths
            try:
                with open(file_path, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    if yaml_config:
                        yaml_configs.append(yaml_config)  # Add loaded config to the list
                        print(f"YAML configuration loaded from: {file_path}")
                    else:
                        print(f"YAML file is empty or invalid: {file_path}")
            except Exception as e:
                print(f"Error loading YAML file: {file_path} - {e}")

        if yaml_configs:  # If we successfully loaded at least one config
            loaded_yaml_configs = yaml_configs  # Update the global variable
            process_yaml_config(yaml_configs)  # Pass the list of configs to process_yaml_config
        else:
            print("No valid YAML configurations loaded.")
    return loaded_yaml_configs  # Return loaded_yaml_configs for potential use


def process_yaml_config(yaml_configs):  # Accepts a list of yaml_configs
    global playground_shapes, gui_elements_config, playground_visualizers
    print("DEBUG: Entering process_yaml_config from module with a list of configs")

    # Initialize empty dictionaries/lists to accumulate data from all configs
    playground_shapes = {}
    playground_visualizers = {}
    gui_elements_config = {'palettes': []}  # Initialize with palettes as a list to append to

    for yaml_config in yaml_configs:  # Iterate through the list of configurations
        print(f"DEBUG: Processing YAML config: {yaml_config}")  # Debug print for each config

        if 'enums' in yaml_config:
            if 'Shapes' in yaml_config['enums']:
                shapes_config = yaml_config['enums']['Shapes']
                print(f"DEBUG: Processing Shapes section: {shapes_config}")
                for shape_name, shape_def in shapes_config.items():
                    shape_data = {
                        'type': shape_def.get('type'),
                        'parameters': shape_def.get('parameters', {}),
                        'runtime_editable': shape_def.get('runtime_editable', [])
                    }
                    playground_shapes[shape_name] = shape_data  # Add to playground_shapes dictionary

            if 'Visualizers' in yaml_config['enums']:  # Parse visualizers if defined (even though enums is not the ideal place)
                visualizers_config = yaml_config['enums']['Visualizers']  # Corrected section name to 'Visualizers'
                print(f"DEBUG: Processing Visualizers section: {visualizers_config}")
                for vis_name, vis_def in visualizers_config.items():
                    vis_type = vis_def.get('type')
                    vis_params = vis_def.get('parameters', {})
                    if vis_type:  # Only create visualizer if type is defined
                        visualizer = create_visualizer(vis_type, vis_name, vis_params)  # Use create_visualizer - assuming it's defined elsewhere or will be
                        if visualizer:
                            playground_visualizers[vis_name] = visualizer
                            print(f"DEBUG: Loaded visualizer '{vis_name}' of type '{vis_type}'")
                        else:
                            print(f"DEBUG: Could not create visualizer '{vis_name}' of type '{vis_type}'")

        if 'gui_elements' in yaml_config:
            gui_config = yaml_config['gui_elements']
            print(f"DEBUG: Processing GUI Elements section: {gui_config}")
            if 'palettes' in gui_config:
                gui_elements_config['palettes'].extend(gui_config['palettes'])  # Extend the palettes list, not replace

    print(f"DEBUG: Final Playground shapes Parsed: {playground_shapes}")
    print(f"DEBUG: Final Playground visualizers Parsed: {playground_visualizers}")
    print(f"DEBUG: Final GUI Elements Parsed: {gui_elements_config}")

    print("DEBUG: Exiting process_yaml_config from module")


def create_visualizer(vis_type, vis_name, vis_params):  # Basic visualizer factory - to be expanded
    if vis_type == 'cartesian':
        from visualizers import CartesianVisualizer  # Import here to avoid circular imports
        return CartesianVisualizer(name=vis_name, parameters=vis_params)
    elif vis_type == 'yaml_viewer':  # Example type for YAMLVisualizer - adjust if needed
        from modules.yaml_config_module.yaml_visualizer import YAMLVisualizer  # Import YAMLVisualizer from module
        return YAMLVisualizer(name=vis_name, parameters=vis_params)  # You might need to adjust parameters for YAMLVisualizer
    else:
        print(f"DEBUG: Unknown visualizer type: {vis_type}")
        return None


def load_default_yaml_config_from_directory(yaml_dir='.'):  # Function to load default YAML configs
    default_yaml_files = [f for f in os.listdir(yaml_dir) if f.endswith(('.yaml', '.yml'))]  # Find all YAML files
    if default_yaml_files:
        default_yaml_paths = [os.path.join(yaml_dir, f) for f in default_yaml_files]  # Create full paths
        print(f"DEBUG: Default YAML files found: {default_yaml_paths}")
        yaml_configs = []
        for file_path in default_yaml_paths:
            try:
                with open(file_path, 'r') as f:
                    yaml_config = yaml.safe_load(f)
                    if yaml_config:
                        yaml_configs.append(yaml_config)
                        print(f"DEBUG: Default YAML configuration loaded from: {file_path}")
                    else:
                        print(f"DEBUG: Default YAML file is empty or invalid: {file_path}")
            except FileNotFoundError:  # This should not happen now, but keep for robustness
                print(f"DEBUG: Default YAML file not found (unexpected): {file_path}")
            except Exception as e:
                print(f"DEBUG: Error loading default YAML file: {file_path} - {e}")
        return yaml_configs  # Return the list of loaded configs
    else:
        print("DEBUG: No default YAML configuration files found in directory.")
        return []  # Return empty list if no files found