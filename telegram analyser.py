#!/usr/bin/python
from html.parser import HTMLParser

class Counter(dict):
    def __missing__(self, key):
        return 0

name_count = Counter()
name_data_count = Counter()
name_flag = False

text_count = 0
text_data_count = 0
text_flag = False

previous_name = ''

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global name_flag
        global text_flag
        
        if tag == 'div':
            if attrs[0][1]=='from_name':
                name_flag=True
            elif attrs[0][1] == 'text':
                text_flag=True
            
    def handle_data(self, data):
        global name_count
        global name_data_count
        global name_flag
        global previous_name
        global text_count
        global text_data_count
        global text_flag
        
        if name_flag:
            name_count[previous_name]+=text_count
            name_data_count[previous_name]+=text_data_count
            text_count = 0
            text_data_count = 0
            data=data.strip()
            previous_name=data
            name_flag=False
        elif text_flag:
            data=data.strip()
            text_data_count+=len(data)
            text_count += 1
            text_flag = False
        

parser = MyHTMLParser()
filename = ""
i = 1
while True:
    if i==1:
        filename = "messages.html"
    else:
        filename = "messages"+str(i)+".html"
    try:
        file = open(filename,"rt",encoding='UTF8')
        read_data = file.read()
        parser.feed(read_data)
        file.close()
        i+=1
    except FileNotFoundError as e:
        print(i)
        break
    
file = open("result.csv", "w")

for key in name_count.keys():
    file.write(key+','+str(name_count[key])+','+str(name_data_count[key])+'\n')
    
file.close()
