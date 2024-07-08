Issue 2: Fix Division by Zero Handling
Title: Bug Report: Incorrect Handling of Division by Zero in Calculator

Checked Other Resources:

I have checked the calculator project's documentation for any notes on division behavior.
I searched GitHub for similar bug reports and found none.
I confirmed that this issue persists in the latest version of the calculator project.
This issue represents a bug in the calculator's logic, not an error in my code.

Buggy Code:
class Calculator:
    def divide(self, a, b):
        return a / b  # Current implementation does not handle division by zero.

Error Message and Stack Trace (if applicable): No explicit error message since Python inherently throws a ZeroDivisionError when attempting to divide by zero. However, the calculator should gracefully handle this case and provide a user-friendly message or behavior.

Description: When attempting to divide by zero, the calculator should not rely on Python's default ZeroDivisionError. Instead, it should handle this case explicitly, either by returning a specific value (e.g., None or float('inf')) or by raising a custom error message that informs the user about the invalid operation. This change would improve the calculator's robustness and user experience.

System Info:

Calculator Project Version: 1.0.0
Python Version: 3.8
Operating System: Windows 10
