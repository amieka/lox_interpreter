from src.tokenizer import Tokenizer


def parse():
    with open("./data/second.lox") as code_file:
        lines = code_file.readlines()
        tokenizer = Tokenizer(source="".join(lines))
        tokenizer.parse()


if __name__ == "__main__":
    parse()
