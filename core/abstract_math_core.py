import math
import numpy as np
import re
print("DEBUG: Я - ФАЙЛ abstract_math_core.py, и я ТОЧНО нахожусь здесь!")
from enum import Enum

def create_layer(name, layer_type, x=0, y=0, z=0):
    return Layer(name=name, layer_type=layer_type, x=x, y=y, z=z)


def create_layer(name, layer_type, x=0, y=0, z=0):
    return Layer(name=name, layer_type=layer_type, x=x, y=y, z=z)

def calculate_rectangle_area(width, height):
    return width * height

def calculate_circle_area(radius):
    return math.pi * radius**2

def calculate_cube_volume(side_length):
    return side_length**3
def evaluate_axiom(axiom_statement, parsed_data):
    """
    Evaluates a semantic axiom statement by parsing it and comparing element properties.
    Supports axioms of the form: "property1 of element1 is comparison_operator property2 of element2;"
    or "property of element is comparison_operator value;"
    Comparison operators: 'greater than', 'less than', 'equal to', 'not equal to'
    """
    print(f"\n--- Evaluating Axiom: {axiom_statement} ---") # Debug print axiom being evaluated

    # --- Parsing the axiom statement using regular expressions ---
    match = re.match(r"([\w_]+) of (\w+) is (greater than|less than|equal to|not equal to) ([\w\.]+)(?: of (\w+))?;", axiom_statement) # более общий регекс

    if not match:
        print(f"  Error: Could not parse axiom statement: '{axiom_statement}'")
        return False # Return False if axiom parsing fails

    prop1_name = match.group(1) # property1 name (e.g., "area")
    element1_name = match.group(2) # element1 name (e.g., "rectangle1")
    comparison_operator_str = match.group(3) # comparison operator string (e.g., "greater than")
    value_or_prop2_name = match.group(4) # value OR property2 name
    element2_name = match.group(5) # element2 name (optional, if comparing property to property)


    print(f"  Parsed axiom: prop1='{prop1_name}', elem1='{element1_name}', op='{comparison_operator_str}', val_or_prop2='{value_or_prop2_name}', elem2='{element2_name}'") # Debug parsed parts


    # --- Get element data and properties ---
    element1_data = None
    for elem_def in parsed_data.get('elements', []):
        if elem_def['name'] == element1_name:
            element1_data = elem_def
            break
    if not element1_data:
        print(f"  Error: Element '{element1_name}' not found in definitions.")
        return False

    element2_data = None # Initialize element2_data to None
    if element2_name: # If comparing property to another property of another element
        for elem_def in parsed_data.get('elements', []):
            if elem_def['name'] == element2_name:
                element2_data = elem_def
                break
        if not element2_data:
            print(f"  Error: Element '{element2_name}' not found in definitions.")
            return False

    prop1_def = None
    for prop_d in element1_data.get('properties', []):
        if prop_d['name'] == prop1_name:
            prop1_def = prop_d
            break
    if not prop1_def:
        print(f"  Error: Property '{prop1_name}' not defined for element '{element1_name}'.")
        return False

    prop1_value = calculate_property_value(prop1_def, parsed_data['enums']['Shapes'].get(element1_name)) # Calculate property value


    prop2_value = None # Initialize prop2_value
    if element2_name: # If comparing property to property
        prop2_def = None
        for prop_d in element2_data.get('properties', []):
            if prop_d['name'] == value_or_prop2_name: # Use value_or_prop2_name as property2 name
                prop2_def = prop_d
                break
        if not prop2_def:
            print(f"  Error: Property '{value_or_prop2_name}' not defined for element '{element2_name}'.")
            return False
        prop2_value = calculate_property_value(prop2_def, parsed_data['enums']['Shapes'].get(element2_name)) # Calculate property2 value
    else: # Comparing property to a numerical value
        try:
            prop2_value = float(value_or_prop2_name) # Try converting to float
        except ValueError:
            print(f"  Error: Invalid numerical value in axiom: '{value_or_prop2_name}'")
            return False


    if prop1_value is None or prop2_value is None:
        print(f"  Error: Could not calculate property values for axiom: '{axiom_statement}'")
        return False


    # --- Perform Comparison ---
    comparison_operator = None
    if comparison_operator_str == "greater than":
        comparison_operator = lambda v1, v2: v1 > v2
    elif comparison_operator_str == "less than":
        comparison_operator = lambda v1, v2: v1 < v2
    elif comparison_operator_str == "equal to":
        comparison_operator = lambda v1, v2: v1 == v2
    elif comparison_operator_str == "not equal to":
        comparison_operator = lambda v1, v2: v1 != v2
    else:
        print(f"  Error: Unknown comparison operator: '{comparison_operator_str}'")
        return False

    axiom_result = comparison_operator(prop1_value, prop2_value)
    print(f"  Axiom result: {prop1_value} {comparison_operator_str} {prop2_value} is {axiom_result}") # Debug print result
    return axiom_result
def calculate_property_value(property_def, shape_data):
    """
    Calculates the value of a property based on its definition and shape data.
    """
    print(f"\n--- calculate_property_value called ---") # Debug print at the beginning
    print(f"   property_def: {property_def}") # Debug print property definition
    print(f"   shape_data: {shape_data}")     # Debug print shape data

    value = property_def.get('value')
    formula = property_def.get('formula')
    property_name = property_def.get('name')

    if value is not None: # If a direct value is given, use it
        print(f"   Using direct value: {value}") # Debug print
        return value
    elif formula: # If there's a formula, evaluate it
        try:
            local_vars = {'math': math} # доступ к math.pi
            if shape_data[0] == 'rectangle':
                local_vars['width'] = shape_data[3]
                local_vars['height'] = shape_data[4]
                local_vars['side_length'] = shape_data[3] # Assume width is side_length for square
                local_vars['radius'] = 0
            elif shape_data[0] == 'circle':
                local_vars['radius'] = shape_data[3]
                local_vars['side_length'] = 0
                local_vars['width'] = 0
                local_vars['height'] = 0

            calculated_value = eval(formula, {}, local_vars) # {} for globals, local_vars for locals
            print(f"   Formula evaluated: {formula} = {calculated_value}") # Debug print formula and result
            return calculated_value
        except Exception as e:
            print(f"   Error evaluating formula for property '{property_name}': {e}")
            return None # Return None if formula evaluation fails
    else:
        print(f"   No value or formula defined for property '{property_name}'") # Debug print
        return None # No value or formula defined

class Figure:
    def __init__(self, name, figure_type):
        self.name = name
        self.type = figure_type #  тип фигуры (пока string, можно сделать Enum в будущем)
        self.center = None # layers(type=center_point) - будет объектом Layer типа center_point
        self.radius = None # math.numeral - float или int
        self.side_length = None # math.numeral - float или int
        self.circle_points = [] # continuum{...} - пока List[Layer] для простоты, в будущем нужно continuum
        self.square_points = [] # list<layers>(type=square_point) - List[Layer]
        self.logistic_map_points = [] # list<layers>(type=logistic_map_point) - List[Layer]
        self.board_cells = [] # list<layers>(type=game_cell) - List[Layer]
        self.current_player = None # enums.Player - Enum Player
        self.game_state = None # enums.GameState - Enum GameState

    def __repr__(self): # Для удобного вывода объектов Figure
        return f"Figure(name='{self.name}', type='{self.type}', center={self.center.name if self.center else None}, radius={self.radius}, side_length={self.side_length}, ...)" # ... (можно добавить больше свойств для вывода)


class Player(Enum):
    X = "X"
    O = "O"
    NONE = "None" # Переименовано из None, так как None - ключевое слово Python

class CellState(Enum):
    EMPTY = "Empty"
    X_MARK = "X_Mark"
    O_MARK = "O_Mark"

class GameState(Enum):
    IN_PROGRESS = "InProgress" # Переименовано для PEP8
    X_WINS = "X_Wins" # Переименовано для PEP8
    O_WINS = "O_Wins" # Переименовано для PEP8
    DRAW = "Draw"


def create_layer(name, layer_type, x=None, y=None, z=None, state=None, row=None, col=None, is_in_set=None, iteration_value=None):
    """
    Функция для создания экземпляра класса Layer.
    """
    return Layer(name=name, layer_type=layer_type, x=x, y=y, z=z, state=state, row=row, col=col, is_in_set=is_in_set, iteration_value=iteration_value)

def distance(layer1, layer2):
    """
    Функция для вычисления евклидова расстояния между двумя слоями (точками) в 3D пространстве.
    Предполагает, что layer1 и layer2 имеют атрибуты x, y, z.
    """
    if layer1.x is None or layer1.y is None or layer1.z is None or layer2.x is None or layer2.y is None or layer2.z is None:
        raise ValueError("Для вычисления расстояния координаты x, y, z должны быть определены для обоих слоев.")
    dx = layer1.x - layer2.x
    dy = layer1.y - layer2.y
    dz = layer1.z - layer2.z
    return math.sqrt(dx**2 + dy**2 + dz**2)

def radians(degrees):
    """
    Функция для перевода градусов в радианы.
    Использует math.radians из стандартной библиотеки math.
    """
    return math.radians(degrees)

def cos(angle_radians):
    """
    Функция для вычисления косинуса угла в радианах.
    Использует math.cos из стандартной библиотеки math.
    """
    return math.cos(angle_radians)

def sin(angle_radians):
    """
    Функция для вычисления синуса угла в радианах.
    Использует math.sin из стандартной библиотеки math.
    """
    return math.sin(angle_radians)

def assert_rule(condition, message):
    """
    Функция для обработки assert выражений в правилах.
    Если условие condition ложно, выбрасывает исключение AssertionError с заданным сообщением message.
    """
    if not condition:
        raise AssertionError(message)
# Mandelbrot functions
def mandelbrot(c, max_iter):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    if n == max_iter:
        return max_iter
    return n

def generate_mandelbrot(width, height, x_min, x_max, y_min, y_max, max_iter):
    image = np.zeros((height, width))
    for j in range(height):
        for i in range(width):
            real = x_min + (x_max - x_min) * i / width
            imag = y_min + (y_max - y_min) * j / height
            c = complex(real, imag)
            image[j, i] = mandelbrot(c, max_iter)
    return image

# Для работы с комплексными числами (если потребуется, например, для множества Мандельброта)
def complex_num(real, imag):
    """
    Функция для создания комплексного числа.
    Использует built-in complex type in Python.
    """
    return complex(real, imag)

def abs_complex(complex_number):
    """
    Функция для вычисления модуля (абсолютного значения) комплексного числа.
    Использует built-in abs() function for complex numbers in Python.
    """
    return abs(complex_number)

def display_geometry_info(data):
    if not data:
        print("No geometry information to display.")
        return

    print("Geometry Information:")

    if data['elements']:
        print("\nElements:")
        for element in data['elements']:
            print(f"  - {element}")

    if data['enums']:
        print("\nEnums:")
        for name, values in data['enums'].items():
            # Convert integer values to strings before joining
            str_values = [str(v) for v in values]  # Convert each value to string
            print(f"  - {name}: {', '.join(str_values)}")

    if data.get('axioms'):  # If axioms exist and are not empty
        print("\nAxioms:")
        for axiom in data['axioms']:
            print(f"  - {axiom['name']}: {axiom['statement']}")

    if data.get('consequences'):  # Same for consequences
        print("\nConsequences:")
        for consequence in data['consequences']:
            print(f"  - {consequence['name']}: {consequence['statement']}")