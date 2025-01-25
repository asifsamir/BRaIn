import javalang

# Recursive function to parse and print class, method, field, and variable signatures


def parse_node(node, signatureTokens, indent=0):
    prefix = "  " * indent  # Indentation for nested elements

    if isinstance(node, javalang.tree.ClassDeclaration):
        class_signature = f"{prefix}Class: {node.name}"

        signatureTokens.append(node.name)

        # Recursively parse the members of the class (fields, methods, constructors, nested classes)
        for member in node.body:
            parse_node(member, signatureTokens,indent + 1)

    elif isinstance(node, javalang.tree.MethodDeclaration):
        method_signature = f"{prefix}Method: {node.name}({', '.join(param.type.name for param in node.parameters)})"
        signatureTokens.append(node.name)
        # add node parameters to signatureTokens
        for param in node.parameters:
            signatureTokens.append(param.type.name)
            signatureTokens.append(param.name)

        # Recursively parse the method body
        if node.body:
            for stmt in node.body:
                parse_node(stmt, indent + 1)

    elif isinstance(node, javalang.tree.ConstructorDeclaration):
        constructor_signature = f"{prefix}Constructor: {node.name}({', '.join(param.type.name for param in node.parameters)})"
        # print(constructor_signature)

        for param in node.parameters:
            signatureTokens.append(param.type.name)
            signatureTokens.append(param.name)

        # Recursively parse the constructor body
        if node.body:
            for stmt in node.body:
                parse_node(stmt, indent + 1)

    elif isinstance(node, javalang.tree.FieldDeclaration):
        for declarator in node.declarators:
            field_signature = f"{prefix}Field: {declarator.name} : {node.type.name}"
            # print(field_signature)

            signatureTokens.append(node.type.name)
            signatureTokens.append(declarator.name)

    elif isinstance(node, javalang.tree.LocalVariableDeclaration):
        # Local variable declarations within methods or constructors
        for declarator in node.declarators:
            variable_signature = f"{prefix}Variable: {declarator.name} : {node.type.name}"
            # print(variable_signature)

            signatureTokens.append(node.type.name)
            signatureTokens.append(declarator.name)


    # elif isinstance(node, javalang.tree.VariableDeclarator):
    #     # For local variables within methods or constructors
    #     # variable_signature = f"{prefix}Variable: {node.name}"
    #     print(variable_signature)

    elif isinstance(node, javalang.tree.LocalVariableDeclaration):
        # Local variable declarations within methods or constructors
        for declarator in node.declarators:
            parse_node(declarator, indent)

    elif isinstance(node, javalang.tree.Statement):
        # Parse statements which may contain nested elements
        if hasattr(node, 'children'):
            for child in node.children:
                parse_node(child, indent + 1)

    # Add more cases as needed for other Java elements (e.g., inner classes, interfaces, etc.)

    return signatureTokens

if __name__ == '__main__':
    signatureTokens = []
    # Load the Java source code from a file
    with open(
            "D:\Research\Data\Intelligent_Feedback\Sources\Apache\CAMEL\camel-1.1.0\\1ddc9d95883fdbb770f19bfeaf42b63f.java",
            'r') as file:
        java_code = file.read()

    # Parse the code
    tree = javalang.parse.parse(java_code)

    # Start parsing from the root of the tree
    for path, node in tree:
        # Look for top-level class declarations and start parsing
        if isinstance(node, javalang.tree.ClassDeclaration):
            signatureTokens = parse_node(node, signatureTokens)

    for token in signatureTokens:
        print(token)