""" web utils """

import ast
import operator


class Expression(object):
    AST_TO_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }

    def __init__(self, expression):
        self._expression = expression

    def __call__(self):
        return self.__class__.evaluate_expression(self._expression)

    @classmethod
    def evaluate(cls, node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return cls.AST_TO_OPERATORS[type(node.op)](cls.evaluate(node.left), cls.evaluate(node.right))
        elif isinstance(node, ast.UnaryOp):
            return cls.AST_TO_OPERATORS[type(node.op)](cls.evaluate(node.operand))
        else:
            raise SyntaxError(node)

    @classmethod
    def evaluate_expression(cls, expression):
        try:
            result = cls.evaluate(ast.parse(expression, mode='eval').body)
        # SyntaxError comes when there is a syntax error in expression
        # KeyError comes when operation is not implemented (check AST_TO_OPERATORS)
        except (SyntaxError, KeyError):
            raise TypeError('Invalid Expression')
        else:
            return result

def evaluate_expression(expression):
    return Expression(expression)()

