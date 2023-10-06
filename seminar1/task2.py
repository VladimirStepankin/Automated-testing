# Задание 2.


import subprocess
import string


def is_command_successful(command, text_to_find):
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, encoding='utf-8')

    translator = str.maketrans("", "", string.punctuation)
    output_words = result.stdout.translate(translator).split()
    print(output_words)
    return text_to_find in output_words


command_example_words = "echo 'Hello, world!'"
text_example_words = "world"
result_words = is_command_successful(command_example_words, text_example_words)

print(result_words)
