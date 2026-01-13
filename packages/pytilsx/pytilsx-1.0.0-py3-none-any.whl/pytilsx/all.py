def invert(value:int | float | bool):
    """
    Inverts the value

    True -> False
    False -> True
    -5 -> 5
    5 -> -5

    Example:
        print(invert(False))
    Output:
        True
    """
    if isinstance(value, bool):
        if value == False:return True
        elif value == True:return False
    elif isinstance(value, int) or isinstance(value, float):
        return value * -1

def bool_to_int(value:bool):
    """Bool to int (True=1, False=0)"""
    return 1 if value else 0

def int_to_bool(value):
    """Int to bool (0=False, else=True)"""
    return bool(value)