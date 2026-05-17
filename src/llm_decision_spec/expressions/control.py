from .base import Expr, _require_expr


class Coalesce(Expr):
    def __init__(self, *exprs: Expr):
        if len(exprs) < 2:
            raise TypeError("Coalesce requires at least 2 Exprs")

        self.exprs = [_require_expr(e, "expr") for e in exprs]

    def eval(self, event: dict):
        for expr in self.exprs:
            v = expr.eval(event)
            if v is not None:
                return v
        return None


class FillNA(Coalesce):
    def __init__(self, expr: Expr, fill_expr: Expr):
        super().__init__(expr, fill_expr)


class NullIf(Expr):
    raise NotImplementedError("NullIf not implemented")
