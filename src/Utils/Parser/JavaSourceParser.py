import re

import javalang as jl
from .SourceRefiner import clear_formatting
# from SourceRefiner import clear_formatting

class JavaSourceParser:
    def __init__(self, data, clear_formatting=False):
        self.data = data
        self.tree = jl.parse.parse(data)
        self.methods = {}
        self.fields = set()
        self.clear_formatting = clear_formatting

    def get_start_end_for_node(self, node_to_find):
        start = None
        end = None
        for path, node in self.tree:
            if start is not None and node_to_find not in path:
                end = node.position
                return start, end
            if start is None and node == node_to_find:
                start = node.position
        return start, end

    def get_string(self, start, end):
        if start is None:
            return ""

        end_pos = None
        if end is not None:
            end_pos = end.line - 1

        lines = self.data.splitlines(True)
        string = "".join(lines[start.line:end_pos])
        string = lines[start.line - 1] + string

        if end is None:
            left = string.count("{")
            right = string.count("}")
            if right - left == 1:
                p = string.rfind("}")
                string = string[:p]

        return string

    def parse_methods(self):
        # get the class name
        class_name = None

        for _, node in self.tree.filter(jl.parser.tree.ClassDeclaration):
            class_name = node.name

            # for this class, get all the methods
            for _, method in node.filter(jl.parser.tree.MethodDeclaration):
                start, end = self.get_start_end_for_node(method)
                method_body = self.get_string(start, end)
                if self.clear_formatting:
                    method_body = clear_formatting(method_body)
                self.methods[method.name] = method_body


        for _, node in self.tree.filter(jl.parser.tree.MethodDeclaration):
            start, end = self.get_start_end_for_node(node)
            method_body = self.get_string(start, end)
            if self.clear_formatting:
                method_body = clear_formatting(method_body)
            self.methods[node.name] = method_body

        return self.methods

    def parse_fields(self):
        for _, node in self.tree.filter(jl.parser.tree.FieldDeclaration):
            start, end = self.get_start_end_for_node(node)
            self.fields.add(self.get_string(start, end).strip())
            # self.fields[node.name] = self.get_string(start, end)

        return self.fields

    def split_camel_case(self, identifier):
        """
        Splits a camelCase or PascalCase identifier into individual words.
        For example, 'isTrue' becomes ['is', 'True'].
        """
        return re.sub('([a-z])([A-Z])', r'\1 \2', identifier).split()

    def parse_class_method_field_name(self, java_code):

        tree = jl.parse.parse(java_code)

        class_names = []
        method_names = []
        field_names = []

        for path, node in tree:
            if isinstance(node, jl.tree.ClassDeclaration):
                class_names.append(node.name)
            elif isinstance(node, jl.tree.MethodDeclaration):
                method_names.append(node.name)
            elif isinstance(node, jl.tree.FieldDeclaration):
                for declarator in node.declarators:
                    field_names.append(declarator.name)

        return class_names, method_names, field_names

if __name__ == '__main__':
    data = '''public class MainClass {
    public int a;
        public static void main(String[] args) {
        int b;
            System.out.println("hello world");
        }

        public void foo() {
            System.out.println("foo");
        }

        public void isTrue() {
            int defIsTrue;
            System.out.println("bar");
        }
    }'''

    parser = JavaSourceParser(data, clear_formatting=True)
    parser.parse_methods()
    class_n, method_n, field_n = parser.parse_class_method_field_name(data)
    class_n = parser.split_camel_case(class_n[0])

    print(class_n)
    print(method_n)
    print(field_n)
    # print(parser.methods)
    # print(parser.parse_fields())
