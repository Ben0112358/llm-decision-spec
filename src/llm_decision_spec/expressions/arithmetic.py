from llm_decision_spec.expressions.base import BinaryExpr, UnaryExpr
from llm_decision_spec.expressions.evaluate import is_missing


def _numeric_binary(left, right, op):
    if is_missing(left) or is_missing(right):
        return None
    if not isinstance(left, (int, float)) or not isinstance(
        right, (int, float)
    ):
        raise TypeError(
            "numeric operation requires int or float, "
            f"got {type(left)}, {type(right)}"
        )
    return op(left, right)


class Add(BinaryExpr):
    def eval(self, event: dict):
        return _numeric_binary(
            self.left.eval(event), self.right.eval(event), lambda a, b: a + b
        )


class Sub(BinaryExpr):
    def eval(self, event: dict):
        return _numeric_binary(
            self.left.eval(event), self.right.eval(event), lambda a, b: a - b
        )


class Mul(BinaryExpr):
    def eval(self, event: dict):
        return _numeric_binary(
            self.left.eval(event), self.right.eval(event), lambda a, b: a * b
        )


class Div(BinaryExpr):
    def eval(self, event: dict):
        return _numeric_binary(
            self.left.eval(event), self.right.eval(event), lambda a, b: a / b
        )


class Pow(BinaryExpr):
    def eval(self, event: dict):
        return _numeric_binary(
            self.left.eval(event), self.right.eval(event), lambda a, b: a**b
        )


class Neg(UnaryExpr):
    def eval(self, event: dict):
        v = self.operand.eval(event)
        if is_missing(v):
            return None
        if not isinstance(v, (int, float)):
            raise TypeError(f"Neg requires numeric value, got {type(v)}")
        return -v


class Abs(UnaryExpr):
    def eval(self, event: dict):
        v = self.operand.eval(event)
        if is_missing(v):
            return None
        if not isinstance(v, (int, float)):
            raise TypeError(f"Abs requires numeric value, got {type(v)}")
        return abs(v)
