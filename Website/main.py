import sys
import re
import json
import os
import requests
from urllib.request import quote, unquote

#读取命令行参数,存储到四个全局变量里(输入文件,输出文件,字段,排序类型)并且判断命令行是否合法,合法返回true,否则false
def get_variables():
    args = sys.argv[1:]
    global input_url
    global output_filename
    input_url = args[0]
    output_filename = args[1]
    return True

#读取网页数据
#如果超时报错;如果>=400报错,如果301,302重定向(自动),下载成功后存储到对应位置,只有正确读取才return true,否则false
def get_website_data():
    #模板字符串,用于报错
    error_info = 'Error|'
    timeout_info = ':this page is timeout '
    wrong_info = ':this page returns '
    global content
    url = input_url
    while True:
        try:
            response = requests.get(url, timeout = (5,10), allow_redirects = True)
        except:
            #超时报错
            sys.stderr.write(error_info + input_url + timeout_info + '\n')
            return False
        status_code = response.status_code
        #状态码错误
        if status_code < 200 or status_code >= 400:
            sys.stderr.write(error_info + input_url + wrong_info + str(status_code) + '\n')
            return False    
        #正确
        else:
            content = response.content.decode("utf-8")
            #content = response.content
            break

    #测试
    #print(content)
    return True

#测试用,读取文件数据
def get_data():
    f = open('input1.html', 'r')
    global content 
    content = f.read()
    print(content)

#用正则表达式搜索content里的内容，并且转化为json
def search_website_data():

    #正则表达式
    pattern_phone_number = re.compile(r'(^|[^0-9a-zA-Z_])(\d{7}|\d{8}|\d{11})([^0-9a-zA-Z_]|$)')
    pattern_name = re.compile(r'([Nn][Aa][Mm][Ee]：|[Nn][Aa][Mm][Ee]:|姓名：|姓名:)([^，,。；;“”"\r\n]*?)([，,。；;“”"\r\n]|$)')
    pattern_website = re.compile(r'([，,。.；;\s])(网址：|网址:)(\s*)([hH][tT][tT][pP][sS]?://)([^，,；;“”""。\s]*)([，,；;“”""。\s])')
    pattern_link = re.compile(r'([^\n\r]*)(链接)([^\n\r]*)(提取码)([^\n\r]*)([\n\r]|$)')

    #搜索的粗糙结果
    phone_number_list = re.findall(pattern_phone_number, content)
    name_list = re.findall(pattern_name, content)
    website_list = re.findall(pattern_website, content)
    link_list = re.findall(pattern_link, content)
    
    #测试
    #print(phone_number_list)
    #print(name_list)
    #print(website_list)
    #print(link_list)

    #拼接成正确的list
    global phone_number_answer
    phone_number_answer = []
    global name_answer
    name_answer = []
    global website_answer
    website_answer = []
    global link_answer
    link_answer = []
    for item in phone_number_list:
        phone_number_answer.append(item[1])
    for item in name_list:
        name_answer.append(item[1])
    for item in website_list:
        website_answer.append(item[3] + item[4])
    for item in link_list:
        link_string = item[0] + item[1] + item[2] + item[3] + item[4]
        link_answer.append(link_string[ : ])

    #测试
    #print(phone_number_answer)
    #print(name_answer)
    #print(website_answer)
    #print(link_answer)

    #转化为dictionary和json
    global answer_dictionary
    answer_dictionary = {}
    answer_dictionary['phone'] = phone_number_answer
    answer_dictionary['name'] = name_answer
    answer_dictionary['url'] = website_answer
    answer_dictionary['shared'] = link_answer
    #测试
    #print(answer_dictionary)
    global answer_json
    answer_json = json.dumps(answer_dictionary, ensure_ascii = False)
    #测试
    #print(answer_json)


#生成文件名，输出json数据
def output_data():
    input_url
    split_thing = os.path.sep
    output_name = unquote(input_url.split(split_thing)[-1])
    output_name_real = output_filename + split_thing + output_name
    #output_name_real = output_filename + split_thing + 'kebab.txt'
    #测试
    #print(output_name_real)
    try:
        f = open(output_name_real, 'w', newline = '')
    except:
        sys.stderr.write("cannot open file\n")
        return False
    f.writelines(answer_json)
    f.close()
    return True

def main():
    get_variables()
    if get_website_data() == False:
        return
    #get_data()
    search_website_data()
    if output_data() == False:
        return
    
if __name__ == '__main__':
    main()
