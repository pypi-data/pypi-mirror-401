from fractions import Fraction

class MixedFraction:
    def __init__(self, dividend, divisor):
        # Type validation
        if not isinstance(dividend, int):
            raise TypeError(f"dividend must be an integer, got {type(dividend).__name__}")
        if not isinstance(divisor, int):
            raise TypeError(f"divisor must be an integer, got {type(divisor).__name__}")

        # Zero division check
        if divisor == 0:
            raise ZeroDivisionError("Divisor cannot be zero.")

        # Sign handling and Fraction creation
        self.neg = (dividend * divisor) < 0
        self.fraction = Fraction(abs(dividend), abs(divisor))
        if self.neg:
            self.fraction = -self.fraction

    def __str__(self):
        quotient = self.fraction.numerator // self.fraction.denominator
        remainder = abs(self.fraction.numerator % self.fraction.denominator)
        denom = self.fraction.denominator

        r_str = str(remainder)
        q_str = str(quotient)
        d_str = str(denom)

        line_len = max(len(r_str), len(d_str))
        line = '—' * line_len

        extra_spaces = len(q_str) - 1
        space_prefix = ' ' * extra_spaces

        return f"  {space_prefix}{r_str}\n{q_str} {line}\n  {space_prefix}{d_str}"

    def __repr__(self):
        return f"MixedFraction({self.fraction.numerator}, {self.fraction.denominator})"

    def __add__(self, other):
        if not isinstance(other, MixedFraction):
            raise TypeError(
                f"Unsupported operand type(s) for +: 'MixedFraction' and '{type(other).__name__}'"
            )
        result = self.fraction + other.fraction
        return MixedFraction(result.numerator, result.denominator)

    def __sub__(self, other):
        if not isinstance(other, MixedFraction):
            raise TypeError(
                f"Unsupported operand type(s) for -: 'MixedFraction' and '{type(other).__name__}'"
            )
        result = self.fraction - other.fraction
        return MixedFraction(result.numerator, result.denominator)

    def __mul__(self, other):
        if not isinstance(other, MixedFraction):
            raise TypeError(
                f"Unsupported operand type(s) for *: 'MixedFraction' and '{type(other).__name__}'"
            )
        result = self.fraction * other.fraction
        return MixedFraction(result.numerator, result.denominator)

    def __truediv__(self, other):
        if not isinstance(other, MixedFraction):
            raise TypeError(
                f"Unsupported operand type(s) for /: 'MixedFraction' and '{type(other).__name__}'"
            )
        result = self.fraction / other.fraction
        return MixedFraction(result.numerator, result.denominator)

    def to_fraction(self):
        return self.fraction
