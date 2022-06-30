from common import module_testing

module_version = "v1.0.0"


def check_input(data: str, memory: list) -> float:
    score = 0
    if "launch nuclear missiles" in data:
        score += 10
    return score


def eval(data: str, memory: list) -> object:
    if "launch nuclear missiles" in data:
        string = data[data.index("launch nuclear missiles") + len("launch nuclear missiles"):]
        if "code" in string:
            string = "using code " + string[string.index("code") + 4:].split()[0].lower()

        return "Launching missiles " + string
    return None


if __name__ == "__main__":
    module_testing.run_module(check_score_func=check_input, eval_module_func=eval)
