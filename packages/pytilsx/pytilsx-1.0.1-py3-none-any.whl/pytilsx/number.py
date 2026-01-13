class calc:
    def __init__(self, example:str):
        """
        Calculates an example
        There are only: + - * / ^
        
        Example:
            calculator = calc("5+3")
            calculator.ignorerrors = False
            result = calculator.Calculate()
            print(result)
        Output:
            8
        """
        self.parsed = self.Parse(example)
        self.ignorerrors = False
        self.example = example

    def Plus(self, a:float, b:float):
        return a + b

    def Minus(self, a:float, b:float):
        return a - b

    def Multiply(self, a:float, b:float):
        return a * b

    def Divide(self, a:float, b:float):
        return a / b
    
    def Degree(self, a:float, b:float):
        abs_exponent = absnum(b)
        result = 1
        current = a
        while abs_exponent > 0:
            if abs_exponent % 2 == 1:
                result *= current
            current *= current
            abs_exponent //= 2
        return 1 / result if b < 0 else result
    
    def Parse(self, text):
        unletters = []
        letters = []
        skip = 0
        digits = "0123456789"

        for letter in text:
            unletters.append(letter)

        for index, letter in enumerate(unletters):
            if skip > 0:
                skip -= 1
                continue

            if letter == "+":
                letters.append("plus")
            elif letter == "-" and (index == 0 or unletters[index-1] in "+-*/^("):
                number = "-"
                nindex = index + 1
                while nindex < len(unletters) and unletters[nindex] in digits:
                    number += unletters[nindex]
                    nindex += 1
                letters.append(number)
                skip = nindex - index - 1
            elif letter == "-":
                letters.append("minus")
            elif letter == "*":
                letters.append("mult")
            elif letter == "^":
                letters.append("degr")
            elif letter == "/":
                letters.append("div")
            elif letter in digits:
                number = letter
                nindex = index + 1
                while nindex < len(unletters) and (unletters[nindex] in digits or unletters[nindex] == "."):
                    number += unletters[nindex]
                    nindex += 1
                letters.append(number)
                skip = nindex - index - 1
            elif letter == ".":
                number = "0."
                nindex = index + 1
                while nindex < len(unletters) and unletters[nindex] in digits:
                    number += unletters[nindex]
                    nindex += 1
                letters.append(number)
                skip = nindex - index - 1
            elif letter == "(":
                letters.append("lbr")
            elif letter == ")":
                letters.append("rbr")

        return letters

    def Interpretter(self, letters:list):
        tokens = letters.copy()

        while "lbr" in tokens:
            start = tokens.index("lbr")
            count = 1
            end = start

            for i in range(start + 1, len(tokens)):
                if tokens[i] == "lbr": count += 1
                elif tokens[i] == "rbr":
                    count -= 1
                    if count == 0:
                        end = i
                        break

            inner = tokens[start + 1:end]
            result = self.Interpretter(inner)
            tokens[start:end + 1] = [str(result)]

        op_groups = [["degr"], ["mult", "div"], ["plus", "minus"]]

        for ops in op_groups:
            i = 0
            while i < len(tokens):
                if tokens[i] in ops:
                    try:
                        a = float(tokens[i-1])
                        b = float(tokens[i+1])

                        if tokens[i] == "degr":
                            res = self.Degree(a, b)
                        elif tokens[i] == "mult":
                            res = self.Multiply(a, b)
                        elif tokens[i] == "div":
                            res = self.Divide(a, b)
                        elif tokens[i] == "plus":
                            res = self.Plus(a, b)
                        elif tokens[i] == "minus":
                            res = self.Minus(a, b)

                        tokens[i-1:i+2] = [str(res)]
                        i = 0
                    except Exception as ex:
                        i += 1
                        if not self.example == "":
                            if not self.ignorerrors:
                                raise ex
                else:
                    i += 1

        return tokens[0]

    def Calculate(self):
        num = float(self.Interpretter(self.Parse(self.example)))
        if num == int(num):
            return str(int(num))
        else:
            return str(num)

def maxnum(value:int | float, maximum:int | float):
    """The number is limited to a maximum value"""
    if value > maximum:
        value = maximum
    return value

def minnum(value:int | float, minimum:int | float):
    """The number is set to a minimum limit"""
    if value < minimum:
        value = minimum
    return value

def absnum(value:int | float):
    """The number becomes positive"""
    return value * 1

def clamp(value: int | float, minimum: int | float, maximum: int | float):
    """Limits the value to the specified minimum and maximum"""
    return minnum(maxnum(value, maximum), minimum)

def lerp(a:int | float, b:int | float, t):
    return a + (b - a) * t

def map_range(value:int | float, from_min:int | float, from_max:int | float, to_min:int | float, to_max:int | float):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min

def iteration(start_value:int | float, example:str, iters:int):
    """
    Repeats the operation with the value several times

    Example:
        print(iteration(5, "+1", 10))
    Output:
        15
    """
    current = start_value
    for _ in range(iters):
        expression = f"{current}{example}"
        current = float(calc(expression).Calculate())
    return current

def pingpong(value:int | float, minimal:int | float, maximum:int | float, step:int | float = 1):
    """
    Movement of a number between min and max with bounces
    
    Example:
        for i in range(10):
            print(pingpong(i, 0, 3))
    Output:
        0, 1, 2, 3, 2, 1, 0, 1, 2, 3
    """
    range_size = maximum - minimal
    if range_size == 0:
        return minimal
    
    cycle_length = range_size * 2
    normalized = (value * step) % cycle_length
    
    if normalized <= range_size:
        result = minimal + normalized
    else:
        result = maximum - (normalized - range_size)
    
    return result

def average(values:list | tuple):
    """Shows the arithmetic mean"""
    if not values:raise ValueError("Values is empty")
    folded = 0
    for value in values:folded += value
    return folded / len(values)

def median(values:list | tuple):
    """It's almost like the arithmetic mean, but it takes a list and sorts it. If the list is even, it takes two values in the middle and divides them by two. If the list is odd, it takes only the central value."""
    if not values:raise ValueError("Values is empty")
    sorted_values = sorted(values)
    if len(sorted_values) % 2:
        return sorted_values[int(len(sorted_values) / 2)]
    else:
        return (sorted_values[int(len(sorted_values) / 2 + 0.5)] + sorted_values[int(len(sorted_values) / 2 - 0.5)]) / 2