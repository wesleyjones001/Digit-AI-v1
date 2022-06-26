from common import preprocessing as pp


def check_input(data: str) -> float:
    test = pp.process(data)
    score = 0.0
    if "how are you" in test:
        score += 4
    if "what up" in test:
        score += 3
    if "good evening" in test:
        score += 3
    if "great day" in test:
        score += 3
    return score


def eval(data, memory):
    processed = pp.process(data)
    if "how are you" in processed:
        return "I'm great as always"
    if "what up" in processed:
        return "Not much. I was build to serve."
    if "great day" in processed:
        return "Yes. It is a great day."
