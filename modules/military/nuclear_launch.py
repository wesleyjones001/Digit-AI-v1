def check_input(data: str, memory: list) -> float:
    score = 0
    if "launch nuclear missiles" in data:
        score += 10
    return score


def eval(data: str, memory: list) -> object:
    if "launch nuclear missiles" in data:
        string = data[data.index("launch nuclear missiles") + len("launch nuclear missiles"):]
        return "Launching missiles at " + string.replace(" ", '')
    return None
