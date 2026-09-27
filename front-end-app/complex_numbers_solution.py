class comp:
    def __init__(self, real, imaginary):
        self.real = real
        self.imaginary = imaginary

    def _format_complex(self, real, imaginary):
        if imaginary >= 0:
            return f"{real}+{imaginary}i"
        return f"{real}{imaginary}i"

    def add(self, other):
        sum_real = self.real + other.real
        sum_imaginary = self.imaginary + other.imaginary
        print(f"Sum of the two Complex numbers :{self._format_complex(sum_real, sum_imaginary)}")

    def sub(self, other):
        diff_real = self.real - other.real
        diff_imaginary = self.imaginary - other.imaginary
        print(f"Subtraction of the two Complex numbers :{self._format_complex(diff_real, diff_imaginary)}")
