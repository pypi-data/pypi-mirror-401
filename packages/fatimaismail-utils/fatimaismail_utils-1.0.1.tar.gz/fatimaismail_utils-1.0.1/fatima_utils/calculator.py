def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b if b != 0 else "Error: Division by zero"

def power(base, exponent):
    return base ** exponent

def percentage(part, whole):
    return (part / whole) * 100 if whole != 0 else 0

def average(numbers):
    return sum(numbers) / len(numbers) if numbers else 0