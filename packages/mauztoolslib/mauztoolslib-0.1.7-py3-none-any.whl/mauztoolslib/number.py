import enum

class Stats(enum.Flag):
    INFINITY = 1
    NEGATIV_INFINITY = 2
    NOTANUMBER = 4
    NORMAL = 8  # Für normale Zahlen

class Number:
    def __init__(self, value):
        # Wenn value schon Number ist, übernehmen
        if isinstance(value, Number):
            self.value = value.value
            self.stats = value.stats
        elif isinstance(value, str):
            self.value = value
            lower_val = value.lower()
            if lower_val == "inf":
                self.stats = Stats.INFINITY
            elif lower_val == "-inf":
                self.stats = Stats.NEGATIV_INFINITY
            elif lower_val == "nan":
                self.stats = Stats.NOTANUMBER
            else:
                self.stats = Stats.NORMAL
        elif isinstance(value, (int, float)):
            self.value = str(value)
            self.stats = Stats.NORMAL
        else:
            raise TypeError("Number value must be str, int, float, or Number")

    # Operatoren: Berechnung über float, Rückgabe als Number mit String
    def _as_float(self):
        if self.stats == Stats.INFINITY:
            return float('inf')
        elif self.stats == Stats.NEGATIV_INFINITY:
            return float('-inf')
        elif self.stats == Stats.NOTANUMBER:
            return float('nan')
        else:
            return float(self.value)

    def __add__(self, other):
        if isinstance(other, Number):
            result = self._as_float() + other._as_float()
        else:
            result = self._as_float() + other
        return Number(str(result))

    def __sub__(self, other):
        if isinstance(other, Number):
            result = self._as_float() - other._as_float()
        else:
            result = self._as_float() - other
        return Number(str(result))

    def __mul__(self, other):
        if isinstance(other, Number):
            result = self._as_float() * other._as_float()
        else:
            result = self._as_float() * other
        return Number(str(result))

    def __truediv__(self, other):
        if isinstance(other, Number):
            result = self._as_float() / other._as_float()
        else:
            result = self._as_float() / other
        return Number(str(result))

    # String-Repräsentation
    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{round(self._as_float())}"

    # Vergleich
    def __eq__(self, other):
        return self._as_float() == (other._as_float() if isinstance(other, Number) else other)

    def __lt__(self, other):
        return self._as_float() < (other._as_float() if isinstance(other, Number) else other)

    def __le__(self, other):
        return self._as_float() <= (other._as_float() if isinstance(other, Number) else other)

    # Prüfen von Flags
    def is_infinite(self):
        return self.stats in (Stats.INFINITY, Stats.NEGATIV_INFINITY)

    def is_nan(self):
        return self.stats == Stats.NOTANUMBER
