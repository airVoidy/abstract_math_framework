import tkinter as tk
from tkinter import filedialog  # Keep filedialog import in driver_script for menu
from tkinter import BooleanVar  # Import BooleanVar for visibility checkbox
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from enum import Enum  #  Импортируем LayerType из abstract_math_layer
# Relative import to get LayerType, Layer, create_layer from core module
from abstract_math_framework.core.abstract_math_layer import LayerType, Layer, create_layer
import functools  # <--- functools импортирован здесь, если нет в update_layer_listbox

# Relative import to get Visualizer and CartesianVisualizer from visualizers directory
from ..visualizers.visualizers import Visualizer, CartesianVisualizer

# Relative import to get load_yaml_config, loaded_yaml_configs, create_visualizer, load_default_yaml_config_from_directory from yaml_config_module
from ..modules.yaml_config_module.config_manager import load_yaml_config, loaded_yaml_configs, create_visualizer, load_default_yaml_config_from_directory

# Relative import to get YAMLVisualizer from yaml_config_module
from ..modules.yaml_config_module.yaml_visualizer import YAMLVisualizer

# --- Глобальные переменные ---
playground_shapes = {}
interactive_layers = [] # Список для хранения слоев
canvas_items_ids = {} # Словарь для хранения canvas object IDs для слоев
selected_layers_for_deletion = [] # Список выбранных слоев для удаления (возможно, пока не используется)
root = None # Добавляем global root
playground_canvas = None
playground_ax = None
palette_frame_container = None
tools_frame_container = None
layer_list_frame = None
remove_button = None


# --- YAML ---
def load_yaml_config():
    file_path = filedialog.askopenfilename(filetypes=[("YAML files", "*.yaml *.yml")])
    if file_path:
        try:
            with open(file_path, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    process_yaml_config(yaml_config)
                    print(f"YAML configuration loaded from: {file_path}")
                else:
                    print("YAML file is empty or invalid.")
        except Exception as e:
            print(f"Error loading YAML file: {e}")

def process_yaml_config(yaml_config):
    global playground_shapes, gui_elements_config
    print("DEBUG: Entering process_yaml_config")
    if 'enums' in yaml_config and 'Shapes' in yaml_config['enums']:
        playground_shapes = {name: data for name, data in yaml_config['enums']['Shapes'].items()}
        print(f"DEBUG: Playground shapes Parsed: {playground_shapes}") # <--- ADD THIS DEBUG PRINT AFTER PARSING
    if 'gui_elements' in yaml_config:
        gui_elements_config = yaml_config['gui_elements']
        print(f"GUI Elements Parsed: {gui_elements_config}")
        create_gui_elements(gui_elements_config) # Передаем считанную конфигурацию GUI
    else:
        print("No 'gui_elements' section found in YAML, using default GUI.")

    parsed_yaml_data = yaml_config # Сохраняем для отладки и возможного использования
    print(f"Parsed YAML data: {parsed_yaml_data}")


# --- GUI ---
def create_gui_elements(gui_elements_config):
    global palette_frame, tools_frame, palette_frame_container, tools_frame_container # Added containers to global

    if 'palettes' in gui_elements_config:
        palettes_config = gui_elements_config['palettes']
        print(f"Конфигурация палет из YAML: {palettes_config}")
        for palette_config in palettes_config:
            if palette_config['name'] == 'Shape Palette':
                palette_frame = create_palette(parent=palette_frame_container, config=palette_config)
            elif palette_config['name'] == 'Tools':
                tools_frame = create_palette(parent=tools_frame_container, config=palette_config)
        print("Палеты созданы из YAML")
    else:
        print("No palette configuration found in YAML.")

def create_palette(parent, config):
    palette_frame_to_use = tk.LabelFrame(parent, text=config['name'])
    palette_frame_to_use.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    print(f"Палета '{config['name']}' создана и упакована: {palette_frame_to_use}, родитель={parent}, root={root}")

    if 'buttons' in config:
        buttons_config = config['buttons']
        print(f"Конфигурация кнопок для палеты '{config['name']}': {buttons_config}")
        for button_config in buttons_config:
            create_button_from_config(palette_frame_to_use, button_config)
    return palette_frame_to_use

def create_button_from_config(palette_frame_to_use, button_config):
    if button_config['type'] == 'shape_button':
        command = lambda prim_type=button_config['primitive_type_name']: draw_shape_on_playground(prim_type)
        button = tk.Button(palette_frame_to_use, text=button_config['label'], command=command)
        print(f"DEBUG: Creating shape button: label={button_config['label']}, primitive_type_name={button_config['primitive_type_name']}, command={command}") # <--- ADD THIS DEBUG PRINT
    elif button_config['type'] == 'tool_button':
        tool_name = button_config['tool_name']
        if tool_name == 'load_yaml_config':
            command = load_yaml_config
        elif tool_name == 'add_point_layer':
            command = lambda: handle_tool_button_press(tool_name) #  Передаем tool_name
        elif tool_name == 'add_center_point_layer':
            command = lambda: handle_tool_button_press(tool_name) # Передаем tool_name
        else:
            command = None
        button = tk.Button(palette_frame_to_use, text=button_config['label'], command=command)
        print(f"Создание кнопки: palette_frame_to_use={palette_frame_to_use}, label={button_config['label']}, command={command}")

    else:
        print(f"Unknown button type: {button_config['type']}")
        return None

    button.pack(side=tk.TOP, fill=tk.X, pady=5)
    print(f"Кнопка создана и упакована: {button_config['label']}, тип: {button_config['type']}, упакована в: {palette_frame_to_use}, родитель={palette_frame_to_use.master}, root={root}")
    return button


def handle_tool_button_press(tool_name):
    print(f"Кнопка инструмента нажата: {tool_name}")
    if tool_name == 'add_point_layer':
        print(f"DEBUG: handle_tool_button_press: calling add_interactive_layer(abstract_math_layer.LayerType.POINT)")
        add_interactive_layer(LayerType.POINT) #  Используем LayerType.POINT
    elif tool_name == 'add_center_point_layer':
        print(f"DEBUG: handle_tool_button_press: calling add_interactive_layer(abstract_math_layer.LayerType.CENTER_POINT)")
        add_interactive_layer(LayerType.CENTER_POINT) # Используем LayerType.CENTER_POINT
    elif tool_name == 'load_yaml_config':
        load_yaml_config()
    else:
        print(f"Unknown tool name: {tool_name}")


def add_interactive_layer(layer_type): #  Принимаем LayerType
    print(f"add_interactive_layer вызван с типом: {layer_type}")
    layer_name = f"{layer_type.value.capitalize()}{len(interactive_layers) + 1}" #  Используем value из LayerType
    new_layer = create_layer(name=layer_name, layer_type=layer_type) # Используем create_layer и LayerType
    interactive_layers.append(new_layer)
    update_layer_listbox() # Обновляем список слоев в GUI
    redraw_playground_canvas()
    print(f"Слой создан с помощью кнопки: {new_layer}, список слоев: {interactive_layers}")


def draw_shape_on_playground(primitive_type_name):
    global playground_ax
    print(f"DEBUG: Entering draw_shape_on_playground with primitive_type_name: {primitive_type_name}") # <--- DEBUG PRINT at function start
    print(f"DEBUG: Current playground_shapes dictionary: {playground_shapes}") # <--- DEBUG PRINT to inspect dictionary content
    if primitive_type_name in playground_shapes:
        shape_data = playground_shapes[primitive_type_name]
        shape_type = shape_data[0]
        coords = shape_data[1:]
        if shape_type == 'rectangle':
            x, y, width, height = coords
            rect = playground_ax.add_patch(plt.Rectangle((x, y), width, height, edgecolor='blue', facecolor='lightblue'))
            playground_canvas.draw()
            playground_shapes[primitive_type_name].append(rect) #  Сохраняем объект Rectangle
            print(f"DEBUG: Нарисован прямоугольник '{primitive_type_name}' с координатами {coords}")
        else:
            print(f"Unknown shape type: {shape_type}")
    else:
        print(f"Primitive type name not found in playground_shapes: {primitive_type_name}")


def redraw_playground_canvas():
    global playground_ax
    print("redraw_playground_canvas вызван")
    playground_ax.clear()
    # --- Рисуем shapes ---
    for shape_name, shape_config in playground_shapes.items():
        shape_type = shape_config[0]
        coords = shape_config[1:] #  Координаты до последнего элемента (Rectangle object)
        if shape_type == 'rectangle':
            x, y, width, height = coords
            playground_ax.add_patch(plt.Rectangle((x, y), width, height, edgecolor='blue', facecolor='lightblue'))

    # --- Рисуем interactive layers ---
    for layer in interactive_layers:
        if layer.visible:
            print(f"Рисование слоя: {layer}")
            # --- ВРЕМЕННАЯ МЕРА: ПРОВЕРКА НАЛИЧИЯ МЕТОДА draw() ---
            if hasattr(layer, 'draw') and callable(layer.draw): # <--- Проверка наличия метода draw и что это функция
                layer.draw(playground_ax)
            # --- КОНЕЦ ВРЕМЕННОЙ МЕРЫ ---

    playground_canvas.draw()
    print("redraw_playground_canvas завершил рисование")


def update_layer_listbox():
    global layer_list_frame, remove_button #  Добавили global layer_list_frame и remove_button
    print("--- START update_layer_listbox ---")
    print(f"update_layer_listbox вызван, remove_button={remove_button}")
    # Очищаем фрейм списка слоев перед перерисовкой
    print(f"layer_list_frame children BEFORE destroy loop: {layer_list_frame.winfo_children()}")
    for child in layer_list_frame.winfo_children():
        child.destroy()
    print(f"layer_list_frame children AFTER destroy loop: {layer_list_frame.winfo_children()}")

    print(f"interactive_layers before render: {interactive_layers}")
    for i, layer in enumerate(interactive_layers):
        layer_item_frame = tk.Frame(layer_list_frame, bg="lightcyan", bd=1, relief=tk.RAISED) # Используем global layer_list_frame
        layer_item_frame.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        layer_label = tk.Label(layer_item_frame, text=layer.name, bg="lightcyan", anchor="w")
        layer_label.pack(side=tk.LEFT, padx=5)

        # --- Чекбокс для выбора слоя для удаления ---
        select_var = tk.BooleanVar(value=False)
        select_checkbutton = tk.Checkbutton(layer_item_frame, text="Select", variable=select_var, bg="lightcyan",
                                             command=functools.partial(toggle_select_command, layer, select_var))
        select_checkbutton.pack(side=tk.RIGHT, padx=5)

        # --- Чекбокс видимости ---
        visibility_var = BooleanVar(value=layer.visible)
        visibility_checkbutton = tk.Checkbutton(layer_item_frame, text="Visible", variable=visibility_var, bg="lightcyan",
                                                 command=functools.partial(toggle_layer_visibility, layer, visibility_var))
        visibility_checkbutton.pack(side=tk.RIGHT, padx=5)

    # --- Логика активации кнопки "Удалить слой" ---
    print("DEBUG: --- НАЧАЛО ЛОГИКИ АКТИВАЦИИ КНОПКИ ---")
    print(f"DEBUG: interactive_layers: {interactive_layers}")
    is_any_layer_selected = False #  Сброс перед проверкой
    if interactive_layers: #  Проверяем, что список слоев не пуст
        print("DEBUG: Список interactive_layers НЕ ПУСТ") #  Для отладки
        for layer in interactive_layers:
            print(f"DEBUG: Проверяю слой: {layer.name}")
            # Теперь состояние берется непосредственно из select_var.get()
            layer_item_frame = layer_list_frame.winfo_children()[i] # Получаем фрейм слоя
            select_checkbox = layer_item_frame.winfo_children()[1] # Чекбокс "Select" - второй элемент
            select_var = select_checkbox.cget("variable") # Получаем связанную BooleanVar

            if select_var: # Убедимся, что BooleanVar существует
                select_var_instance = root.getvar(select_var) # Получаем экземпляр BooleanVar по имени
                if select_var_instance:
                    if select_var_instance.get():
                        is_any_layer_selected = True
                        print(f"DEBUG: Слой '{layer.name}' выбран через Checkbox: {select_var_instance.get()}")
                        break # Если хотя бы один слой выбран, кнопка активна, можно выйти
                    else:
                        print(f"DEBUG: Слой '{layer.name}' НЕ выбран через Checkbox: {select_var_instance.get()}")
                else:
                    print(f"DEBUG: BooleanVar instance is None for layer: {layer.name}")
            else:
                print(f"DEBUG: BooleanVar name is None for layer: {layer.name}")
    else:
        print("DEBUG: Список interactive_layers ПУСТ") #  Отладка пустого списка
    print(f"DEBUG: is_any_layer_selected = {is_any_layer_selected}") # <--- ДОБАВЛЕНА ОТЛАДОЧНАЯ ПЕЧАТЬ ЗДЕСЬ
    if is_any_layer_selected:
        remove_button.config(state=tk.NORMAL) # Используем global remove_button
        print("DEBUG: Кнопка 'Удалить слой' АКТИВИРОВАНА")
    else:
        remove_button.config(state=tk.DISABLED) # Используем global remove_button
        print("DEBUG: Кнопка 'Удалить слой' ДЕАКТИВИРОВАНА")
    print("DEBUG: --- КОНЕЦ ЛОГИКИ АКТИВАЦИИ КНОПКИ ---")
    print("--- END update_layer_listbox ---")


def toggle_layer_visibility(layer, visibility_var):
    print(f"Видимость слоя '{layer.name}' изменена на: {visibility_var.get()}")
    layer.visible = visibility_var.get() # Обновляем свойство visible слоя
    redraw_playground_canvas() #  Перерисовываем canvas после изменения видимости

def toggle_select_command(layer, select_var):
    layer_selected = select_var.get()
    print(f"Слой '{layer.name}' выбран для удаления: {layer_selected}")
    # Здесь можно добавить логику для обработки выбора слоя для удаления,
    # например, добавление/удаление слоя из списка selected_layers_for_deletion


def remove_selected_layers():
    global interactive_layers

    layers_to_remove = []
    for i, layer in enumerate(interactive_layers):
        layer_item_frame = layer_list_frame.winfo_children()[i] # Получаем фрейм слоя
        select_checkbox = layer_item_frame.winfo_children()[1] # Чекбокс "Select" - второй элемент
        select_var_name = select_checkbox.cget("variable") # Получаем имя BooleanVar
        select_var = root.getvar(select_var_name) # Получаем экземпляр BooleanVar

        if select_var and select_var.get():
            layers_to_remove.append(layer)

    if not layers_to_remove:
        print("Нет выбранных слоев для удаления.")
        return

    print(f"Слои для удаления: {[layer.name for layer in layers_to_remove]}")

    interactive_layers = [layer for layer in interactive_layers if layer not in layers_to_remove]
    update_layer_listbox()
    redraw_playground_canvas()

    print(f"Слои после удаления: {interactive_layers}")



def start_gui():
    global root, playground_canvas, playground_ax, palette_frame_container, tools_frame_container, layer_list_frame, remove_button # Добавляем globals
    root = tk.Tk()
    root.title("Интерактивная Песочница")

    # --- Фреймы ---
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    left_frame = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    center_frame = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN)
    center_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    right_frame = tk.Frame(main_frame, bd=2, relief=tk.SUNKEN, width=200) #  Фиксированная ширина для правой панели
    right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10,  )
    right_frame.pack_propagate(False) #  Чтобы ширина правой панели не менялась от содержимого

    palette_frame_container = tk.Frame(left_frame)
    palette_frame_container.pack(side=tk.TOP, fill=tk.Y, expand=True)

    tools_frame_container = tk.Frame(left_frame)
    tools_frame_container.pack(side=tk.TOP, fill=tk.Y, expand=True)


    # --- Холст Matplotlib ---
    playground_fig = Figure(figsize=(5, 5), dpi=100)
    playground_ax = playground_fig.add_subplot(111)
    playground_ax.set_xlim([-10, 10])
    playground_ax.set_ylim([-10, 10])
    playground_ax.set_aspect('equal', adjustable='box')
    playground_canvas = FigureCanvasTkAgg(playground_fig, master=center_frame)
    playground_canvas_widget = playground_canvas.get_tk_widget()
    playground_canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # --- Панель инструментов Matplotlib ---
    toolbar_frame = tk.Frame(center_frame) #  Создаем фрейм для toolbar
    toolbar_frame.pack(side=tk.TOP, fill=tk.X) #  Упаковываем фрейм *выше* холста
    toolbar = NavigationToolbar2Tk(playground_canvas, toolbar_frame) #  Помещаем toolbar во фрейм
    toolbar.update()


    # --- Фрейм для списка слоев и кнопки "Удалить слой" ---
    layer_control_frame = tk.Frame(right_frame)
    layer_control_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    layer_list_frame = tk.Frame(layer_control_frame, bg="lightcyan", bd=2, relief=tk.SUNKEN) #  Цвет для наглядности
    layer_list_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
    print(f"DEBUG: layer_list_frame created: {layer_list_frame}")


    remove_button = tk.Button(layer_control_frame, text="Удалить слой", command=remove_selected_layers, state=tk.DISABLED)
    print(f"DEBUG: Before remove_button creation: layer_list_frame={layer_list_frame}, is_instance(layer_list_frame, tk.Frame)={isinstance(layer_list_frame, tk.Frame)}") #  Отладка frame
    remove_button.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
    print(f"DEBUG: After remove_button creation: remove_button={remove_button}, is_instance(remove_button, tk.Button)={isinstance(remove_button, tk.Button)}") # Отладка button

    update_layer_listbox() #  Первоначальная отрисовка списка слоев (пустого)


    # --- Меню ---
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Load Config YAML", command=load_yaml_config)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)


    # --- Обработка событий ---
    root.bind("<KeyPress>", handle_keypress) #  Привязка обработки keypress
    print("Связывание событий установлено")

    redraw_playground_canvas() #  Первоначальная отрисовка canvas (с Rectangle1)
    print("Начальный redraw_playground_canvas вызов ПОСЛЕ mainloop()")


    print("Правила песочницы распарсены и GUI успешно запущен.")
    root.mainloop()



def handle_keypress(event):
    print(f"Key pressed: {event.keysym}")
    if event.keysym == 'l':
        load_yaml_config()
    elif event.keysym == 'p':
        handle_tool_button_press('add_point_layer')
    elif event.keysym == 'c':
        handle_tool_button_press('add_center_point_layer')
    elif event.keysym == 'r':
        draw_shape_on_playground('rectangle1')


if __name__ == "__main__":
    print("Запускаю GUI...")
    # --- Загрузка YAML конфигурации по умолчанию при старте, если есть ---
    default_yaml_path = 'playground.yaml'
    try:
        with open(default_yaml_path, 'r') as f:
            print("DEBUG: Пытаюсь загрузить YAML файл...") # <--- НОВАЯ ОТЛАДОЧНАЯ ПЕЧАТЬ ВНУТРИ TRY
            default_yaml_config = yaml.safe_load(f)
            if default_yaml_config:
                process_yaml_config(default_yaml_config)
                print(f"YAML конфигурация по умолчанию загружена из: {default_yaml_path}")
            else:
                print("YAML конфигурация по умолчанию пуста или невалидна, используются правила песочницы по умолчанию.")
    except FileNotFoundError:
        print("YAML конфигурация не загружена, используются правила песочницы по умолчанию.")

    start_gui()