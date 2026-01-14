def add(a, b):
    return a + b
def subtract(a, b):
    return a - b
def multiply(a, b):
    return a * b
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b
def power(a, b):
    return a ** b
def modulus(a, b):
    return a % b
def floor_divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a // b
def square_root(a):
    if a < 0:
        raise ValueError("Cannot take square root of negative number.")
    return a ** 0.5
def percentage(a, b):
    return (a / 100) * b

def main():
    print("Calculator Module")
    print("Available operations: add, subtract, multiply, divide, power, modulus, floor_divide, square_root, percentage")
    while True:
        operation = input("Enter operation (or 'exit' to quit): ").strip().lower()
        if operation == 'exit':
            break
        try:
            if operation in ['add', 'subtract', 'multiply', 'divide', 'power', 'modulus', 'floor_divide', 'percentage']:
                a = float(input("Enter first number: "))
                b = float(input("Enter second number: "))
                if operation == 'add':
                    print("Result:", add(a, b))
                elif operation == 'subtract':
                    print("Result:", subtract(a, b))
                elif operation == 'multiply':
                    print("Result:", multiply(a, b))
                elif operation == 'divide':
                    print("Result:", divide(a, b))
                elif operation == 'power':
                    print("Result:", power(a, b))
                elif operation == 'modulus':
                    print("Result:", modulus(a, b))
                elif operation == 'floor_divide':
                    print("Result:", floor_divide(a, b))
                elif operation == 'percentage':
                    print("Result:", percentage(a, b))
            elif operation == 'square_root':
                a = float(input("Enter number: "))
                print("Result:", square_root(a))
            else:
                print("Invalid operation.")
        except ValueError as e:
            print("Error:", e)
if __name__ == "__main__":
    main()