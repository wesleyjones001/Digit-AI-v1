# Greetings module v1.0.0
# The module enables basic greetings for the AI.

from common import preprocessing as pp
import random

module_version = "v1.0.0"


def check_input(data: str, memory: list) -> float:
    test = pp.process(data)
    score = 0.0
    if "hello" == test or "hey" == test:
        score += 10
    if "how are you" in test:
        score += 4
    if "what up" in test:
        score += 2
    if "whats up with you" in test:
        score += 3
    if "how is your day" in test:
        score += 6
    if "good morning" in test:
        score += 7
    if "good afternoon" in test:
        score += 7
    if "good evening" in test:
        score += 7
    if "great morning" in test:
        score += 5
    if "great afternoon" in test:
        score += 5
    if "great evening" in test:
        score += 5
    if "nice to see you" in test:
        score += 5
    if "long time no see" in test:
        score += 6
    return score


responses = [["I'm great as always", "I am doing well. How about you?",
              "Well, today I feel like I accomplished something. <<REACT_SMILE>>", "I am happy.",
              "I feel like I am learning new things."],
             ["Not much is going on. I was build to serve. <<REACT__SMILE>>", "I am happy to be here for you.",
              "The sky is up. <<REACT_LAUGH>>"],
             ["Yes. It is a great day.", "Today is great.", "Today is good, but not as great as yesterday!",
              "Indeed. Keep up the positivity."],
             ["Good morning.", "Good morning Sir.<<REACT__SALUTE>>", "Have a nice day."],
             ["Good afternoon.", "It's a great day. Keep it going. <<REACT_SMILE>>",
              "It's been good so far, keep it up! <<REACT_CHEER>>"],
             ["Good evening.", "This was a nice day.", "We did good. What are we doing tomorrow? <<REACT_SHRUG>>"],
             ["Nice to see you to! <<REACT_WAVE>>", "We are all a happy family. <<REACT_SMILE>>",
              "Nice to see you to. I missed you. <<REACT_HUG>>"],
             ["Hello.", "Howdy.", "Hello Sir. <<REACT_SALUTE>>", "Good day.", "Hello master."]]


def eval(data, memory) -> object:
    processed = pp.process(data)
    if "how are you" in processed:
        return random.choice(responses[0])
    if "what up" in processed:
        return random.choice(responses[1])
    if "great day" in processed:
        return random.choice(responses[2])
    if "good morning" in processed:
        return random.choice(responses[3])
    if "good afternoon" in processed:
        return random.choice(responses[4])
    if "good evening" in processed:
        return random.choice(responses[5])
    if "great morning" in processed:
        return random.choice(responses[3])
    if "great afternoon" in processed:
        return random.choice(responses[4])
    if "great evening" in processed:
        return random.choice(responses[5])
    if "nice to see you" in processed:
        return random.choice(responses[6])
    if "long time no see" in processed:
        return random.choice(responses[6])
    if "hello" == processed or "hey" == processed:
        return random.choice(responses[7])
    return None
