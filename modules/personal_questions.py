from common import preprocessing as pp


def check_input(data: str, memory: list) -> float:
    test = pp.process(data)
    score = 0.0
    if "what is your" in test:
        score += 6
    if "what is your favorite" in test:
        score += 6
    if "would you" in test:
        score += 2.5
    if "is your" in test:
        score += 1
    if "will you" in test:
        score += 1
    return score


def eval(data, memory) -> object:
    return "Personal questions coming soon!"
