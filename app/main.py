import sys


# import pyparsing - available if you need it!
# import lark - available if you need it!

class Grep:
    def __init__(self, line:str, pattern: str) -> None:
        self.line = line
        self.pattern = pattern
    
    def match_alphanumeric(self) -> bool:
        return self.match_alphabetic() or self.match_digits() or "_" in self.line
    
    def match_alphabetic(self) -> bool:
        return any(True if ord(character) in range(97,97+26) else False for character in self.line.lower())
    
    def match_digits(self) -> bool:
        return any(character.isdigit() for character in self.line)
    
    def match_pattern(self) -> bool | RuntimeError:
        match self.pattern:
            case "\w":
                return self.match_alphanumeric()
            case "\d":
                return self.match_digits()
            case _:
                if len(self.pattern) ==1:
                    return self.pattern in self.line
                else:
                    raise RuntimeError(f"Unhandled pattern: {self.pattern}")


def main():
    grep = Grep(sys.stdin.read(), sys.argv[2])
    
    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    if grep.match_pattern():
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
