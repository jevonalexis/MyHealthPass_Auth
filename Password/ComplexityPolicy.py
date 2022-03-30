class ComplexityPolicy:
    min_length: int
    max_length: int
    lowercase_needed: bool
    uppercase_needed: bool
    number_needed: bool
    special_characters: str

    def __init__(self, min_length: int, max_length: int, lowercase_needed: bool, uppercase_needed: bool,
                 number_needed: bool, special_characters: str = None):
        self.min_length = min_length
        self.max_length = max_length
        self.lowercase_needed = lowercase_needed
        self.uppercase_needed = uppercase_needed
        self.number_needed = number_needed
        self.special_characters = special_characters

    __repr__ = __str__ = lambda self: f"({self.min_length}-{self.max_length} characters\n" \
                                      f"Lowercase: {'required' if self.lowercase_needed else 'not required'}\n" \
                                      f"Uppercase: {'required' if self.uppercase_needed else 'not required'}\n" \
                                      f"Number: {'required' if self.number_needed else 'not required'}\n" \
                                      f"Special character: {'required' if self.special_characters else 'not required'})"
