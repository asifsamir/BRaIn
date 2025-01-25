import javalang

def parse_java_methods_and_constructors(file_path):
    with open(file_path, 'r') as file:
        java_code = file.read()

    tree = javalang.parse.parse(java_code)
    classes_methods_dict = {}

    lines = java_code.splitlines()

    for _, class_node in tree.filter(javalang.tree.ClassDeclaration):
        class_name = class_node.name
        methods_dict = {}

        # Helper function to get the code block based on braces
        def get_code_block(start_line, start_column):
            brace_count = 0
            in_block = False
            code_block_lines = []
            for i, line in enumerate(lines[start_line:], start=start_line):
                if i == start_line:
                    line = line[start_column:]
                brace_count += line.count('{')
                brace_count -= line.count('}')
                code_block_lines.append(line)
                if brace_count == 0 and in_block:
                    break
                if '{' in line:
                    in_block = True
            return code_block_lines

        # Extract methods
        for method_node in class_node.methods:
            method_name = method_node.name
            start_position = method_node.position.line - 1
            start_column = method_node.position.column - 1

            # Ensure we capture the full method signature (which might span multiple lines)
            while not lines[start_position].strip().endswith('{'):
                start_position += 1

            method_code_lines = get_code_block(start_position, start_column)
            method_code = '\n'.join(method_code_lines)
            methods_dict[method_name] = method_code

        # Extract constructors
        for constructor_node in class_node.constructors:
            constructor_name = constructor_node.name
            start_position = constructor_node.position.line - 1
            start_column = constructor_node.position.column - 1

            # Ensure we capture the full constructor signature (which might span multiple lines)
            while not lines[start_position].strip().endswith('{'):
                start_position += 1

            constructor_code_lines = get_code_block(start_position, start_column)
            constructor_code = '\n'.join(constructor_code_lines)
            methods_dict[constructor_name] = constructor_code

        classes_methods_dict[class_name] = methods_dict

    return classes_methods_dict

if __name__ == "__main__":
    classes_methods = parse_java_methods_and_constructors('java_file.java')
    for class_name, methods in classes_methods.items():
        print(f"Class: {class_name}")
        for method_name, method_code in methods.items():
            print(f"  Method/Constructor: {method_name}\n  Code:\n{method_code}\n")
