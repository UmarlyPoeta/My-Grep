import sys


# import pyparsing - available if you need it!
# import lark - available if you need it!

class Grep:
    def __init__(self, line: str, pattern: str) -> None:
        self.line = line
        self.pattern = pattern

    def match_alphanumeric(self, character: chr) -> bool:
        return self.match_alphabetic(character) or self.match_digits(character) or "_" == character

    @staticmethod
    def match_alphabetic(character: chr) -> bool:
        return ord(character) in range(97, 97+26)

    @staticmethod
    def match_digits(character: chr) -> bool:
        return character.isdigit()

    @staticmethod
    def match_groups(character: chr, group_characters: str, is_negative: bool = False) -> object:
        return character not in group_characters if is_negative else character in group_characters

    def brackets_valid(self) -> bool:
        try:
            if "]" in self.pattern and self.pattern.index("]") > self.pattern.index("["):
                return True
        except ValueError:
            return False

    def check_if_found(self) -> bool:
        line_pointer = 0
        pattern_pointer = 0

        found = False
        if self.pattern[pattern_pointer] == "^":
            if not self.pattern[pattern_pointer + 1] == self.line[line_pointer]:
                return False
            else:
                pattern_pointer += 1
        
        while line_pointer < len(self.line) and pattern_pointer < len(self.pattern):
            match self.pattern[pattern_pointer]:
                case "\\":
                    pattern_pointer += 1
                    if self.pattern[pattern_pointer] == "w":
                        found = self.match_alphanumeric(self.line[line_pointer])
                    elif self.pattern[pattern_pointer] == "d":
                        found = self.match_digits(self.line[line_pointer])
                    else:
                        return False
                case "[":
                    if self.brackets_valid():
                        if self.pattern[pattern_pointer + 1] == "^":
                            extracted_characters = self.pattern[pattern_pointer+2:self.pattern[pattern_pointer:].index("]")]
                            found = self.match_groups(self.line[line_pointer], extracted_characters, True)
                        else:
                            extracted_characters = self.pattern[pattern_pointer+1:self.pattern[pattern_pointer:].index("]")]
                            found = self.match_groups(self.line[line_pointer], extracted_characters)
                        if self.pattern[pattern_pointer:].index("]") + 1 < len(self.pattern):
                            pattern_pointer = self.line[line_pointer:].index("]") + 1
                        else:
                            line_pointer += 1
                            continue
                case _:
                    try:
                        if self.pattern[pattern_pointer + 1 ] == "+":
                            is_found = False
                            while self.line[line_pointer] == self.pattern[pattern_pointer]:
                                line_pointer += 1
                                found = True
                                is_found = True
                            if not is_found:
                                pattern_pointer = 0
                            
                            pattern_pointer += 2
                    except IndexError:
                        pass
                    
                    try:
                        if self.pattern[pattern_pointer + 1 ] == "?":
                            if self.line[line_pointer] == self.pattern[pattern_pointer]:
                                line_pointer += 1
                                found = True
                            pattern_pointer += 2
                    except IndexError:
                        pass
                    found = self.line[line_pointer] == self.pattern[pattern_pointer]
                    if pattern_pointer + 1 == len(self.pattern) - 1 and self.pattern[pattern_pointer + 1] == "$":
                        if line_pointer == len(self.line) - 1:
                            return True
                        else:
                            return False
            line_pointer += 1
            if found:
                pattern_pointer += 1
            else:
                pattern_pointer = 0

            if line_pointer >= len(self.line) and pattern_pointer < len(self.pattern):
                return False

            if pattern_pointer == len(self.pattern) - 1:
                break
        return found


def main():
    grep = Grep(sys.stdin.read(), sys.argv[2])
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if grep.check_if_found():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
