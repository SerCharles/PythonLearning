import sys
import os
import csv
import base64
import json
import re
class prussia:
    full_name = "Koenigreich Preussen"
    def __init__(self, army, population, king = "Wilhelm", anschlussed = False, *args, **kwargs):
        self.army = army
        self.population = population
        self.king = king
        self.anschlussed = anschlussed
        self.tuple = ()
        self.tuple = args
        self.dictionary = {}
        self.dictionary = kwargs
    def show(self):
        print(self.full_name)
        print(self.army)
        print(self.population)
        print(self.king)
        print(self.anschlussed)
        print(self.tuple)
        print(self.dictionary)
    
class deutschland(prussia):
    def change(self):
        self.anschlussed = True
        self.army = 0
        self.population = 80000000

def file():
    arg_list = sys.argv[1:]
    source = arg_list[0]
    end = arg_list[1]
    try:
        f = open(source, "r")
        list_file = f.readlines()
        f.close()
    except:
        sys.stderr.write("Error: cannot open the file\n")
        return
    print(list_file)
    for i in range(10):
        end_list = os.path.split(end)
        end_dir = end_list[0]
        end_file = end_list[1]
        if os.path.exists(end_dir):
            f = open(end, "a")
        else:
            os.makedirs(end_dir)
            f = open(end, "a")
        for item in list_file:
            f.write(item)
        f.close()

def csv_file():
    f = open("input.csv", "r")
    json_f = open("output.txt","w")
    reader = csv.DictReader(f)
    for row in reader:
        if row["halal"] == "FALSE":
            row["price"] = int(row["price"])
            row["halal"] = False
            print(base64.urlsafe_b64encode(b'kebab'))
            json_f.write(json.dumps(row, ensure_ascii = False))
    f.close()
    json_f.close()



def basic():
    sum = 0
    for i in range(100):
        sum += i
    print(sum)
    string_a =  "Number %i won!" % 12
    print(string_a)
    list_test = [1,2,3,4,5]
    print(list_test)
    list_test.remove(1)
    print(list_test)
    length = len(list_test)
    for i in range(length):
        j = length - 1 - i
        if j % 2 == 0:
            del(list_test[j])
    print(list_test)
    dic_test = {"kebab":1,"boerk":10,"anschluss":"ueber alles in der Welt"}
    while True:
        if "reich" in dic_test.keys():
            print(dic_test["reich"])
            print(dic_test)
            break
        else:
            del(dic_test["kebab"])
            del(dic_test["boerk"])
            dic_test["reich"] = "boerk"
    sgl = prussia(200000, 10000000, "Charles", False, "woerk", "krieg", start_year = 1701, success_year = 1871, end_year = 1947)
    sgl.show()
    sgl_now = deutschland(200000, 10000000, "Charles", False, "woerk", "krieg", start_year = 1701, success_year = 1871, end_year = 1947)
    sgl_now.change()
    sgl_now.show()

def regular():
    f = open("test.txt","r")
    content = f.read()
    pattern = re.compile(r'(^|\s|[,.:;；"，。：‘’“”])([^\W\d]+)(\d：|\d:|[1-9]\d：|[1-9]\d:|[1-9]\d\d:|[1-9]\d\d：)(\d|[1-9]\d|[1-9]\d\d)([^\W\d]+)($|\s|[,.:;；"，。：‘’“”])')
    answer_list = re.findall(pattern, content, )
    for item in answer_list:
        answer = item[1] + item[2] + item[3] + item[4]
        sys.stdout.write(answer + '\n')
    f.close()

def main():
    string_aa = "红军最强大！"
    print(string_aa)

if __name__ == '__main__':
    main()