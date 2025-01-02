import os
import assignment1 as a
import re
import tempfile

test_path = 'GA1_test_cases 2'
temp_path = 'text.txt'

inputs = []

for file in os.listdir(test_path):
    if re.fullmatch('input[0-9]+.txt', file):
        inputs.append(file)

outputs = ['output' + input[5:] for input in inputs]

for input, output in zip(inputs, outputs):
    a.min_num_attendees(os.path.join(test_path, input), temp_path)

    with open(os.path.join(test_path, output)) as output_file, open(temp_path) as temp_file:
        print('\033[92m' if output_file.read() == temp_file.read() else f'\033[91m', end='')
        print(input, end='')
        print('\033[0m')

if os.path.exists(temp_path):
    os.remove(temp_path)
