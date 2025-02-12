def is_valid_enum_name(name):
    # Example: Check if the name starts with a letter and contains only alphanumeric characters and underscores
    if not name[0].isalpha():
        return False
    for char in name:
        if not (char.isalnum() or char == '_'):
            return False
    return True

def is_valid_axiom_name(name):
    # Similar validation for axiom names (customize as needed)
    # ... (implement your validation logic here)
    return True # Placeholder

def is_valid_consequence_name(name):
    # Similar validation for consequence names
    # ... (implement your validation logic here)
    return True # Placeholder

def parse_abstract_math_declarations(abstract_math_code):  
    parsed_data = {}

    # 1. Parsing define_elements block
    elements_start = abstract_math_code.find("abstract_math define_elements(){")
    if elements_start != -1:
        elements_end = abstract_math_code.find("}", elements_start)
        if elements_end != -1:
            elements_content = abstract_math_code[elements_start + len("abstract_math define_elements(){"):elements_end].strip()
            parsed_data['elements'] = [elem.strip() for elem in elements_content.split(';') if elem.strip()]
        else:
            print("Parsing Error: Closing '}' not found for define_elements block")
            return None
    else:
        print("Parsing Error: 'abstract_math define_elements(){' block not found")
        return None

    # 2. Parsing define_enums block
    enums_start = abstract_math_code.find("enums define_enums(){")
    if enums_start != -1:
        enums_end = abstract_math_code.find("}", enums_start)
        if enums_end != -1:
            enums_content = abstract_math_code[enums_start + len("enums define_enums(){"):enums_end].strip()
            parsed_data['enums'] = {}

            enum_lines = enums_content.split("\n")
            for line in enum_lines:
                line = line.strip()
                if not line:
                    continue
                
                enum_name_start = line.find("enum{")
                if enum_name_start != -1:
                    enum_name_end = line.find("=")
                    if enum_name_end != -1 and enum_name_start < enum_name_end:
                        enum_name = line[enum_name_start + len("enum{"):enum_name_end].strip()
                        if not is_valid_enum_name(enum_name):  # Ensure this validation is defined
                            print(f"Parsing Error: Invalid enum name '{enum_name}'")
                            return None

                        enum_values_str = line[enum_name_end + len("=") + 1:].strip()
                        enum_values = [val.strip() for val in enum_values_str.split(',') if val.strip()]

                        # Correctly store enum values for each enum name
                        parsed_data['enums'][enum_name] = enum_values
                    else:
                        print(f"Parsing Error: Incorrect enum declaration: '{line}'")
                        return None
        else:
            print("Parsing Error: Closing '}' not found for define_enums block")
            return None
    else:
        print("Parsing Error: 'enums define_enums(){' block not found")
        return None

    # 3. Parsing define_axioms block
    axioms_start = abstract_math_code.find("axioms define_axioms(){")
    if axioms_start != -1:
        axioms_end = abstract_math_code.find("}", axioms_start)
        if axioms_end != -1:
            axioms_content = abstract_math_code[axioms_start + len("axioms define_axioms(){"):axioms_end].strip()
            parsed_data['axioms'] = []  # Initialize list for axioms

            axiom_lines = axioms_content.split("\n")
            for line in axiom_lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")  # Split axiom name and statement
                if len(parts) == 2:
                    axiom_name = parts[0].strip()
                    if not is_valid_axiom_name(axiom_name):  # Ensure this validation is defined
                        print(f"Parsing Error: Invalid axiom name '{axiom_name}'")
                        return None
                    axiom_statement = parts[1].strip()
                    parsed_data['axioms'].append({'name': axiom_name, 'statement': axiom_statement})
                else:
                    print(f"Parsing Error: Incorrect axiom format: '{line}'")
                    return None
        else:
            print("Parsing Error: Closing '}' not found for define_axioms block")
            return None
    else:
        print("Parsing Error: 'axioms define_axioms(){' block not found")
        return None

    # 4. Parsing define_consequences block
    consequences_start = abstract_math_code.find("consequences define_consequences(){")
    if consequences_start != -1:
        consequences_end = abstract_math_code.find("}", consequences_start)
        if consequences_end != -1:
            consequences_content = abstract_math_code[consequences_start + len("consequences define_consequences(){"):consequences_end].strip()
            parsed_data['consequences'] = []  # Initialize list for consequences

            consequence_lines = consequences_content.split("\n")
            for line in consequence_lines:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")  # Split consequence name and statement
                if len(parts) == 2:
                    consequence_name = parts[0].strip()
                    if not is_valid_consequence_name(consequence_name):  # Ensure this validation is defined
                        print(f"Parsing Error: Invalid consequence name '{consequence_name}'")
                        return None
                    consequence_statement = parts[1].strip()
                    parsed_data['consequences'].append({'name': consequence_name, 'statement': consequence_statement})
                else:
                    print(f"Parsing Error: Incorrect consequence format: '{line}'")
                    return None
        else:
            print("Parsing Error: Closing '}' not found for define_consequences block")
            return None
    else:
        print("Parsing Error: 'consequences define_consequences(){' block not found")
        return None
    
    if parsed_data is None:  # Check if parsing failed *immediately*
        print("YAML parsing failed. Check your YAML file.")
        return  # Exit if parsing failed
    return parsed_data
