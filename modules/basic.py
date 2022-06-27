def check_input(data: str, memory: list) -> float:
    score = 0
    if data == "":
        score = 10
    return score


def eval(data: str, memory: list) -> object:
    if data == "":
        return ""
