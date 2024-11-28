class ParameterValidator:
    """Validates user input for fractal flame parameters"""

    @staticmethod
    def get_positive_int(prompt: str, error_message: str) -> int:
        """Prompt user for a positive integer with validation"""
        while True:
            try:
                value = int(input(prompt))
                if value > 0:
                    return value
                else:
                    print(error_message)
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

    @staticmethod
    def get_float(prompt: str) -> float:
        """Prompt user for a floating-point number with validation"""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("Invalid input. Please enter a valid floating-point number.")
