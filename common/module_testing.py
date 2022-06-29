import time


class CommandExecutionResult:
    def __init__(self, data: object, result: object):
        # May add more fields later as needed
        self.data = data
        self.exe_time = round(time.time())
        if result is not None:
            self.result = result
        else:
            self.result = None


def run_module(check_score_func, eval_module_func, client_command_history: list = []):
    print("Initializing module test.")
    print()
    while True:
        input_string = input("Input: ")

        print("Score: ", check_score_func(input_string, client_command_history))

        result = eval_module_func(input_string, client_command_history)
        print("Result: ", result)
        client_command_history.append(CommandExecutionResult(input_string, result))
