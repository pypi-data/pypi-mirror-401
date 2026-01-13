import pyobfstrsopsk.ast_compat as ast

from pyobfstrsopsk.ast_annotation import get_parent
from pyobfstrsopsk.transforms.suite_transformer import SuiteTransformer


class ReverseStrings(SuiteTransformer):
    """
    Reverse string literals and wrap them in a reverse_string function call
    """

    def __init__(self):
        self.reverse_func_name = None
        self.reverse_func_added = False
        self.in_f_string = False

    def visit_JoinedStr(self, node):
        # Don't reverse strings inside f-strings
        old_in_f_string = self.in_f_string
        self.in_f_string = True
        try:
            # Visit values but don't reverse string literals inside
            new_values = []
            for value in node.values:
                if isinstance(value, (ast.Str, ast.Constant)) and isinstance(getattr(value, 'value', getattr(value, 's', None)), str):
                    # Skip reversing strings in f-strings
                    new_values.append(value)
                else:
                    new_values.append(self.visit(value))
            node.values = new_values
            return node
        finally:
            self.in_f_string = old_in_f_string

    def visit_Module(self, node):
        # Generate a unique name for the reverse function using the same naming scheme
        from pyobfstrsopsk.rename.name_generator import name_generator
        gen = name_generator()
        self.reverse_func_name = next(gen)
        # Use a simple parameter name that won't conflict
        self.reverse_param_name = 's'
        
        # Visit all nodes first
        node.body = [self.visit(child) for child in node.body]
        
        # Add the reverse_string function at the beginning of the module
        if self.reverse_func_added:
            # Create function: def _stein_xxx(s): return s[::-1]
            # Use lambda style to avoid parameter renaming issues: lambda s: s[::-1]
            # Actually, let's use a simple function with a preserved parameter
            reverse_func = self.add_child(
                ast.FunctionDef(
                    name=self.reverse_func_name,
                    args=ast.arguments(
                        args=[ast.arg(arg=self.reverse_param_name, annotation=None)],
                        vararg=None,
                        kwonlyargs=[],
                        kw_defaults=[],
                        kwarg=None,
                        defaults=[]
                    ),
                    body=[
                        ast.Return(
                            value=ast.Subscript(
                                value=ast.Name(id=self.reverse_param_name, ctx=ast.Load()),
                                slice=ast.Slice(
                                    lower=None,
                                    upper=None,
                                    step=ast.UnaryOp(op=ast.USub(), operand=ast.Constant(value=1))
                                ),
                                ctx=ast.Load()
                            )
                        )
                    ],
                    decorator_list=[],
                    returns=None
                ),
                parent=node
            )
            
            # Mark the parameter and function name to preserve them from renaming
            # Actually, we'll let it be renamed since it will still work
            # The function name will be renamed, but the calls will use the renamed version
            
            node.body.insert(0, reverse_func)
        
        return node
        
        return node

    def visit_Constant(self, node):
        # Skip strings in f-strings
        if self.in_f_string:
            return node
        
        # Skip docstrings (they're typically in Expr nodes at the start of functions/classes)
        parent = get_parent(node)
        if isinstance(parent, ast.Expr) and isinstance(get_parent(parent), (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            # Check if this is a docstring (first statement in body)
            grandparent = get_parent(parent)
            if isinstance(grandparent, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
                if grandparent.body and grandparent.body[0] == parent:
                    return node  # Skip docstrings
        
        if isinstance(node.value, str) and len(node.value) > 0:
            # Reverse the string
            reversed_value = node.value[::-1]
            
            # Replace with a function call
            self.reverse_func_added = True
            return ast.Call(
                func=ast.Name(id=self.reverse_func_name, ctx=ast.Load()),
                args=[ast.Constant(value=reversed_value)],
                keywords=[]
            )
        return node

    def visit_Str(self, node):
        # Skip strings in f-strings
        if self.in_f_string:
            return node
        
        # Skip docstrings
        parent = get_parent(node)
        if isinstance(parent, ast.Expr) and isinstance(get_parent(parent), (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
            grandparent = get_parent(parent)
            if isinstance(grandparent, (ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef, ast.Module)):
                if grandparent.body and grandparent.body[0] == parent:
                    return node  # Skip docstrings
        
        if len(node.s) > 0:
            # Reverse the string
            reversed_value = node.s[::-1]
            
            # Replace with a function call
            self.reverse_func_added = True
            # Use the same node type (Str) for Python < 3.8 compatibility
            return ast.Call(
                func=ast.Name(id=self.reverse_func_name, ctx=ast.Load()),
                args=[ast.Str(s=reversed_value)],
                keywords=[]
            )
        return node

    def visit_Bytes(self, node):
        if len(node.s) > 0:
            # Reverse the bytes
            reversed_value = node.s[::-1]
            
            # Replace with a function call
            self.reverse_func_added = True
            return ast.Call(
                func=ast.Name(id=self.reverse_func_name, ctx=ast.Load()),
                args=[ast.Bytes(s=reversed_value)],
                keywords=[]
            )
        return node