"""COGL File Parser
"""
import csv as csv_


class CSV:
    """A pretty basic CSV parser.

    Has no other attributes except for the array.
    """

    def encode(array, delim=',') -> str:
        """Saves the array into a CSV string.

        :param list array: The array to be encoded.
        :param string delim: The delimiter of the CSV string.
        :return: Encoded CSV string.
        :rtype: str
        """
        result = ""
        try:
            for row in array:
                for x in row:
                    result += str(x) + delim
                result += "\n"
            return result
        except Exception as e:
            print("Couldn't encode string.", e)
            return None

    def decode(string: str) -> list:
        """Loads the Grid from a CSV string.

        :param str string: The string to be decoded.
        :return: The decoded array.
        :rtype: array
        """
        reader = csv_.reader(string.split('\n'), delimiter=',')
        result = []
        row = []

        try:
            for row_ in reader:
                for x in row_:
                    if x == "1" or x == "0":
                        row.append(int(x))
                if len(row) != 0:
                    result.append(row)
                    row = []
            return result
        except Exception as e:
            print("Couldn't decode string.", e)
            return None


class RLE:
    """A Run Length Encoded file parser.

    https://conwaylife.com/wiki/Run_Length_Encoded
    """

    def encode(array, name: str, author: str = "", comments: str = "", rule="B3/S23"):
        print(array)
        parser = RLE(len(array), len(array[0]), rule, name, author, comments)

        # Add the header rows
        parser.encode_header()

        # Add the rules
        parser.encode_rules()

        # Encode and add the pattern string
        parser.encode_pattern(array)

        return parser

    def decode(text: str):
        parser = RLE()

        # Parse the file line by line
        for line in text.split("\n"):
            parser.decode_line(line)

        # Decode the extracted pattern string
        parser.decode_pattern()

        return parser

    def __init__(self, w: int = 0, h: int = 0, r: str = "", n: str = "", a: str = "", c: str = "", e: str = "", d: list = []):
        self.width = w
        self.height = h
        self.rule = r
        self.name = n
        self.author = a
        self.comments = c
        self.encoded = e
        self.decoded = d

    def encode_header(self) -> None:
        """Converts data into header lines and writes them into self.encoded.
        """
        if self.name != "":
            self.encoded = "#N " + self.name
        if self.author != "":
            self.encoded += "\n" + "#O " + self.author
        if self.comments != "":
            lines = self.comments.split("\n")
            for line in lines:
                self.encoded += "\n" + "#C " + line

    def encode_rules(self) -> None:
        """Converts data into the rules and writes them into self.encoded.
        """
        self.encoded += "\n" + "x = " + str(self.width) + ", y = " + str(self.height)
        if self.rule != "":
            self.encoded += ", rule = " + self.rule

    def encode_pattern(self, array) -> None:
        """Converts the array into an encoded string and writes it into self.encoded.
        """
        result = ""
        last_value = None
        count = 0
        for row in array:
            for value in row:
                # If the value is the same as the last value, increment the count
                if value == last_value:
                    count += 1
                # If the value is different from the last value, append the count and value to the result string
                # and reset the count and last_value variables
                else:
                    if count > 1:
                        result += str(count)
                    if last_value is not None:
                        if last_value:
                            result += "o"
                        else:
                            result += "b"
                    count = 1
                    last_value = value
            # If the last value was a 1, append the final count and value to the result string
            if last_value == 1:
                if count > 1:
                    result += str(count)
                result += "o"
            result += "$"
            count = 0
            last_value = None
        # Remove the last $
        result = result[:-1] + "!"

        # Line breaks after 70 chars
        for x in range(len(result)):
            if not x % 70 and x != 0:
                result = result[:(x + int(x / 71))] + "\n" + result[(x + int(x / 71)):]

        self.encoded += "\n" + result

    def decode_line(self, line: str) -> None:
        """Read lines of file and determine its type.

        Because the number of lines is variable, look at the first character
        per line to determine it's type.

        # is a header
        x are the rules
        Everything else should be the encoded pattern.
        """
        if line.startswith("#"):
            self.decode_header(line)
        elif line.startswith("x"):
            self.decode_rule(line)
        else:
            self.encoded += line

    def decode_header(self, line: str) -> None:
        """Converts the header lines into data.

        Header lines start with # and are followed by one of the following characters:
        C: Is a comment
        O: The author
        N: Name of the pattern
        """
        if line[1:].startswith("C"):
            self.comments += line[2:] + "\n"
        elif line[1:].startswith("O"):
            self.author = line[2:]
        elif line[1:].startswith("N"):
            self.name = line[2:]
        else:
            raise Exception("Unknown header,")

    def decode_rule(self, line: str) -> None:
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

    def decode_pattern(self) -> None:
        """Decodes the pattern string and write the array into self.decoded.

        The rules are as follows:
        b = Dead cell
        o = Alive cell
        $ = New row
        ! = End of string
        Any number in front of b or o is a multiplier. (So 2b is [0, 0].)
        Dead cells at the end of a row can be omitted.
        """
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
        self.decoded = result
