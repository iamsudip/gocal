""" web utils """

import ast
import operator
import string


class ExpressionHandler(object):
    # Flag to change the evaluator
    USE_AST_EVALUATOR = False

    def __init__(self, expression):
        self._expression = expression

    def __call__(self):
        AST_EVALUATOR = ASTExpressionEvaluator
        BASIC_EVALUATOR = ExpressionEvaluator
        if self.__class__.USE_AST_EVALUATOR:
            evaluator = AST_EVALUATOR
        else:
            evaluator = BASIC_EVALUATOR
        return evaluator(self._expression)


class EvaluateExpressionError(Exception):
    pass


class ASTExpressionEvaluator(object):
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
            raise EvaluateExpressionError('Invalid Expression')
        else:
            return result


class ExpressionEvaluator(object):
    def __init__(self, expression):
        self.operators = []
        self.operands = []
        self._expression = expression
        self.prev_token = None

    def __call__(self):
        return self.evaluate()

    @staticmethod
    def check_precedence(operand1, operand2):
        if not operand2:
            return False
        if operand1 in ('*', '/') and operand2 in ('+', '-'):
            return False
        else:
            return True

    @staticmethod
    def get_operator_function(op):
        """
        Returns the function mapped to operator
        """
        op_func_map = {
            '*': operator.mul,
            '/': operator.truediv,
            '+': operator.add,
            '-': operator.sub,
        }
        return op_func_map.get(op)

    def operator_peek(self):
        """
        Returns the top value of the operators stack if not empty
        """
        if self.operators:
            return self.operators[-1]
        else:
            return None

    def simplify_expression(self):
        """
        Just pops from operators stack and pops twice to get the operands from
        operands stack, applies operator and pushes the result to operand stack
        """
        current_operator = self.operators.pop()
        right, left = float(self.operands.pop()), float(self.operands.pop())
        current_value = ExpressionEvaluator.get_operator_function(
            current_operator)(left, right)
        self.operands.append(current_value)

    def evaluate(self):
        for token in self._expression:
            if token == ' ':
                continue
            elif token in ['*', '/', '+', '/']:
                if not self.operators:
                    self.operators.append(token)
                else:
                    while ExpressionEvaluator.check_precedence(token, self.operator_peek()):
                        self.simplify_expression()
                    self.operators.append(token)
            elif token in list(string.digits):
                if self.prev_token and self.prev_token.isdigit():
                    self.operands.pop()
                    self.operands.append(self.prev_token+token)
                else:
                    self.operands.append(token)
            else:
                raise EvaluateExpressionError('Invalid Expression')
            self.prev_token = token
        while self.operators:
            self.simplify_expression()
        result = self.operands.pop()
        return result


def evaluate_expression(expression):
    return ExpressionHandler(expression)()

