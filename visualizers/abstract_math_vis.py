# abstract_math_vis.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_agg import FigureCanvasAgg
import math
import networkx as nx

def visualize_shape(rule, ax, parsed_data):
    shape_type = rule['shape_type']
    shape_visualizer = rule.get('shape_visualizer', 'shapes_2d')

    if shape_visualizer == 'shapes_2d':
        if shape_type == "rectangle1":
            shape_data = parsed_data['enums']['Shapes']['Rectangle1']
            rectangle_visualizer(ax, shape_data)
        elif shape_type == "circle1":
            shape_data = parsed_data['enums']['Shapes']['Circle1']
            circle_visualizer(ax, shape_data)
        elif shape_type == "impossible_staircase1":
            impossible_staircase_visualizer(ax)
        elif shape_type == "penrose_triangle1":
            penrose_triangle_visualizer(ax)
        else:
            print(f"Unknown shape type: {shape_type} for 2D visualizer")
    elif shape_visualizer == 'shapes_3d':
        if shape_type == "Cube1":
            shape_data = parsed_data['enums']['Shapes_3D']['Cube1']
            cube_visualizer(ax, shape_data)
        else:
            print(f"Unknown shape type: {shape_type} for 3D visualizer")
    else:
        print(f"Unknown visualizer: {shape_visualizer}")

def rectangle_visualizer(ax, shape_data):
    """Visualizes a rectangle on the given axes."""
    _, center_x, center_y, width, height = shape_data
    rect = patches.Rectangle((center_x - width / 2, center_y - height / 2), width, height, linewidth=1, edgecolor='blue', facecolor='lightblue')
    ax.add_patch(rect)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Rectangle')

def circle_visualizer(ax, shape_data):
    """Visualizes a circle on the given axes."""
    _, center_x, center_y, radius = shape_data
    circle = patches.Circle((center_x, center_y), radius, linewidth=1, edgecolor='red', facecolor='lightcoral')
    ax.add_patch(circle)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Circle')

def cube_visualizer(ax, shape_data):
    """Visualizes a cube on 3D axes."""
    if ax.name != '3d':
        print("Warning: cube_visualizer requires 3D axes.")
        return

    _, center_x, center_y, center_z, side_length = shape_data
    half_side = side_length / 2
    vertices = [
        [center_x - half_side, center_y - half_side, center_z - half_side],
        [center_x + half_side, center_y - half_side, center_z - half_side],
        [center_x + half_side, center_y + half_side, center_z - half_side],
        [center_x - half_side, center_y + half_side, center_z - half_side],
        [center_x - half_side, center_y - half_side, center_z + half_side],
        [center_x + half_side, center_y - half_side, center_z + half_side],
        [center_x + half_side, center_y + half_side, center_z + half_side],
        [center_x - half_side, center_y + half_side, center_z + half_side]
    ]
    edges = [
        [vertices[0], vertices[1]], [vertices[1], vertices[2]], [vertices[2], vertices[3]], [vertices[3], vertices[0]], # Bottom face
        [vertices[4], vertices[5]], [vertices[5], vertices[6]], [vertices[6], vertices[7]], [vertices[7], vertices[4]], # Top face
        [vertices[0], vertices[4]], [vertices[1], vertices[5]], [vertices[2], vertices[6]], [vertices[3], vertices[7]]  # Vertical edges
    ]

    for edge in edges:
        x = [point[0] for point in edge]
        y = [point[1] for point in edge]
        z = [point[2] for point in edge]
        ax.plot(x, y, z, color='green')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Cube')

def impossible_staircase_visualizer(ax):
    """Visualizes an Impossible Staircase illusion (2D)."""
    points_staircase = [
        [0, 0], [1, 0], [1, 1], [0, 1],
        [1, 0], [1, -1], [2, -1], [2, 0],
        [2, 0], [2, 1], [3, 1], [3, 0],
        [0, 1], [0, 2], [3, 2], [3, 1]
    ]
    lines_indices = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [8, 9], [9, 10], [10, 11], [11, 8],
        [12, 13], [13, 14], [14, 15], [15, 12],

        [1, 4], [2, 7], [3, 12], [7, 8], [11, 14]
    ]

    for indices in lines_indices:
        p1 = points_staircase[indices[0]]
        p2 = points_staircase[indices[1]]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='gray')

    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Impossible Staircase')
    ax.axis('off') # Turn off axes for cleaner illusion


def penrose_triangle_visualizer(ax):
    """Visualizes a Penrose Triangle illusion (2D)."""
    points_segment1 = [[0, 0], [2, 0], [2, 0.2], [0, 0.2]]
    points_segment2 = [[2, 0], [2.2, 2], [2.4, 0], [4.4, 0]]
    points_segment3 = [[0, 0.2], [2.4, 0.2], [2.2, 2.2], [0, 2]]

    polygon1 = plt.Polygon(points_segment1, facecolor='lightcoral', edgecolor='black', linewidth=1, alpha=0.8)
    polygon2 = plt.Polygon(points_segment2, facecolor='lightcoral', edgecolor='black', linewidth=1, alpha=0.8)
    polygon3 = plt.Polygon(points_segment3, facecolor='lightcoral', edgecolor='black', linewidth=1, alpha=0.8)

    ax.add_patch(polygon1)
    ax.add_patch(polygon2)
    ax.add_patch(polygon3)

    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Penrose Triangle')
    ax.axis('off')  # Turn off axes for cleaner illusion

def visualize_mandelbrot(params):
    width = params.get('width', 500)
    height = params.get('height', 400)
    max_iter = params.get('max_iter', 100)

    x_min, x_max = params.get('x_min', -2.0), params.get('x_max', 1.0)
    y_min, y_max = params.get('y_min', -1.5), params.get('y_max', 1.5)

    pixels = [[mandelbrot_set(x_min + (x_max - x_min) * x / width,
                             y_min + (y_max - y_min) * y / height, max_iter)
               for x in range(width)]
              for y in range(height)]

    fig, ax = plt.subplots(figsize=(width/100, height/100), dpi=100) # Adjust figure size
    ax.imshow(pixels, cmap='magma', extent=[x_min, x_max, y_min, y_max])
    ax.set_title('Mandelbrot Set')
    ax.axis('off') # Turn off axes for Mandelbrot plot
    plt.tight_layout() # Adjust layout to prevent labels from being clipped
    plt.show()


def mandelbrot_set(c_real, c_imag, max_iter):
    z = complex(0, 0)
    c = complex(c_real, c_imag)
    for i in range(max_iter):
        if abs(z) > 2:
            return i
        z = z*z + c
    return max_iter

def visualize_logistic_equation(params):
    x0 = params.get('x0', 0.2)
    r = params.get('r', 3.9)
    iterations = params.get('iterations', 150)

    x_values = [x0]
    for _ in range(iterations):
        x_values.append(r * x_values[-1] * (1 - x_values[-1]))

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(range(iterations + 1), x_values, linestyle='-', marker='o', markersize=3)
    ax.set_xlabel('Iteration')
    ax.set_ylabel('x_n')
    ax.set_title('Logistic Equation: x_(n+1) = r * x_n * (1 - x_n)')
    ax.grid(True)
    plt.show()

def visualize_graph(enums, elements):
    graph_data = enums.get('GraphData', {}).get('GraphExample', {})
    if not graph_data:
        print("No GraphDataExample found in enums.")
        return

    nodes_positions = graph_data.get('nodes', [])
    clusters_indices = graph_data.get('clusters', [])

    G = nx.Graph()
    for i, pos in enumerate(nodes_positions):
        G.add_node(i, pos=pos)

    pos_dict = nx.get_node_attributes(G, 'pos')
    if not pos_dict:
        print("No node positions available for graph visualization.")
        return


    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(G, positions_graph_nodes(nodes_positions), with_labels=True, node_color='lightblue', node_size=500, ax=ax)


    # Highlight clusters (example - color nodes in clusters)
    colors = ['lightcoral', 'lightgreen', 'lightskyblue', 'lightgoldenrodyellow', 'lightpink']
    for i, cluster_nodes in enumerate(clusters_indices):
        cluster_color = colors[i % len(colors)] # Cycle through colors if more clusters than colors
        nx.draw_networkx_nodes(G, positions_graph_nodes(nodes_positions), nodelist=cluster_nodes, node_color=cluster_color, node_size=500, ax=ax)


    ax.set_title('Example Graph Visualization')
    plt.show()

def positions_graph_nodes(nodes_positions):
    pos_dict = {}
    for i, pos in enumerate(nodes_positions):
        pos_dict[i] = pos
    return pos_dict


def visualize_enums_as_points(enum_data):
    if not enum_data:
        print("No enum data provided for point visualization.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    point_count = 0
    labels = []
    x_coords = []
    y_coords = []

    for enum_name, enum_value in enum_data.items():
         if isinstance(enum_value, list) and len(enum_value) >= 3 and (enum_value[0] in ["point", "center_point", "circle"]): #Example criteria, adjust as needed
            shape_type = enum_value[0]
            x = enum_value[1]
            y = enum_value[2]

            point_count += 1
            labels.append(enum_name)
            x_coords.append(x)
            y_coords.append(y)
            ax.plot(x, y, marker='o', markersize=8, linestyle='none', label=enum_name) # Plot each enum as a point


    if point_count > 0:
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')
        ax.set_title('Enum Values as Points')
        ax.grid(True)
        ax.legend() # Show legend to identify points
        ax.set_aspect('equal', adjustable='box') # Equal aspect ratio for point plots
        plt.show()
    else:
        print("No suitable enum values found for point visualization (needs to be list of [type, x, y, ...])")


def visualize_enums(enums):
    for enum_name, enum_values in enums.items():
        if enum_name == 'Shapes':
             visualize_enums_as_points(enum_values) #Special case for Shapes enum, visualize as points for now - can be extended
             return # Avoid visualizing 'Shapes' again as default

        if isinstance(enum_values, list):
            print(f"List Enum: {enum_name} = {enum_values}")
        elif isinstance(enum_values, dict):
             print(f"Dict Enum: {enum_name} =")
             for key, value in enum_values.items():
                 print(f"  {key}: {value}")
        else:
            print(f"Enum: {enum_name} = {enum_values}")


def execute_visualization_bt(parsed_data):
    visualization_plan = {}

    axioms_config = parsed_data.get('axioms', {})
    axiom_results = {}
    for axiom_name, axiom_statement in axioms_config.items():
        axiom_results[axiom_name] = abstract_math_core.evaluate_axiom(axiom_statement, parsed_data)
        print(f"Axiom '{axiom_name}': '{axiom_statement}' is {axiom_results[axiom_name]}")


    consequences_config = parsed_data.get('consequences', {})
    executed_consequences = []

    for consequence_name, consequence_rule in consequences_config.items():
        condition_str = consequence_rule.get('condition')
        actions = consequence_rule.get('actions', [])

        if condition_str:
            condition_result = abstract_math_core.evaluate_condition(condition_str, axiom_results, executed_consequences) # Condition can depend on axioms or previously executed consequences
        else: # No condition, always execute
            condition_result = True

        if condition_result:
            print(f"Executing consequence: '{consequence_name}' because condition '{condition_str}' is met.")
            executed_consequences.append(consequence_name) # Track executed consequences

            for action in actions:
                action_type = list(action.keys())[0] # Action is dict with single key-value pair
                action_params = action[action_type]

                if action_type == 'visualize_element':
                    element_to_visualize = action_params
                    if consequence_name not in visualization_plan:
                        visualization_plan[consequence_name] = [] # Initialize list for this consequence if not exists
                    visualization_plan[consequence_name].append({'action': 'visualize_element', 'params': element_to_visualize})
                    #visualize_element(element_to_visualize, parsed_data) # Execute visualization directly if needed, or defer to plan
                elif action_type == 'log_message':
                     message = action_params
                     print(f"Log from consequence '{consequence_name}': {message}")
                else:
                    print(f"Unknown action type in consequence '{consequence_name}': {action_type}")
        else:
            print(f"Condition not met for consequence: '{consequence_name}' condition: '{condition_str}'. Not executing actions.")

    return visualization_plan


def visualize_element(element_rule, parsed_data):
    element_name = element_rule['name']
    visualizer_type = element_rule['visualizer']

    fig, ax = None, None # Initialize figure and axes to None

    if visualizer_type == 'shapes_2d':
        fig, ax = plt.subplots(figsize=(6, 6)) # Create figure and axes
        visualize_shape({'shape_type': element_name, 'shape_visualizer': visualizer_type}, ax, parsed_data)
    elif visualizer_type == 'shapes_3d':
        fig = plt.figure(figsize=(6, 6))
        ax = fig.add_subplot(111, projection='3d') # Create 3D axes
        visualize_shape({'shape_type': element_name, 'shape_visualizer': visualizer_type}, ax, parsed_data)
    elif visualizer_type == 'mandelbrot_set':
        visualize_mandelbrot(parsed_data.get('mandelbrot_params', {}))
    elif visualizer_type == 'logistic_equation':
        visualize_logistic_equation(parsed_data.get('logistic_equation_params', {}))
    elif visualizer_type == 'graph':
        visualize_graph(parsed_data.get('enums', {}), parsed_data.get('elements', {}))
    elif visualizer_type == 'enums':
        visualize_enums(parsed_data.get('enums', {}))
    elif visualizer_type == 'enums_as_points':
         visualize_enums_as_points(parsed_data.get('enums', {}).get('Shapes', {})) # Example to visualize 'Shapes' enum as points

    else:
        print(f"Unknown visualizer type: {visualizer_type} for element: {element_name}")
        return None # Indicate visualization failed

    if fig and ax: # Only show plot if figure and axes were created (i.e., not for Mandelbrot which manages its own plotting)
        ax.set_aspect('equal', adjustable='box') # Keep aspect ratio equal for 2D plots
        plt.tight_layout()
        plt.show()
        return fig, ax # Return figure and axes if created

    return None, None # Return None if no figure/axes created or visualization failed