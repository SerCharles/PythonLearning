import sys
from math import *

def input_int():
    global number_list
    number_content = sys.stdin.readline()
    number_list = []
    number_list = number_content.split(' ')
    for i in range(len(number_list)):
        number_list[i] = int(number_list[i])
        #print(number_list[i])
def sort_int():
    length = len(number_list)
    for i in range(length):
        for j in range(i):
            if number_list[i] < number_list[j]:
                temp = number_list[i]
                number_list[i] = number_list[j]
                number_list[j] = temp

def main():
    input_int()
    sort_int()
    length = len(number_list)
    for i in range(length):
        sys.stdout.write(str(number_list[i]))
        if i != length - 1:
            sys.stdout.write(' ')

if __name__ == '__main__':
    main()

        