import json
import sys
from math import *

def input_content():
    global input_json
    input_str = sys.stdin.readline()
    if input_str[-1] == '\n':
        input_str = input_str[0:-1]
    input_json = json.loads(input_str)
    #print(input_json)

def calculate_one(operation, num_1, num_2):
    if operation == 'add':
        return num_1 + num_2
    elif operation == 'sub':
        return num_1 - num_2
    elif operation == 'mul':
        return num_1 * num_2
    else:
        return num_1 / num_2

def calculate_result(json_part):
    operation = json_part["op"]
    if operation == "value":
        return json_part["input"]
    
    json_1 = json_part["input"][0]
    json_2 = json_part["input"][1]
    num_1 = calculate_result(json_1)
    num_2 = calculate_result(json_2)
    return calculate_one(operation, num_1, num_2)


def main():
    input_content()
    result = calculate_result(input_json)
    result_real = "%.2f" % result
    sys.stdout.write(result_real)
if __name__ == '__main__':
    main()
