import yaml
def parse_abstract_math_declarations(code):
    # Временно просто возвращаем None, чтобы не было ошибок.
    # В будущем здесь будет РЕАЛЬНЫЙ код парсера YAML.
    return None
def parse_geometry_rules_file(rules_file):
    """
    Parses geometry rules from a YAML file.
    Returns a list of rule dictionaries.
    """
    try:
        with open(rules_file, 'r') as file:
            rules = yaml.safe_load(file)
            return rules.get('geometry_rules', [])
    except FileNotFoundError:
        print(f"Error: Geometry rules file '{rules_file}' not found.")
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML in '{rules_file}': {e}")
        return []

def parse_abstract_math_declarations(code):
    data = {'elements': [], 'enums': {}, 'axioms': [], 'consequences': [], 'mandelbrot_params':{}, 'logistic_equation_params':{}, 'gui_elements': {}} # Initialize 'gui_elements'

    try:
        print("YAML code:", code)
        blocks = yaml.safe_load(code)

        if blocks is None:
            print("YAML file is empty or contains invalid YAML.")
            return None

        # --- Parse gui_elements block ---
        if "gui_elements" in blocks:
            data['gui_elements'] = blocks["gui_elements"]
            print("GUI Elements Parsed:", data['gui_elements']) # DEBUG: Print parsed gui_elements

        if "abstract_math" in blocks and "define_elements" in blocks["abstract_math"]:
            elements = blocks["abstract_math"]["define_elements"]
            data['elements'] = []
            for element_def in elements: # Changed 'element' to 'element_def' to avoid shadowing
                element_data = {} # Create a dictionary to hold element data
                if isinstance(element_def, dict) and "element" in element_def and isinstance(element_def['element'], dict) and "name" in element_def['element']:
                    element_config = element_def['element']
                    element_name = element_config['name']
                    element_data['name'] = element_name
                    element_data['visualizer'] = element_config.get('visualizer')

                    properties_config = element_config.get('properties', []) # Get properties, default to empty list
                    element_data['properties'] = [] # Initialize properties list for the element
                    for prop_def in properties_config: # Iterate through properties
                        if isinstance(prop_def, dict) and "property" in prop_def:
                            property_name = prop_def['property']
                            property_value = prop_def.get('value') # Get 'value' or None if not present
                            property_formula = prop_def.get('formula') # Get 'formula' or None if not present
                            element_data['properties'].append({
                                'name': property_name,
                                'value': property_value,
                                'formula': property_formula
                            })
                    data['elements'].append(element_data) # Append the element data dictionary

        if "enums" in blocks:
            enums_block = blocks["enums"]
            data['enums'] = {}
            for enum_category_name, enum_category_data in enums_block.items():
                data['enums'][enum_category_name] = {} # Initialize category dictionary
                if isinstance(enum_category_data, dict): # Handle nested enums (like GraphData)
                    for enum_name, enum_data in enum_category_data.items():
                        if enum_category_name == "GraphData" and enum_name == "GraphExample" and isinstance(enum_data, dict): # Special handling for GraphExample clusters
                            graph_enum_data = {} # Dictionary for graph-specific data
                            graph_enum_data['nodes'] = enum_data.get('nodes', []) # Parse nodes as before
                            graph_enum_data['clusters'] = enum_data.get('clusters', []) # PARSE CLUSTERS HERE
                            data['enums']['GraphData'][enum_name] = graph_enum_data # Store graph data with clusters
                        else: # Regular enums (Shapes, Colors, etc.)
                            data['enums'][enum_category_name][enum_name] = enum_data # Store as before
                elif isinstance(enum_category_data, list): # Handle simple list enums (like Colors)
                    data['enums'][enum_category_name] = enum_category_data
                else: # Handle flat enums directly under categories
                    data['enums'][enum_category_name] = enum_category_data # For flat enums (like Colors if flat)


                if enum_category_name == "Shapes": # Parse cluster for Shapes (points)
                    for shape_enum_name, shape_enum_data in enum_category_data.items():
                        if isinstance(shape_enum_data, list) and shape_enum_data[0] == "point" and len(shape_enum_data) >= 5: # Check for point and cluster data
                            data['enums']['Shapes'][shape_enum_name] = shape_enum_data # Keep existing point data
                            cluster_name = shape_enum_data[4] # Extract cluster name from 5th position
                            data['enums']['Shapes'][shape_enum_name].append(cluster_name) # Append cluster name to shape_data list

        if "mandelbrot_params" in blocks:
            data['mandelbrot_params'] = blocks["mandelbrot_params"]

        if "logistic_equation_params" in blocks:
            data['logistic_equation_params'] = blocks["logistic_equation_params"]

        if "axioms" in blocks:
            data['axioms'] = [{'name': k, 'statement': v} for k, v in blocks["axioms"].items()]

        if "consequences" in blocks:
            data['consequences'] = [{'name': k, 'statement': v} for k, v in blocks["consequences"].items()]

        return data

    except yaml.YAMLError as e:
        print(f"YAML Error: {e}")
        return None
    except Exception as e:
        print(f'Parsing Error: {e}')
        return None