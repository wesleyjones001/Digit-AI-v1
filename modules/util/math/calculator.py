import builtins

from common import preprocessing
from common import module_testing

module_version = "v1.0.0"


def translate_to_math(input: str):
    new_data = input.replace(" plus ", " + ").replace(" times ", " * ").replace(" multiplied by ", " * ").replace(
        " divided by ", " / ").replace(" minus ", " - ").replace(" subtracted by ", " - ").replace("what is ",
                                                                                                   "").replace(
        "calculate ", "").replace("compute ", "").replace(".", "").replace("import", "").replace("_", "")

    return new_data


def check_input(data: str, memory: list) -> float:
    symbols = ["+", "-", "/", "*"]
    score = 0
    if "what is " in data:
        score = 3
    for s in symbols:
        if s in data:
            score += 1
    if "compute" in data:
        score += 3
    if "calculate" in data:
        score += 2
    return score


def eval(data: str, memory: list) -> str:
    processed_data = translate_to_math(data)
    try:
        output = builtins.eval(processed_data)
        return "The answer is " + str(output)
    except ZeroDivisionError:
        return "Can not divide by zero"
    except Exception as ex:
        return str(ex)


if __name__ == "__main__":
    module_testing.run_module(check_score_func=check_input, eval_module_func=eval)
