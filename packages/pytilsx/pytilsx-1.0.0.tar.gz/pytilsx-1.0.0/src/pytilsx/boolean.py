def xor(a:bool, b:bool):
    """Exclusive OR (XOR)"""
    return a != b

def nand(a:bool, b:bool):
    """AND-NOT (NAND)"""
    return not (a and b)

def nor(a:bool, b:bool):
    """OR-NOT (NOR)"""
    return not (a or b)

def xnor(a:bool, b:bool):
    """Exclusive OR-NOT (XNOR)"""
    return a == b

def all_true(*args):
    """Are all values True"""
    return all(args)

def any_true(*args):
    """At least one value True"""
    return any(args)

def majority(*args):
    """Most values are True"""
    return sum(args) > len(args) / 2

def exactly_n(n:bool, *args):
    """Exactly n values True"""
    return sum(args) == n

def to_bool(value):
    """Converting to bool with different types"""
    if isinstance(value, str):
        return value.lower() in ("true", "1", "on", "y")
    return bool(value)

def count_trues(*args):
    """Counting True values"""
    return sum(bool(x) for x in args)

def count_falses(*args):
    """Counting False values"""
    return sum(not bool(x) for x in args)