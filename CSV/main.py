import csv
import sys
import os
import random
from math import *

#生成一个a，b间随机数(<=a, < b)
def get_random_number(a, b):
    random_number = random.random()
    random_number *= (b - a)
    secret_number = floor(random_number) + a
    return secret_number


#判断一个数是不是实数,排除无穷与nan情况,如果正确就返回true,否则返回false,参考了这个文章https://blog.csdn.net/zc_stats/article/details/87779335
def judge_float(x):
    try:
        float(x)
        #if str(x) in ['inf', 'infinity', 'INF', 'INFINITY', 'True', 'NAN', 'nan', 'False', '-inf', '-INF', '-INFINITY', '-infinity', 'NaN', 'Nan']:
        if isnan(float(x)) == True or isinf(float(x)) == True:
            return False
        else:
            return True
    except:
        return False

#判断一个csv是否合法
def judge_whether_valid(content_list, title):
    number = len(content_list)
    length = len(title)
    whether_repeat = False
    #先判断标题重复性
    for i in range(length):
        for j in range(i):
            if title[i] == title[j]:
                whether_repeat = True
    if whether_repeat == True:
        return False
    #再判断有没有行数不等
    for i in range(number):
        if len(content_list[i]) != length:
            return False
    return True
            

#读取命令行参数,存储到四个全局变量里(输入文件,输出文件,字段,排序类型)并且判断命令行是否合法,合法返回true,否则false
def get_variables():
    args = sys.argv[1:]
    global input_filename
    global output_filename
    global factor
    global sort_type
    input_filename = args[0]
    output_filename = args[-1]
    factor = None
    sort_type = True
    length = len(args)
    if length == 3:
        factor = args[1]
    elif length == 4:
        factor = args[1]
        if args[2] == 'DESC':
            sort_type = False
        else:
            sys.stderr.write('Error: invalid sort type, must be DESC!\n')
            return False
    elif length == 2:
        pass
    else:
        sys.stderr.write('Error: invalid input!\n')
    #测试
    #print(input_filename, output_filename, factor, sort_type)
    return True


#读取csv,判断文件是否能打开,并且存储到全局变量里.能打开返回True,否则返回False,参考了这个https://www.cnblogs.com/yanglang/p/7126660.html
def input_csv():
    global title
    global content
    content = []
    title = None
    try:
        f = open(input_filename, 'r', encoding = 'utf-8')
    except IOError:
        sys.stderr.write('Error: cannot open the file\n')
        return False
    content_list_raw = f.readlines()
    for i in range(len(content_list_raw)):
        if i == 0:
            title = content_list_raw[i].split(',')
        else:
            content.append(content_list_raw[i].split(','))

    if title == None:
        return True
    else:
        #删除最后一个\n
        if title[-1][-1] == '\n':
            title[-1] = title[-1][0 : -1]
        for item in content:
            if item[-1][-1] == '\n':
                item[-1] = item[-1][0 : -1]
        #测试
        #print(title)
        #print(content)
        #判断是否合法
        if judge_whether_valid(content, title) == False:
            sys.stderr.write('Error: invalid CSV file\n')
            return False
        else:
            return True
    


#遍历csv待排序的位置,删除不能排序的行.如果排序位置找不到,返回False,否则返回True
def initialize_data():
    global sort_place
    sort_place = None
    #没有排序操作,直接复制粘贴就好了
    if factor == None:
        return True
    #有排序操作,需要在title里找字段
    if title == None:
        sys.stderr.write('Error: cannot operate the file\n')
        return False
    title_length = len(title)
    for i in range(title_length):
        if title[i] == factor:
            sort_place = i
            break
    #不能输出:报错
    if sort_place == None:
        sys.stderr.write('Error: cannot operate the file\n')
        return False
    #清理列表,必须反向遍历
    content_length = len(content)
    for i in range(content_length - 1, -1, -1):
        if judge_float(content[i][sort_place]) == False:
            del content[i]
        #else:
            #content[i][sort_place] = float(content[i][sort_place])
    #测试
    #print(sort_place, content)
    return True


#升序下,a<b输出-1,=输出0,>输出1.降序相反
def compare(element_a, element_b):
    if float(element_a[sort_place]) == float(element_b[sort_place]):
        return 0
    elif float(element_a[sort_place]) < float(element_b[sort_place]):
        if sort_type == True:
            return -1
        else:
            return 1
    else:
        if sort_type == True:
            return 1
        else:
            return -1

#交换i与j
def swap(the_list, i, j):
    if i == j:
        return
    temp = the_list[i][ : ]
    the_list[i] = the_list[j][ : ]
    the_list[j] = temp[ : ]


#一轮快排,start是头,end是尾+1
def divide(the_list, start, end):
    length = end - start
    #长度不够:直接返回
    if length <= 1:
        return -1
    #随机快排
    criterion_number = get_random_number(start, end)
    swap(the_list, criterion_number, end - 1)
    
    criterion = the_list[end - 1]
    small_border = start - 1
    for i in range(start, end - 1):
        compare_result = compare(the_list[i], criterion)
        if compare_result == 0 or compare_result == -1:
            small_border += 1            
            swap(the_list, small_border, i)
    small_border += 1
    swap(the_list, small_border, end - 1)
    return small_border

#快排,end是尾+1
def quick_sort(the_list, start, end):
    middle = divide(the_list, start, end)
    if(middle == -1):
        return
    quick_sort(the_list, start, middle)
    quick_sort(the_list, middle + 1, end)

#写回文件,如果无法创建文件就返回false,否则返回true,参考了这个https://blog.csdn.net/zhayushui/article/details/81179908
def write_back():
    #切分文件夹和文件名,文件名可以直接打开,文件夹必须判断是否存在,而且还要考虑文件夹是本地的情况
    filelist = os.path.split(output_filename)
    filepath = filelist[0]
    filename = filelist[1]
    #测试
    #print(filepath, filename)
    if filepath == '' or os.path.exists(filepath) == True:
        #f = open(output_filename, 'w', newline = '\n', encoding = 'UTF-8')
        f = open(output_filename, 'w', newline = '\n')
    else:
        try:
            os.makedirs(filepath)
        except:
            sys.stderr.write('Error: make file fail\n')
            return False
        #f = open(output_filename, 'w', newline = '\n', encoding = 'UTF-8')
        f = open(output_filename, 'w', newline = '\n')
    #writer = csv.writer(f)
    if title != None:
        for i in range(len(title)):
            f.write(str(title[i]))
            if i != len(title) - 1:
                f.write(',')
            else:
                f.write('\n')
    #writer.writerow(title)
    if content != None:    
        for row in content:
            for i in range(len(row)):
                f.write(str(row[i]))
                if i != len(row) - 1:
                    f.write(',')
                else:
                    f.write('\n')
    f.close()
    return True

def main():
    if get_variables() == False:
        return
    if input_csv() == False:
        return
    if initialize_data() == False :
        return

    if sort_place != None:
        quick_sort(content, 0, len(content))

    #测试
    #print(content)
    write_back()

if __name__ == '__main__':
    main()