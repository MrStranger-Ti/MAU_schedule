class ParserError(Exception):
    def __str__(self):
        return "Parser didn't find any data."
