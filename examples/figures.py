import json
import yaml
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import re
import abstract_math_vis
import abstract_math_parser


def main():
    parse_file = "math_definitions.yaml"
    try:
        with open(parse_file, 'r') as f:
            code = f.read()

            parsed_result = abstract_math_parser.parse_abstract_math_declarations(code)
    
            if parsed_result is None:  # Check if parsing failed *immediately*
                print("YAML parsing failed. Check your YAML file.")
                return  # Exit if parsing failed
    
            # Now you can safely use parsed_result because it's *not* None
            visualization_plan = abstract_math_vis.execute_visualization_bt(parsed_result) # Execute behavior tree
            elements_to_visualize = visualization_plan.get("elements_to_visualize", [])
    
    
            for element_name in elements_to_visualize: # Visualize only elements chosen by BT
                element_data = None
                for element in parsed_result.get('elements', []):
                    if element.get('name') == element_name:
                        element_data = element
                        break
                if element_data:
                    abstract_math_vis.visualize_element(element_data, parsed_result)
            for element in parsed_result.get('elements', []):
                abstract_math_vis.visualize_element(element, parsed_result)
    except FileNotFoundError:
        print(f"File not found: {parse_file}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()