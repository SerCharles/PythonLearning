import random
import sys
from math import floor

#生成一个1-100间随机数
def get_random_number():
    random_number = random.random()
    random_number *= 100
    secret_number = floor(random_number) + 1
    return secret_number

#判断输入的数字与随机数的大小关系.如果matched就返回true,否则返回false
def judge_num(secret_num, guess_num):
    if guess_num < secret_num:
        sys.stdout.write('smaller\n')
        return False
    elif guess_num > secret_num:
        sys.stdout.write('bigger\n')
        return False
    else:
        sys.stdout.write('matched\n')
        return True

#读入一个数,如果合法,返回数本身,否则返回-1
def input_num():
    input_content = sys.stdin.readline().strip('\n')
    #排除非数字,小数负数等,还有0开头数字情况
    if input_content.isdigit() == False:
        return -1
    elif input_content[0] == '0':
        return -1
    #判断数字大小
    try:
        input_number = int(input_content)
    except:
        return -1
    if input_number < 1 or input_number > 100:
        return -1
    else:
        return input_number

def main():
    secret_number = get_random_number()
    while True:
        current = input_num()
        if current == -1:
            sys.stderr.write('Error: Invalid number, you have to input an integer between 1 and 100\n')
            break
        else:
            whether_success = judge_num(secret_number, current)
            if whether_success:
                break
if __name__ == '__main__':
    main()


