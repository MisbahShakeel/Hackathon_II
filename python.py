#!/usr/bin/env python3
"""
Interactive Python Script with Multiple Task Options

This script provides a menu-driven interface for users to choose which task they want to run.
"""

def task_1_hello_world():
    """Simple hello world task"""
    print("\n--- Hello World Task ---")
    print("Hello, World!")
    print("This is Task 1 running successfully!")
    input("\nPress Enter to continue...")


def task_2_calculator():
    """Simple calculator task"""
    print("\n--- Calculator Task ---")
    print("Simple Calculator")
    print("Operations: +, -, *, /")

    try:
        num1 = float(input("Enter first number: "))
        operator = input("Enter operator (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 != 0:
                result = num1 / num2
            else:
                print("Error: Division by zero!")
                return
        else:
            print("Invalid operator!")
            return

        print(f"Result: {num1} {operator} {num2} = {result}")
    except ValueError:
        print("Error: Please enter valid numbers!")

    input("\nPress Enter to continue...")


def task_3_number_guessing():
    """Number guessing game task"""
    import random

    print("\n--- Number Guessing Game ---")
    print("I'm thinking of a number between 1 and 100.")
    print("Try to guess it!")

    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess < secret_number:
                print("Too low! Try a higher number.")
            elif guess > secret_number:
                print("Too high! Try a lower number.")
            else:
                print(f"Congratulations! You guessed the number in {attempts} attempts!")
                break
        except ValueError:
            print("Please enter a valid number!")

    input("\nPress Enter to continue...")


def task_4_string_operations():
    """String manipulation task"""
    print("\n--- String Operations ---")
    text = input("Enter a string: ")

    print(f"\nOriginal string: '{text}'")
    print(f"Uppercase: '{text.upper()}'")
    print(f"Lowercase: '{text.lower()}'")
    print(f"Title case: '{text.title()}'")
    print(f"Reversed: '{text[::-1]}'")
    print(f"Word count: {len(text.split())}")
    print(f"Character count: {len(text)}")

    input("\nPress Enter to continue...")


def task_5_fibonacci():
    """Fibonacci sequence generator task"""
    print("\n--- Fibonacci Sequence Generator ---")
    try:
        n = int(input("Enter the number of terms to generate: "))
        if n <= 0:
            print("Please enter a positive number!")
            return

        print(f"Fibonacci sequence ({n} terms):")
        a, b = 0, 1
        for i in range(n):
            if i == 0:
                print(a, end=" ")
            elif i == 1:
                print(b, end=" ")
            else:
                c = a + b
                print(c, end=" ")
                a, b = b, c
        print()  # New line after sequence
    except ValueError:
        print("Please enter a valid number!")

    input("\nPress Enter to continue...")


def show_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("           PYTHON TASK MENU")
    print("="*50)
    print("Choose a task to run:")
    print("1. Hello World")
    print("2. Calculator")
    print("3. Number Guessing Game")
    print("4. String Operations")
    print("5. Fibonacci Sequence Generator")
    print("6. Exit")
    print("="*50)


def main():
    """Main function to run the menu-driven interface"""
    print("Welcome to the Interactive Python Task Runner!")

    # Dictionary mapping menu choices to functions
    tasks = {
        '1': task_1_hello_world,
        '2': task_2_calculator,
        '3': task_3_number_guessing,
        '4': task_4_string_operations,
        '5': task_5_fibonacci
    }

    while True:
        show_menu()
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice in tasks:
            tasks[choice]()
        elif choice == '6':
            print("\nThank you for using the Python Task Runner!")
            print("Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1 and 6.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()