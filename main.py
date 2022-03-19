from src.tokenizer import Tokenizer


def parse():
    with open("second.lox") as code_file:
        lines = code_file.readlines()
        tokenizer = Tokenizer(source="".join(lines))
        tokenizer._parse()


if __name__ == "__main__":
    parse()
