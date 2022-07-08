from common import module_testing

module_version = "v1.0.1"


def check_input(data: str, memory: list) -> float:
    score = 0
    if "launch" in data and "missile" in data:
        score += 10
    if len(memory) > 0 and "<<MODULE_QUESTION_NUCLEAR_LAUNCH_ASK_1>>" in memory[-1].result:
        score += 10
    return score


def eval(data: str, memory: list) -> object:
    if len(memory) > 0 and memory[-1].result is not None and "<<MODULE_QUESTION_NUCLEAR_LAUNCH_ASK_1>>" in memory[-1].result:
        target = None
        if data.strip() == "":
            return "Invalid target. Launch aborted."
        if "target" in data:
            target = data[data.index("target"):len("target")]
        elif " at " in data:
            target = data[data.index(" at "):len(" at ")]
        else:
            target = data.strip()
        return "Launching missiles at " + target
    elif "launch" in data and "missiles" in data:
        string = data[data.index("missiles") + len("missiles"):].strip()
        if string == "":
            return "Who are we targeting? <<MODULE_QUESTION_NUCLEAR_LAUNCH_ASK_1>>"
        if "code" in string:
            string = "using code " + string[string.index("code") + 4:].split()[0].lower()

        return "Launching missiles " + string
    elif "launch" in data and "missile" in data:
        string = data[data.index("missile") + len("missile"):].strip()
        if string == "":
            return "Who are we targeting? <<MODULE_QUESTION_NUCLEAR_LAUNCH_ASK_1>>"
        if "code" in string:
            string = "using code " + string[string.index("code") + 4:].split()[0].lower()

        return "Launching missiles " + string

    return None


if __name__ == "__main__":
    module_testing.run_module(check_score_func=check_input, eval_module_func=eval)
