class RLE:
    """A Run Length Encoded file parser.

    https://conwaylife.com/wiki/Run_Length_Encoded
    """

    def __init__(self):
        self.width = None
        self.height = None
        self.rule = None
        self.comments = ""
        self.name = ""
        self.author = ""
        self.encoded = ""
        self.decoded = []

    def decode(self, text: str):
        for line in text.split("\n"):
            self.parse_line(line)

        return self.parse_pattern()

    def encode(self, array):
        # TODO
        return

    def parse_line(self, line: str):
        """Read lines of file and determine its type.

        Because the number of lines is variable, look at the first character
        per line to determine it's type.

        # is a comment
        x are the rules
        Everything else should be encoded pattern.
        """
        if line.startswith("#"):
            print(f"comment: {line}")
        elif line.startswith("x"):
            self.parse_rule_line(line)
        else:
            self.encoded += line

    def parse_rule_line(self, line: str):
        """Extracts rules by splitting after the ',' and '='.

        Rules commonly look like this:
        x = 12, y = 10
        But they can also have a 'rule' variable determining the game rules:
        x = 12, y = 10, rule = B3/S23
        """
        parts = line.split(",")

        x_parts = parts[0].split("=")
        self.width = int(x_parts[1].strip())

        y_parts = parts[1].split("=")
        self.height = int(y_parts[1].strip())

        # Third rule is not mandatory
        try:
            r_parts = parts[2].split("=")
            self.rule = r_parts[1].strip()
        except:
            pass

    def parse_pattern(self):
        result = []
        row = []
        multiplier = 1

        for char in self.encoded:
            if char == 'b':
                row.extend([0] * multiplier)
                multiplier = 1
            elif char == 'o':
                row.extend([1] * multiplier)
                multiplier = 1
            elif char == '$':
                row.extend([0] * (self.width - len(row)))
                if len(row) > self.width:
                    raise Exception("Line too long for pattern width.")
                result.append(row)
                row = []
            elif char.isdigit():
                if multiplier > 1:
                    multiplier = int(str(multiplier) + char)
                else:
                    multiplier = int(char)
            elif char == '!':
                result.append(row)
                break
        return result
