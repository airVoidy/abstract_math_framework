# parse_rules.py
import sys
import yaml
import matplotlib.pyplot as plt
from abstract_math_vis import visualize_impossible_staircase_3d, visualize_penrose_triangle_2d, visualize_shape  # <--- Import visualize_shape from vis module
import abstract_math_parser
import abstract_math_vis

def main():
    """ Главная функция для запуска парсера abstract_math и правил геометрии. """

    if len(sys.argv) < 2:
        print("Использование: python parse_rules.py <имя_файла.parse> [<имя_файла_геометрии.yaml>]")
        print("<имя_файла.parse> - Файл с кодом abstract_math.")
        print("<имя_файла_геометрии.yaml> (опционально) - Файл с правилами геометрии (по умолчанию: geometry_definitions.yaml).")
        sys.exit(1)

    abstract_math_filepath = sys.argv[1]  # First argument: abstract math file
    geometry_rules_file = sys.argv[1] # Default geometry rules file

    if len(sys.argv) > 2: # Check if a second argument (geometry rules file) is provided
        geometry_rules_file = sys.argv[2] # Override default with user-provided file

    try:
        with open(abstract_math_filepath, 'r', encoding='utf-8') as f:
            abstract_math_code = f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл с abstract_math кодом '{abstract_math_filepath}' не найден.")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при чтении файла abstract_math кода '{abstract_math_filepath}': {e}")
        sys.exit(1)

    print(f"\n----- Парсинг файла abstract_math кода: {abstract_math_filepath} -----")
    print("Код abstract_math из файла:\n")
    print(abstract_math_code)

    # Placeholder for abstract_math parsing and visualization - if needed in the future
    parsed_result = abstract_math_parser.parse_abstract_math_declarations(abstract_math_code)
    visualization_plan = abstract_math_vis.execute_visualization_bt(parsed_result)
    elements_to_visualize = visualization_plan.get("elements_to_visualize", [])


    geometry_rules = abstract_math_parser.parse_geometry_rules_file(sys.argv[1]) # Parse geometry rules using (possibly) user-provided file

    if geometry_rules:
        print(f"\n----- Parsing geometry rules file: {geometry_rules_file} -----")
        for rule in geometry_rules:
            fig, ax_2d = plt.subplots() # Create figure and axes for each rule
            ax_2d.set_aspect('equal')

            visualization_success = visualize_shape(rule, ax_2d) # Visualize shape using dispatcher

            if visualization_success:
                output_filename = f"{rule['shape_enum']}_matplotlib.png"
                fig.savefig(output_filename)
                plt.close(fig)
                print(f" Saved visualization to {output_filename}")
            else:
                print(f" Visualization failed for {rule['shape_enum']}")
    else:
        print(f" No geometry rules found in {geometry_rules_file}")

    # Placeholder for abstract_math element visualization - if needed in the future
    for element_name in elements_to_visualize:
        element_data = None
        for element in parsed_result.get('elements', []):
            if element.get('name') == element_name:
                element_data = element
                break
        if element_data:
            abstract_math_vis.visualize_element(element_data, parsed_result)

    # Placeholder for abstract_math parsing result output - if needed in the future
    print("\nРезультат парсинга abstract_math кода:")
    if parsed_result:
        print(parsed_result)
        for element in parsed_result.get('elements', []):
            abstract_math_vis.visualize_element(element, parsed_result)
    else:
        print("Парсинг abstract_math кода не удался (вернул None)")


if __name__ == "__main__":
    main()