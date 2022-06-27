# Welcome to Digit

# Table of contents
1. [What is a digit module](#what-is-a-digit-module)
2. [How to include a module](#how-to-include-a-module)

## What is a digit module
A digit module is a component that adds a specific functionality. For example, if I wanted to create a feature that enables Digit to turn on the lights then you would use a module.
A module consists of two main functions. The first is a ```py
check_score(command:str, client_command_history:list)```. This second is ```py eval(command:str, client_command_history:list)```.
This first function `check_score()` is called on every command input to check if the module pertains to that command. It outputs a float to indicate how likely that module should be used. The module with the highest score output for each command is teh one that will be used.

The next function is the `eval()` function. It is the most important part of the module. It is like to main function of a normal program. The `eval()` function is used to execute the module with the input command and command history.

Together these to component functions allow a module to be selected and used to process input.
There is no limit to how many modules can be used! The more modules used, the more functions Digit will have.

This is a basic module template:
```py
# basic check_score function
def check_score(command:str, client_command_history:list) -> float:
    score = 0
    if "hello server" in command:
        score += 5
    return score

# basic eval function
def eval(command:str, client_command_history:list) -> object:
    if "hello server" in command:
        return "Hello, my name is Digit. I am a friendly chatbot."
    return None
```

## How to include a module
It is super easy to include a module. Just copy it to the `modules` folder in the Digit directory. Digit will handel the rest.

