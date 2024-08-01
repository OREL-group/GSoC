from langchain.output_parsers import RegexParser


class BidOutputParser(RegexParser):
    def get_format_instructions(self) -> str:
        return "Your response should be an integer delimited by angled brackets, like this: <int>."


class QualityRatingParser(RegexParser):
    def get_format_instructions(self) -> str:
        return "Your response should be an integer between 1 and 5, delimited by angled brackets, like this: <int>."
